# -*- coding: utf-8 -*-

import sys
sys.path.append("../") 
import torch
from torch import nn
from .base_model import BaseModel
from ..layers import embedding_layer, MultiLayerDNN, interaction_layer, LR_layer


class DCN(BaseModel):
    def __init__(self, feature_encoder, model_id='DNN',
                 device='cpu', task='classification', **kwargs):
        
        super(DCN, self).__init__(feature_encoder, model_id, device, patience=kwargs['patience'],
                                 model_dir=kwargs['model_dir'])
        
        self.cross_depth = kwargs["cross_depth"]
        self.embedding_size = kwargs["embedding_size"]

        self.dnn_inp_dim = self.feature_encoder.numric_col_num \
                                      + self.feature_encoder.catgr_col_num * kwargs["embedding_size"]
                                      
        self.mlps = MultiLayerDNN(input_dim=self.dnn_inp_dim,
                                  hidden_dims=kwargs["hidden_dims"],
                                  output_dim=kwargs["output_dim"],
                                  activations=kwargs["activations"],
                                  drop_out_rates=kwargs["drop_out_rates"],
                                  layernorms=kwargs["layernorms"]
                                  )
        
        for i in range(self.cross_depth):
                setattr(self, 'cross_weight_' + str(i+1),
                        torch.nn.Parameter(torch.randn(self.dnn_inp_dim)))
                setattr(self, 'cross_bias_' + str(i + 1),
                        torch.nn.Parameter(torch.zeros(self.dnn_inp_dim)))
        
        self.aggregate_fc = nn.Linear(self.dnn_inp_dim + kwargs["output_dim"], 1) # [cross_score, dnn_score] -> final score
        
        self.embedder = embedding_layer(feature_encoder, kwargs["embedding_size"])
        self.compile(kwargs['optimizer'], loss=kwargs['loss'], metrics=kwargs['metrics'], l2_reg=kwargs['l2_reg'])
        self.init_weights()

    def cross(self, feature_emb_flatten):
        '''
        x_0 : b x  multi_emb_size
        x_0 * x_l :  b x 1
        '''
        x_0 = feature_emb_flatten
        x_l = x_0 # b x dim
        for i in range(self.cross_depth):
            weight_vec = getattr(self,'cross_weight_'+str(i+1)) # dim x 1
            bias = getattr(self,'cross_bias_'+str(i+1))
            dot_res =  torch.matmul(x_l, weight_vec.view(-1, 1))  # b x 1
            mul_res = dot_res * x_0 # 
            result = mul_res + bias + x_l
            x_l = result
        return result
    
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
        
        cross_logit = self.cross(dnn_input_merged)
        dnn_logit = self.mlps(dnn_input_merged)
        
        final_logit = torch.cat([cross_logit, dnn_logit], dim=-1)
        
        prob = self.aggregate_fc(final_logit).sigmoid()
        loss = self.loss_fn(prob, y)
        return_dict = {'loss': loss, 'prob': prob}
        return return_dict
