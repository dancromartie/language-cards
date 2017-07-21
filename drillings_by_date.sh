 cat drill_log.txt | awk -F, '{print $2}' | python sub_epochs.py | sort | uniq -c
