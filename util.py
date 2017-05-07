import re


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
