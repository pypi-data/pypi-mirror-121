import torch
import torch.nn.functional as F
import torch.nn as nn
from torch.utils.tensorboard import SummaryWriter

def nn_unet_loss(output, target, writer = None, dice = True, ce = True, device = 0, background_index = 0, alpha = 10.0):
    """
    output => (batch size, deep supervision, n_classes. x, y, z)
    resolution이 낮아질 수록 1/2가 됨.
    """
    n_bs, n_ds, _ = output.shape[0], output.shape[1], output.shape[2]
    loss = dice_loss(output, target, background_index).unsqueeze(0)
    acc_value = 0.5
    weight = torch.ones(n_ds).to(device)
    for i in range(n_ds):
        weight[i] = acc_value ** i
    
    weight = weight / weight.sum()
    weight = weight.view(1, 1, n_ds)
    loss = loss * weight
    loss = loss.mean() * alpha
    loss2 = deepsupervision_CE_loss(output, target, device).view(n_bs, n_ds, -1)
    loss2 = loss2 * weight.view(1, n_ds, 1)
    loss2 = loss2.mean()
    if writer != None:
        writer.add_scalar('Loss/dice', loss)
        writer.add_scalar('Loss/CE', loss2)
    
    return loss + loss2
    

def dice_loss(output, target, background_index, smooth = 1.0):
    n_bs, n_ds, n_cls = output.shape[0], output.shape[1], output.shape[2]
    mask = torch.arange(0, n_cls) != background_index
    target = F.one_hot(target, num_classes= n_cls).permute(0, 4, 1, 2, 3)[:,mask]
    target = target.view(n_bs, 1, n_cls - 1) # Deep Supervision과 차원을 맞춰 Vectorization을 위해 Unsqueeze
    dice_output = output.view(n_bs, n_ds, n_cls, -1)[:, :, mask] # 2D, 3D에 모두 상관없이 사용하기 위헤 마지막 차원을 -1로 핀다.
    

    intersection = (dice_output * target).sum(dim = (-1, -2))
    union = dice_output.sum(dim = (-1, -2)) + (n_ds * target.sum(dim = (-1, -2)))
    
    dice = 2.0 * (intersection + smooth) / (union + smooth)
    loss = 1.0 - dice
    
    return loss



def deepsupervision_CE_loss(output, target, weight, device = 0):
    n_bs, n_ds, n_cls = output.shape[0], output.shape[1], output.shape[2]
    result = torch.zeros((n_ds, n_bs)).to(device)
    target = target.view(n_bs, -1)
    target = torch.tile(target, (1, n_ds, 1)).view(n_bs * n_ds, -1)
    output = output.view(n_bs * n_ds, n_cls, -1)
    if weight:
        return F.cross_entropy(output, target, weight, reduction = 'none')
    
    else:
        return F.cross_entropy(output, target, reduction = 'none')



def binary_dice_loss(output, target, smooth = 1.0):
    n_bs, n_ds, n_cls = output.shape[0], output.shape[1], output.shape[2]
    target = target.view(n_bs, 1, n_cls, -1)
    output = output.view(n_bs, n_ds, n_cls, -1)

    intersection = (output * target).sum(dim = (-1, -2))
    union = output.sum(dim = (-1, -2)) + (n_ds * target.sum(dim = (-1, -2)))
    dice = 2.0 * (intersection + smooth) / (union + smooth)
    loss = 1.0 - dice

    loss = loss.unsqueeze(0)
    acc_value = 0.5
    weight = torch.ones(n_ds).to(output.device.index)

    for i in range(n_ds):
        weight[i] = acc_value ** i
    
    weight = weight / weight.sum()
    weight = weight.view(1, 1, n_ds)
    loss = loss * weight
    loss = loss.mean() * n_ds

    return loss



class Deep_Supervision_Loss(nn.Module):
    """
    1. 모든 Loss Funtion은 Reduction이어야한다.
    2. Target (Batch Size, x, y, z) 의 형태이며 element는 class number이다.
    3. Input은 (Batch Size, n_class, x, y, z) 형태이다.

    """
    def __init__(self, n_deepsupervision, loss1, loss2 = None, regularizer = 1.0, deep_supervision_weight = 0.5):
        super(Deep_Supervision_Loss, self).__init__()
        self.n_deepsupervision = n_deepsupervision
        loss1.reduction = 'none'
        if loss2 != None:
            loss1.reduction = 'none'
        self.loss1 = loss1
        self.loss2 = loss2
        self.regularizer = regularizer
        self.deep_supervision_weight = deep_supervision_weight
        self.writer = SummaryWriter()
        
    
    def forward(self, output, target):
        batch_size, deep_supervision_size, channel_size, size_x, size_y, size_y = output.shape
        output = output.reshape(batch_size * deep_supervision_size, channel_size, -1)
        target = target.reshape(batch_size, 1, -1).repeat(1, deep_supervision_size,1).reshape(batch_size * deep_supervision_size, -1)

        result = self.loss1(output, target).mean(-1)
        print('loss1', result)
        self.writer.add_scalar('Iteration_Loss/loss1', result[0])
        if self.loss2 != None:
            result += self.loss2(output, target).mean(-1) * self.regularizer
            self.writer.add_scalar('Iteration_Loss/loss2', result[0])

        result = result.view(batch_size, deep_supervision_size, -1)
    
        weight = torch.ones(deep_supervision_size).to(output.device.index)
        acc_value = self.deep_supervision_weight
        for i in range(deep_supervision_size):
            weight[i] = acc_value ** i
    
        weight = weight / weight.sum()
        weight = weight.view(1,deep_supervision_size ,1)
        result = result * weight

        return result.mean()
        


class Binary_Dice_Loss(nn.Module):
    def __init__(self, smooth = 1.0):
        super(Binary_Dice_Loss, self).__init__()
        self.smooth = smooth
    
    def forward(self, output, target):
        # output shape => (n_bs, 1, -1)
        # target shape => (n_bs, -1)
        n_bs = output.shape[0]
        output = output.view(n_bs, -1)
        intersection = (output * target).sum(-1)  # (n_bs, n_ds)
        union = output.sum(-1) + target.sum(-1)
        dice = 2.0 * (intersection + self.smooth) / (union + self.smooth)
        return 1 - dice


class Multi_Dice_Loss(nn.Module):
    def __init__(self, num_classes, smooth = 1.0, background_index = 0):
        super(Multi_Dice_Loss, self).__init__()
        self.smooth = smooth
        self.background_index = background_index
        self.num_classes = num_classes
        self.mask = (torch.arange(0, num_classes) != self.background_index)
        self.reduction = 'none'

    def forward(self, output, target):
        #output shape => (n_bs, n_classes, -1)
        #target shape => (n_bs, -1)
        self.mask.to(output.device.index)
        n_bs = output.shape[0]
        output = output.view(n_bs, self.num_classes, -1)
        target = target.view(n_bs, -1)
        output = output[:, self.mask].permute(0, 2, 1) # (n_bs,  -1, n_cls)
        target = F.one_hot(target, num_classes = self.num_classes)
        target = target[:,:, self.mask]
        intersection = output * target #각 class 별 intersection score를 합함.
        union = output.sum((-1,-2)) + target.sum((-1,-2)) #각 class 별 union score를 합함.
        union = union.view(n_bs, 1, 1)
        dice = 2.0 * (intersection + self.smooth) / (union + self.smooth)
        
        return 1 - dice.mean(-1)


