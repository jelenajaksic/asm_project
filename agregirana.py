from networkx.algorithms import community
from networkx.algorithms.community import k_clique_communities
from operator import itemgetter
from collections import deque
import collections
import numpy as np
import powerlaw
import networkx as nx
import pandas
import matplotlib.pyplot as plt
import scipy.stats as stats

df2018 = pandas.read_csv('data/final2018.csv')
players2018 = pandas.read_csv('data/players2018.csv')

df2018 = df2018[(df2018['winner_rank'] != 0)]
df2018 = df2018[(df2018['loser_rank'] != 0)]

df2018 = df2018.drop(columns=['tourney_level', 'date', 'winner_id', 'winner_state',
                              'loser_id', 'loser_state', 'winner_rank', 'winner_points', 'loser_rank', 'loser_points'])
df2018['weight'] = 1

df2019 = pandas.read_csv('data/final2019.csv')
players2019 = pandas.read_csv('data/players2019.csv')

df2019 = df2019[(df2019['winner_rank'] != 0)]
df2019 = df2019[(df2019['loser_rank'] != 0)]

df2019 = df2019.drop(columns=['tourney_level', 'date', 'winner_id', 'winner_state',
                              'loser_id', 'loser_state', 'winner_rank', 'winner_points', 'loser_rank', 'loser_points'])
df2019['weight'] = 1

df2020 = pandas.read_csv('data/final2020.csv')
players2020 = pandas.read_csv('data/players2020.csv')

df2020 = df2020[(df2020['winner_rank'] != 0)]
df2020 = df2020[(df2020['loser_rank'] != 0)]

df2020 = df2020.drop(columns=[ 'tourney_level', 'date', 'winner_id', 'winner_state',
                              'loser_id', 'loser_state', 'winner_rank', 'winner_points', 'loser_rank', 'loser_points'])
df2020['weight'] = 1

frames = [df2018, df2019, df2020]
agregirano = pandas.concat(frames)

G = nx.from_pandas_edgelist(agregirano.groupby([agregirano.winner_name, agregirano.loser_name]).sum(
).reset_index(), 'winner_name', 'loser_name', edge_attr=True)

allp = pandas.concat([players2018, players2019, players2020])
for node in G.nodes():
    turniri18 = df2018[(df2018['winner_name'] == node) |
                       (df2018['loser_name'] == node)]
    turniri19 = df2019[(df2019['winner_name'] == node) |
                       (df2019['loser_name'] == node)]
    turniri20 = df2020[(df2020['winner_name'] == node) |
                       (df2020['loser_name'] == node)]
    turniri18 = turniri18.groupby(by=['tourney_name'])
    turniri19 = turniri19.groupby(by=['tourney_name'])
    turniri20 = turniri20.groupby(by=['tourney_name'])
    G.nodes[node]['state'] = allp[allp['name'] == node]['state'].iloc[0]

    if not players2020[players2020['name'] == node].empty:
        points2020 = int(
            players2020[players2020['name'] == node]['points'].iloc[0])
    else:
        points2020 = 0
    if not players2019[players2019['name'] == node].empty:
        points2019 = int(
            players2019[players2019['name'] == node]['points'].iloc[0])
    else:
        points2019 = 0
    if not players2018[players2018['name'] == node].empty:
        points2018 = int(
            players2018[players2018['name'] == node]['points'].iloc[0])
    else:
        points2018 = 0

    G.nodes[node]['points'] = points2020+points2019+points2018
    G.nodes[node]['tourney_num'] = len(turniri18.groups.keys(
    ))+len(turniri19.groups.keys())+len(turniri20.groups.keys())


points=list(nx.get_node_attributes(G,'points').values())
points.sort(reverse=True)
print(points)
points = list(dict.fromkeys(points))

for i in range(len(points)):
    nodesWithPoints = [x for x,y in G.nodes(data=True) if y['points']==points[i]]
    print(nodesWithPoints)
    for j in range(len(nodesWithPoints)):
        G.nodes[nodesWithPoints[j]]['rank']=i+1
        G.nodes[nodesWithPoints[j]]['rank_c']=0 if i<150 else 1

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


def plot_degree_histogram(g, normalized=True, weight=None):

    degree_sequence = sorted([d for n, d in g.degree(
        weight=weight)], reverse=True)  # degree sequence
    degreeCount = collections.Counter(degree_sequence)
    aux_x, aux_y = zip(*degreeCount.items())

    n_nodes = g.number_of_nodes()
    aux_y = list(aux_y)
    if normalized:
        for i in range(len(aux_y)):
            aux_y[i] = aux_y[i]/n_nodes

    return aux_x, aux_y


print(nx.info(G))
# c = list(k_clique_communities(G, 7))
# print(len(c))
# for i in range(len(c)):
#     print(i)
#     t=list(c[i])
#     for j in range(len(t)):
#         print(t[j])
#         G.nodes[t[j]]['k7']=i
# print(list(c[0]))
# nx.write_gml(G, "kklik2020_7.gml")

# communities_generator = community.girvan_newman(G)
# print(communities_generator)
# j=0
# level0=next(communities_generator)
# dd = deque(communities_generator, maxlen=1)
# last_element = dd.pop()
# # for p in range():
# #     level=next(communities_generator)
# for c in last_element:
#     for i in range(len(list(c))):
#         G.nodes[list(c)[i]]['gn']=j
#     j+=1

# nx.write_gml(G, "gn2020_p.gml")

# Rang u odnosu na broj turnira
plt.figure()
x = nx.get_node_attributes(G, 'rank').values()
y = nx.get_node_attributes(G, 'tourney_num').values()
plt.bar(x, y)
plt.xlabel('Rang')
plt.ylabel('Broj odigranih turnira')

# razlika tezinskog i netezinskog cvora
plt.figure()
degs = G.degree()
ranks, degrees = zip(*[(G.nodes[node]['rank'], val)
                       for (node, val) in G.degree()])
ranksw, degreesw = zip(*[(G.nodes[node]['rank'], val)
                         for (node, val) in G.degree(weight='weight')])
degreesw = np.array(degreesw)-np.array(degrees)
plt.bar(ranksw, degreesw)
plt.xlabel('Rang')
plt.ylabel('Razlika tezinskog i netezinskog stepena cvora')

# jezgro mreze

core = nx.k_core(G)
print(core.nodes())

for node in core:
    G.nodes[node]['core'] = 1
ranks_core = [G.nodes[node]['rank'] for (node) in G.nodes()]
ranks_core.sort()
print(ranks_core)


# distribucija stepena

plt.figure()
degrees = [G.degree(n) for n in G.nodes()]
plt.hist(degrees)
plt.title('Distribucija cvorova po stepenu')

plt.figure()
degrees = [G.degree(n, weight='weight') for n in G.nodes()]
plt.hist(degrees)
plt.title('Distribucija cvorova po tezinskom stepenu')

# plt.figure()
# degrees = [G.degree(n) for n in G.nodes()]
# degree_sequence = sorted(degrees, reverse=True)
# plt.loglog(degree_sequence, '.')
# plt.title('Distribucija cvorova po stepenu')
# fit = powerlaw.Fit(degree_sequence)
# fig2 = fit.plot_pdf(color='b', linewidth=2)
# fit.power_law.plot_pdf(color='g', linestyle='--', ax=fig2)


plt.figure()
plt.title('Distribucija cvora po stepenu (log-log scale)')
plt.xlabel('Degree')
plt.ylabel('Frequency')
plt.xscale("log")
plt.yscale("log")
plt.ylim(0.001, 10)
plt.plot(*plot_degree_histogram(G), 'o')

plt.figure()
plt.title('Distribucija cvora po tezinskom stepenu (log-log scale)')
plt.xlabel('Degree')
plt.ylabel('Frequency')
plt.xscale("log")
plt.yscale("log")
plt.ylim(0.001, 10)
plt.plot(*plot_degree_histogram(G, weight="weight"), 'o')

# stepen cvora u zavisnosti od ranga

plt.figure()
ranks, degrees = zip(*[(G.nodes[node]['rank'], val)
                       for (node, val) in G.degree()])
plt.scatter(ranks, degrees, s=1)
plt.xlabel('Rang')
plt.ylabel('Stepen cvora')


# ego mreze

ego_mrezaNDJ = nx.ego_graph(G, 'Novak Djokovic')
ego_mrezaRF = nx.ego_graph(G, 'Roger Federer')
ego_mrezaRN = nx.ego_graph(G, 'Rafael Nadal')
nx.write_gml(ego_mrezaNDJ, "NovakAgr.gml")
nx.write_gml(ego_mrezaRF, "FedererAgr.gml")
nx.write_gml(ego_mrezaRN, "NadalAgr.gml")

# VELIKA TROJKA EGO UNIJA
velika_trojka_ego_pom = nx.compose(ego_mrezaNDJ, ego_mrezaRF)
velika_trojka_ego = nx.compose(velika_trojka_ego_pom, ego_mrezaRN)
nx.write_gml(velika_trojka_ego, "velika_trojka_egoAgr.gml")

# ASORTATIVNOST

# asortativnost na osnovu netežinskog stepena čvora
r1 = nx.degree_assortativity_coefficient(G)
print(f"Koeficijent asortativnosti na osnovu netežinskog stepena čvora: {r1}")

# asortativnost na osnovu težinskog stepena čvora
r2 = nx.degree_assortativity_coefficient(G, weight='weight')
print(f"Koeficijent asortativnosti na osnovu težinskog stepena čvora: {r2}")

r3=nx.attribute_mixing_matrix(G, "rank_c")
print(f"Koeficijent asortativnosti na atributa za kategoriju ranga:\n {r3}")


# KOEF KLASTERIZACIJE

id_igraca, clustering_coef = zip(*nx.clustering(G, weight="weight").items())

nenula = [(id_ig, cc)
          for id_ig, cc in zip(id_igraca, clustering_coef) if cc > 0]

df = pandas.DataFrame(nenula, columns=["id", "cc"])
df.sort_values('cc', inplace=True)

max_lokalni_stepen_klasterisanja = max(clustering_coef)

prosecni_stepen_klasterisanja = nx.average_clustering(G)

print(f"Max lokalni cc: {max_lokalni_stepen_klasterisanja}")
print(f"Prosečan cc: {prosecni_stepen_klasterisanja}")

# centralnosti
df = calculate_centralities(G)
labele = ['DC', 'CC', 'BC', 'EVC']
cross_correlation_matrix = pandas.DataFrame(
    columns=['DC', 'CC', 'BC', 'EVC'], index=['DC', 'CC', 'BC', 'EVC'])
p_val_matrix = pandas.DataFrame(columns=['DC', 'CC', 'BC', 'EVC'], index=[
                                'DC', 'CC', 'BC', 'EVC'])

for ind in labele:
    for col in labele:
        cross_correlation_matrix[ind][col], p_val_matrix[ind][col] = stats.kendalltau(
            df[ind], df[col])

print(cross_correlation_matrix)
print(p_val_matrix)

# distribucija broja turnira u odnosu na podlogu i godinu održavanja
barWidth = 0.25
labels = ['2018', '2019', '2020']
print(labels)
hard = [len((df2018[df2018['surface']=='Hard'].groupby([df2018.tourney_name])).groups.keys()),len((df2019[df2019['surface']=='Hard'].groupby([df2019.tourney_name])).groups.keys()), len((df2020[df2020['surface']=='Hard'].groupby([df2020.tourney_name])).groups.keys())]
clay = [len((df2018[df2018['surface']=='Clay'].groupby([df2018.tourney_name])).groups.keys()),len((df2019[df2019['surface']=='Clay'].groupby([df2019.tourney_name])).groups.keys()), len((df2020[df2020['surface']=='Clay'].groupby([df2020.tourney_name])).groups.keys())]
grass = [len((df2018[df2018['surface']=='Grass'].groupby([df2018.tourney_name])).groups.keys()),len((df2019[df2019['surface']=='Grass'].groupby([df2019.tourney_name])).groups.keys()), len((df2020[df2020['surface']=='Grass'].groupby([df2020.tourney_name])).groups.keys())]

r1 = np.arange(len(hard))
r2 = [x + barWidth for x in r1]
r3 = [x + barWidth for x in r2]

# Make the plot
plt.figure()
plt.bar(r1, hard, color='#69808a', width=barWidth, edgecolor='white', label='Hard')
plt.bar(r2, clay, color='#a35103', width=barWidth, edgecolor='white', label='Clay')
plt.bar(r3, grass, color='#557f2d', width=barWidth, edgecolor='white', label='Grass')
 
# Add xticks on the middle of the group bars
plt.ylabel('Broj turnira')
plt.xlabel('Godina', fontweight='bold')
plt.xticks([r + barWidth for r in range(len(hard))], ['2018', '2019', '2020'])
 
# Create legend & Show graphic
plt.legend()


# distribucija broja mečeva u odnosu na podlogu i godinu održavanja

barWidth = 0.25
labels = ['2018', '2019', '2020']
print(labels)
hard = [(df2018[df2018['surface']=='Hard']).size,(df2019[df2019['surface']=='Hard']).size, (df2020[df2020['surface']=='Hard']).size]
clay = [(df2018[df2018['surface']=='Clay']).size,(df2019[df2019['surface']=='Clay']).size, (df2020[df2020['surface']=='Clay']).size]
grass = [(df2018[df2018['surface']=='Grass']).size,(df2019[df2019['surface']=='Grass']).size, (df2020[df2020['surface']=='Grass']).size]

r1 = np.arange(len(hard))
r2 = [x + barWidth for x in r1]
r3 = [x + barWidth for x in r2]

# Make the plot
plt.figure()
plt.bar(r1, hard, color='#69808a', width=barWidth, edgecolor='white', label='Hard')
plt.bar(r2, clay, color='#a35103', width=barWidth, edgecolor='white', label='Clay')
plt.bar(r3, grass, color='#557f2d', width=barWidth, edgecolor='white', label='Grass')
 
# Add xticks on the middle of the group bars
plt.ylabel('Broj meceva')
plt.xlabel('Godina', fontweight='bold')
plt.xticks([r + barWidth for r in range(len(hard))], ['2018', '2019', '2020'])
 
plt.legend()
nx.write_gml(G, 'mrezaAGR.gml')
plt.show()
