# -*- coding: utf-8 -*-

import sys
sys.path.append("../") 
import torch
from torch import nn
from .base_model import BaseModel
from ..layers import embedding_layer, MultiLayerDNN, LR_layer


class xDeepFM(BaseModel):
    def __init__(self, feature_encoder, model_id='DNN',
                 device='cpu', task='classification', **kwargs):
        
        super(xDeepFM, self).__init__(feature_encoder, model_id, device, patience=kwargs['patience'],
                                 model_dir=kwargs['model_dir'])
        
        self.embedding_size = kwargs["embedding_size"]
        self.cin_layer_dims = kwargs["cin_layer_dims"]

        self.mlps = MultiLayerDNN(input_dim=self.feature_encoder.numric_col_num \
                                      + self.feature_encoder.catgr_col_num * kwargs["embedding_size"],
                                  hidden_dims=kwargs["hidden_dims"],
                                  output_dim=kwargs["output_dim"],
                                  activations=kwargs["activations"],
                                  drop_out_rates=kwargs["drop_out_rates"],
                                  layernorms=kwargs["layernorms"]
                                  )
        
        self._LR_layer = LR_layer(self.feature_encoder, activation=None, use_bias=True)
                
        # out, how many filters
        # kernel_size, how long the convention kernel
        for i, l_size in enumerate(self.cin_layer_dims):
            in_channels = self.feature_encoder.catgr_col_num ** 2 if i == 0 \
                                else self.feature_encoder.catgr_col_num * self.cin_layer_dims[i-1]
            out_channels = l_size
            setattr(self, 'conv1d_' + str(i+1),\
                    nn.Conv1d(in_channels,
                              out_channels,
                              kernel_size=1))
#            
        self.exfm_fc = nn.Linear(sum(self.cin_layer_dims), 1)
        
        self.embedder = embedding_layer(feature_encoder, kwargs["embedding_size"])
        self.compile(kwargs['optimizer'], loss=kwargs['loss'], metrics=kwargs['metrics'], l2_reg=kwargs['l2_reg'])
        self.init_weights()

    def cin(self, feature_emb):
        final_result = []
        X0 = feature_emb   # b x field_size x emb_size
        Xk = X0
        for i in range(len(self.cin_layer_dims)):
            cross_vec = X0[:, None, ...] * Xk[..., None, :] # Hadamard product
            cross_vec = cross_vec.view(self.batch_size, -1, self.embedding_size)
            cross_vec = getattr(self,'conv1d_'+ str(i+1))(cross_vec) \
                                    .view(self.batch_size,-1, self.embedding_size)
            cross_vec = cross_vec.relu()  ## Add non-linear part
            Xk = cross_vec
            final_result.append(cross_vec.sum(dim=-1))
        final_result = torch.cat(final_result, dim=-1)
        return final_result
    
    
    def forward(self, inputs):
        """
        Inputs: [X,y]
        """
        x, y = inputs
        x = x.to(self.device)
        y = y.float().to(self.device).view(-1, 1)
        self.batch_size = y.size(0)
        
        embedding_dict = self.embedder(x, merge_ui=True)
        
        dnn_input_merged = None
        embedding_vectors = None
        
        # categorical features
        if "categorical" in embedding_dict:
            embedding_vectors = embedding_dict["categorical"]
            embedding_vectors_flatten = embedding_vectors.view(self.batch_size, -1)
            dnn_input_merged = embedding_vectors_flatten

        # numerical features
        if "numeric" in embedding_dict:
            numeric_vectors = embedding_dict["numeric"]
            dnn_input_merged = torch.cat([dnn_input_merged, numeric_vectors], dim=1)
        
        cin_logit = self.exfm_fc(self.cin(embedding_vectors))
        dnn_logit = self.mlps(dnn_input_merged)
        
        final_logit = cin_logit + dnn_logit
        
        prob = final_logit.sigmoid()
        loss = self.loss_fn(prob, y)
        return_dict = {'loss': loss, 'prob': prob}
        return return_dict
