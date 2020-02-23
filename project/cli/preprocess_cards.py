import json
import numpy as np
import os.path
from pyspark.context import SparkContext
from pyspark.sql import SparkSession
from metaflow import FlowSpec, Parameter, step


class PreprocessCards(FlowSpec):
    keyruneCodes = Parameter('keyruneCodes', default='THB,ELD,M20WAR')
    
    @step
    def start(self):
        """ Begin here. """
        
        self.list_keyruneCodes = list()
        
        for code in self.keyruneCodes.split(','):
            json_file = f'../dataset/{code}.json'
            
            if os.path.exists(json_file):
                self.list_keyruneCodes.append(code)
        
        self.next(self.load_data, foreach='list_keyruneCodes')

    @step
    def load_data(self):
        """ Read data. """
        self.code = self.input
        
        json_file = f'../dataset/{self.code}.json'
        cards = None
        with open(json_file, 'r') as fp:
            raw_data = json.load(fp)
            cards = raw_data['cards']
        n = len(cards)
        
        self.cards = cards
        
        self.next(self.join)
    
    @step
    def join(self, inputs):
        """Join our parallel branches and merge results into a dictionary."""
        self.results = [input.code for input in inputs]
        self.next(self.end)

    @step
    def end(self):
        """ Finalize and clean up. """
        print("All done.")


if __name__ == "__main__":
    # run preprocess_cards.py run --keyruneCodes 'THB,ELD'
    PreprocessCards()
