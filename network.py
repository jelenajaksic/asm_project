import networkx as nx
import pandas
import matplotlib.pyplot as plt
import scipy.stats as stats

df2018 = pandas.read_csv('data/final2020.csv')
players2018 = pandas.read_csv('data/players2020.csv')

df2018 = df2018.drop(columns=['tourney_name','surface','tourney_level','date','winner_id','winner_state','loser_id','loser_state','winner_rank','winner_points','loser_rank','loser_points'])
df2018['weight']=1

G=nx.from_pandas_edgelist(df2018.groupby([df2018.winner_name, df2018.loser_name]).sum().reset_index(), 'winner_name', 'loser_name', edge_attr=True)

for node in G.nodes():
    #print(G.nodes['Adam Moundir'])
    #print(players2018[players2018['name']==node]['state'].iloc[0])
    G.nodes[node]['state']= players2018[players2018['name']==node]['state'].iloc[0]


nx.write_gml(G, "test2018.gml")
print(nx.info(G))
""" print(df2018[(df2018['winner_name']=='Novak Djokovic') &  (df2018['loser_name']=='Rafael Nadal')])
print(df2018[(df2018['loser_name']=='Novak Djokovic') &  (df2018['winner_name']=='Rafael Nadal')]) """


""" nx.draw(G, with_labels=True) """


#EGO 
""" ego_mreza = nx.ego_graph(G, 'Nicolas Jarry')
print(f"Čvorovi ego mreže igrača crraii su {ego_mreza.nodes}")
plt.figure(figsize=(15,10))
tezine_grana = nx.get_edge_attributes(ego_mreza,'weight')
pos = nx.circular_layout(ego_mreza)
#pos = nx.spring_layout(ego_mreza)
#print(pos)
nx.draw_networkx(ego_mreza, pos)
nx.draw_networkx_edge_labels(ego_mreza, pos, edge_labels = tezine_grana)

plt.show() """

#ASORTATIVNOST

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
print("Lokalni stepeni klasterisanja koji nisu nula:")
print(df)

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