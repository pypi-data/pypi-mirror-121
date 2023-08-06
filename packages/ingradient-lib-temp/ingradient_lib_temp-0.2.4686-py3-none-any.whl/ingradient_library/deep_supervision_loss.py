import torch
import torch.nn.functional as F


def deep_supervision_loss(output, target, writer = None, dice = True, ce = True, device = 0, background_index = 0, alpha = 10.0):
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



def interactive_loss(output, target, smooth = 1.0):
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
    loss = loss.mean()

    return loss