from tensorflow.python.keras.callbacks import Callback
import logging
import numpy as np
from ..utils import Monitor

class EvaluateMetricsCallback(Callback):
    def __init__(self, monitor='AUC', save_best_only=True, monitor_mode='max', patience=2, 
                 every_x_epoches=1, workers=2, **kwargs):
        self._every_x_epoches = every_x_epoches # float acceptable
        self._monitor = Monitor(kv=monitor)
        self._save_best_only = save_best_only
        self._mode = monitor_mode
        self._patience = patience
        self._best_metric = np.Inf if self._mode == 'min' else -np.Inf
        self._stopping_steps = 0
        self._total_batches = 0
        self._workers = workers
        
    def on_train_begin(self, logs={}):
        self._batches = self.params['steps']
        self._every_x_batches = int(np.ceil(self._every_x_epoches * self._batches))
        logging.info("**** Start training: {} batches/epoch ****".format(self._batches))

    def on_batch_end(self, batch, logs={}):
        self._total_batches += 1
        if (batch + 1) % self._every_x_batches == 0 or (batch + 1) % self._batches == 0:
            val_logs = self.model.evaluate_generator(self.model.valid_gen, self._workers)
            logs.update(val_logs)
            epoch = round(float(self._total_batches) / self._batches, 2)
            self.checkpoint_and_earlystop(epoch, val_logs)
            logging.info('******* {}/{} batches finished *******'.format(batch + 1, self._batches))

    def on_epoch_end(self, epoch, logs={}):
        if 'loss' in logs:
            logging.info('[Train] loss: {:.6f}'.format(logs['loss']))
        logging.info('************ Epoch={} end ************'.format(epoch + 1))

    def checkpoint_and_earlystop(self, epoch, logs):
        monitor_value = self._monitor.get_value(logs)
        if (self._mode == 'min' and monitor_value > self._best_metric) or \
           (self._mode == 'max' and monitor_value < self._best_metric):
            self._stopping_steps += 1
            logging.info('Monitor({}) drops: {:.6f}'.format(self._mode, monitor_value))
        else:
            self._stopping_steps = 0
            self._best_metric = monitor_value
            if self._save_best_only:   
                logging.info('Save best model: monitor({}): {:.6f}'.format(self._mode, monitor_value))
                self.model.save(self.model.checkpoint, overwrite=True)
        if self._stopping_steps * self._every_x_epoches >= self._patience:
            self.model.stop_training = True
            logging.info('Early stopping at epoch={:g}'.format(epoch))
        if not self._save_best_only:
            self.model.save(self.model.checkpoint, overwrite=True)
