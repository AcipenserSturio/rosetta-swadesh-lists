
# from internetarchive import search_items
# for i in search_items('swadesh collection:rosettaproject'):
#     print(i['identifier'])
#
# >> swadesh-archive.txt

import re
import requests
from pathlib import Path

import concurrent.futures


def get_swadesh_codes():
    with open("swadesh-archive.txt") as f:
        for line in f.read().split("\n"):
            if "swadesh" not in line:
                continue
            code = re.findall(r"(?<=_)...(?=_)", line)[0]
            if Path(f"out/{code}.txt").exists():
                continue
            print(code)
            yield line, code


def request(item):
    line, code = item
    link = f"https://archive.org/download/{line}/{code}.txt"
    response = requests.get(link)
    with open(f"out/{code}.txt", "wb") as f:
        f.write(response.content)


with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(request, get_swadesh_codes())
