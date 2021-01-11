import pandas

players=pandas.read_csv('data/atp_players.csv')
players['id']=players['id'].astype(str)
ranks=pandas.read_csv('data/atp_rankings_10s.csv')
ranks=ranks.fillna(0)
ranks['ranking_date']=ranks['ranking_date'].astype(str)
ranks['player']=ranks['player'].astype(str)
ranks['rank']=ranks['rank'].astype(int)
ranks['points']=ranks['points'].astype(int)

#2020
rank2020=pandas.read_csv('data/atp_rankings_current.csv')
rank2020['id']=rank2020['id'].astype(str)

rank2020=rank2020.merge(players, how='left',on='id')
print(rank2020.columns)
rank2020['name']=rank2020['name'] + ' ' + rank2020['surname']
rank2020=rank2020.drop(columns=['hand', 'birth', 'surname'])
rank2020['date']=rank2020['date'].apply(lambda x: pandas.to_datetime(str(x), format='%Y%m%d'))


rank2020.to_csv('data/2020ranks.csv', index=False)

#2019
rank2019=ranks[ranks['ranking_date'].str.contains('2019')]
print(rank2019['ranking_date'].drop_duplicates())

rank2019=rank2019.merge(players, how='inner',left_on='player', right_on='id')
print(rank2019.columns)
rank2019['name']=rank2019['name'] + ' ' + rank2019['surname']
rank2019=rank2019.drop(columns=['hand', 'birth', 'surname'])

rank2019=rank2019.rename(columns={'ranking_date':'date', 'player':'id', 'id':'b'})
rank2019=rank2019.drop(columns=['b'])
rank2019['date']=rank2019['date'].apply(lambda x: pandas.to_datetime(str(x), format='%Y%m%d'))

rank2019.to_csv('data/2019ranks.csv', index=False)

#2018
rank2018=ranks[ranks['ranking_date'].str.contains('2018')]
print(rank2018['ranking_date'].drop_duplicates())

rank2018=rank2018.merge(players, how='inner',left_on='player', right_on='id')
print(rank2018.columns)
rank2018['name']=rank2018['name'] + ' ' + rank2018['surname']
rank2018=rank2018.drop(columns=['hand', 'birth', 'surname'])

rank2018=rank2018.rename(columns={'ranking_date':'date', 'player':'id', 'id':'b'})
rank2018=rank2018.drop(columns=['b'])
rank2018['date']=rank2018['date'].apply(lambda x: pandas.to_datetime(str(x), format='%Y%m%d'))

rank2018.to_csv('data/2018ranks.csv', index=False)