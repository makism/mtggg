import json
import numpy as np
import sklearn
from sklearn import preprocessing


class Dataset(object):
    def __init__(self):
        self.colorIdentities = list()


if __name__ == "__main__":
    rng = np.random.RandomState(1)

    json_file = "/home/makism/Dropbox/mtgp/dataset/AllCards.json"
    with open(json_file, "r") as fp:
        data = json.load(fp)

    n = len(data)
    s = np.int32(0.01 * n)

    random_keys = rng.choice(list(data.keys()), size=s)

    # subset_data = {key: data[key] for key in random_keys}
    subset_data = [data[key] for key in random_keys]

    ds = Dataset()

    all_ColorIdentities = list(map(lambda card: card["colorIdentity"], subset_data))
    unique_colorIdentities, counts = np.unique(all_ColorIdentities, return_counts=True)

    tmp = list(map(lambda x: "".join(x), unique_colorIdentities))
    print(tmp)

    all_Colors = map(lambda card: card["colors"], subset_data)
    all_CMC = map(lambda card: card["convertedManaCost"], subset_data)
    all_Power = map(lambda card: card["power"], subset_data)
    all_Thoughness = map(lambda card: card["thoughmess"], subset_data)
    all_Types = map(lambda card: card["types"], subset_data)
    all_SubTypes = map(lambda card: card["subtypes"], subset_data)
    all_SuperTypes = map(lambda card: card["supertypes"], subset_data)

    print(list(all_SubTypes))

    x = subset_data[0]
    # print(x.keys())
    # dict_keys(['colorIdentity', 'colors', 'convertedManaCost', 'edhrecRank', 'foreignData', 'layout', 'legalities', 'manaCost', 'mtgstocksId', 'name',
    #            'power', 'printings', 'purchaseUrls', 'rulings', 'scryfallOracleId', 'subtypes', 'supertypes', 'text', 'toughness', 'type', 'types', 'uuid'])

    # for key in x.keys():
    # print("{0} -> {1}".format(key, x[key]))

    # le = sklearn.preprocessing.LabelEncoder().fit(tmp)
    # le.classes_

    x["text"]

    y = subset_data[1]
    y["text"]

    documents = [x["text"], y["text"]]

    import gensim
    from gensim import corpora
    from pprint import pprint

    # Tokenize(split) the sentences into words
    texts = [[text for text in doc.split()] for doc in documents]

    data = [card["text"] for card in subset_data if "text" in card]

    # Import all the dependencies
    from gensim.models.doc2vec import Doc2Vec, TaggedDocument
    from nltk.tokenize import word_tokenize

    tagged_data = [
        TaggedDocument(words=word_tokenize(_d.lower()), tags=[str(i)])
        for i, _d in enumerate(data)
    ]

    tagged_data

    max_epochs = 100
    vec_size = 20
    alpha = 0.025

    model = Doc2Vec(size=vec_size, alpha=alpha, min_alpha=0.00025, min_count=1, dm=1)

    model.build_vocab(tagged_data)

    for epoch in range(max_epochs):
        print("iteration {0}".format(epoch))
        model.train(tagged_data, total_examples=model.corpus_count, epochs=model.iter)
        # decrease the learning rate
        model.alpha -= 0.0002
        # fix the learning rate, no decay
        model.min_alpha = model.alpha

    model.save("d2v.model")

    len(model.docvecs)

    model.docvecs[0]

    from gensim.models.doc2vec import Doc2Vec

    model = Doc2Vec.load("d2v.model")
    # to find the vector of a document which is not in training data
    test_data = word_tokenize("target noncreature".lower())
    v1 = model.infer_vector(test_data)
    print("V1_infer", v1)

    # model.docvecs.similarity("target noncreature", "0")

    # to find most similar doc using tags
    # similar_doc = model.docvecs.most_similar("1")
    # print(similar_doc)

    # model.docvecs["1"]
