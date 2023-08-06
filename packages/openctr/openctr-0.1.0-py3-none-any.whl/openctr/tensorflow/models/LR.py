from .base_model import BaseModel
from ..layers import input_layer, LR_layer

class LR(BaseModel):
    def __init__(self, feature_encoder, model_id='LR', **kwargs):
        inputs, outputs = self._forward(feature_encoder, **kwargs)
        super(LR, self).__init__(feature_encoder, inputs=inputs, outputs=outputs, 
                                 model_id=model_id, **kwargs)
        
    def _forward(self, feature_encoder, l2_reg=None, initializer="RandomNormal(stddev=0.0001)", 
                 task="classification", use_bias=True, seed=None, **kwargs):
        inputs = input_layer(feature_encoder)
        outputs = LR_layer(feature_encoder, inputs, regularizer=l2_reg, initializer=initializer,
                           final_activation=self.get_final_activation(task), use_bias=use_bias, seed=seed)
        return inputs, outputs