import numpy as np 
import torch
import os
import random

from datetime import datetime
from PIL import Image
from statistics import mean
from torch import nn
from torchvision import transforms, models
from torch.utils.data import DataLoader, Dataset
from tqdm.auto import tqdm

from .CustomModels import avail_models
  

### Helpful functions that can be used throughout ###
def get_timestamp():
    '''Creates a timestamp, typically useful for generating unique file names for models and images.
    '''
    now = datetime.now()
    timestamp = now.strftime("%d.%m.%Y %H:%M:%S,%f")
    return timestamp


def reload_models(model:nn.Module, model_dir:str, folder_name:str, device="cuda", debug=False) -> list:
    '''Reloads multiple models based on a directory passed through. Useful for quickly loading directories 
    
    Parameters
    ----------
    `model` : `nn.Module`\n
        The model.
    `model_dir` : `str`\n
        Path to the directory.
    `folder_name` : `str`\n
        Name of the folder.
    `device` : `str`, `optional`\n
        String representation of the GPU core to use or the CPU, by default "cuda".
    `debug` : `bool`, `optional`\n
        Boolean indicating whether to print out debugging information or not.

    
    Returns
    -------
    `models` : `list`\n
        List of all the saved models in evaluation mode.
    
    '''
    
    models = []

    print('Reading in models...')
    path = os.path.join(model_dir, folder_name)
    for i, (subdir, dirs, files) in enumerate(os.walk(path)):
        if not files:
            continue

        for f in files:
            if debug:
                print(f'Reading {f}')
                
            model = model.to(device)
            weights = os.path.join(subdir, f)
            model.load_state_dict(state_dict=torch.load(weights)['model_state_dict'])
            model.eval()
            models.append(model)

    return models


def clear_dirs(dir:str):
    '''Clears out files in a directory. 
    
    Parameters
    ----------
    `dir` : `str`\n
        Path to the directory
            
    '''
    
    walk = list(os.walk(dir))
    walk.sort()
    for i, (subdir, dirs, files) in enumerate(walk):
        if not files:
            continue
        
        for f in files:
            remove_path = os.path.join(subdir, f)
            os.remove(remove_path)
            

def create_fold_dirs(target_dir:str, dir_names:list):
    '''Creates fold directories.
    
    Parameters
    ----------
    `target_dir` : `str`\n
        String representation of the path to the directory.
    `dir_names` : `list`\n
        List of the subdirectory names.
    
    '''
    
    for d in dir_names:
        dirs = os.path.join(target_dir, d)
        os.makedirs(dirs, exist_ok=True)

        
def create_fold_names(model_name:str, n_splits=5) -> list:
    """
    List comprehension that creates the folder names.

    Parameters
    ----------
    `model_name` : `str`\n
        Model name.
    `n_splits` : `int`, `optional`\n
        Number of splits used for kfold cross validation, by default 5

    Returns
    -------
    `list`\n
        Returns a list of all the folder names.
    """    
    
    dir_names = [f"{model_name}_fold_{idx}" for idx in range(n_splits+1)]
    dir_names.append(f"{model_name}_eval")
    return dir_names

            
def remove_outliers(data:list, constant=1.5):
    """
    Removes outliers from a given dataset. Must be numerical.

    Parameters
    ----------
    `data` : `list`\n
        List of the data points.
    `constant` : `float`, `optional`\n
        Constant used for determining an outlier using the IQR, by default 1.5.

    Returns
    -------
    `ndarray`\n
        ndarray of data with outliers removed.
        
    """    
    
    data.sort()
    upper_quartile = np.percentile(data, 75, interpolation="nearest")
    lower_quartile = np.percentile(data, 25, interpolation="nearest")
    iqr = upper_quartile - lower_quartile
    l_outlier = lower_quartile - (constant * iqr)
    u_outlier = upper_quartile + (constant * iqr)
    data_clean = [d for d in data if d >= l_outlier and d <= u_outlier]
  
    return np.array(data_clean)


def time_to_predict(model:nn.Module, loader:DataLoader, constant=1.5, device="cuda") -> list:
    """
    Calculates the time to predict on a dataset and removes outliers.

    Parameters
    ----------
    `model` : `nn.Module`\n
        The model.
    `loader` : `DataLoader`\n
        Dataloader with the images to predict on.
    `constant` : `float`, `optional`\n
        Constant used for determining an outlier using the IQR, by default 1.5.
    `device` : `str`, `optional`\n
        String representation of the GPU core to use or the CPU, by default "cuda".

    Returns
    -------
    `list`\n
        Prints some information about the deltas distribution and returns a list of the deltas
    """    
    
    deltas = []
        
    for images, labels in tqdm(loader, 
                               desc="Predicting...".title()):
        
        images = images.to(device, dtype=torch.float)
        labels = labels.to(device, dtype=torch.long)
        start = datetime.now()
        model(images).to(device, dtype=torch.long) # we don't care about the output
        end = datetime.now()
        delta = (end - start).total_seconds() * 1000
        deltas.append(delta)

    deltas = remove_outliers(deltas)
        
    print(f'\nNumber of Predictions:{len(deltas)}\tClassification Time Mean: {np.mean(deltas):.4f}ms\tClassification Time Max: {np.max(deltas):.4f}ms\tClassification Time Min: {np.min(deltas):.4f}ms')
    return deltas


def random_sampling(dataset:dict, num_of_images=1000) -> list:
    """
    Does a random oversampling of the `dataset` to balance all of the classes.

    Parameters
    ----------
    `dataset` : `dict`\n
        Dict representation of the dataset.
    `num_of_images` : `int`, `optional`\n
        Number of images for each class, will repopulate the other classes proportionally, by default 1000.

    Returns
    -------
    `list`\n
        Returns a list 
    """    

    balanced_data = list()
    num_of_classes = len(dataset.keys())
    for i in range(num_of_classes):
        num_of_additional_imgs = num_of_images - len(dataset[i])
        for j in range(num_of_additional_imgs):
            dataset[i].append(random.choice(dataset[i]))
            
        balanced_data += dataset[i]

    return balanced_data


class CustomDataset(Dataset):
    
    def __init__(self, train_utils, mode="train"):
        """
        Extending class of `torchvision`'s `Dataset` abstract class.

        Attributes
        ----------
        `TODO`
        
        Parameters
        ----------
        `train_utils`\n
            Training Utilities instance.
        `mode` : `str`, `optional`\n
            String representation of whether we're testing/validating or training, by default "train".
        """        
        
        super(Dataset, self).__init__()
        folds, X, y, ids = train_utils.split_data_and_create_folds()
        self.folds = folds
        self.X = X
        self.y = y
        self.ids = ids
        self.train_transform = train_utils.train_transform
        self.test_transform = train_utils.test_transform
        self.mode = mode
        self.selected_item = ()
        

    def __getitem__(self, index):
        item = self.X[index]
        label = self.y[index]
        item = transforms.ToPILImage()(item)
            
        if self.mode == "train":
            ret = (self.train_transform(item), label) if self.train_transform else (item, label)
            
        elif self.mode == "test":
            ret = (self.test_transform(item), label) if self.test_transform else (item, label)
        
        self.selected_item = (self.ids[index], ret) # (filename, picture)
        return ret

        
    def set_mode(self, new_mode:str):
        """
        Changes the mode to either 'train' or 'test'.

        Parameters
        ----------
        `new_mode` : `str`\n
            String representation of the new mode.
            
        Raises
        ------
        `TypeError`\n
            If `new_mode` is not either 'train' or 'test'
        """   
        if new_mode != "train" and new_mode != "test":
            raise TypeError("Invalid string entered. Must be either 'train' or 'test'.")
            return
            
        self.mode = new_mode

    def __len__(self):
        return len(self.X)
      