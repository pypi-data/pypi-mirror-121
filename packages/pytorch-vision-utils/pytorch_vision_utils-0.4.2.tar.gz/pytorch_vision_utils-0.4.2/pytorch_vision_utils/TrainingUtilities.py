import hashlib
import os
import torch
import yaml
import numpy as np

from PIL import Image
from pprint import pprint
from mdutils.mdutils import MdUtils
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from statistics import mean
from torch import nn
from torch.utils.data import DataLoader, Dataset
from tqdm.auto import tqdm
from torchvision.utils import save_image
from torchvision import (datasets, 
                         transforms, 
                         models)

from .CustomModels import avail_models
from .DataVisualizations import DataVisualizationUtilities
from .Utilities import (CustomDataset, 
                        get_timestamp, 
                        create_fold_dirs, 
                        create_fold_names,
                        time_to_predict)


class TrainingUtilities:
    
    def __init__(self, model_name:str, parameters_path="parameters.yml", mode="train", device=""):
        """
        Useful functions for training PyTorch models. Providing a `/path/to/parameters.yml` is required to work properly, assumed to be in
        the project directory. Encapsulates all of the hyperparameter tuning into one convenient class to toy with by hand or automate by 
        creating yml file.\n
        CAUTION: Currently in flux constantly, check back often for any documentation updates.

        Attributes
        ----------
        `TODO`

        Parameters
        ----------
        `model_name` : `str`\n
            Name of the model.
        `device` : `str`, `optional`\n
            String representation of the device to train on, by default ""
        `parameters_path` : `str`, `optional`\n
            String representation of the path to the "parameters.yml" file, by default "parameters.yml".
        `mode` : `str`, `optional`\n
            String representation of the mode of training, by default "train"
        """  
        
        self.model_name = model_name
        self.parameters_path = parameters_path
        self.device = torch.device(device) if device else torch.device("cuda" if torch.cuda.is_available() else "cpu")     
        self.model = nn.Module().to(device=self.device)
        self.md_file = None
        
        # VARIABLE INITIALIZATION
        self.data_dir = ""
        self.test_dir = ""
        self.model_dir = ""
        self.media_dir = ""
        self.inc_dir = ""
        self.classes = []
        self.batch_size = 0
        self.eta = 0
        self.patience = 0
        self.crop_size = 0
        self.degrees = 0
        self.hue = 0
        self.saturation = 0
        self.contrast = 0
        self.brightness = 0
        self.monitor = ""
        self.min_delta = float("inf")
        self.lr_patience = 0
        self.factor = 0
        self.n_splits = 0
        self.input_size = []
        self.mean = []
        self.std = []
        self.train_transform = None
        self.test_transform = None
        self.dataset = None
        self.loader = None
        self.mode = mode
        
        
        
    def set_model_parameters(self, model_name:str, mode="train", debug=False):
        """
        Switches the model parameters based on which model architecture in use and whether we are training
        or testing. 

        Parameters
        ----------
        `model_name` : `str`\n
            Model name.
        `mode` : `str`, `optional`\n
            String representation of the mode of training, by default "train"
            
        Raises
        ------
        `TypeError`\n
            Raised when there `new_mode` is neither "train" or "test".
            
        """    
        if mode != "train" and mode != "test":
            raise TypeError("Invalid string entered. Must be either 'train' or 'test'.")
            return    
        
        with open(self.parameters_path, "r") as f:
            yml_file = yaml.load(f, Loader=yaml.FullLoader)
            
            self.classes = yml_file["classes"]
            self.n_splits = yml_file["n_splits"]
            
            self.data_dir = yml_file["data_dir"]
            self.test_dir = yml_file["test_dir"]
            self.model_dir = yml_file["model_dir"]
            self.media_dir = yml_file["media_dir"]
            self.inc_dir = yml_file["inc_dir"]
            
            settings = yml_file[model_name]
           
        if debug: 
            pprint(settings)

        # HYPERPARAMETERS
        self.model_name = model_name
        self.batch_size = settings["batch_size"]
        self.eta = settings["eta"]
        self.patience = settings["patience"]
        self.crop_size = settings["crop_size"]
        self.degrees = settings["degrees"]
        self.hue = settings["hue"]
        self.saturation = settings["saturation"]
        self.contrast = settings["contrast"]
        self.brightness = settings["brightness"]
        self.monitor = settings["monitor"]
        self.min_delta = settings["min_delta"]
        self.lr_patience = settings["lr_patience"]
        self.factor = settings["factor"]
        self.input_size = settings["input_size"]
        self.mean = settings["mean"]
        self.std = settings["std"]
        self.mode = mode
        self.md_file: MdUtils
        
        self.model = self._set_model(self.model_name, debug).to(self.device)
            
        self.train_transform = transforms.Compose([transforms.Resize(self.input_size),
                                                   transforms.ColorJitter(hue=self.hue, brightness=self.brightness,
                                                                          saturation=self.saturation, contrast=self.contrast),
                                                    transforms.CenterCrop(self.crop_size),
                                                    transforms.RandomRotation(degrees=self.degrees),
                                                    transforms.RandomPerspective(p=1.0), # we always want a bit of distortion
                                                    transforms.ToTensor(),
                                                    transforms.Normalize(mean=self.mean, std=self.std)])
        
        self.test_transform = transforms.Compose([transforms.Resize(self.input_size),
                                                  transforms.CenterCrop(self.crop_size),
                                                  transforms.ToTensor(),
                                                  transforms.Normalize(mean=self.mean, std=self.std)])
                                        
        self.dataset = CustomDataset(self, mode=self.mode)
        self.loader = self.create_loader(self.dataset, batch_size=self.batch_size, shuffle=True)
        
    
        
    def set_test_transform(self, new_transform:transforms.Compose):
        """
        Sets the test transform.

        Parameters
        ----------
        `new_transform` : `transforms.Compose`\n
            The new transform to be used.
        """        
        self.test_transform = new_transform
        
    
    def set_mode(self, new_mode:str):
        """
        Sets the mode for both the TrainingUtilities instance, but also the CustomDataset.

        Parameters
        ----------
        `new_mode` : `str`\n
            String representation of the new mode.
        
        Raises
        ------
        `TypeError`\n
            Raised when there `new_mode` is neither "train" or "test".
            
        """   
        
        if new_mode != "train" and new_mode != "test":
            raise TypeError("Invalid string entered. Must be either 'train' or 'test'.")
            return
         
        self.mode = new_mode
        self.loader.dataset.mode = new_mode


    def _set_model(self, model_name:str, debug=False):
        """
        Changes the model based on a given name.

        Parameters
        ----------
        `model_name` : `str`\n
            The new model name.
            
        Raises
        ------
        `ValueError`\n
            Raised when there is an unrecognized `model_name`.
        """     
        model = avail_models[model_name](num_classes=len(self.classes))
        if debug:
            print(model)
            
        return model


    def reload_weights(self, model_name:str, model_weights_path:str, mode="train", debug=False):
        """
        Reloads a model with specific weights. Used for continuing training after some sort of interruption

        Parameters
        ----------
        `model_name` : `str`\n
            Model name.
        `model_weights_path` : `str`\n
            String representation to the model weights path.
        `mode` : `str`, `optional`\n
            String representation of the new mode, by default "test".
        """        
        
        weights = torch.load(model_weights_path)["model_state_dict"]
        self.set_model_parameters(model_name, mode=mode, debug=debug)
        self.model.load_state_dict(weights)


    def load_weights(self, model_name:str, model_weights_path:str, mode="test", debug=False):
        """
        Loads a model with specific weights. Used for testing.

        Parameters
        ----------
        `model_name` : `str`\n
            Model name.
        `model_weights_path` : `str`\n
            String representation to the model weights path.
        `mode` : `str`, `optional`\n
            String representation of the new mode, by default "test".
        """        
        
        weights = torch.load(model_weights_path)["model_state_dict"]
        self.set_model_parameters(model_name, mode=mode, debug=debug)
            
        self.model.load_state_dict(weights)
        self.model.eval()
        print("Model in eval mode.")
        

    def create_loader(self, dataset:Dataset, batch_size:int, shuffle=True) -> DataLoader:
        """
        Creates loader given a dataset.

        Parameters
        ----------
        `dataset` : `Dataset`\n
            Custom Dataset.
        `batch_size` : `int`\n
            Batch size.
        `shuffle` : `bool`, `optional`\n
            Boolean representing whether to shuffle the data or not, by default True.

        Returns
        -------
        `DataLoader`\n
            DataLoader with the correct setting for training.
        """        
        return torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)
    

    def to_categorical(self) -> OneHotEncoder:
        """
        Converts the labels from names to integers.

        Returns
        -------
        `OneHotEncoder`\n
            A one-hot encoded scikit-learn object.
        """        
        
        labels = np.array(self.classes)
        label_encoder = LabelEncoder()
        integer_encoded = label_encoder.fit_transform(labels)
        
        onehot_encoder = OneHotEncoder(sparse=False)
        integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
        return onehot_encoder.fit_transform(integer_encoded)
        
    
    def split_data_and_create_folds(self) -> tuple:
        """
        Creates dataset and creates splits for k-fold cross validation.

        Returns
        -------
        `tuple`\n
            Returns a tuple containing a list fold indices, ndarray representation of the input image, ndarray of the ground-truth
            classification, and an ndarray containing the id's for each input image.\n
            NOTE: Keep in mind the negative class will not always be `0` using this function, will have to possibly be revised
        """        
        
        X = [] # inputs
        y = [] # outputs
        ids = []

        walk = list(os.walk(self.data_dir))
        walk.sort()
        for i, (subdir, dirs, files) in enumerate(walk):
            if not files:
                continue

            print(f'Creating {subdir}...')
            for f in files:
                ids.append(f"{i-1}_{files[:-4]}")
                img_path = os.path.join(subdir, f)
                img = Image.open(img_path)
                img = img.resize(size=self.input_size)
                img = img.convert('RGB')
                img = np.asarray(img)
                X.append(img)
                y.append(i-1)

        print(f'{len(X)} total images loaded')
        folds = list(StratifiedKFold(n_splits=self.n_splits, shuffle=True).split(X, y))
        return folds, np.array(X), np.array(y), np.array(ids)
    
    
    def _loop_fn(self, dataset:Dataset, loader:DataLoader, criterion, optimizer) -> tuple:
        """
        The function that actually does the loop for training. Likely isn't used directly, refer to the `train` or `_train` function.

        Parameters
        ----------
        `dataset` : `Dataset`\n
            The custom dataset.
        `loader` : `DataLoader`\n
            The dataloader.
        `criterion`\n
            The loss function.
        `optimizer`\n
            The optimization function.

        Returns
        -------
        `tuple`\n
            Returns a tuple containing the average cost and accuracy of a given batch.
        """        
        
        if self.mode == "train":
            self.model.train()
        elif self.mode == "test":
            self.model.eval()

        cost = correct = 0
        for feature, target in tqdm(loader, 
                                    desc=self.mode.title()+"\t"):
            
            feature, target = feature.to(self.device, dtype=torch.float32), target.to(self.device, dtype=torch.long)
            output = self.model(feature)
            loss = criterion(output, target)
            self.model.metric = loss
            
            if self.mode == "train":
                loss.backward()
                optimizer.step()
                optimizer.zero_grad()

            cost += loss.item() * feature.shape[0]
            correct += (output.argmax(1) == target).sum().item()

        cost = cost / len(dataset)
        acc = correct / len(dataset)
        return cost, acc
        
    
    @torch.no_grad() # https://deeplizard.com/learn/video/0LhiS6yu2qQ
    def get_predictions(self, fold) -> tuple:
        """
        Gets all of the predictions. Useful for determining model performance.

        Parameters
        ----------
        `fold` : int\n
            Number representing the current fold during k-fold cross validation.

        Returns
        -------
        `tuple`\n
            Returns a tuple containing the model predictions and the ground truths.
        """        
        
        y_pred = torch.tensor([]).to(self.device, dtype=torch.long)
        y_true = torch.tensor([]).to(self.device, dtype=torch.long)
        
        for images, labels in self.loader:
            images = images.to(self.device, dtype=torch.float32)
            labels = labels.to(self.device, dtype=torch.long)
            target = labels.to(self.device, dtype=torch.long).cpu().numpy()[0]
            
            pred = self.model(images).to(self.device, dtype=torch.long)
            y_pred = torch.cat((y_pred, pred), dim=0)
            y_true = torch.cat((y_true, labels), dim=0)
            
            corrects = (labels == pred.argmax(1))
            for idx, is_correct in enumerate(corrects.cpu().numpy()):
                if self.inc_dir and not is_correct:
                    tensor_img = transforms.ToTensor()(DataVisualizationUtilities()._im_convert(tensor=images[idx].cpu(), mean=self.mean, std=self.std))
                    
                    hash_ = hashlib.sha256(get_timestamp().encode('utf-8')).hexdigest()[:5]
                    path_name = f"{self.model_name}_{fold}" if fold=="eval" else f"{self.model_name}_fold_{fold}"
                    img_path = os.path.join(self.inc_dir, path_name, f"{hash_}_{labels[idx]}.png")
                    save_image(tensor_img, img_path)
                                     
        return y_pred, y_true
            
            
    def add_plot_to_md(self, title:str, plot_name:str, extension=".jpg"):
        """
        Adds a plot to the report markdown.

        Parameters
        ----------
        `title` : `str`\n
            The title for the plot
        `plot_name` : `str`\n
            The name of the plot
        """      
          
        self.md_file.new_line("### {}".format(title.title()))
        self.md_file.new_paragraph("![{}]({}{} \"{}\")".format(plot_name, "./"+plot_name, extension, plot_name))
    
    
    def _outer_loop(self, fold:int, show_graphs: bool, dry_run: bool) -> tuple:
        train_idx, test_idx = self.dataset.folds[fold]
        train_dataset = torch.utils.data.Subset(self.dataset, train_idx)
        test_dataset = torch.utils.data.Subset(self.dataset, test_idx)
        
        train_dataset.transform = self.train_transform
        test_dataset.transform = self.test_transform
        
        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(self.model.parameters(), lr=self.eta)
        lr_scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=self.factor, patience=self.lr_patience, verbose=True)
        return self._train(train_dataset, test_dataset, criterion, optimizer, fold, scheduler=lr_scheduler, 
                                dry_run=dry_run, show_graphs=show_graphs)
        
    
    def evaluate_model(self, model_name, model_weights_path):
        """
        Evaluates the model using the images from the test directory

        Parameters
        ----------
        `model_name` : str\n
            String representation of the model name
        `model_weights_path` : str\n
            String representation of the graph
        """  
              
        self.load_weights(model_name=model_name, 
                          model_weights_path=model_weights_path,
                          mode="test")
        
        # METRICS GRAPH
        metrics = "metrics_graph_{}_{}".format(self.model_name, "eval")
        metrics_graph = DataVisualizationUtilities().display_metric_results(fold="eval", train_utils=self)
        metrics_path = os.path.join(self.media_dir, metrics+".jpg")
        metrics_graph.savefig(metrics_path, dpi=300)
        self.add_plot_to_md("Confusion Matrix [{}]".format("Eval"), metrics)
        
        # ROC GRAPH
        if len(self.classes) == 2:
            roc = "roc_graph_{}_{}".format(self.model_name, "eval")
            roc_graph = DataVisualizationUtilities().display_roc_curve(0, train_utils=self)
            roc_path = os.path.join(self.media_dir, roc+".jpg")
            roc_graph.savefig(roc_path, dpi=300)
            self.add_plot_to_md("ROC Curve [{}]".format("Eval"), roc)
        
        
    def train(self, model_name:str, 
              show_graphs=True, 
              dry_run=True, 
              debug=False, 
              max_epoch=1000) -> tuple:
        """
        Wrapper function for the actual training method. Will likely be edited in the future to be more customizable.

        Parameters
        ----------
        `model_name` : `str`\n
            Model name.
        `show_graphs` : `bool`, `optional`\n
            Boolean representing whether or not to display graphs, by default True.
        `dry_run` : `bool`, `optional`\n
            Boolean representing whether we're training to evaluate hyperparameter tuning or training the model for model comparisons, by default True.
        `max_epoch` : `int`, `optional`\n
            Integer representing the maximum number of epochs to train the model for, by default 1000.

        Returns
        -------
        `tuple`\n
            Returns a tuple containing the average loss and average accuracy.

        """        
        self.set_model_parameters(model_name=model_name, debug=debug)
        report_path = "report_{}.md".format(self.model_name)
        media_path = os.path.join(self.media_dir, report_path)
        self.md_file = MdUtils(file_name=media_path, title='{} Results'.format(self.model_name.title()))
        
        dir_names = create_fold_names(self.model_name, n_splits=self.n_splits)
        create_fold_dirs(self.inc_dir, dir_names)
        losses = []
        accuracies = []
        
        # `dry_run=True` means that we're doing k-fold cross validation and to not save any of the models
        if dry_run:
            for fold, (train_idx, test_idx) in enumerate(self.dataset.folds):
                print('\nFold ', fold+1)
                loss, acc = self._outer_loop(fold=fold, show_graphs=show_graphs, dry_run=dry_run)
                
                losses.append(loss)
                accuracies.append(acc)
                self._set_model(model_name=self.model_name, debug=debug) # creates a new instance of the model
                self.md_file.new_line()
          
        # `dry_run=False` means we're training this model to actually be used         
        else:
            fold = 0
            loss, acc = self._outer_loop(fold=fold+1, show_graphs=show_graphs, dry_run=dry_run)

            losses.append(loss)
            accuracies.append(acc)
            
        avg_loss = mean(losses)
        avg_acc = mean(accuracies)
        
        results = f'Average Loss: {avg_loss:.5f}  |  Average Accuracy: {avg_acc:.5f}'
        print(results)
        
        self.md_file.new_paragraph("`{}`".format(results))
        # self.md_file.create_md_file()
        return avg_loss, avg_acc
    
    
    def _generate_graphs(self, fold: int, early_stopping, 
                        train_total_loss: list, train_total_acc: list, val_total_loss: list,
                        val_total_acc: list, show_graphs: bool):
        
        # RESULTS GRAPH
        results = "results_graph_{}_{}".format(self.model_name, fold)
        results_graph = DataVisualizationUtilities().display_results(train_total_loss, train_total_acc, val_total_loss, val_total_acc, 
                                                                     title=early_stopping.model_name)
        results_path = os.path.join(self.media_dir, results+".jpg")
        results_graph.savefig(results_path, dpi=300)
        self.add_plot_to_md("Training and Validation Results [{}]".format(fold), results)
        
        
        # METRICS GRAPH
        metrics = "metrics_graph_{}_{}".format(self.model_name, fold)
        metrics_graph = DataVisualizationUtilities().display_metric_results(fold=fold, train_utils=self)
        metrics_path = os.path.join(self.media_dir, metrics+".jpg")
        metrics_graph.savefig(metrics_path, dpi=300)
        self.add_plot_to_md("Confusion Matrix [{}]".format(fold), metrics)
        
        
        # ROC GRAPH
        if len(self.classes) == 2:
            roc = "roc_graph_{}_{}".format(self.model_name, fold)
            roc_graph = DataVisualizationUtilities().display_roc_curve(0, train_utils=self)
            roc_path = os.path.join(self.media_dir, roc+".jpg")
            roc_graph.savefig(roc_path, dpi=300)
            self.add_plot_to_md("ROC Curve [{}]".format(fold), roc)
    
    
        # DISPLAY GRAPHS
        if show_graphs:
            results_graph.show()
            metrics_graph.show()
            if len(self.classes) == 2:
                roc_graph.show()
    
    
    # https://stackoverflow.com/questions/58996242/cross-validation-for-mnist-dataset-with-pytorch-and-sklearn
    def _train(self, train_dataset:Dataset, 
               test_dataset:Dataset, 
               criterion, 
               optimizer, 
               fold:int, 
               max_epoch=1000, 
               scheduler=None, 
               shuffle=True, 
               show_graphs=True, 
               dry_run=False) -> tuple:
        """Does the actual training. Implements early stopping and some debugging.
        """        
        
        early_stopping = EarlyStopping(model_dir=self.model_dir, model_name=self.model_name, fold=fold, min_delta=self.min_delta)
        train_total_loss = []
        train_total_acc = []
        val_total_loss = []
        val_total_acc = []
        test_loader = self.create_loader(test_dataset, batch_size=self.batch_size, shuffle=shuffle)
        train_loader = self.create_loader(train_dataset, batch_size=self.batch_size, shuffle=shuffle)
            
        epoch = 1
        for e in range(max_epoch):
            print(f'\nEpoch {fold}.{epoch}')
            self.set_mode("train")
            train_cost, train_score = self._loop_fn(train_dataset, train_loader, criterion, optimizer)
            with torch.no_grad():
                self.set_mode("test")
                test_cost, test_score = self._loop_fn(test_dataset, test_loader, criterion, optimizer)
                
            if scheduler:
                scheduler.step(test_cost)
                
            train_total_loss.append(train_cost)
            train_total_acc.append(train_score)
            val_total_loss.append(test_cost)
            val_total_acc.append(test_score)
                
            es_counter = early_stopping.checkpoint(self.model, epoch, test_cost, test_score, optimizer, dry_run=dry_run)
            print(f'\nTrain Loss: {train_cost:.3f}   | Train Acc: {train_score:.4f}  | Val Loss: {test_cost:.3f}   | Val Acc: {test_score:.4f}')
            print(f'Early Stopping Patience at: {es_counter}')
                
            if es_counter == self.patience:
                
                self.model.eval()
                self._generate_graphs(fold=fold, early_stopping=early_stopping,
                                     train_total_loss=train_total_loss, train_total_acc=train_total_acc,
                                     val_total_loss=val_total_loss, val_total_acc=val_total_acc, 
                                     show_graphs=show_graphs)
                    
                break
            
            epoch += 1

        return early_stopping.min_loss, early_stopping.max_acc
    



class EarlyStopping():
    
    def __init__(self, 
                 model_dir:str, 
                 model_name:str, 
                 fold:int, min_delta=0):
        """
        Class for early stopping, because only plebs rely on set amounts of epochs.
        
        Attributes
        ----------
        `TODO`

        Parameters
        ----------
        `model_name` : `str`\n
            Model name.
        `fold` : `int`\n
            Number representing the current fold.
        `min_delta` : `int`, `optional`\n
            Smallest number the given metric needs to change in order to count as progress, by default 0.
        """        
        
        self.min_loss = float('inf')
        self.max_acc = -float('inf')
        self.min_delta = min_delta
        self.model_name = model_name 
        self.path = str(os.path.join(model_dir, self.model_name+'.pth'))
        self.count = 0
        self.first_run = True
        self.best_model = None
        
        
    def checkpoint(self, model:nn.Module, epoch:int, loss:float, acc:float, optimizer, dry_run=False) -> int:
        """
        Creates the checkpoint and keeps track of when we should stop training. You can choose whether or not you'd like to save the model based on the `dry_run` parameter.
        
        Parameters
        ----------
        `model` : `nn.Module`\n
            The model to be saved.
        `epoch` : `int`\n
            Number representing the current epoch.
        `loss` : `float`\n
            Current loss.
        `acc` : `float`\n
            Current accuracy.
        `optimizer`
            The optimization function currently in use.
        `dry_run` : `bool`, `optional`\n
            Boolean representing whether we're training to evaluate hyperparameter tuning or training the model for comel comparisons, by default True.

        Returns
        -------
        `int`\n
            Returns a number representing the current level of patience reached.
        """        
        
        print(f'Loss to beat: {(self.min_loss - self.min_delta):.4f}')
        if (self.min_loss - self.min_delta) > loss or self.first_run:
            self.first_run = False
            self.min_loss = loss
            self.max_acc = acc
            self.best_model = model
            self.count = 0
            if not dry_run:
                torch.save({'epoch': epoch,
                            'model_state_dict': model.state_dict(),
                            'optimizer_state_dict': optimizer.state_dict(),
                            'loss': loss,}, self.path)
            
        else:
            self.count += 1
            
        return self.count
   
   