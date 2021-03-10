# pypi
from trax import layers

# this project
from .help_me import input_encoder as input_encoder_fn
from .help_me import pre_attention_decoder as pre_attention_decoder_fn
from .help_me import prepare_attention_input as prepare_attention_input_fn

def NMTAttn(input_vocab_size: int=33300,
            target_vocab_size: int=33300,
            d_model: int=1024,
            n_encoder_layers: int=2,
            n_decoder_layers: int=2,
            n_attention_heads: int=4,
            attention_dropout: float=0.0,
            mode: str='train') -> layers.Serial:
    """Returns an LSTM sequence-to-sequence model with attention.

    The input to the model is a pair (input tokens, target tokens), e.g.,
    an English sentence (tokenized) and its translation into German (tokenized).

    Args:
    input_vocab_size: int: vocab size of the input
    target_vocab_size: int: vocab size of the target
    d_model: int:  depth of embedding (n_units in the LSTM cell)
    n_encoder_layers: int: number of LSTM layers in the encoder
    n_decoder_layers: int: number of LSTM layers in the decoder after attention
    n_attention_heads: int: number of attention heads
    attention_dropout: float, dropout for the attention layer
    mode: str: 'train', 'eval' or 'predict', predict mode is for fast inference

    Returns:
    A LSTM sequence-to-sequence model with attention.
    """
    # Step 0: call the helper function to create layers for the input encoder
    input_encoder = input_encoder_fn(input_vocab_size, d_model, n_encoder_layers)

    # Step 0: call the helper function to create layers for the pre-attention decoder
    pre_attention_decoder = pre_attention_decoder_fn(mode, target_vocab_size, d_model)

    # Step 1: create a serial network
    model = layers.Serial( 
        
      # Step 2: copy input tokens and target tokens as they will be needed later.
      layers.Select([0, 1, 0, 1]),
        
      # Step 3: run input encoder on the input and pre-attention decoder on the target.
      layers.Parallel(input_encoder, pre_attention_decoder),
        
      # Step 4: prepare queries, keys, values and mask for attention.
      layers.Fn('PrepareAttentionInput', prepare_attention_input_fn, n_out=4),
        
      # Step 5: run the AttentionQKV layer
      # nest it inside a Residual layer to add to the pre-attention decoder activations(i.e. queries)
      layers.Residual(layers.AttentionQKV(d_model,
                                          n_heads=n_attention_heads,
                                          dropout=attention_dropout, mode=mode)),
      
      # Step 6: drop attention mask (i.e. index = None
      layers.Select([0, 2]),
        
      # Step 7: run the rest of the RNN decoder
      [layers.LSTM(d_model) for _ in range(n_decoder_layers)],
        
      # Step 8: prepare output by making it the right size
      layers.Dense(target_vocab_size),
        
      # Step 9: Log-softmax for output
      layers.LogSoftmax()
    )
    return model
