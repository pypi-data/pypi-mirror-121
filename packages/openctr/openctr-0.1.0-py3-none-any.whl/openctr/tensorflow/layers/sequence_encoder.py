import tensorflow as tf
from tensorflow.python.keras.layers import Layer
from tensorflow.python.keras import backend as K

class MaskedAveragePooling(Layer):
    def __init__(self, supports_masking=True, **kwargs):
        self.supports_masking = supports_masking
        super(MaskedAveragePooling, self).__init__(**kwargs)

    def compute_mask(self, inputs, mask=None):
        return None

    def call(self, x, mask=None):
        if mask is not None:
            # mask (batch, maxlen)
            mask = K.cast(mask, K.floatx())
            # mask (batch, embedding_size, maxlen)
            mask = K.repeat(mask, x.shape[-1])
            # mask (batch, maxlen, embedding_size)
            mask = tf.transpose(mask, [0, 2, 1])
            x = x * mask
            return K.sum(x, axis=1) / (K.sum(mask, axis=1) + 1e-16)
        else:
            return K.mean(x, axis=1)

    def compute_output_shape(self, input_shape):
        return (input_shape[0], input_shape[2])

class MaskedSumPooling(MaskedAveragePooling):
    def call(self, x, mask=None):
        if mask is not None:
            # mask (batch, maxlen)
            mask = K.cast(mask, K.floatx())
            # mask (batch, embedding_size, maxlen)
            mask = K.repeat(mask, x.shape[-1])
            # mask (batch, maxlen, embedding_size)
            mask = tf.transpose(mask, [0, 2, 1])
            x = x * mask
        return K.sum(x, axis=1)