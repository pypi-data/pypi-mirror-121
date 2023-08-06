import objectpath
import logging
import numpy as np
import yahoo_fantasy_api as yfa
import deez_stats.pyquery.database_query as dbq
import deez_stats.pyquery.yahoo_query as yq
import deez_stats.pyquery.json_query as jq

logging.basicConfig(level=logging.INFO)


class LeagueInfo:
    def __init__(self, sc, season=None, week=None):
        self.sc = sc
        self.league_key = None
        self.league_id = None
        self.name = None
        self.url = None
        self.logo_url = None
        self.num_teams = None
        self.num_matchups = None
        self.week = week
        self.start_week = None
        self.start_date = None
        self.end_week = None
        self.end_date = None
        self.game_id = None
        self.season = season
        self.cur_season = None
        self.weekly_matchups = None
        self.manager_names = None
        self._update_LeagueInfo()

    def get_weekly_matchups(self, with_names=True):
        matchups = yfa.League(self.sc, self.league_key).matchups(week=self.week)
        tree = objectpath.Tree(matchups)
        self.weekly_matchups = []
        self.weekly_matchups.append(list(map(int, list(tree.execute('$..team_id')))))
        self.weekly_matchups.append(list(map(float, list(tree.execute('$..team_points.total')))))
        self.weekly_matchups = np.array(self.weekly_matchups).T.tolist()  # transpose array to pair id with team points
        if with_names is True:
            for i in self.weekly_matchups:
                i[0] = self.manager_names[i[0]]
        logging.info('Found weekly matchups')

    def get_weekly_matchup_history(self):
        wmh = []
        for i in range(self.num_matchups):
            wmh.append(dbq.matchup_history(self.weekly_matchups[2 * i][0], self.weekly_matchups[2 * i + 1][0]))
            # matchups will be returned in the order manager[2*i] will always compete against manager[2*i+1]
        logging.info('Returning weekly matchup history object')
        return wmh

    def season_to_league_key(self):
        ids = jq.get_game_league_ids(self.season)
        return '{}.l.{}'.format(ids[0], ids[1])

    def get_current_season(self):
        raw_game_data = yq.json_query(self.sc, 'game/nfl')
        self.cur_season = int(list(jq.search_json_key(raw_game_data, '..season'))[0])

    def get_manager_names(self, lg, clean=True):
        nicknames = lg.yhandler.get_standings_raw(self.league_key)
        tree = objectpath.Tree(nicknames)
        mn = []
        mn.append(list(tree.execute('$..manager_id')))
        mn.append(list(tree.execute('$..nickname')))
        mn = dict(np.array(mn).T.tolist())
        keys_values = mn.items()
        self.manager_names = {int(key): str(value) for key, value in keys_values}
        if clean is True:
            self._clean_manager_names()

    def _clean_manager_names(self):
        cleaned_names = jq.get_cleaned_names()
        for key, value in self.manager_names.items():
            try:
                self.manager_names[key] = cleaned_names[value]
            except KeyError:  # not everyone's name is wrong so pass on the correct names
                pass

    def _update_LeagueInfo(self):
        self.get_current_season()
        if self.season is None:  # grab current season
            self.season = self.cur_season
            logging.info('No season specified, using current season.')
        self.league_key = self.season_to_league_key()
        league = yfa.League(self.sc, self.league_key)
        settings = league.settings()
        self.league_id = jq.search_json_key(settings, '.league_id')
        self.name = jq.search_json_key(settings, '.name')
        self.url = jq.search_json_key(settings, '.url')
        self.logo_url = jq.search_json_key(settings, '.logo_url')
        self.num_teams = jq.search_json_key(settings, '.num_teams')
        self.num_matchups = self.num_teams // 2
        self.start_week = int(jq.search_json_key(settings, '.start_week'))
        self.start_date = jq.search_json_key(settings, '.start_date')
        self.end_week = int(jq.search_json_key(settings, '.end_week'))
        self.end_date = jq.search_json_key(settings, '.end_date')
        self.game_code = jq.search_json_key(settings, '.game_code')
        if self.week is None:
            self.week = jq.search_json_key(settings, '.current_week')
            logging.info('No week specified, using current week.')
        self.get_manager_names(league)
        self.get_weekly_matchups()
