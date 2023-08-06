current_rating_1 = 600
current_rating_2 = 300

transformed_rating_1 = 10 ** (current_rating_1 / 400)
transformed_rating_2 = 10 ** (current_rating_2 / 400)

print('{} {}'.format(transformed_rating_1, transformed_rating_2))

expected_rating_1 = transformed_rating_1 / (transformed_rating_1 + transformed_rating_2)
expected_rating_2 = transformed_rating_2 / (transformed_rating_1 + transformed_rating_2)

print('{} {}'.format(expected_rating_1, expected_rating_2))

score_player_1 = 1
score_player_2 = 0

K = 32
updated_elo_1 = round(current_rating_1 + K * (score_player_1 - expected_rating_1))
updated_elo_2 = round(current_rating_2 + K * (score_player_2 - expected_rating_2))

print('{} {}'.format(updated_elo_1, updated_elo_2))
