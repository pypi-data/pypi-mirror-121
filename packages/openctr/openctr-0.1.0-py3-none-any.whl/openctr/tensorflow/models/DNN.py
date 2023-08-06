from .base_model import BaseModel
from ..layers import input_layer, embedding_layer, DNN_layer
from tensorflow.python.keras.layers import Activation, Concatenate

class DNN(BaseModel):
    def __init__(self, feature_encoder, model_id="DNN", **kwargs):
        inputs, outputs = self._forward(feature_encoder, **kwargs)
        super(DNN, self).__init__(feature_encoder, inputs=inputs, outputs=outputs, 
                                  model_id=model_id, **kwargs)
        
    def _forward(self, feature_encoder, embedding_dim=10, task="classification", embedding_regularizer=None, 
                 kernel_regularizer=None, embedding_initializer="RandomNormal(stddev=0.0001)", 
                 kernel_initializer="glorot_normal", hidden_units=[64, 64, 64], hidden_activations="relu", 
                 dropout_rates=0, batch_norm=False, seed=None, **kwargs):
        inputs = input_layer(feature_encoder)
        embed_vecs = embedding_layer(feature_encoder, inputs, embedding_dim,
                                     initializer=embedding_initializer, regularizer=embedding_regularizer,
                                     seed=seed, name_prefix="embed_")
        embed_tensor = Concatenate()(embed_vecs)
        output = DNN_layer(embed_tensor, output_dim=1, hidden_units=hidden_units, hidden_activations=hidden_activations,
                           dropout_rates=dropout_rates, final_activation=self.get_final_activation(task), 
                           batch_norm=batch_norm, initializer=kernel_initializer, regularizer=kernel_regularizer, seed=seed)
        return inputs, output