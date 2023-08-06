from tensorflow.python.keras.regularizers import l2, l1, l1_l2
from tensorflow.python.keras.initializers import *
import random
import numpy as np
import os
import tensorflow as tf
from tensorflow.python.keras.optimizers import *
import logging

def set_optimizer(optimizer):
    if isinstance(optimizer, str):
        if '(' in optimizer:
            return eval(optimizer)
        elif optimizer == 'adam':
            return Adam(lr=1e-3, epsilon=1e-8, clipvalue=100)
    return optimizer

def set_loss(loss):
    if isinstance(loss, str):
        if loss in ['bce', 'binary_crossentropy', 'binary_cross_entropy']:
            loss = 'binary_crossentropy'
        else:
            raise NotImplementedError('loss={} is not supported.'.format(loss))
    return loss

def set_regularizer(reg):
    if not reg:
        return None
    elif isinstance(reg, float):
        return l2(reg)
    elif isinstance(reg, str):
        if '(' in reg:
            try:
                return eval(reg)
            except:
                pass
    raise NotImplementedError('reg={} is not supported.'.format(reg))

def set_initializer(initializer, seed=None):
    if isinstance(initializer, str):
        try:
            if '(' not in initializer:
                return eval(initializer)(seed=seed)
            elif 'seed' in initializer:
                return eval(initializer)
            else:
                return eval(initializer.rstrip(')') + ', seed={})'.format(seed))
        except:
            pass 
    return initializer

def seed_everything(seed=2019):
    logging.info('Setting random seed={}'.format(seed))
    if seed >= 0:
        random.seed(seed)
        np.random.seed(seed)
        os.environ['PYTHONHASHSEED'] = str(seed)
        tf.set_random_seed(seed)

