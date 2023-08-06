import json
import objectpath

BASE_URI = 'https://fantasysports.yahooapis.com/fantasy/v2/'


def json_query(oauth2_token, url):
    url = BASE_URI + url + '?format=json'
    response = oauth2_token.session.get(url)
    json_data = json.loads(str(response.content, 'utf-8'))
    return json_data

# get from database maybe, initial season pull or manual enrty but only once a season


# league_id = 53342  # need to figure out get_league_id()
# game_id = 406  # need to figure out get_game_id()

# 2020
league_id = 228404
game_id = 399
team_id = 1

week = 1


# def get_team_info_raw(game_id, league_id, team_id):
#     url = BASE_URI + 'team/{}.l.{}.t.{}'.format(game_id, league_id, team_id)
#     return json_query(oauth2_token, url)


# def get_matchups_raw(game_id, league_id, team_id, week):
#     url = BASE_URI + 'team/{}.l.{}.t.{}/matchups;weeks={}'.format(game_id, league_id, team_id, week)
#     return json_query(oauth2_token, url)


# def get_league_info_raw(game_id, league_id):
#     url = BASE_URI + 'league/{}.l.{}'.format(game_id, league_id)
#     return json_query(oauth2_token, url)


# def get_scoreboard_raw(game_id, league_id, week):
#     url = BASE_URI + 'league/{}.l.{}/scoreboard;week={}'.format(game_id, league_id, week)
#     return json_query(oauth2_token, url)


# def search_json_key(data, json_key):
#     tree = objectpath.Tree(data)
#     return(list(tree.execute('$..{}'.format(json_key)))[0])  # result of search


# # data = get_team_info_raw(game_id, league_id, team_id)
# # search_result = search_json_key(data, 'manager_id')

# # data = get_league_info_raw(game_id, league_id, week)
# # matchups = search_json_key(data, 'matchups')

# with open('outfile.json', 'w') as outfile:
#     json.dump(data, outfile, indent=4)

# with open('outfile2.json', 'w') as outfile:
    # json.dump(matchups, outfile, indent=4)
