import numpy as np
import torch


def is_overlap(points, current_point):
    if current_point in points:
        return True
    else:
        return False

def get_random_sample(points, candidates, batch_index):
    n_candidates = len(candidates[0])
    index = np.random.choice(np.arange(n_candidates), size = (n_candidates,), replace = False)
    p_batch = batch_index
    i = 0
    x = candidates[0][index[i]]
    y = candidates[1][index[i]]
    z = candidates[2][index[i]]
    
    while is_overlap(points, current_point=[p_batch, x, y, z]) and i < len(index) - 1:
        i += 1
        p_batch = batch_index
        x = candidates[0][index[i]]
        y = candidates[1][index[i]]
        z = candidates[2][index[i]]
    
    point = [p_batch, x, y, z]
    if not is_overlap(points, point):
        points.append([torch.tensor(p_batch).long(), x.long(), y.long(), z.long()])
    return points

def point_sampler(target, prev_seg = None, positive_points = [], negative_points = []):
    # target shpae, prev_seg => (batch, x, y, z)
    # positive_points, negative_points => (n, 4) [(batch_index, x_index, y_index, z_index), ...과 같은 방식], 입력 시 Transpose를 이용해 쉽게 넣을 수 있다.
    # 초기값 세팅
    bs, x, y, z = target.shape
    if prev_seg == None:
        prev_seg = torch.zeros(target.shape).to(target.device.index)
    
    for batch_index in range(bs):
        if (prev_seg[batch_index] != target[batch_index]).sum() == 0:
            # Ground truth = Predicted Segmentation
            continue

        elif prev_seg[batch_index].sum() >= target[batch_index].sum():
            # negative sampling
            candidates = torch.where((target * (prev_seg != target)) == 0)
            negative_points = get_random_sample(negative_points, candidates, batch_index)

        elif prev_seg[batch_index].sum() < target[batch_index].sum():
            # positive sampling
            candidates = torch.where((target * (prev_seg != target)) == 1)
            positive_points = get_random_sample(positive_points, candidates, batch_index)
    
    return positive_points, negative_points


def points_to_volume(shape, points, mode = 'positive', device = None):
        result = torch.zeros(shape).to(device)
        if len(points) == 0:
            return result
        bs = torch.tensor(points).T[0].long().to(device)
        x = torch.tensor(points).T[1].long().to(device)
        y = torch.tensor(points).T[2].long().to(device)
        z = torch.tensor(points).T[3].long().to(device)
        if mode == 'positive':
            result[(bs, x, y, z)] = 1
        
        elif mode == 'negative':
            result[(bs, x, y, z)] = -1
        return result