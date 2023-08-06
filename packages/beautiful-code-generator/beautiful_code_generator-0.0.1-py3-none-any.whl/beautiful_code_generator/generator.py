import json
import random
import pkg_resources
import pandas as pd


def _load_json_data(name):
    stream = pkg_resources.resource_stream(__name__, f'data/{name}.json')
    return json.load(stream)


ADJECTIVES = _load_json_data('adjectives')
NAMES = _load_json_data('names')
SURNAMES = _load_json_data('surnames')

# with open('data/adjectives.json') as json_file:
#     ADJECTIVES = json.load(json_file)
#
# with open('data/names.json') as json_file:
#     NAMES = json.load(json_file)
#
# with open('data/surnames.json') as json_file:
#     SURNAMES = json.load(json_file)


def generate_code():
    return "-".join([
        random.choice(ADJECTIVES),
        random.choice(ADJECTIVES),
        random.choice(NAMES),
        random.choice(SURNAMES)])