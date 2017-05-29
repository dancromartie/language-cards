import collections
import csv
import random
import re
import subprocess
import sys
import time

import util


def find_due_cards(card_ids):
    due_cards = []
    current_epoch = int(time.time())
    with open("due_dates") as f_in:
        reader = csv.reader(f_in, delimiter=" ")
        for row in reader:
            if int(row[1]) < current_epoch:
                if row[0] in card_ids:
                    interval = None
                    # TODO interval is new feature.  unwind once all cards have this
                    if len(row) > 2:
                       interval = int(row[2])
                    card = {
                        "id": row[0],
                        "due_date": row[1],
                        "interval": interval
                    }
                    due_cards.append(card)
    return due_cards


def get_card_by_id(cards, card_id):
    matches = [card for card in cards if card["id"] == card_id]
    assert len(matches) == 1
    return matches[0]


def add_due_date_to_file(due_id, due_epoch, interval):
    due_date_string = "%s %s %s\n" % (due_id, due_epoch, interval)
    with open("due_dates", "a") as f_out:
        f_out.write(due_date_string)


def log_answer(due_id, interval):
    with open("drill_log.txt", "a") as f_out:
        f_out.write("%s,%s,%s\n" % (due_id, int(time.time()), interval))


def estimate_remaining_time(start_epoch, num_completed, num_total):
    current_epoch = int(time.time())
    seconds_elapsed = current_epoch - start_epoch
    seconds_per = seconds_elapsed * 1.0 / num_completed
    estimated_seconds = seconds_elapsed + seconds_per * (num_total - num_completed)
    return estimated_seconds / 60


def remove_similar(due_cards):
    """
    You don't want to practice an english->foreign and foreign->english version of the
    same word on the same day.  It's kind of cheating, as it gives you too much of a reminder.
    """
    deduped = {}
    for card in due_cards:
        base_id = re.sub(r"._to_.", "", card["id"])
        # Just overwrite the existing one if we ever get the same base id again
        # This won't be foolproof if you practice later in another session,
        # but, this scenario shouldn't happen too often anyways, except for words that you're
        # having trouble learning that are stuck at an interval of around 1.
        deduped[base_id] = card
    return [card for key, card in deduped.items()]


def main():
    start_epoch = int(time.time())
    words_file_path = sys.argv[1]
    cards = util.from_cookie_jar(words_file_path)
    candidate_ids = ["e_to_f" + x["id"] for x in cards]
    candidate_ids += ["f_to_e" + x["id"] for x in cards]
    due_cards = find_due_cards(candidate_ids)
    due_cards = remove_similar(due_cards)
    random.shuffle(due_cards)
    word_counter = 0
    for due_card in due_cards:
        word_counter += 1
        due_id = due_card["id"]
        base_id = re.sub("\w_to_\w", "", due_id)
        if word_counter > 1:
            remaining_time_estimate = estimate_remaining_time(
                start_epoch, word_counter - 1, len(due_cards))
            print("Estimated total practice time: %.1f mins" % remaining_time_estimate)
        print("Word %s of %s" % (word_counter, len(due_cards)))
        print("Due id: %s, Base id: %s, Interval: %s" % (due_id, base_id, due_card["interval"]))
        direction = re.search("(\w_to_\w)", due_id).group(1)
        # "due_card" so far was just from the practice logs,
        # This is the full fetch now.
        full_card = get_card_by_id(cards, base_id)
        if direction == "f_to_e":
            print("Foreign: %s" % full_card["foreign"])
        else:
            print("English: %s" % full_card["english"])

        interval = due_card["interval"]
        assert interval is None or interval < 300

        practice_in_x_days = None
        while not practice_in_x_days:
            response = input("Enter an interval for this card:")
            if response == "a":
                if direction == "f_to_e":
                    print(full_card["english"])
                else:
                    print(full_card["foreign"])
                print(full_card["notes"])
            elif re.match(r"^r?\d+$", response):
                practice_in_x_days = int(response.replace("r", ""))
                interval = practice_in_x_days
            elif re.match(r"^r?[di]+$", response):
                if interval is None:
                    print("cant add to interval of None")
                    continue
                interval += response.count("i")
                interval -= response.count("d")
                # Don't let it go 0 or negative
                interval = max(1, interval)
                practice_in_x_days = interval
            elif response == "w":
                interval = 1
                practice_in_x_days = interval
            else:
                print("Bad characters")
                continue
        assert 0 <= practice_in_x_days <= 100
        due_epoch = int(time.time()) + int(practice_in_x_days) * 86400
        add_due_date_to_file(due_id, due_epoch, interval)
        log_answer(due_id, interval)


def clean_due_dates():
    subprocess.call(["python", "clean_due_dates.py"])


if __name__ == "__main__":
    try:
        main()
    finally:
        clean_due_dates()
