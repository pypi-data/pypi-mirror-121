from tensorflow.python.keras.layers import Dense, Dropout, BatchNormalization, Activation
from ..utils import set_initializer, set_regularizer


def DNN_layer(input_tensor, output_dim=1, hidden_units=[], hidden_activations=None, dropout_rates=0, 
              final_activation=None, batch_norm=False, use_bias=True, initializer="glorot_normal", 
              regularizer=None, seed=None):
    initializer = set_initializer(initializer, seed=seed)
    regularizer = set_regularizer(regularizer)
    if not isinstance(dropout_rates, list):
        dropout_rates = [dropout_rates] * len(hidden_units)
    if not isinstance(hidden_activations, list):
        hidden_activations = [hidden_activations] * len(hidden_units)
    for hidden_unit, activation, dropout in zip(hidden_units, hidden_activations, dropout_rates):
        input_tensor = Dense(hidden_unit, use_bias=use_bias,
                             kernel_initializer=initializer,
                             kernel_regularizer=regularizer,
                             bias_regularizer=regularizer)(input_tensor)
        if batch_norm:
            input_tensor = BatchNormalization()(input_tensor)
        input_tensor = Activation(activation)(input_tensor)
        if dropout > 0:
            input_tensor = Dropout(rate=dropout)(input_tensor)
    # Final layer without dropout
    output_tensor = Dense(output_dim, use_bias=use_bias,
                         kernel_initializer=initializer,
                         kernel_regularizer=regularizer,
                         bias_regularizer=regularizer)(input_tensor)
    # if batch_norm:
    #     output_tensor = BatchNormalization()(output_tensor)
    if final_activation:
        output_tensor = Activation(final_activation)(output_tensor)
    return output_tensor