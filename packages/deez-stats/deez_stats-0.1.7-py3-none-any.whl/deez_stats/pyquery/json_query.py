import json
import objectpath

# files
GAME_LEAGUE_ID_FILE = 'files/game_league_ids.json'
CLEANED_NAMES_FILE = 'files/cleaned_names.json'
OUTPUT_FILE = 'output/outfile{}.json'


def search_json_key(data, json_key):
    tree = objectpath.Tree(data)
    return tree.execute('${}'.format(json_key))  # result of search


def dump_to_outfile(data, num=None):
    out_num = ''
    if num is not None:
        out_num = num
    with open(OUTPUT_FILE.format(out_num), 'w') as outfile:
        json.dump(data, outfile, indent=4)


def read_from_json(file):
    with open(file, 'r') as infile:
        return json.load(infile)


def get_game_league_ids(year):
    data = read_from_json(GAME_LEAGUE_ID_FILE)
    return [data[str(year)]['game_id'], data[str(year)]['league_id']]


def get_cleaned_names():
    data = read_from_json(CLEANED_NAMES_FILE)
    return data
