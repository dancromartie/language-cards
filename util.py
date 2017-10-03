import re
import time


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


def get_recently_drilled(path, num_days=1):
    drilled_ids = []
    now = int(time.time())
    with open(path) as f_in:
        for line in f_in:
            drill_id = line.strip().split(",")[0]
            epoch = line.strip().split(",")[1]
            if (now - int(epoch)) < 86400 * num_days:
                drilled_ids.append(drill_id)
    return drilled_ids


def remove_similar(due_ids, recently_drilled_ids):
    to_return = []
    for due_id in due_ids:
        found = False
        due_base_id = re.search(r"\w_to_\w(.*)", due_id).group(1)
        for recent_id in recently_drilled_ids:
            recent_base_id = re.search(r"\w_to_\w(.*)", recent_id).group(1)
            if recent_base_id == due_base_id:
                found = True
        if not found:
            to_return.append(due_id)
    return to_return
