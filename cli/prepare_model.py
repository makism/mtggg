from metaflow import FlowSpec, step
import json
import numpy as np


class PrepModel(FlowSpec):
    @step
    def start(self):
        """ Begin here. """
        self.next(self.parse)

    @step
    def parse(self):
        """ Parse the cards. """
        json_file = "/home/makism/Dropbox/mtgp/dataset/M20.json"
        with open(json_file, "r") as fp:
            raw_data = json.load(fp)
            cards = raw_data["cards"]

        n = len(cards)
        s = np.int32(0.1 * n)

        self.next(self.end)

    @step
    def end(self):
        """ Finalize and clean up. """
        print("All done")


if __name__ == "__main__":
    PrepModel()
