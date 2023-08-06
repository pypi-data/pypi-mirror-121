import tensorflow as tf
from collections import OrderedDict
from tensorflow.python.keras.layers import Layer, Input, Embedding, Dense, Concatenate, \
                                           Add, Activation, Flatten, Multiply, Dot, Dropout
from tensorflow.python.keras import backend
from ..layers import AddBias, embedding_layer, slice_layer, dot_product_layer


def LR_layer(feature_encoder, inputs, initializer="random_uniform", regularizer=None,
             final_activation=None, use_bias=True, seed=None):
    embedding_dim = 1 # A trick for quick one-hot encoding in LR
    embed_weights = embedding_layer(feature_encoder,
                                    inputs,
                                    embedding_dim,
                                    initializer=initializer,
                                    regularizer=regularizer,
                                    seed=seed,
                                    name_prefix="lr_")
    output = Add()(embed_weights)
    if use_bias:
        output = AddBias(regularizer=regularizer)(output)
    if final_activation:
        output = Activation(final_activation)(output)
    return output

def FM_layer(feature_encoder, inputs, embedding_vectors, initializer="random_uniform",
             regularizer=None, final_activation=None, use_bias=True, seed=None):
    lr_out = LR_layer(feature_encoder, inputs, initializer=initializer, regularizer=regularizer,
                      final_activation=None, use_bias=use_bias, seed=seed)
    dot_out = dot_product_layer(embedding_vectors)
    output = Add()(dot_out + [lr_out])
    if final_activation:
        output = Activation(final_activation)(output)
    return output
