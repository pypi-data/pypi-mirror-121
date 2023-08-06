from torch.utils.tensorboard import SummaryWriter
import torch.optim as optim
from torch.utils.data import random_split
import torch
from ingradient_library.dataloads import *
from ingradient_library.model import *
from ingradient_library.preprocessing import *
from ingradient_library.deep_supervision_loss import *
from ingradient_library.visualization import *
from ingradient_library.optimizer import SAMSGD
from ingradient_library.sampling import *


class Trainer(object):
    def __init__(self, tr_dataloader, model,  optimizer, loss_func, scheduler,
                n_epoch = 1000, val_dataloader = None, save_path = None):
        self.model = model
        self.optimizer = optimizer
        self.loss_func = loss_func
        self.n_epoch = n_epoch
        self.save_path = save_path
        self.visualization = None
        self.tr_dl = tr_dataloader
        self.val_dl = val_dataloader
        self.scheduler = scheduler
        

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
        for e in range(self.n_epoch):
            self.tr_dl.new_epoch()
            n_iter = 0
            self.model.train()
            
            while not self.tr_dl.is_end():
                n_iter += 1
                images, seg = self.tr_dl.generate_train_batch()
                if isinstance(self.optimizer, SAMSGD):
                    def closure():
                        self.optimizer.zero_grad()
                        output = self.model(images)
                        loss = self.loss_func(output, seg)
                        train_loss = loss.item()
                        loss.backward()
                        return loss
                    self.optimizer.step(closure)
                
                else:
                    output = self.model(images)
                    self.optimizer.zero_grad()
                    loss = self.loss_func(output, seg)
                    train_loss = loss.item()
                    if self.tr_dl.current_index == 0:
                        deep_supervision_visualization(output, seg)
                    loss.backward()
                    self.optimizer.step()
            if n_iter > 0 :
                train_loss /= n_iter
            writer.add_scalar('Epoch_Loss/train', train_loss)

            if self.val_dl != None:
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
                if n_iter > 0 :
                    val_loss /= n_iter
                writer.add_scalar('Epoch_Loss/valid', val_loss)
            self.scheduler.step()
            if self.save_path != None:
                file_name = 'epoch'+ str(e) + '_model_state_dict.pkl'
                torch.save(self.model.state_dict(), os.path.join(self.save_path, file_name))
        


class Interactive_Trainer(object):
    def __init__(self, tr_dataloader,  model,  optimizer, loss_func, scheduler,
                n_epoch = 1000, val_dataloader = None, save_path = None, n_point = 10):
        self.model = model
        self.optimizer = optimizer
        self.loss_func = loss_func
        self.n_epoch = n_epoch
        self.save_path = save_path
        self.visualization = None
        self.tr_dl = tr_dataloader
        self.val_dl = val_dataloader
        self.n_point = n_point
        self.scheduler = scheduler
    
    def run(self, visualization_ineterval = 20):
        writer = SummaryWriter()
        for e in range(self.n_epoch):
            self.tr_dl.new_epoch()
            train_loss = 0
            n_iter = 0
            self.model.train()
            
            while not self.tr_dl.is_end():
                n_iter += 1
                images, seg = self.tr_dl.generate_train_batch()
                bs, _, nx, ny, nz = images.shape #bs, n_modalities, 
                #First
                positive_points, negative_points = point_sampler(seg)
                output = self.model(images, positive_points, negative_points)
                self.optimizer.zero_grad()
                loss = self.loss_func(output, seg)
                train_loss = loss.item()
                
                center = output.shape[3] // 2
                if self.tr_dl.current_index % visualization_ineterval == 0:
                    print("points : ", 0)
                    deep_supervision_visualization(output, seg)
                writer.add_scalar('Loss/no_click'+'0', train_loss)
                loss.backward()
                self.optimizer.step()

                for i in range(self.n_point):
                    self.optimizer.zero_grad()
                    prev_seg = (output[:, 0] > 0.5).long()
                    positive_points, negative_points = point_sampler(seg, prev_seg, positive_points, negative_points)
                    output = self.model(images, positive_points, negative_points, prev_seg)
                    loss = self.loss_func(output, seg)
                    train_loss = loss.item()
                    if self.tr_dl.current_index % visualization_ineterval == 0:
                        print("points : ",i + 1)
                        deep_supervision_visualization(output, seg)
                    writer.add_scalar('Loss/clicks_'+str(i+1), train_loss)
                    loss.backward()
                    self.optimizer.step()
            self.scheduler.step()


            if self.save_path != None:
                file_name = 'epoch'+ str(e) + '_model_state_dict.pkl'
                torch.save(self.model.state_dict(), os.path.join(self.save_path, file_name))
