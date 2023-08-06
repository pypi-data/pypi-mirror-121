import torch
import torch.nn as nn
import torch.nn.functional as F
import SimpleITK as sitk
from torch.utils.data import Dataset
import numpy as np
import pickle
import numpy as numpy
import os

class CustomDataset(Dataset):
    def __init__(self, root_dir, device = None, normalizer = None, mode = 'train', dim = '3d', correct_direction = True, resample = None):
        self.root_dir = root_dir
        self.image_name = []
        self.info_name = []
        self.device = device
        self.normalizer = normalizer
        self.mode = mode
        self.dim = dim
        self.resample = resample
        self.correct_direction = correct_direction
        if resample != None :
            self.resample.device = device
        if normalizer != None:
            self.normalizer.device = device


        for file_name in os.listdir(root_dir):            
            if 'npz' in file_name:
                self.image_name.append(file_name)
            
            elif 'pkl' in file_name:
                self.info_name.append(file_name)
                    
        self.image_name = sorted(self.image_name)
        self.info_name = sorted(self.info_name)

    def __len__(self):
        return len(self.image_name)
    
    def set_direction(self, img, direction):
        direction = np.array(direction).reshape(3,3)
        inverse = np.where(direction == -1)[0]
        permute = np.where(direction != 0)[1]
        if 0 in inverse:
            img = img[::-1, :, :]

        if 1 in inverse:
            img = img[:, ::-1, :]

        if 2 in inverse:
            img = img[:, :, ::-1]

        return img.transpose(permute)
    
    def __getitem__(self, idx):
        info_file = open(os.path.join(self.root_dir,self.info_name[idx]), 'rb')
        info_data = pickle.load(info_file)
        info_file.close()
        data = np.load(os.path.join(self.root_dir, self.image_name[idx]))
        

        x = data['x']
        y = data['y']
        if len(x.shape) == 3 and self.dim == '3d':
            #modality가 1개인 경우
            x = np.expand_dims(x, axis = 0)
        elif len(x.shape) == 2 and self.dim == '2d':
            x = np.expand_dims(x, axis = 0)

        if self.correct_direction:
            for i in range(len(x)):
                x[i] = self.set_direction(x[i], info_data['direction'])
            y = self.set_direction(y, info_data['direction'])

        if self.normalizer:
            x = self.normalizer(x)
        
        
        if self.resample != None:
            y = torch.tensor(y.copy())
            result = self.resample(torch.vstack((x, y.unsqueeze(0))), info_data)
            x = result[:-1]
            y = result[-1].squeeze(0)

        if self.mode == 'train' :
            return x, y, info_data
        
        elif self.mode == 'test':
            return x, info_data



class DataLoader3D(object):

    def __init__(self, dataset, num_iteration = 2, patch_size = (128,128,128), transform= None, device = 0, batch_size = 2, seg_one_hot = False, is_half = False, info_class = None):
        self.dataset = dataset
        self.current_index = 0
        self.patch_size = np.array(patch_size)
        self.batch_size = batch_size
        self.now_iter = 0
        self.images, self.seg, self.info = self.get_image_seg(self.current_index)
        self.device = device
        self.pass_patient_index = []
        self.num_iteration = num_iteration
        self.seg_one_hot = seg_one_hot
        self.is_half = is_half
        self.info_class = info_class #[0, 1, 3, 4] 이런식
        self.transform = transform

    
    def new_epoch(self):
        self.now_iter = 0
        self.current_index = 0
    
    def is_end(self):
        return self.current_index == len(self.dataset) and self.now_iter == 0
    
    def return_class(self):
        return np.unique(self.seg)

    def next_index(self):
        if self.now_iter == self.num_iteration:
            self.images, self.seg, self.info = self.get_image_seg(self.current_index)
            self.current_index += 1
            self.now_iter = 0
        
        else:
            self.now_iter += 1

    def get_image_seg(self, current_index): #patch size보다 전체 이미지 크기가 작을 경우 padding을 진행
        images, seg, info = self.dataset[current_index]
        if isinstance(images, np.ndarray):
            images = torch.tensor(images.copy())
        if isinstance(seg, np.ndarray):
            seg = torch.tensor(seg.copy())
        image_shape = np.array(images[0].shape)
        if np.any(image_shape < self.patch_size):
            odd_pad = ((self.patch_size - image_shape) % 2 != 0).astype(int)
            even_pad = np.repeat(np.clip(((self.patch_size - image_shape)/2).astype(int), 0, np.inf), 2)
            for i in range(len(odd_pad)):
                even_pad[i*2] += odd_pad[i]
            even_pad = tuple(even_pad[::-1].astype(int).copy())
            images = F.pad(images, even_pad, "constant", 0 )
            seg = F.pad(seg, even_pad, "constant", 0 )

        return images, seg, info


    def get_oversample_patch(self, non_zero_coords, shape_to_index):
        oversample_high = np.clip(np.max(non_zero_coords, axis = 1) + 1, self.patch_size/2 - 1, shape_to_index - self.patch_size/2)
        oversample_low = np.clip(np.min(non_zero_coords, axis = 1), self.patch_size/2 - 1, shape_to_index - self.patch_size/2)
        oversample_center = np.random.randint(low = oversample_low, high = oversample_high + 1)

        oversample_patch_upper_bound = oversample_center + (self.patch_size/2) + 1
        oversample_patch_lower_bound = oversample_center - (self.patch_size/2 - 1)
        oversample_patch_bound = np.concatenate((oversample_patch_lower_bound.reshape(-1,1),oversample_patch_upper_bound.reshape(-1,1)), axis = 1).astype(int)

        oversample_patch_images = self.images[:, oversample_patch_bound[0][0] : oversample_patch_bound[0][1],
                                          oversample_patch_bound[1][0] : oversample_patch_bound[1][1],
                                          oversample_patch_bound[2][0] : oversample_patch_bound[2][1]]
        oversample_patch_seg = self.seg[oversample_patch_bound[0][0] : oversample_patch_bound[0][1],
                                          oversample_patch_bound[1][0] : oversample_patch_bound[1][1],
                                          oversample_patch_bound[2][0] : oversample_patch_bound[2][1]]
        
        return np.expand_dims(oversample_patch_images , axis = 0), np.expand_dims(oversample_patch_seg , axis = 0)

    def get_normal_patch(self, non_zero_coords, shape_to_index):
        normal_center = np.random.randint(low = self.patch_size/2 - 1, high = shape_to_index - (self.patch_size/2) + 1 )
        normal_patch_upper_bound = normal_center + (self.patch_size/2) + 1
        normal_patch_lower_bound = normal_center - (self.patch_size/2 - 1)
        normal_patch_bound = np.concatenate((normal_patch_lower_bound.reshape(-1,1),normal_patch_upper_bound.reshape(-1,1)), axis = 1).astype(int)
        normal_patch_images = self.images[:, normal_patch_bound[0][0] : normal_patch_bound[0][1],
                                          normal_patch_bound[1][0] : normal_patch_bound[1][1],
                                          normal_patch_bound[2][0] : normal_patch_bound[2][1]]
        normal_patch_seg = self.seg[normal_patch_bound[0][0] : normal_patch_bound[0][1],
                                          normal_patch_bound[1][0] : normal_patch_bound[1][1],
                                          normal_patch_bound[2][0] : normal_patch_bound[2][1]]
        
        return np.expand_dims(normal_patch_images , axis = 0), np.expand_dims(normal_patch_seg , axis = 0)
    



    def generate_train_batch(self):
        non_zero_coords = np.array(np.where(self.seg != 0))
        shape_to_index = np.array(self.images[0].shape) - 1 

        if self.batch_size == 1 :
            result_images, result_seg = self.get_normal_patch(non_zero_coords, shape_to_index)


        for i_b in range(self.batch_size//2):
            oversample_images, oversample_seg = self.get_oversample_patch(non_zero_coords, shape_to_index)
            normal_images, normal_seg = self.get_normal_patch(non_zero_coords, shape_to_index)

            if i_b == 0:
                result_images = np.concatenate((normal_images, oversample_images), axis = 0) #bs, n, x, y, z
                result_seg = np.concatenate((normal_seg, oversample_seg), axis = 0) #bs, x, y, z
            
            else:
                result_images = np.concatenate((result_images, oversample_images), axis = 0)
                result_seg = np.concatenate((result_seg, oversample_seg), axis = 0)
                result_images = np.concatenate((result_images, normal_images), axis = 0)
                result_seg = np.concatenate((result_seg, normal_seg), axis = 0)

        self.next_index()
        
    
        
        result_images = torch.Tensor(result_images).to(self.device)
        result_seg = torch.Tensor(result_seg).to(self.device)


        if self.transform:
            result_images, result_seg = self.transform(result_images, result_seg, self.info)
        
        if self.seg_one_hot:
            result_seg = F.one_hot(result_seg.long(),  num_classes = len(self.info_class)).permute(0, 4, 1, 2, 3)

        if self.is_half:
            result_images = result_images.half()
    

        return result_images, result_seg.long()



class Interactive_DataLoader(DataLoader3D):
    def __init__(self, dataset, num_iteration = 1, patch_size = (128,128,128), batch_size = 2, device = None, transform = None):
        self.dataset = dataset
        self.current_index = 0
        self.patch_size = np.array(patch_size)
        self.images, self.seg, self.info = self.get_image_seg(self.current_index)
        self.device = device
        self.num_iteration = num_iteration
        self.now_iter = 0
        self.batch_size = batch_size
        self.transform = transform
        
    def get_image_seg(self, current_index):
        return super().get_image_seg(current_index)
    
    def next_index(self):
        return super().next_index()
    
    def is_end(self):
        return super().is_end()
    
    def new_epoch(self):
        return super().new_epoch()
    
    def get_oversample_patch(self, non_zero_coords, shape_to_index):
        return super().get_oversample_patch(non_zero_coords, shape_to_index)

    def generate_train_batch(self):
        non_zero_coords = np.array(np.where(self.seg != 0))
        shape_to_index = np.array(self.images[0].shape) - 1 

        oversample_images, oversample_seg = self.get_oversample_patch(non_zero_coords, shape_to_index) #bs, n, x, y,z // bs, x, y, z
        oversample_images = torch.Tensor(oversample_images).to(self.device)
        oversample_seg = torch.Tensor(oversample_seg).to(self.device)

        if self.transform != None: 
            oversample_images, oversample_seg = self.transform(oversample_images, oversample_seg, self.info)
            
        oversample_images, oversample_seg = self.sampling(oversample_images.squeeze(0), oversample_seg)
        self.next_index()

        return oversample_images, oversample_seg
    
    def sampling(self, images, seg):
        category = torch.unique(seg)
        for i in range(self.batch_size):
            random_index = torch.randint(low = 1, high = len(category), size =(1,)).to(seg.device.index)
            if i == 0:
                new_seg = (seg == category[random_index]).long()

            else:
                new_seg = torch.vstack((new_seg, (seg == category[random_index]).long()))
        new_images = torch.tile(images, [self.batch_size, *(torch.tensor(images.shape)//torch.tensor(images.shape))])
        
        return new_images, new_seg
    