import collections
import csv

lines_by_id = collections.defaultdict(list)

with open("due_dates") as f_in:
    reader = csv.reader(f_in, delimiter=" ")
    for row in reader:
        card_id = row[0]
        due_date = row[1]
        lines_by_id[card_id].append(int(due_date))

with open("due_dates", "w") as f_out:
    for card_id in lines_by_id:
        due_dates_this_card = lines_by_id[card_id]
        due_dates_this_card.sort(reverse=True)
        first_epoch = due_dates_this_card[0]
        f_out.write("%s %s\n" % (card_id, first_epoch))
