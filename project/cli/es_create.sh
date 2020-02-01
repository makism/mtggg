#!/bin/bash

curl -XPUT 'http://localhost:9200/mtgp/' -d '{
    "settings" : {
        "index" : {
            "number_of_shards" : 1,
            "number_of_replicas" : 1
        }
    }
}'
