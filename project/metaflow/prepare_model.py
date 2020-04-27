import gensim
from gensim import corpora
from pprint import pprint
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
import json
import numpy as np
import sklearn
import umap
from pymongo import MongoClient
from pyspark.context import SparkContext
from pyspark.sql import SparkSession
from metaflow import FlowSpec, step


class PrepModel(FlowSpec):
    @step
    def start(self):
        """ Begin here. """
        self.next(self.load_data)

    @step
    def load_data(self):
        """ Read data. """
        spark = SparkSession.builder.appName("mtggg").getOrCreate()

        df = spark.read.parquet("../dataset/M20_cards.parquet")
        as_dict = df.rdd.map(lambda row: row.asDict())
        self.cards = as_dict.collect()

        self.next(self.tokenize)

    @step
    def tokenize(self):
        """ Tokenize cards' texts. """
        field_text = "filteredText"

        data_list = [
            {"number": card["number"], "text": card[field_text]}
            for card in self.cards
            if field_text in card
            if card[field_text] is not None
        ]
        data = list(map(lambda card: card["text"], data_list))

        self.tagged_data = [
            TaggedDocument(words=word_tokenize(_d.lower()), tags=[str(i)])
            for i, _d in enumerate(data)
            if _d is not None
        ]

        self.next(self.train_model)

    @step
    def train_model(self):
        """ Train a text model. """
        max_epochs = 100
        vec_size = 50
        alpha = 0.025

        model = Doc2Vec(
            vector_size=vec_size, alpha=alpha, min_alpha=0.00025, min_count=1, dm=1
        )
        model.build_vocab(self.tagged_data)

        for epoch in range(max_epochs):
            model.train(
                self.tagged_data, total_examples=model.corpus_count, epochs=model.epochs
            )
            # decrease the learning rate
            model.alpha -= 0.0002
            # fix the learning rate, no decay
            model.min_alpha = model.alpha

        X = list()
        for i in range(len(model.docvecs)):
            X.append(model.docvecs[i])

        self.docvecs = np.array(X)

        self.next(self.project)

    @step
    def project(self):
        """ Perform dimensionality reduction on the feature vectors. """
        rng = np.random.RandomState(0)
        pca = sklearn.decomposition.PCA(random_state=rng)
        X = pca.fit_transform(self.docvecs)

        self.next(self.embed)

    @step
    def embed(self):
        """ Embed feature vectors using UMAP. """
        rng = np.random.RandomState(0)
        self.embedded_docvecs = umap.UMAP(
            n_neighbors=5, metric="cosine", random_state=rng, transform_seed=rng
        ).fit_transform(self.docvecs)

        self.next(self.end)

    #     @step
    #     def save_feature_vectors(self):
    #         """ Save feature vectors to MongoDB. """
    #         client = MongoClient("localhost")
    #         db = client['mtgp']

    #         self.feats = [{'number': card['number'], 'docvect': feature_vector.tolist(), 'embedded_vect': embedded_vector.tolist()}
    #                      for card, feature_vector, embedded_vector in zip(self.cards, self.docvecs, self.embedded_docvecs)
    #         ]

    #         result = db.mlfeats.insert_many(self.feats)

    #         self.next(self.end)

    @step
    def end(self):
        """ Finalize and clean up. """
        print("All done")


if __name__ == "__main__":
    PrepModel()
