import pandas

def get_players(df):
    df_win=df[['winner_id','winner_name','winner_state', 'winner_rank', 'winner_points']]
    df_win=df_win.rename(columns={'winner_id':'id','winner_name':'name','winner_state':'state','winner_rank':'rank', 'winner_points':'points'})
    df_los=df[['loser_id','loser_name','loser_state', 'loser_rank', 'loser_points']]
    df_los=df_los.rename(columns={'loser_id':'id','loser_name':'name','loser_state':'state','loser_rank':'rank', 'loser_points':'points'})

    df_players=pandas.concat([df_win,df_los])
    df_players=df_players.drop_duplicates()
    return df_players

df2018 = pandas.read_csv('data/final2018.csv')
df2019 = pandas.read_csv('data/final2019.csv')
df2020 = pandas.read_csv('data/final2020.csv')

players2018=get_players(df2018)
players2019=get_players(df2019)
players2020=get_players(df2020)

players2018.to_csv('data/players2018.csv', index=False)
players2019.to_csv('data/players2019.csv', index=False)
players2020.to_csv('data/players2020.csv', index=False)
