import sys
import os
import numpy as np
import torch
import random

def seed_everything(seed=1029):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True

def set_device(gpu=-1):
    if gpu != -1 and torch.cuda.is_available():
        device = torch.device('cuda: ' + str(gpu))
    else:
        device = torch.device('cpu')   
    return device

def set_optimizer(optimizer):
    if isinstance(optimizer, str):
        if optimizer.lower() == 'adam':
            optimizer = 'Adam'
        return getattr(torch.optim, optimizer)

def set_loss(loss):
    if isinstance(loss, str):
        if loss in ['bce', 'binary_crossentropy', 'binary_cross_entropy']:
            loss = 'binary_cross_entropy'
        else:
            raise NotImplementedError('loss={} is not supported.'.format(loss))
    return loss

def set_regularizer(reg):
    p_norm = 2
    weight = None
    if isinstance(reg, float):
        weight = reg
    elif isinstance(reg, str):
        try:
            p_norm = int(reg[1])
            weight = float(reg.rstrip(')').split('(')[-1])
        except:
            raise NotImplementedError('regularizer={} is not supported.'.format(reg))
    return p_norm, weight

def set_activation(activation):
    if isinstance(activation, str):
        if activation.lower() == 'relu':
            return 'ReLU'
        elif activation.lower() == 'sigmoid':
            return 'Sigmoid'