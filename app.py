import json
import random
import re
import subprocess
import time

from flask import Flask, render_template, request

import practice
import util

webapp = Flask(__name__)


@webapp.route("/language", methods=["POST", "GET"])
def page():
    if request.method == "POST":
        submitted_increment = request.form["increment"]
        submitted_interval = request.form["interval"]
        submitted_id = request.form["card-id"]
        assert submitted_increment.isdigit() or submitted_increment == "w"
        assert submitted_interval.isdigit()
        if submitted_increment == "w":
            new_interval = 1
            due_epoch = int(time.time() + int(86400 * .8))
        else:
            new_interval = int(submitted_interval) + int(submitted_increment)
            due_epoch = int(time.time() + new_interval * 86400)
    
        practice.add_due_date_to_file(submitted_id, due_epoch, new_interval)
        practice.log_answer(submitted_id, new_interval)
        subprocess.call(["python", "clean_due_dates.py"])
        time.sleep(1)

    card = get_a_card()
    if card == "nothing to practice":
        return "nothing to practice"
    if card["direction"] == "e_to_f":
        card["question"] = card["english"]
        card["answer"] = card["foreign"]
    else:
        card["question"] = card["foreign"]
        card["answer"] = card["english"]
    return render_template("single_question.html", card=card)


def get_a_card():
    words_file_path = "chinese_words"
    cards = util.from_cookie_jar(words_file_path)
    candidate_ids = ["e_to_f" + x["id"] for x in cards]
    candidate_ids += ["f_to_e" + x["id"] for x in cards]
    due_cards = practice.find_due_cards(candidate_ids)
    if not due_cards:
        return "nothing to practice"

    orig_id = due_cards[0]["id"]
    interval = due_cards[0]["interval"]
    direction = re.search(r"\w_to_\w", orig_id).group(0)
    base_id = re.sub("\w_to_\w", "", orig_id)

    full_card = practice.get_card_by_id(cards, base_id)
    full_card["orig_id"] = orig_id
    full_card["direction"] = direction
    full_card["interval"] = interval
    return full_card


if __name__ == "__main__":
    webapp.run("127.0.0.1", port=5129)
