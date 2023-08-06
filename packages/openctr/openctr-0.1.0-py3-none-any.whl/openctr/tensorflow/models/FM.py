from .base_model import BaseModel
from ..layers import input_layer, embedding_layer, FM_layer

class FM(BaseModel):
    def __init__(self, feature_encoder, model_id="FM", **kwargs):
        inputs, outputs = self._forward(feature_encoder, **kwargs)
        super(FM, self).__init__(feature_encoder, inputs=inputs, outputs=outputs, 
                                 model_id=model_id, **kwargs)
        
    def _forward(self, feature_encoder, embedding_dim=10, regularizer=None, 
                 initializer="RandomNormal(stddev=0.0001)", task="classification", 
                 seed=None, **kwargs):
        inputs = input_layer(feature_encoder)
        embed_vecs = embedding_layer(feature_encoder, inputs, embedding_dim,
                                     initializer=initializer, regularizer=regularizer,
                                     seed=seed, name_prefix="emb_")
        outputs = FM_layer(feature_encoder, inputs, embed_vecs, regularizer=regularizer, 
                           initializer=initializer, final_activation=self.get_final_activation(task), 
                           use_bias=True, seed=seed)
        return inputs, outputs
