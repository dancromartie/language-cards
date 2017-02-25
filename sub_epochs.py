from datetime import datetime, time
import re
import sys

def replace_func(matches):
    epoch = matches.group(0)
    # This produces a naive date, but that's not so bad
    date_and_time = datetime.fromtimestamp(float(epoch))
    date = datetime.combine(date_and_time, time.min)
    date_string = date.strftime("%Y-%m-%d")
    return date_string

EPOCH_PATTERN = r"\d{7,}"
for line in sys.stdin:
    line = line.strip()
    line = re.sub(EPOCH_PATTERN, replace_func, line)
    print(line)
