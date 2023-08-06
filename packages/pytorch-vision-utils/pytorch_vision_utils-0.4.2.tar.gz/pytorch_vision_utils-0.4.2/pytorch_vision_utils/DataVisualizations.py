import torch
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from statistics import mean
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, auc


class DataVisualizationUtilities:
    
    def __init__(self, device=""):
        """
        This class serves as a collection of helpful functions when working with `torchvision` and image data in general.

        Attributes
        ----------
        `device` : str\n
            String representation of the GPU core to use or the CPU
        
        """  
        sns.set_theme()              
        self.device = torch.device(device) if device else torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    
    def _im_convert(self, tensor, mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)) -> np.ndarray:
        """
        Private function for converting an image so it can be displayed using matplotlib functions properly.

        Parameters
        ----------
        `tensor`\n
            Tensor represention of image data.
        `mean` : `tuple` or `list`, `optional`\n
            Mean of the data; used for de-normalization of the image, by default (0.485, 0.456, 0.406).
        `std` : `tuple` or `list`, `optional`\n
            Standard deviation of the data; used for de-normalaztion of the image, by default (0.229, 0.224, 0.225).

        Returns
        -------
        `ndarray`\n
            Returns ndarry de-normalizazed representation of an image.
        """        
        
        image = tensor.clone().detach().numpy()
        image = image.transpose(1, 2, 0)
        image = image * np.array(std) + np.array(mean) # [0, 1] -> [0, 255]
        image = image.clip(0, 1)
        return image
    

    def display_dataset(self, train_utils):
        """
        Displays the dataset. Useful for making sure your data was loaded properly.

        Parameters
        ----------
        `train_utils`\n
            TrainingUtilities instance.
        """        
        
        print(train_utils.mode)
        dataiter = iter(train_utils.loader)
        images, labels = dataiter.next()
        print(images.shape)
        fig = plt.figure(figsize=(25, 4))

        for idx in np.arange(min(train_utils.batch_size, 20)):
            ax = fig.add_subplot(2, 10, idx+1, xticks=[], yticks=[])
            plt.imshow(self._im_convert(images[idx], mean=train_utils.mean, std=train_utils.std))
            ax.set_title(train_utils.classes[labels[idx].numpy()])

                
    
    def display_metric_results(self, fold, train_utils, figsize=(7, 7)):
        """
        Displays classification report and confusion matrix.

        Parameters
        ----------
        `fold` : `any`\n
            Title representing the current fold during k-fold cross validation.
        `train_utils`\n
            TrainingUtilities instance.
        `figsize` : `tuple`, `optional`\n
            Tuple representing the dimensions of the figure in inches, by default (7, 7).  
        """        
        
        with torch.no_grad():
            y_pred, y_true = train_utils.get_predictions(fold)
            
        # y_true = torch.tensor(y_true).to(self.device, dtype=torch.long).clone().detach()
        xticks = yticks = train_utils.classes
        
        print("Classification Report\n")
        clr = classification_report(y_true.cpu(), y_pred.argmax(dim=1).cpu(), target_names=xticks)
        print(clr)
        fold = fold.title() if fold=="eval" else fold
        train_utils.md_file.new_line("### Classification Report [{}]".format(fold))
        train_utils.md_file.insert_code(str(clr))
        print("Confusion Matrix")
        cnf_mat = confusion_matrix(y_true.cpu(), y_pred.argmax(dim=1).cpu())

        # plot
        plt.figure(figsize=figsize)
        sns.heatmap(cnf_mat, 
                    xticklabels=xticks, 
                    yticklabels=yticks, 
                    annot=True, 
                    cmap="Blues_r", 
                    fmt=".4g", 
                    linewidths=1)
        
        plt.ylabel('Ground Truth')
        plt.xlabel('Predictions')
        return plt
        
        
        
    def display_results(self, loss:float, acc:float, val_loss:float, val_acc:float, title:str, figsize=(7, 7)):
        """
        Displays the accuracy and loss training results.

        Parameters
        ----------
        `loss` : `float`\n
            Training loss.
        `acc` : `float`\n
            Training accuracy.
        `val_loss` : `float`\n
            Validation loss.
        `val_acc` : `float`\n
            Validation accuracy.
        `title` : `str`\n
            Title of the graph.
        `figsize` : `tuple`, `optional`\n
            Tuple representing the dimensions of the figure in inches, by default (7, 7).
            
        """        
            
        plt.figure(figsize=figsize)
        plt.subplot(2, 1, 1)

        plt.plot(acc, label='Training Accuracy', color='blue')
        plt.plot(val_acc, label='Validation Accuracy', color='lightseagreen')
        plt.legend(loc='lower right')
        plt.ylabel('Accuracy')
        plt.ylim([0, 1.2])
        plt.title('Training and Validation Accuracy '+ title)

        y_upper_bound = max(max(loss), max(val_loss))
        plt.subplot(2, 1, 2)
        plt.plot(loss, label='Training Loss', color='blue')
        plt.plot(val_loss, label='Validation Loss', color='lightseagreen')
        plt.legend(loc='upper right')
        plt.ylabel('Cross Entropy')
        plt.ylim([0, y_upper_bound+y_upper_bound*0.2])
        plt.title('Training and Validation Loss '+ title)
        plt.xlabel('epoch')
        return plt
        
        
    def display_benchmark_results(self, pred_times1, pred_times2, model_name1:str, model_name2:str, figsize=(7, 7), shade=True, 
                                  legend=True, bw_adjust=5, color1="blue", color2="purple"):
        """
        Displays benchmark prediction times.

        Parameters
        ----------
        `pred_times1` : `list` or `ndarray`\n
            Collection of predicition times for the first model for comparison.
        `pred_times2` : `list` or `ndarray`\n
            Collection of predicition times for the second model for comparison.
        `model_name1` : `str`\n
            First model name.
        `model_name2` : `str`\n
            Second model name.
        `figsize` : `tuple`, `optional`\n
            Tuple representing the dimensions of the figure in inches, by default (7, 7).
        `shade` : `bool`, `optional`\n
            Boolean representing whether to shade in the figure or not, by default True.
        `legend` : `bool`, `optional`\n
            Boolean representing whether to show the legend or not, by default True.
        `bw_adjust` : `int`, `optional`\n
            Number representing the width of the line in pixels, by default 5.
        `color1` : `str`, `tuple`, `list`\n
            Structured representation of the color for model 1, by default "blue".
        `color2` : `str`, `optional`\n
            Structured representation of the color for model 2, by default "purple".
        """        
        
        plt.figure(figsize=(7, 7))
        x_max = max(max(pred_times1), max(pred_times2))
        sns.kdeplot(x=pred_times1, color=color1, shade=shade, label=model_name1, bw_adjust=bw_adjust)
        sns.kdeplot(x=pred_times2, color=color2, shade=shade, label=model_name2, bw_adjust=bw_adjust)
        
        plt.xlabel('Time (ms)')
        plt.xlim([0, x_max+x_max*0.3])
        plt.title(f'Benchmark Results')
        plt.legend(loc="upper right")
        plt.show()
        # return plt

        
    def display_roc_curve(self, fold:int, train_utils, figsize=(7, 7)):
        """
        Displays ROC curve.

        Parameters
        ----------
        `fold` : int\n
            Number representing the current fold during k-fold cross validation.
        `train_utils` : `TrainingUtilities`\n
            TrainingUtilities instance.
        `figsize` : `tuple`, `optional`\n
            Tuple representing the dimensions of the figure in inches, by default (7, 7).
        """        
        
        if len(train_utils.classes) > 2:
            return
        
        with torch.no_grad():
            y_pred, y_true = train_utils.get_predictions(fold)
            y_pred, y_true = y_pred.argmax(dim=1).cpu().clone().detach(), torch.tensor(y_true).cpu().clone().detach()
        
        fpr, tpr, thresholds = roc_curve(y_pred, y_true)
        roc_auc = auc(fpr, tpr)
        
        plt.title('ROC Results for {}'.format(train_utils.model_name.title()))
        plt.figure(figsize=figsize)
        plt.plot(fpr, tpr, linewidth=2, label=train_utils.model_name + f" area: {roc_auc:.4f}", color='blue')
        plt.plot([0, 1], [0, 1], 'k--')
        plt.axis([0, 1, 0, 1])
        plt.xlim([-0.02, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.legend(loc="lower right")
        
        return plt


  