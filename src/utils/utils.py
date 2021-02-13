import math
import os
import random

import numpy as np
import torch


def seed_torch(seed=42):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True


class EarlyStopping:
    """Early stops the training if validation loss doesn't improve after a given patience."""
    def __init__(self, patience=7, verbose=False, save_path='checkpoint.pt',
                 counter=0, best_score=None, val_loss_history=[], save_latest_path=None):
        """
        Args:
            patience (int): How long to wait after last time validation loss improved.
                            Default: 7
            verbose (bool): If True, prints a message for each validation loss improvement. 
                            Default: False
            save_path (str): Directory for saving a model.
                             Default: "'checkpoint.pt'"
        """
        self.patience = patience
        self.verbose = verbose
        self.save_path = save_path
        self.counter = counter
        self.best_score = best_score
        self.save_latest_path = save_latest_path
        self.early_stop = False
        self.val_loss_min = np.Inf
        self.val_loss_history = val_loss_history

    def __call__(self, val_loss, model, preds, epoch):

        score = -val_loss
        self.val_loss_history.append(val_loss)

        if self.best_score is None:
            self.best_score = score
            self.save_checkpoint(val_loss, model, preds, epoch)
            self.save_latest(val_loss, model, preds, epoch, score)
        elif score >= self.best_score:
            self.counter = 0
            self.best_score = score
            self.save_checkpoint(val_loss, model, preds, epoch)
            self.save_latest(val_loss, model, preds, epoch, score)
        # nanになったら学習ストップ
        elif math.isnan(score):
            self.early_stop = True
        else:
            self.counter += 1
            if self.save_latest_path is not None:
                self.save_latest(val_loss, model, preds, epoch, score)
            if self.verbose:
                print(f'EarlyStopping counter: {self.counter} out of {self.patience}')
            if self.counter >= self.patience:
                self.early_stop = True

    def save_checkpoint(self, val_loss, model, preds, epoch):
        '''Saves model when validation loss decrease.'''
        if self.verbose:
            print(f'Validation loss decreased ({self.val_loss_min:.10f} --> {val_loss:.10f}).  Saving model ...')
        torch.save({'model': model.state_dict(), 'preds': preds, 'epoch' : epoch, 
                    'best_score' : self.best_score, 'counter' : self.counter, 
                    'val_loss_history': self.val_loss_history},
                   self.save_path)
        self.val_loss_min = val_loss

    def save_latest(self, val_loss, model, preds, epoch, score):
        '''Saves latest model.'''
        torch.save({'model': model.state_dict(), 'preds': preds, 'epoch' : epoch, 
                    'score' : score, 'counter' : self.counter, 
                    'val_loss_history': self.val_loss_history},
                   self.save_latest_path)
        self.val_loss_min = val_loss
