from torch import nn
from .base_model import BaseModel
from ..layers import FM_Layer, EmbeddingLayer


class FM(BaseModel):
    def __init__(self, feature_encoder, model_id='FM', gpu=-1, task='classification', 
                 learning_rate=1e-3, embedding_initializer="torch.nn.init.normal_(std=1e-4)", 
                 embedding_dim=10, regularizer=None, **kwargs):
        super(FM, self).__init__(feature_encoder, model_id=model_id, gpu=gpu, 
                                 embedding_regularizer=regularizer, kernel_regularizer=regularizer,
                                 **kwargs)
        self.embedding_layer = EmbeddingLayer(feature_encoder, embedding_dim)
        self.fm_layer = FM_Layer(feature_encoder, final_activation=self.get_final_activation(task), 
                                 use_bias=True)
        self.compile(kwargs['optimizer'], loss=kwargs['loss'], lr=learning_rate)
        self.init_weights(embedding_initializer=embedding_initializer)
            
    def forward(self, inputs):
        """
        Inputs: [X, y]
        """
        X, y = self.inputs_to_device(inputs)
        embedding_vectors = self.embedding_layer(X)
        y_pred = self.fm_layer(X, embedding_vectors)
        loss = self.loss_with_reg(y_pred, y)
        return_dict = {'loss': loss, 'y_pred': y_pred}
        return return_dict

