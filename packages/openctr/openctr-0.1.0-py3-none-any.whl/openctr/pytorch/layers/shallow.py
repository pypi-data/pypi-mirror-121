import torch
from torch import nn
from .core import EmbeddingLayer, InnerProductLayer

class LR_Layer(nn.Module):
    def __init__(self, feature_encoder, final_activation=None, use_bias=True):
        super(LR_Layer, self).__init__()
        self.bias = nn.Parameter(torch.zeros(1)) if use_bias else None
        self.final_activation = getattr(nn, final_activation)() if final_activation else None
        # A trick for quick one-hot encoding in LR
        self.embedding_layer = EmbeddingLayer(feature_encoder, 1)
            
    def forward(self, X):
        embed_weights = self.embedding_layer(X)
        output = torch.stack(embed_weights).sum(dim=0)
        if self.bias is not None:
            output += self.bias
        if self.final_activation is not None:
            output = self.final_activation(output)
        return output

class FM_Layer(nn.Module):
    def __init__(self, feature_encoder, final_activation=None, use_bias=True):
        super(FM_Layer, self).__init__()    
        self.inner_product_layer = InnerProductLayer()
        self.lr_layer = LR_Layer(feature_encoder, final_activation=None, use_bias=use_bias)
        self.final_activation = getattr(nn, final_activation)() if final_activation else None

    def forward(self, X, embedding_vectors):
        lr_out = self.lr_layer(X)
        dot_out = self.inner_product_layer(embedding_vectors)
        output = lr_out + dot_out
        if self.final_activation is not None:
            output = self.final_activation(output)
        return output
        