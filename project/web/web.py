from flask import Flask, render_template, request
from pymongo import MongoClient
from elasticsearch import Elasticsearch


app = Flask(__name__)
client = MongoClient()


@app.route("/search/", methods=["POST"])
def web_search():
    param_search = request.form["search_query"]
    results = []
    total = 0

    if param_search is not "":
        es = Elasticsearch("http://localhost:9200/mtggg/cards")

        query = {"query": {"match": {"name": param_search}}, "from": 0, "size": 10}
        hits = es.search(body=query)

        results = [hit for hit in hits["hits"]["hits"]]
        total = hits["hits"]["total"]

    return render_template(
        "search.html",
        search_query=param_search,
        search_results=results,
        num_results=total,
    )


@app.route("/similar/<card>/")
def web_similar(card):
    card = int(card)

    card_details = client.mtggg.cards.find_one({"number": card})
    card_features = client.mtggg.cards_features.find_one({"number": card})
    # ml_feats = client.mtggg.ml.feats.v3.find_one({"number": card})
    ml_similar = client.mtggg.ml.similar.find_one({"number": card})

    similar_cards = list()
    if ml_similar is not None:
        for card_id in ml_similar["similar"]:
            card = client.mtggg.cards.find_one({"number": card_id})
            similar_cards.append(card)

    return render_template(
        "similar_cards.html", card=card_details, similar_cards=similar_cards
    )


@app.route("/all/")
@app.route("/all/<page>")
def web_all(page=0):
    cards = client.mtggg.cards.find()
    cards_total = cards.count()

    page = int(page)
    limit = 10
    total_pages = int(cards_total / 10.0)
    skip = int(page * 10.0)

    cards = cards.skip(skip).limit(limit).sort("name")
    num_cards = cards.count()

    previous_page = page - 1
    if previous_page < 0:
        previous_page = -1
    next_page = page + 1
    if next_page > total_pages:
        next_page = -1
    pagination = {"previous": previous_page, "next": next_page}

    return render_template(
        "cards.html",
        cards=cards,
        num_cards=10,
        cards_total=cards_total,
        page=page,
        total_pages=total_pages,
        pagination=pagination,
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
