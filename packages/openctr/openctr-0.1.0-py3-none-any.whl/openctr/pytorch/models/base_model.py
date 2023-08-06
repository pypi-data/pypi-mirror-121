import torch.nn as nn
import numpy as np
import torch
import os
import logging
from tqdm import tqdm
from ...metrics import evaluate_metrics
from ...pytorch.utils import set_device, set_optimizer, set_loss, set_regularizer
from ...utils import Monitor

class BaseModel(nn.Module):
    def __init__(self, feature_encoder, model_id="BaseModel", gpu=-1, monitor="AUC", 
                 save_best_only=True, monitor_mode="max", patience=2, every_x_epochs=1,
                 embedding_regularizer=None, kernel_regularizer=None, 
                 reduce_lr_on_plateau=True, **kwargs):
        super(BaseModel, self).__init__()
        self.device = set_device(gpu)
        self._monitor = Monitor(kv=monitor)
        self._monitor_mode = monitor_mode
        self._patience = patience
        self._every_x_epochs = every_x_epochs # float acceptable
        self._save_best_only = save_best_only
        self._embedding_regularizer = embedding_regularizer
        self._kernel_regularizer = kernel_regularizer
        self._reduce_lr_on_plateau = reduce_lr_on_plateau
        self.model_id = model_id
        self.experiment_id = '_'.join([model_id, feature_encoder.dataset_id])
        self.checkpoint = os.path.abspath(os.path.join(kwargs['model_dir'], 
                                          feature_encoder.dataset_id + '/'
                                          + self.experiment_id + '_model.ckpt'))
        self._validation_metrics = kwargs['metrics']

    def compile(self, optimizer, loss, lr=1e-3):
        try:
            self.optimizer = set_optimizer(optimizer)(self.parameters(), lr=lr)
        except:
            raise NotImplementedError("optimizer={} is not supported.".format(optimizer))
        try:
            self.loss_fn = getattr(torch.functional.F, set_loss(loss))
        except:
            raise NotImplementedError("loss={} is not supported.".format(loss))

    def loss_with_reg(self, y_pred, y_true):
        total_loss = self.loss_fn(y_pred, y_true)
        if self._embedding_regularizer or self._kernel_regularizer:
            emb_p, emb_lambda = set_regularizer(self._embedding_regularizer)
            kernel_p, kernel_lambda = set_regularizer(self._kernel_regularizer)
            for name, param in self.named_parameters():
                if param.requires_grad:
                    if 'embedding_layer' in name:
                        if self._embedding_regularizer:
                            total_loss += (emb_lambda / emb_p) * torch.norm(param, emb_p) ** emb_p
                    else:
                        if self._kernel_regularizer:
                            total_loss += (kernel_lambda / kernel_p) \
                                          * torch.norm(param, kernel_p) ** kernel_p
        return total_loss

    def init_weights(self, embedding_initializer=None):
        def _initialize(m):
            if type(m) == nn.Embedding:
                if embedding_initializer is not None:
                    try:
                        initializer = embedding_initializer.replace('(', '(m.weight,')
                        eval(initializer)
                    except:
                        raise NotImplementedError('embedding_initializer={} is not supported.'\
                                                  .format(embedding_initializer))
                else:
                    nn.init.xavier_normal_(m.weight)
            if type(m) == nn.Linear:
                nn.init.xavier_normal_(m.weight)
                if m.bias is not None:    
                    m.bias.data.fill_(0)
        self.apply(_initialize)
        
    def inputs_to_device(self, inputs):
        X, y = inputs
        X = X.to(self.device)
        y = y.float().view(-1, 1).to(self.device)
        self.batch_size = y.size(0)
        return X, y
    
    def on_batch_end(self, batch, logs={}):
        self._total_batches += 1
        if (batch + 1) % self._every_x_batches == 0 or (batch + 1) % self._batches_per_epoch == 0:
            val_logs = self.evaluate_generator(self.valid_gen)
            epoch = round(float(self._total_batches) / self._batches_per_epoch, 2)
            self.checkpoint_and_earlystop(epoch, val_logs)
            logging.info('--- {}/{} batches finished ---'.format(batch + 1, self._batches_per_epoch))

    def reduce_learning_rate(self, factor=0.1, min_lr=1e-6):
        for param_group in self.optimizer.param_groups:
            reduced_lr = max(param_group['lr'] * factor, min_lr)
            param_group['lr'] = reduced_lr
        return reduced_lr

    def checkpoint_and_earlystop(self, epoch, logs, min_delta=1e-6):
        monitor_value = self._monitor.get_value(logs)
        if (self._monitor_mode == 'min' and monitor_value > self._best_metric - min_delta) or \
           (self._monitor_mode == 'max' and monitor_value < self._best_metric + min_delta):
            self._stopping_steps += 1
            logging.info('Monitor({}) STOP: {:.6f} !'.format(self._monitor_mode, monitor_value))
            if self._reduce_lr_on_plateau:
                current_lr = self.reduce_learning_rate()
                logging.info('Reduce learning rate on plateau: {:.6f}'.format(current_lr))
        else:
            self._stopping_steps = 0
            self._best_metric = monitor_value
            if self._save_best_only:   
                logging.info('Save best model: monitor({}): {:.6f}'\
                             .format(self._monitor_mode, monitor_value))
                self.save_weights(self.checkpoint)
        if self._stopping_steps * self._every_x_epochs >= self._patience:
            self._stop_training = True
            logging.info('Early stopping at epoch={:g}'.format(epoch))
        if not self._save_best_only:
            self.save_weights(self.checkpoint)
            
    def fit_generator(self, data_generator, epochs=1, validation_data=None,
                      verbose=0, max_gradient_norm=10., **kwargs):
        """
        Training a model and valid accuracy.
        Inputs:
        - iter_train: I
        - iter_val: .
        - optimizer: Abstraction of optimizer used in training process, e.g., "torch.optim.Adam()""torch.optim.SGD()".
        - epochs: Integer, number of epochs.
        - verbose: Bool, if print.
        """
        self.valid_gen = validation_data
        self._max_gradient_norm = max_gradient_norm
        self._best_metric = np.Inf if self._monitor_mode == 'min' else -np.Inf
        self._stopping_steps = 0
        self._total_batches = 0
        self._batches_per_epoch = len(data_generator)
        self._every_x_batches = int(np.ceil(self._every_x_epochs * self._batches_per_epoch))
        self._stop_training = False
        self._verbose = verbose
        self.to(device=self.device)
        logging.info("**** Start training: {} batches/epoch ****".format(self._batches_per_epoch))
        
        for epoch in range(epochs):
            epoch_loss = self.train_on_epoch(data_generator)
            logging.info('Train loss: {:.6f}'.format(epoch_loss))
            if self._stop_training:
                break
            else:
                logging.info('************ Epoch={} end ************'.format(epoch + 1))            
        logging.info('Training finished.')
        logging.info('Load best model: {}'.format(self.checkpoint))
        self.load_weights(self.checkpoint)

    def train_on_epoch(self, data_generator):
        epoch_loss = 0
        model = self.train()
        tqdm_batch_iterator = tqdm(data_generator)
        for batch_index, batch_data in enumerate(tqdm_batch_iterator, 1):
            self.optimizer.zero_grad()
            return_dict = model.forward(batch_data)
            loss = return_dict["loss"]
            loss.backward()
            nn.utils.clip_grad_norm_(self.parameters(), self._max_gradient_norm)
            self.optimizer.step()
            epoch_loss += loss.item()
            self.on_batch_end(batch_index)
            if self._stop_training:
                break
        return epoch_loss / self._batches_per_epoch

    def evaluate_generator(self, data_generator):
        self.eval()  # set to evaluation mode
        with torch.no_grad():
            y_pred = []
            y_true = []
            for batch_data in data_generator:
                return_dict = self.forward(batch_data)
                y_pred.extend(return_dict["y_pred"].data.cpu().numpy())
                y_true.extend(batch_data[1].data.cpu().numpy().reshape(-1))
            y_pred = np.array(y_pred, np.float64)
            val_logs = evaluate_metrics(y_true, y_pred, self._validation_metrics)
            return val_logs
                
    def save_weights(self, checkpoint):
        torch.save(self.state_dict(), checkpoint)
    
    def load_weights(self, checkpoint):
        self.load_state_dict(torch.load(checkpoint, map_location=self.device))

    def get_final_activation(self, task='classification'):
        if task == 'classification':
            return 'Sigmoid'
        elif task == 'regression':
            return None
        else:
            raise NotImplementedError('task={} is not supported.'.format(task))

    def plot_grad_flow(self, named_parameters):
        ''' Plots the gradients flowing through different layers in the net during training.
        Can be used for checking for possible gradient vanishing / exploding problems.
        
        Usage: Plug this function in Trainer class after loss.backwards() as 
        "plot_grad_flow(self.model.named_parameters())" to visualize the gradient flow
        '''
        import matplotlib.pyplot as plt
        from matplotlib.lines import Line2D

        ave_grads = []
        max_grads= []
        layers = []
        for n, p in named_parameters:
            print(n)
            if(p.requires_grad) and ("bias" not in n):
                layers.append(n)
                ave_grads.append(p.grad.abs().mean())
                max_grads.append(p.grad.abs().max())
        plt.bar(np.arange(len(max_grads)), max_grads, alpha=0.1, lw=1, color="c")
        plt.bar(np.arange(len(max_grads)), ave_grads, alpha=0.1, lw=1, color="b")
        plt.hlines(0, 0, len(ave_grads)+1, lw=2, color="k" )
        plt.xticks(range(0,len(ave_grads), 1), layers, rotation="vertical")
        plt.xlim(left=0, right=len(ave_grads))
        plt.ylim(bottom = -0.001, top=0.02) # zoom in on the lower gradient regions
        plt.xlabel("Layers")
        plt.ylabel("average gradient")
        plt.title("Gradient flow")
        plt.grid(True)
        plt.legend([Line2D([0], [0], color="c", lw=4),
                    Line2D([0], [0], color="b", lw=4),
                    Line2D([0], [0], color="k", lw=4)], ['max-gradient', 'mean-gradient', 'zero-gradient'])