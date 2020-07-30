# pylint: disable-all
import json
import os.path
from metaflow import FlowSpec, Parameter, step

import config
from mf_common_base import MF_Common_Base


class PrepareCards(FlowSpec, MF_Common_Base):
    @step
    def start(self):
        """ Begin here. """

        self.parse_keyruneCodes(ftype="json")

        self.next(self.process_json, foreach="list_keyruneCodes")

    @step
    def process_json(self):
        """ Read data. """

        self.code = self.input

        json_file = f"{config.DATASET}/{self.code}.json"
        cards = None
        with open(json_file, "r") as fp:
            raw_data = json.load(fp)
            cards = raw_data["cards"]
        n = len(cards)

        fname = f"{config.OUTPUT_DATASET}/{self.code}.json"
        with open(fname, "w") as fp:
            json.dump(cards, fp)

        self.next(self.join)

    @step
    def join(self, inputs):
        """Join our parallel branches."""

        self.next(self.end)

    @step
    def end(self):
        """ Finalize and clean up. """

        print("All done.")


if __name__ == "__main__":
    PrepareCards()
