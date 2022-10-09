from pyspark.sql import types as T


SCHEMA_STAGE = T.StructType(
    [
        T.StructField("artist", T.StringType(), True),
        T.StructField("availability", T.ArrayType(T.StringType(), True), True),
        T.StructField("boosterTypes", T.ArrayType(T.StringType(), True), True),
        T.StructField("borderColor", T.StringType(), True),
        T.StructField("colorIdentity", T.ArrayType(T.StringType(), True), True),
        T.StructField("colors", T.ArrayType(T.StringType(), True), True),
        T.StructField("convertedManaCost", T.DoubleType(), True),
        T.StructField("edhrecRank", T.LongType(), True),
        T.StructField("finishes", T.ArrayType(T.StringType(), True), True),
        T.StructField("flavorText", T.StringType(), True),
        T.StructField(
            "foreignData",
            T.ArrayType(
                T.StructType(
                    [
                        T.StructField("flavorText", T.StringType(), True),
                        T.StructField("language", T.StringType(), True),
                        T.StructField("multiverseId", T.LongType(), True),
                        T.StructField("name", T.StringType(), True),
                        T.StructField("text", T.StringType(), True),
                        T.StructField("type", T.StringType(), True),
                    ]
                ),
                True,
            ),
            True,
        ),
        T.StructField("frameEffects", T.ArrayType(T.StringType(), True), True),
        T.StructField("frameVersion", T.StringType(), True),
        T.StructField("hasFoil", T.BooleanType(), True),
        T.StructField("hasNonFoil", T.BooleanType(), True),
        T.StructField(
            "identifiers",
            T.StructType(
                [
                    T.StructField("cardKingdomFoilId", T.StringType(), True),
                    T.StructField("cardKingdomId", T.StringType(), True),
                    T.StructField("cardsphereId", T.StringType(), True),
                    T.StructField("mcmId", T.StringType(), True),
                    T.StructField("mcmMetaId", T.StringType(), True),
                    T.StructField("mtgArenaId", T.StringType(), True),
                    T.StructField("mtgjsonV4Id", T.StringType(), True),
                    T.StructField("mtgoId", T.StringType(), True),
                    T.StructField("multiverseId", T.StringType(), True),
                    T.StructField("scryfallId", T.StringType(), True),
                    T.StructField("scryfallIllustrationId", T.StringType(), True),
                    T.StructField("scryfallOracleId", T.StringType(), True),
                    T.StructField("tcgplayerProductId", T.StringType(), True),
                ]
            ),
            True,
        ),
        T.StructField("isAlternative", T.BooleanType(), True),
        T.StructField("isOnlineOnly", T.BooleanType(), True),
        T.StructField("isPromo", T.BooleanType(), True),
        T.StructField("isRebalanced", T.BooleanType(), True),
        T.StructField("isReprint", T.BooleanType(), True),
        T.StructField("isStarter", T.BooleanType(), True),
        T.StructField("isStorySpotlight", T.BooleanType(), True),
        T.StructField("keywords", T.ArrayType(T.StringType(), True), True),
        T.StructField("language", T.StringType(), True),
        T.StructField("layout", T.StringType(), True),
        T.StructField(
            "leadershipSkills",
            T.StructType(
                [
                    T.StructField("brawl", T.BooleanType(), True),
                    T.StructField("commander", T.BooleanType(), True),
                    T.StructField("oathbreaker", T.BooleanType(), True),
                ]
            ),
            True,
        ),
        T.StructField(
            "legalities",
            T.StructType(
                [
                    T.StructField("alchemy", T.StringType(), True),
                    T.StructField("brawl", T.StringType(), True),
                    T.StructField("commander", T.StringType(), True),
                    T.StructField("duel", T.StringType(), True),
                    T.StructField("explorer", T.StringType(), True),
                    T.StructField("future", T.StringType(), True),
                    T.StructField("gladiator", T.StringType(), True),
                    T.StructField("historic", T.StringType(), True),
                    T.StructField("historicbrawl", T.StringType(), True),
                    T.StructField("legacy", T.StringType(), True),
                    T.StructField("modern", T.StringType(), True),
                    T.StructField("pauper", T.StringType(), True),
                    T.StructField("paupercommander", T.StringType(), True),
                    T.StructField("penny", T.StringType(), True),
                    T.StructField("pioneer", T.StringType(), True),
                    T.StructField("premodern", T.StringType(), True),
                    T.StructField("standard", T.StringType(), True),
                    T.StructField("vintage", T.StringType(), True),
                ]
            ),
            True,
        ),
        T.StructField("loyalty", T.StringType(), True),
        T.StructField("manaCost", T.StringType(), True),
        T.StructField("manaValue", T.DoubleType(), True),
        T.StructField("name", T.StringType(), True),
        T.StructField("number", T.StringType(), True),
        T.StructField("originalPrintings", T.ArrayType(T.StringType(), True), True),
        T.StructField("originalText", T.StringType(), True),
        T.StructField("originalType", T.StringType(), True),
        T.StructField("power", T.StringType(), True),
        T.StructField("printings", T.ArrayType(T.StringType(), True), True),
        T.StructField("promoTypes", T.ArrayType(T.StringType(), True), True),
        T.StructField(
            "purchaseUrls",
            T.StructType(
                [
                    T.StructField("cardKingdom", T.StringType(), True),
                    T.StructField("cardKingdomFoil", T.StringType(), True),
                    T.StructField("cardmarket", T.StringType(), True),
                    T.StructField("tcgplayer", T.StringType(), True),
                ]
            ),
            True,
        ),
        T.StructField("rarity", T.StringType(), True),
        T.StructField("rebalancedPrintings", T.ArrayType(T.StringType(), True), True),
        T.StructField(
            "rulings",
            T.ArrayType(
                T.StructType(
                    [
                        T.StructField("date", T.StringType(), True),
                        T.StructField("text", T.StringType(), True),
                    ]
                ),
                True,
            ),
            True,
        ),
        T.StructField("securityStamp", T.StringType(), True),
        T.StructField("setCode", T.StringType(), True),
        T.StructField("subtypes", T.ArrayType(T.StringType(), True), True),
        T.StructField("supertypes", T.ArrayType(T.StringType(), True), True),
        T.StructField("text", T.StringType(), True),
        T.StructField("toughness", T.StringType(), True),
        T.StructField("type", T.StringType(), True),
        T.StructField("types", T.ArrayType(T.StringType(), True), True),
        T.StructField("uuid", T.StringType(), True),
        T.StructField("variations", T.ArrayType(T.StringType(), True), True),
    ]
)
