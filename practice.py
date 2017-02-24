import csv
import re
import subprocess
import time

def find_due_cards():
    due_cards = []
    current_epoch = int(time.time())
    with open("due_dates") as f_in:
        reader = csv.reader(f_in, delimiter=" ")
        for row in reader:
            if int(row[1]) < current_epoch:
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
    due_ids = find_due_cards()
    cards = from_cookie_jar("words")
    for due_id in due_ids:
        print("Card id: %s" % due_id)
        card = get_card_by_id(cards, due_id)
        print("Foreign: %s" % card["foreign"])
        num_days = int(input("In how many seconds would you like to see this again?: "))
        assert 0 <= num_days <= 100
        due_epoch = int(time.time()) + int(num_days) * 1
        add_due_date_to_file(due_id, due_epoch)


def clean_due_dates():
    subprocess.call(["python", "clean_due_dates.py"])


if __name__ == "__main__":
    try:
        main()
    finally:
        clean_due_dates()
