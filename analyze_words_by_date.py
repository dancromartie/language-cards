from datetime import datetime
import re
import sys

first_date = None
total_words = 0
for line in sys.stdin:
    line = line.strip()
    count, date = re.split("\s+", line)
    count = int(count)
    total_words += count
    if not first_date:
        first_date = date

first_date_obj = datetime.strptime(first_date, "%Y-%m-%d")
last_date_obj = datetime.now()
total_days = (last_date_obj - first_date_obj).days
print("Cards per day: %s" % (total_words * 1.0 / total_days))
print("Total days: %s" % total_days)
print("Total words: %s" % total_words)
