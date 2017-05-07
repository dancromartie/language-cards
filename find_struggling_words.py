import re
import sys

import pandas as pd

import util

cards = util.from_cookie_jar(sys.argv[1])
data = pd.read_csv("drill_log.txt", sep=",", names=["id", "epoch", "interval"])
gb = data.groupby("id")["interval"].agg(["mean", "count"])
ids_struggling = list(gb[(gb["count"] > 1) & (gb["mean"] < 5)].index)
base_ids_struggling = set([re.sub(r"._to_.", "", id_) for id_ in ids_struggling])
cards_struggling = [card for card in cards if card["id"] in base_ids_struggling]
for cs in cards_struggling:
    print(cs)
