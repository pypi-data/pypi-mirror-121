import torch
from torch import nn
from .base_model import BaseModel
from ..layers import EmbeddingLayer, DNN_Layer, LR_Layer

class WideDeep(BaseModel):
    def __init__(self, feature_encoder, model_id='WideDeep', gpu=-1, task='classification', 
                 learning_rate=1e-3, embedding_initializer="torch.nn.init.normal_(std=1e-4)", 
                 embedding_dim=10, hidden_units=[64, 64, 64], hidden_activations='ReLU', 
                 dropout_rates=0, batch_norm=False, **kwargs):
        super(WideDeep, self).__init__(feature_encoder, model_id=model_id, gpu=gpu, **kwargs)
        self.embedding_layer = EmbeddingLayer(feature_encoder, embedding_dim)
        self.lr_layer = LR_Layer(feature_encoder, final_activation=None, use_bias=False)
        self.dnn = DNN_Layer(input_dim=embedding_dim * feature_encoder.num_fields,
                             output_dim=1, hidden_units=hidden_units,
                             hidden_activations=hidden_activations,
                             final_activation=None, dropout_rates=dropout_rates, 
                             batch_norm=batch_norm, use_bias=True)
        final_activation = self.get_final_activation(task)
        self.final_activation = getattr(nn, final_activation)() if final_activation else None
        self.compile(kwargs['optimizer'], loss=kwargs['loss'], lr=learning_rate)
        self.init_weights(embedding_initializer=embedding_initializer)
            
    def forward(self, inputs):
        """
        Inputs: [X,y]
        """
        X, y = self.inputs_to_device(inputs)
        embedding_vectors = self.embedding_layer(X)
        y_pred = self.lr_layer(X, embedding_vectors)
        embedding_tensor = torch.cat(embedding_vectors, dim=1)
        y_pred += self.dnn(embedding_tensor)
        if self.final_activation is not None:
            y_pred = self.final_activation(y_pred)
        loss = self.loss_with_reg(y_pred, y)
        return_dict = {'loss': loss, 'y_pred': y_pred}
        return return_dict
