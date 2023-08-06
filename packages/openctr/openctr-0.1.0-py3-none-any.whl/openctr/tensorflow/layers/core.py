import tensorflow as tf
from collections import OrderedDict
from itertools import combinations
from tensorflow.python.keras.layers import Layer, Input, Embedding, Multiply, Dot, Lambda, Flatten,\
                                           Add, Subtract, Dense, Activation
from tensorflow.python.keras import backend as K
from ..layers.sequence_encoder import *
from tensorflow.python.keras import initializers
from ..utils import set_initializer, set_regularizer

def slice_layer(X, index, axis=1):
    return Lambda(lambda x: tf.gather(x, index, axis=axis))(X)

def input_layer(feature_encoder):
    input_shape = sum(feature_spec["max_len"] if feature_spec["type"] == "sequence" else 1 
                      for feature, feature_spec in feature_encoder.feature_specs.items())
    inputs = Input(shape=(input_shape,))
    return inputs

def embedding_layer(feature_encoder, inputs, embedding_dim, initializer="random_uniform", 
                    regularizer=None, name_prefix="emb_", seed=None, 
                    feature_types=["numeric", "categorical", "sequence"]):
    # By default, use 'RandomNormal' to initialize embeddings to avoid nan loss
    embedding_columns = OrderedDict()
    embedding_vectors = []
    initializer = set_initializer(initializer, seed=seed)
    regularizer = set_regularizer(regularizer)
    for feature, feature_spec in feature_encoder.feature_specs.items():
        if feature_spec["type"] == "numeric" and "numeric" in feature_types:
            inp = slice_layer(inputs, [feature_spec["index"]])
            embedding_vec = Dense(embedding_dim, activation=None, use_bias=False,
                                  kernel_initializer=initializer,
                                  kernel_regularizer=regularizer,
                                  name=name_prefix + feature)(inp)
            embedding_vectors.append(embedding_vec)
        elif feature_spec["type"] == "categorical" and "categorical" in feature_types:
            embedding_columns[feature] = \
                Embedding(input_dim=feature_spec["vocab_size"],
                          output_dim=embedding_dim,
                          embeddings_initializer=initializer,
                          embeddings_regularizer=regularizer,
                          input_length=1,
                          name=name_prefix + feature)
            inp = slice_layer(inputs, feature_spec["index"])
            embedding_vectors.append(Flatten()(embedding_columns[feature](inp)))
        elif feature_spec["type"] == "sequence" and "sequence" in feature_types:
            embedding_columns[feature] = \
                Embedding(input_dim=feature_spec["vocab_size"],
                          output_dim=embedding_dim,
                          embeddings_initializer=initializer,
                          embeddings_regularizer=regularizer,
                          input_length=feature_spec["max_len"],
                          mask_zero=True,
                          name=name_prefix + feature)
            inp = slice_layer(inputs, feature_spec["index"])
            seq_embed_matrix = embedding_columns[feature](inp)
            if "encoder" in feature_spec:
                try:
                    seq_encoder_layer = eval(feature_spec["encoder"])
                except:
                    raise RuntimeError('Squence encoder={} is not supported.'.format(feature_spec["encoder"]))
            else:
                seq_encoder_layer = MaskedAveragePooling()
            seq_embed_vec = seq_encoder_layer(seq_embed_matrix)
            embedding_vectors.append(seq_embed_vec)
    return embedding_vectors

def elementwise_multiply_layer(embedding_vectors):
    interact_vecs = []
    for emb1, emb2 in combinations(embedding_vectors, 2):
        element_multiply_vec = Multiply()([emb1, emb2])
        interact_vecs.append(element_multiply_vec)
    return interact_vecs

def dot_product_layer(embedding_vectors):
    dot_values = []
    for emb1, emb2 in combinations(embedding_vectors, 2):
        dot_product = Dot(axes=1)([emb1, emb2])
        dot_values.append(dot_product)
    return dot_values

def fast_dot_product_layer(embedding_vectors):
    sum_vec = Add()(embedding_vectors)
    diff_vecs = [Subtract()([sum_vec, v]) for v in embedding_vectors]
    dot_values = [Dot(axes=1)([d, v]) for d, v in zip(diff_vecs, embedding_vectors)]
    return dot_values

class AddBias(Layer):
    def __init__(self, regularizer=None, **kwargs):
        super(AddBias, self).__init__(**kwargs)
        self.regularizer = set_regularizer(regularizer)
        self.initializer = initializers.get("zero")

    def build(self, input_shape):
        self.bias = self.add_weight("bias", shape=(1,), initializer=self.initializer,
                                    regularizer=self.regularizer, trainable=True)
        super(AddBias, self).build(input_shape)

    def call(self, input):
        return self.bias + input

    def compute_output_shape(self, input_shape):
        return input_shape

    def get_config(self):
        return super(AddBias, self).get_config()


