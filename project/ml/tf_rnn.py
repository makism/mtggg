from tf_rnn_common import *


def tf_rnn_predict(model_weights, corpus_file):
    """ """

    #
    vocab, sequences, text_arr, char_to_ind, ind_to_char = prepare_corpus(corpus_file)

    #
    dataset = sequences.map(create_seq_targets)
    dataset = dataset.shuffle(buffer_size).batch(batch_size, drop_remainder=True)

    # Length of the vocabulary in chars
    vocab_size = len(vocab)

    #
    model = create_model(vocab_size, embed_dim, rnn_neurons, batch_size=1)
    model.load_weights(model_weights)
    model.build(tf.TensorShape([1, None]))
    model.summary()

    #
    random_card = np.random.choice(text_arr)

    #
    result_text = generate_text(
        model, random_card, char_to_ind, ind_to_char, temp=1.0, gen_size=500
    )

    lst = [f"{line}" for line in result_text.split("\n")]
    lst = lst[:-1]

    return lst
