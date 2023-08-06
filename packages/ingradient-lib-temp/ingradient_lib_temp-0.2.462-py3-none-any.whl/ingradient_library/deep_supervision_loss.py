import torch
import torch.nn.functional as F


def deep_supervision_loss(output, target, CE_weight = None, device = 0):

    """
    output => (batch size, deep supervision, n_classes. x, y, z)
    resolution이 낮아질 수록 1/2가 됨.
    """
    device = output.device.index
    n_bs, n_ds, _ = output.shape[0], output.shape[1], output.shape[2]
    loss = dice_loss(output, target).unsqueeze(0)
    acc_value = 0.5
    weight = torch.ones(n_ds).to(device)
    for i in range(n_ds):
        weight[i] = acc_value ** i
    weight = weight / weight.sum()
    weight = weight.view(1, 1, n_ds)
    loss = loss * weight
    loss = loss.mean()
    loss2 = deepsupervision_CE_loss(output, target, CE_weight, device).view(n_bs, n_ds, -1)
    loss2 = loss2 * weight.view(1, n_ds, 1)
    
    return loss + loss2.mean()
    

def dice_loss(output, target, smooth = 1.0, background_index = 0):
    n_bs, n_ds, n_cls = output.shape[0], output.shape[1], output.shape[2]
    mask = torch.arange(0, n_cls) != background_index
    target = F.one_hot(target, num_classes= n_cls).permute(0, 4, 1, 2, 3)[:,mask]
    target = target.view(n_bs, 1, n_cls - 1, -1) # Deep Supervision과 차원을 맞춰 Vectorization을 위해 Unsqueeze
    dice_output = output.view(n_bs, n_ds, n_cls, -1)[:, :, mask] # 2D, 3D에 모두 상관없이 사용하기 위헤 마지막 차원을 -1로 핀다.
    

    intersection = (dice_output * target).sum(dim = (-1, -2))
    union = dice_output.sum(dim = (-1, -2)) + target.sum(dim = (-1, -2))
    
    dice = 2.0 * (intersection + smooth) / (union + smooth)
    loss = 1.0 - dice
    
    return loss


def deepsupervision_CE_loss(output, target, weight, device = 0):
    n_bs, n_ds, n_cls = output.shape[0], output.shape[1], output.shape[2]
    result = torch.zeros((n_ds, n_bs)).to(device)
    target = target.view(n_bs, -1) # Deep Supervision과 차원을 맞춰 Vectorization을 위해 Unsqueeze
    target = torch.tile(target, (1, n_ds, 1)).view(n_bs * n_ds, -1)
    output = output.view(n_bs * n_ds, n_cls, -1) # 2D, 3D에 모두 상관없이 사용하기 위헤 마지막 차원을 -1로 핀다.
    if weight:
        return F.cross_entropy(output, target, weight, reduction = 'none')
    
    else:
        return F.cross_entropy(output, target, reduction = 'none')
    