import sqlite3
import pandas as pd
# import matplotlib.pyplot as plt


def execute_sqlite(sql_query):
    connection = sqlite3.connect('database/history.db')
    cursor = connection.cursor()
    result = cursor.execute(sql_query)
    result = list(result)
    cursor.close()
    connection.close()
    return result


def execute_commit(sql_query):
    connection = sqlite3.connect('database/history.db')
    cursor = connection.cursor()
    result = cursor.execute(sql_query)
    result = list(result)
    cursor.close()
    connection.commit()
    connection.close()
    return result


def execute_row_factory(sql_query):
    connection = sqlite3.connect('database/history.db')
    connection.row_factory = lambda cursor, row: row[0]
    c = connection.cursor()
    result = c.execute(sql_query)
    result = list(result)
    c.close()
    connection.close()
    return result


def get_manager_names(season):
    query_string = '''
        SELECT   manager_id,
                 manager_name
        FROM     manager
        WHERE    season == {}
        ORDER BY manager_id ASC;
    '''.format(season)
    result = execute_sqlite(query_string)
    return result


def matchup_history(manager_name, opponent_name):
    class WeeklyMatchupHistory:
        def __init__(self):
            self.manager_name = None
            self.opponent_name = None
            self.manager_avg_score = None
            self.opponent_avg_score = None
            self.manager_wins = 0
            self.opponent_wins = 0
            self.matchup_history = None

    wmh = WeeklyMatchupHistory()
    wmh.manager_name = manager_name
    wmh.opponent_name = opponent_name

    query_string = '''
        SELECT  season,
                manager_name,
                opponent_name,
                manager_score,
                opponent_score,
                result
        FROM    schedule
        WHERE   manager_name = "{}" AND opponent_name = "{}"
    '''.format(wmh.manager_name, wmh.opponent_name)
    result = execute_sqlite(query_string)

    df = pd.DataFrame(result, columns=['season', 'Manager', 'Opponent', 'Manager Score', 'Opponent Score', 'Result'])

    wmh.matchup_history = df
    wmh.manager_avg_score = df['Manager Score'].mean()
    wmh.opponent_avg_score = df['Opponent Score'].mean()

    try:
        wmh.manager_wins = df.Result.value_counts().W
    except AttributeError:
        wmh.manager_wins = 0

    try:
        wmh.opponent_wins = df.Result.value_counts().L
    except AttributeError:
        wmh.opponent_wins = 0
    # print(df.to_string(index=False))
    # print(df)

    # print("The current record between {} and {} is {} - {}. \
    #     ".format(wmh.manager_name, wmh.opponent_name, wmh.manager_wins, wmh.opponent_wins))

    # print("The average score between {} and {} is {:0.2f} - {:0.2f}. \n \
    #     ".format(wmh.manager_name, wmh.opponent_name, wmh.manager_avg_score, wmh.opponent_avg_score))
    return wmh


def get_manager_score_history(manager_name):
    query_string = '''
        SELECT  manager_score
        FROM    schedule
        WHERE   manager_name = "{}"
        ORDER BY manager_score DESC;
    '''.format(manager_name)
    result = execute_row_factory(query_string)
    return result


def update_weekly_results(li, update=False, display=True):
    df = pd.DataFrame(li.weekly_matchups, columns=['manager_name', 'manager_score'])
    df.insert(0, 'season', df.shape[0] * [li.season])
    df.insert(1, 'week', li.week)
    opponents = df.shape[0] * ['']
    opponent_scores = df.shape[0] * [0]
    results = []
    for i in range(df.shape[0] // 2):
        opponents[2 * i + 1] = df['manager_name'][2 * i]
        opponents[2 * i] = df['manager_name'][2 * i + 1]
        opponent_scores[2 * i + 1] = df['manager_score'][2 * i]
        opponent_scores[2 * i] = df['manager_score'][2 * i + 1]
        if df['manager_score'][2 * i] > df['manager_score'][2 * i + 1]:
            results.append('W')
            results.append('L')
        else:
            results.append('L')
            results.append('W')

    df['opponent_name'] = opponents
    df['opponent_score'] = opponent_scores
    df['results'] = results
    df['elo'] = df.shape[0] * [0]

    if display is True:
        print(df)

    if update is True:
        for i in range(df.shape[0]):
            row = df.iloc[[i]]  # based on index
            row = row.values.tolist()[0]
            query_string = '''
                INSERT INTO     schedule (
                                season,
                                week,
                                manager_name,
                                manager_score,
                                opponent_name,
                                opponent_score,
                                result,
                                elo)
                VALUES          ({}, {}, '{}', {}, '{}', {}, '{}', {})
            '''.format(*row)
            execute_commit(query_string)


def get_past_matchups(season, week):
    query_string = '''
        SELECT  *
        FROM    schedule
        WHERE   season = "{}" AND week = "{}"
    '''.format(season, week)
    result = execute_sqlite(query_string)
    return result


def get_table_column_names(table):
    query_string = '''
        PRAGMA table_info({})
    '''.format(table)
    result = execute_sqlite(query_string)
    return result
