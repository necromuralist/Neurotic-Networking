# from pypi
from trax import layers
from trax.fastmath import numpy as fastmath_numpy

import trax

def input_encoder(input_vocab_size: int, d_model: int,
                     n_encoder_layers: int) -> layers.Serial:
    """ Input encoder runs on the input sentence and creates
    activations that will be the keys and values for attention.
    
    Args:
        input_vocab_size: vocab size of the input
        d_model:  depth of embedding (n_units in the LSTM cell)
        n_encoder_layers: number of LSTM layers in the encoder

    Returns:
        tl.Serial: The input encoder
    """
    input_encoder = layers.Serial( 
        layers.Embedding(input_vocab_size, d_model),
        [layers.LSTM(d_model) for _ in range(n_encoder_layers)]
    )
    return input_encoder

def pre_attention_decoder(mode: str, target_vocab_size: int, d_model: int) -> layers.Serial:
    """ Pre-attention decoder runs on the targets and creates
    activations that are used as queries in attention.
    
    Args:
        mode: 'train' or 'eval'
        target_vocab_size: vocab size of the target
        d_model:  depth of embedding (n_units in the LSTM cell)
    Returns:
        tl.Serial: The pre-attention decoder
    """
    return layers.Serial(
        layers.ShiftRight(mode=mode),
        layers.Embedding(target_vocab_size, d_model),
        layers.LSTM(d_model)
    )

def prepare_attention_input(encoder_activations: fastmath_numpy.array,
                            decoder_activations: fastmath_numpy.array,
                            inputs: fastmath_numpy.array) -> tuple:
    """Prepare queries, keys, values and mask for attention.
    
    Args:
        encoder_activations fastnp.array(batch_size, padded_input_length, d_model): output from the input encoder
        decoder_activations fastnp.array(batch_size, padded_input_length, d_model): output from the pre-attention decoder
        inputs fastnp.array(batch_size, padded_input_length): padded input tokens
    
    Returns:
        queries, keys, values and mask for attention.
    """
    keys = encoder_activations
    values = encoder_activations
    queries = decoder_activations    
    mask = inputs != 0

    mask = fastmath_numpy.reshape(mask, (mask.shape[0], 1, 1, mask.shape[1]))
    mask += fastmath_numpy.zeros((1, 1, decoder_activations.shape[1], 1))
    return queries, keys, values, mask
