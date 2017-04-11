import collections
import csv

lines_by_id = collections.defaultdict(list)

with open("due_dates") as f_in:
    reader = csv.reader(f_in, delimiter=" ")
    for row in reader:
        card_id = row[0]
        due_date = int(row[1])
        interval = None
        # TODO interval is new feature.  unwind once all cards have this
        if len(row) > 2:
            interval = int(row[2])
        practice_record = {
            "id": card_id,
            "due_date": due_date,
            "interval": interval
        }
        lines_by_id[card_id].append(practice_record)

with open("due_dates", "w") as f_out:
    for card_id in lines_by_id:
        practice_records_this_card = lines_by_id[card_id]
        practice_records_this_card.sort(key=lambda x: x["due_date"], reverse=True)
        to_write = practice_records_this_card[0]
        if to_write["interval"] is not None:
            f_out.write("%s %s %s\n" % (to_write["id"], to_write["due_date"], to_write["interval"]))
        else:
            f_out.write("%s %s\n" % (to_write["id"], to_write["due_date"]))
