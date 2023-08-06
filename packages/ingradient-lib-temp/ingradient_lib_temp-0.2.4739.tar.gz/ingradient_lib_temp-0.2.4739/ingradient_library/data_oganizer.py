from ingradient_library.preprocessing import Cropping
import SimpleITK as sitk
import pickle
import os
import numpy as np

class Data_Organizer(object):
    def __init__(self, SAVE_PATH, ID = 'ingradient'):
        self.crop = Cropping()
        self.SAVE_PATH = SAVE_PATH
        self.ID = ID
    

    def run(self, seg_path, img_path_list, index, modality = ['CT']):
        seg = sitk.ReadImage(seg_path)
        save_dict = dict()
        save_dict['spacing'] = seg.GetSpacing()
        save_dict['direction'] = seg.GetDirection()
        save_dict['origin'] = seg.GetOrigin()
        save_dict['modality'] = modality
        seg = sitk.GetArrayFromImage(seg)
        save_path = os.path.join(self.SAVE_PATH, self.ID+str(index)+'_info.pkl')
        pickle_file = open(save_path, 'wb')
        pickle.dump(save_dict, pickle_file)
        pickle_file.close()

        for i in range(len(img_path_list)):
            img_path = img_path_list[i]
            img = sitk.ReadImage(img_path)
            img = sitk.GetArrayFromImage(img)
            if len(img.shape) != 4:
                img = np.expand_dims(img, axis = 0)
            if i == 0:
                images = img
            else:
                images = np.vstack(images, img)
            
        img_arr, seg_arr = self.crop(images, seg)
        np.savez(os.path.join(self.SAVE_PATH, self.ID+str(index)+'.npz'), x =img_arr, y=seg_arr)