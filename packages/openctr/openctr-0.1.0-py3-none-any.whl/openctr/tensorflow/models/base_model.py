from tensorflow.python.keras.models import Model
from ...metrics import evaluate_metrics
from datetime import datetime
import os
from ..callbacks import EvaluateMetricsCallback
from ..utils import set_optimizer, set_loss
import logging

class BaseModel(Model):
    def __init__(self, feature_encoder, inputs, outputs, model_id="BaseModel", **kwargs):
        super(BaseModel, self).__init__(inputs=inputs, outputs=outputs)
        self._validation_metrics = kwargs["metrics"]
        self.compile(set_optimizer(kwargs["optimizer"]), loss=set_loss(kwargs["loss"]))
        self.valid_gen = None
        self.model_id = model_id
        self.experiment_id = "_".join([model_id, feature_encoder.dataset_id])
        self.checkpoint = os.path.abspath(os.path.join(kwargs["model_dir"], feature_encoder.dataset_id + "/" 
                                          + self.experiment_id + "_model.ckpt"))
        self.callbacks = [EvaluateMetricsCallback(**kwargs)]

    def evaluate_generator(self, data_generator, max_queue_size=10, workers=2,
                           use_multiprocessing=False, verbose=0):
        steps = len(data_generator)
        y_true = data_generator.get_labels()
        y_pred = self.predict_generator(data_generator, steps=steps, max_queue_size=max_queue_size,
                                        workers=workers, use_multiprocessing=use_multiprocessing,
                                        verbose=verbose)
        result = evaluate_metrics(y_true, y_pred, self._validation_metrics)
        return result

    def fit_generator(self, generator, epochs=1, verbose=0, validation_data=None, workers=1, 
                      use_multiprocessing=False, max_queue_size=1000, **kwargs):
        self.valid_gen = validation_data
        steps_per_epoch = len(generator)
        super(BaseModel, self).fit_generator(generator=generator, steps_per_epoch=steps_per_epoch, 
                                             epochs=epochs, verbose=verbose, callbacks=self.callbacks, 
                                             workers=workers, use_multiprocessing=use_multiprocessing, 
                                             shuffle=False, max_queue_size=max_queue_size)
        logging.info("Training finished.")

    def get_final_activation(self, task="classification"):
        if task == "classification":
            return "sigmoid"
        elif task == "regression":
            return None
        else:
            raise NotImplementedError("task={} is not supported.".format(task))