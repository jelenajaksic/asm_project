import networkx as nx
import pandas
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np

matches = pandas.read_csv('data/final2018.csv')
players = pandas.read_csv('data/players2018.csv')

matches = matches.drop(columns=['surface','tourney_level','date','winner_id','winner_state','loser_id','loser_state','winner_rank','winner_points','loser_rank','loser_points'])
matches['weight']=1

G=nx.from_pandas_edgelist(matches.groupby([matches.winner_name, matches.loser_name]).sum().reset_index(), 'winner_name', 'loser_name', edge_attr=True)

turniri=matches[(matches['winner_name']=='Novak Djokovic') | (matches['loser_name']=='Novak Djokovic')]
turniri=turniri.groupby(by=['tourney_name'])
print(len(turniri.groups.keys()))
for node in G.nodes():
    #print(G.nodes['Adam Moundir'])
    #print(players[players['name']==node]['state'].iloc[0])
    turniri=matches[(matches['winner_name']==node) | (matches['loser_name']==node)]
    turniri=turniri.groupby(by=['tourney_name'])
    G.nodes[node]['state']= players[players['name']==node]['state'].iloc[0]
    G.nodes[node]['rank']= int(players[players['name']==node]['rank'].iloc[0])
    G.nodes[node]['tourney_num']=len(turniri.groups.keys())

# plt.figure()
# x = nx.get_node_attributes(G, 'rank').values()
# print(x)
# y = nx.get_node_attributes(G, 'tourney_num').values()
# plt.bar(x,y)
# plt.xlabel('ATP rang')
# plt.ylabel('Broj odigranih turnira')

plt.figure()
degs=G.degree()
print(degs)
ranks, degrees = zip(*[(G.nodes[node]['rank'],val) for (node, val) in G.degree()])
ranksw, degreesw = zip(*[(G.nodes[node]['rank'],val) for (node, val) in G.degree(weight='weight')])
print(degrees)
degreesw=np.array(degreesw)-np.array(degrees)
plt.bar(ranksw,degreesw)
plt.xlabel('ATP rang')
plt.ylabel('Razlika tezinskog i netezinskog stepena cvora')
# plt.bar(ranks,degrees)
# plt.show()
print(G.nodes['Novak Djokovic'])
# nx.write_gml(G, 'mreza2018.gml')
print(nx.info(G))
""" print(df2018[(df2018['winner_name']=='Novak Djokovic') &  (df2018['loser_name']=='Rafael Nadal')])
print(df2018[(df2018['loser_name']=='Novak Djokovic') &  (df2018['winner_name']=='Rafael Nadal')]) """
""" nx.draw(G, with_labels=True) """

# CORE

core = nx.k_core(G)
print(core.nodes())

ranks_core = [G.nodes[node]['rank'] for (node) in G.nodes()]
ranks_core.sort()
print(ranks_core)

#distribucija stepena
plt.figure()
degrees = [G.degree(n) for n in G.nodes()]
plt.hist(degrees)
plt.title('Distribucija cvorova po stepenu')

plt.figure()
ranks, degrees = zip(*[(G.nodes[node]['rank'],val) for (node, val) in G.degree()])
plt.scatter(ranks, degrees, s=1)
# slope, intercept, r, p, stderr = stats.linregress(ranks, degrees)
# plt.plot(ranks, intercept + slope * ranks)
plt.xlabel('ATP rang')
plt.ylabel('Stepen cvora')

plt.show()
#EGO 
ego_mrezaNDJ = nx.ego_graph(G, 'Novak Djokovic')
ego_mrezaRF =nx.ego_graph(G, 'Roger Federer')
ego_mrezaRN =nx.ego_graph(G, 'Rafael Nadal')
# nx.write_gml(ego_mrezaNDJ, "Novak2020.gml")
# nx.write_gml(ego_mrezaRF, "Federer2020.gml")
# nx.write_gml(ego_mrezaRN, "Nadal2020.gml")
""" print(f"Čvorovi ego mreže igrača crraii su {ego_mreza.nodes}")
plt.figure(figsize=(15,10))
tezine_grana = nx.get_edge_attributes(ego_mreza,'weight')
pos = nx.circular_layout(ego_mreza)
#pos = nx.spring_layout(ego_mreza)
#print(pos)
nx.draw_networkx(ego_mreza, pos)
nx.draw_networkx_edge_labels(ego_mreza, pos, edge_labels = tezine_grana)

plt.show() """

#VELIKA TROJKA EGO UNIJA
velika_trojka_ego_pom = nx.compose(ego_mrezaNDJ,ego_mrezaRF)
velika_trojka_ego = nx.compose(velika_trojka_ego_pom,ego_mrezaRN)
# nx.write_gml(velika_trojka_ego, "velika_trojka_ego2020.gml")

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