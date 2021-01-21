import networkx as nx
import pandas
import matplotlib.pyplot as plt
import scipy.stats as stats

df2018 = pandas.read_csv('data/final2018.csv')
players2018 = pandas.read_csv('data/players2018.csv')

df2018 = df2018[(df2018['winner_rank']!=0)]
df2018=df2018[(df2018['loser_rank']!=0)]

df2018 = df2018.drop(columns=['tourney_name','surface','tourney_level','date','winner_id','winner_state','loser_id','loser_state','winner_rank','winner_points','loser_rank','loser_points'])
df2018['weight']=1

df2019 = pandas.read_csv('data/final2019.csv')
players2019 = pandas.read_csv('data/players2019.csv')

df2019 = df2019[(df2019['winner_rank']!=0)]
df2019=df2019[(df2019['loser_rank']!=0)]

df2019 = df2019.drop(columns=['tourney_name','surface','tourney_level','date','winner_id','winner_state','loser_id','loser_state','winner_rank','winner_points','loser_rank','loser_points'])
df2019['weight']=2

df2020= pandas.read_csv('data/final2020.csv')
players2020 = pandas.read_csv('data/players2020.csv')

df2020 = df2020[(df2020['winner_rank']!=0)]
df2020=df2020[(df2020['loser_rank']!=0)]

df2020 = df2020.drop(columns=['tourney_name','surface','tourney_level','date','winner_id','winner_state','loser_id','loser_state','winner_rank','winner_points','loser_rank','loser_points'])
df2020['weight']=2

frames=[df2018,df2019,df2020]
agregirano=pandas.concat(frames)

G=nx.from_pandas_edgelist(agregirano.groupby([agregirano.winner_name, agregirano.loser_name]).sum().reset_index(), 'winner_name', 'loser_name', edge_attr=True)

nx.write_gml(G, "agregirana.gml")


# asortativnost na osnovu netežinskog stepena čvora
r1 = nx.degree_assortativity_coefficient(G)
print(f"Koeficijent asortativnosti na osnovu netežinskog stepena čvora: {r1}")

# asortativnost na osnovu težinskog stepena čvora
r2 = nx.degree_assortativity_coefficient(G, weight='weight')
print(f"Koeficijent asortativnosti na osnovu težinskog stepena čvora: {r2}")


#KOEF KLASTERIZACIJE

id_igraca, clustering_coef = zip(*nx.clustering(G, weight = "weight").items())

nenula = [(id_ig, cc)  for id_ig, cc in zip(id_igraca, clustering_coef) if cc > 0]

df = pandas.DataFrame(nenula, columns = ["id", "cc"])
df.sort_values('cc', inplace = True)

max_lokalni_stepen_klasterisanja = max(clustering_coef)

prosecni_stepen_klasterisanja = nx.average_clustering(G)

print(f"Max lokalni cc: {max_lokalni_stepen_klasterisanja}")
print(f"Prosečan cc: {prosecni_stepen_klasterisanja}")
# print("Lokalni stepeni klasterisanja koji nisu nula:")
# print(df)

## centralnosti

def calculate_centralities(G):

    DC_dict = nx.degree_centrality(G)
    CC_dict = nx.closeness_centrality(G)
    BC_dict = nx.betweenness_centrality(G)
    EVC_dict = nx.eigenvector_centrality(G)

    df1 = pandas.DataFrame.from_dict(DC_dict, orient='index', columns=['DC'])
    df2 = pandas.DataFrame.from_dict(CC_dict, orient='index', columns=['CC'])
    df3 = pandas.DataFrame.from_dict(BC_dict, orient='index', columns=['BC'])
    df4 = pandas.DataFrame.from_dict(EVC_dict, orient='index', columns=['EVC'])
    df = pandas.concat([df1, df2, df3, df4], axis=1)
    return df

df = calculate_centralities(G)
labele = ['DC', 'CC', 'BC', 'EVC']
cross_correlation_matrix = pandas.DataFrame(columns = ['DC', 'CC', 'BC', 'EVC'], index = ['DC', 'CC', 'BC', 'EVC'])
p_val_matrix = pandas.DataFrame(columns = ['DC', 'CC', 'BC', 'EVC'], index = ['DC', 'CC', 'BC', 'EVC'])

for ind in labele:
    for col in labele:
        cross_correlation_matrix[ind][col], p_val_matrix[ind][col] =  stats.kendalltau(df[ind], df[col])

print(cross_correlation_matrix)
print(p_val_matrix)