import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding, Dropout, GRU
from tensorflow.keras.losses import sparse_categorical_crossentropy
from tensorflow.keras.callbacks import EarlyStopping

# Batch size
batch_size = 128

# Buffer size to shuffle the dataset so it doesn't attempt to shuffle
# the entire sequence in memory. Instead, it maintains a buffer in which it shuffles elements
buffer_size = 10000

# The embedding dimension
embed_dim = 128

# Number of RNN units
rnn_neurons = 1024


def load_corpus(filename):
    path_to_file = filename
    text = open(path_to_file, "r").read()

    return text


def prepare_corpus(corpus_fname, seq_len=20):
    text = load_corpus(corpus_fname)

    text_arr = text.split("\n")

    vocab = sorted(set(text))

    char_to_ind = {u: i for i, u in enumerate(vocab)}

    ind_to_char = np.array(vocab)

    encoded_text = np.array([char_to_ind[c] for c in text])

    total_num_seq = len(text) // (seq_len + 1)

    # Create Training Sequences
    char_dataset = tf.data.Dataset.from_tensor_slices(encoded_text)

    sequences = char_dataset.batch(seq_len + 1, drop_remainder=True)

    return vocab, sequences, text_arr, char_to_ind, ind_to_char


def create_seq_targets(seq):
    input_txt = seq[:-1]
    target_txt = seq[1:]

    return input_txt, target_txt


def sparse_cat_loss(y_true, y_pred):
    return sparse_categorical_crossentropy(y_true, y_pred, from_logits=True)


def create_model(vocab_size, embed_dim, rnn_neurons, batch_size):
    model = Sequential()
    model.add(Embedding(vocab_size, embed_dim, batch_input_shape=[batch_size, None]))
    model.add(
        GRU(
            rnn_neurons,
            return_sequences=True,
            stateful=True,
            recurrent_initializer="glorot_uniform",
            reset_after=True,
        )
    )
    model.add(Dense(vocab_size))
    model.compile(optimizer="adam", loss=sparse_cat_loss)

    # inputs = Input(batch_shape=[batch_size])
    # x = Embedding(vocab_size, embed_dim)(inputs)
    # x = GRU(rnn_neurons, return_sequences=True, stateful=True, recurrent_initializer='glorot_uniform')(x)
    # outputs = Dense(vocab_size)(x)
    # model = Model(inputs, outputs)
    # model.compile(loss='sparse_categorical_crossentropy', optimizer=Adam())

    return model


def generate_text(model, start_seed, char_to_ind, ind_to_char, gen_size=100, temp=1.0):
    # Number of characters to generate
    num_generate = gen_size

    # Vecotrizing starting seed text
    input_eval = [char_to_ind[s] for s in start_seed]

    # Expand to match batch format shape
    input_eval = tf.expand_dims(input_eval, 0)

    # Empty list to hold resulting generated text
    text_generated = []

    temperature = temp

    # Here batch size == 1
    model.reset_states()

    for i in range(num_generate):

        # Generate Predictions
        predictions = model(input_eval)

        # Remove the batch shape dimension
        predictions = tf.squeeze(predictions, 0)

        # Use a cateogircal disitribution to select the next character
        predictions = predictions / temperature
        predicted_id = tf.random.categorical(predictions, num_samples=1)[-1, 0].numpy()

        # Pass the predicted charracter for the next input
        input_eval = tf.expand_dims([predicted_id], 0)

        # Transform back to character letter
        text_generated.append(ind_to_char[predicted_id])

    return start_seed + "".join(text_generated)
