from tf_rnn_common import *

#
vocab, sequences, text_arr, char_to_ind, ind_to_char = prepare_corpus("card_names.txt")

#
dataset = sequences.map(create_seq_targets)
dataset = dataset.shuffle(buffer_size).batch(batch_size, drop_remainder=True)

# Length of the vocabulary in chars
vocab_size = len(vocab)

#
model = create_model(vocab_size, embed_dim, rnn_neurons, batch_size=1)

model.summary()

earlyStop = EarlyStopping(monitor="val_loss", verbose=2, mode="min", patience=3)

#
model.fit(dataset, validation_data=dataset, epochs=50, callbacks=[earlyStop], verbose=1)

#
model.save("rnn_all_sets.h5")
