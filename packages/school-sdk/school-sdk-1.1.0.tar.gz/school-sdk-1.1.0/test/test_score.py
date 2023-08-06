# -*- coding: utf-8 -*-
'''
    :file: test_score.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/09/20 22:59:24
'''
import json
import sys
import os

cur_path = os.path.abspath(__file__)
parent = os.path.dirname
sys.path.append(parent(parent(cur_path)))

from school_sdk import SchoolClient

gdust = SchoolClient('172.16.254.1', exist_verify=True)

user = gdust.user_login('2018133209', '123qwe')

score = user.get_score(year=2020, term=2)
print(score, type(score))
# with open("test\\data.json", 'w', encoding='utf-8') as f:
#     f.write(json.dumps(score))