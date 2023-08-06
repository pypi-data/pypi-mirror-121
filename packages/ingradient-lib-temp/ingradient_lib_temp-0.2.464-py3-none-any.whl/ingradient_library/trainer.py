from torch.utils.tensorboard import SummaryWriter
import torch.optim as optim
from torch.utils.data import random_split
import torch
from dataloads import *
from model import *
from preprocessing import *
from data_augmentation import *
from deep_supervision_loss import *
from visualization import *
from optimizer import SAMSGD


class Trainer(object):
    def __init__(self, tr_dataloader, val_dataloader, model, model_kwargs, optimizer, optim_kwargs, lr_decay_ratio, loss_func,
                n_epoch, save_path = None, visualization = None):
        self.model = model(**model_kwargs)
        self.optimizer = optimizer(self.model.parameters(), **optim_kwargs)
        self.lr_rate = optim_kwargs['lr']
        self.lr_decay_ratio = lr_decay_ratio
        self.loss_func = loss_func
        self.n_epoch = n_epoch
        self.save_path = save_path
        self.visualization = None
        self.tr_dl = tr_dataloader
        self.val_dl = val_dataloader
        

    def load_model_state_dict(self, path, load_classifier = False):
        pretrained_dict = torch.load(path)
        if not load_classifier:
            classifier = list(self.model._modules)[-1]
            for k in list(pretrained_dict.keys()):
                if classifier in k:
                    del pretrained_dict[k]

        current_dict = self.backbone.state_dict()
        current_dict.update(pretrained_dict)
        self.backbone.load_state_dict(current_dict)

    def run(self):
        writer = SummaryWriter()
        for e in range(self.epoch):
            self.optimizer.param_groups[0]['lr'] = self.lr_rate * ((e/self.epoch)**self.lr_decay_ratio)
            self.tr_dl.new_epoch()
            train_loss = 0
            n_iter = 0
            self.model.train()
            
            while self.tr_dl.is_end():
                n_iter += 1
                image, seg = self.tr_dl.generate_train_batch()
                if isinstance(self.optimizer, SAMSGD):
                    def closure():
                        self.optimizer.zero_grad()
                        output = self.model(images)
                        loss = self.loss_func(output, seg)
                        train_loss += loss.item()
                        loss.backward()
                        return loss
                    self.optimizer.step(closure)
                
                else:
                    output = self.model(images)
                    self.optimizer.zero_grad()
                    loss = self.loss_func(output, seg)
                    train_loss += loss.item()
                    loss.backward()
                    self.optimizer.step()
                
            train_loss /= n_iter
            writer.add_scalar('Loss/train', train_loss)

            
            self.val_dl.new_epoch()
            val_loss = 0
            n_iter = 0
            self.model.eval()
            while not self.val_dl.is_end():
                n_iter +=1
                with torch.no_grad():
                    images, seg = self.val_dl.generate_train_batch()
                    output = self.model(images)
                    loss = self.loss_func(output, seg)
                    val_loss += loss.item()
                    if self.visualization != None:
                        if self.val_dl.current_index == 0:
                            self.visualization(output, seg)
            val_loss /= n_iter
            writer.add_scalar('Loss/valid', train_loss)
            if self.save_path != None:
                file_name = 'epoch'+ str(e) + '_model_state_dict.pkl'
                torch.save(self.model.state_dict(), os.path.join(self.save_path, file_name))
        

        writer = SummaryWriter()
