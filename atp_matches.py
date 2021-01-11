import pandas

df = pandas.read_csv('data/atp_matches_2020.csv')

df = df.drop(columns=['tourney_id', 'draw_size', 'match_num', 'winner_seed', 'winner_entry', 'winner_hand', 'winner_ht', 'winner_age', 'loser_seed', 'loser_entry', 'loser_hand', 'loser_ht', 'loser_age', 'score', 'best_of', 'round', 'minutes', 'w_ace', 'w_df',
                      'w_svpt', 'w_1stIn', 'w_1stWon', 'w_2ndWon', 'w_SvGms', 'w_bpSaved', 'w_bpFaced', 'l_ace', 'l_df', 'l_svpt', 'l_1stIn', 'l_1stWon', 'l_2ndWon', 'l_SvGms', 'l_bpSaved', 'l_bpFaced', 'winner_rank', 'winner_rank_points', 'loser_rank', 'loser_rank_points'])

df['tourney_name']=df['tourney_name'].apply(
    lambda x: (x if not 'Davis Cup' in x else 'Davis Cup'))

df.to_csv('data/2020.csv', index=False)


