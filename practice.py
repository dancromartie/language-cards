import csv
import random
import re
import subprocess
import sys
import time

def find_due_cards(card_ids):
    due_cards = []
    current_epoch = int(time.time())
    with open("due_dates") as f_in:
        reader = csv.reader(f_in, delimiter=" ")
        for row in reader:
            if int(row[1]) < current_epoch:
                if row[0] in card_ids:
                    due_cards.append(row[0])
    return due_cards


def from_cookie_jar(path):
    cookies = []
    file_text = open(path).read()
    chunks = re.split("-{40}", file_text)
    chunks = [x.strip() for x in chunks if x.strip()]
    for chunk in chunks:
        chunk_dict = {}
        for line in chunk.split("\n"):
            field, val = [x.strip() for x in line.split(":", 1)]
            chunk_dict[field] = val
        cookies.append(chunk_dict)
    return cookies


def get_card_by_id(cards, card_id):
    matches = [card for card in cards if card["id"] == card_id]
    assert len(matches) == 1
    return matches[0]


def add_due_date_to_file(due_id, due_epoch):
    due_date_string = "%s %s\n" % (due_id, due_epoch)
    with open("due_dates", "a") as f_out:
        f_out.write(due_date_string)


def main():
    words_file_path = sys.argv[1]
    cards = from_cookie_jar(words_file_path)
    card_ids = [x["id"] for x in cards]
    due_ids = find_due_cards(card_ids)
    for due_id in due_ids:
        print("Card id: %s" % due_id)
        card = get_card_by_id(cards, due_id)
        direction = random.choice(["f_to_e", "e_to_f"])
        if direction == "f_to_e":
            print("Foreign: %s" % card["foreign"])
        else:
            print("English: %s" % card["english"])
        valid_response = False
        while not valid_response:
            response = input("In how many days would you like to see this again?: ")
            if response == "a":
                if direction == "f_to_e":
                    print(card["english"])
                else:
                    print(card["foreign"])
                print(card["notes"])
            else:
                num_days = int(response)
                valid_response = True
        assert 0 <= num_days <= 100
        due_epoch = int(time.time()) + int(num_days) * 86400
        add_due_date_to_file(due_id, due_epoch)


def clean_due_dates():
    subprocess.call(["python", "clean_due_dates.py"])


if __name__ == "__main__":
    try:
        main()
    finally:
        clean_due_dates()
