import os
from os import listdir
from os.path import isfile
import re
import json


old_path = '.\\old'
new_path = '.\\new'
old_localisation_file_path = '.\\old_localisation_file'
old_files = []
regex = r'\s*([\w\d:\.]*)\s*(.*)'
raw_local_content = []
record_dict = {}
files = [f for f in listdir(old_path) if isfile(os.path.join(old_path, f))]

for f in files:
    raw_json = {}
    raw_local_json = {}
    record_list = []
    old_localisation_file = os.path.join(old_localisation_file_path, f)
    with open(os.path.join(old_path, f), 'r', encoding='utf-8-sig') as raw:
        raw_content = raw.read().splitlines()
    if os.path.exists(old_localisation_file):
        with open(old_localisation_file, 'r', encoding='utf-8-sig') as raw_local:
            raw_local_content = raw_local.read().splitlines()
        del raw_local_content[0]
    title = raw_content[0]
    del raw_content[0]
    for i in raw_content:
        result = re.search(regex, i)
        if result is None:
            continue
        raw_json[result.group(1)] = result.group(2)
        record_list.append(result.group(1))
    for i in raw_local_content:
        result = re.search(regex, i)
        if result is None:
            continue
        if result.group(1) in record_list:
            raw_json[result.group(1)] = result.group(2)
            record_list.remove(result.group(1))

    record_dict[f] = record_list

    with open(os.path.join(new_path, f), 'w', encoding='utf-8-sig') as writer:
        writer.write(f'{title}\n')
        for k, v in raw_json.items():
            writer.write(f' {k} {v}\n')
    print(record_list)
with open('differance.json', 'w' , encoding='utf-8-sig') as outfile:
    json.dump(record_dict, outfile)