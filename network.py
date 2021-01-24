import powerlaw
import networkx as nx
import pandas
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np
import collections
from collections import deque
from operator import itemgetter
from networkx.algorithms.community import k_clique_communities
from networkx.algorithms import community

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


matches = pandas.read_csv('data/final2020.csv')
players = pandas.read_csv('data/players2020.csv')


matches = matches[(matches['winner_rank'] != 0)]
matches = matches[(matches['loser_rank'] != 0)]

matches = matches.drop(columns=['surface', 'tourney_level', 'date', 'winner_id', 'winner_state',
                                'loser_id', 'loser_state', 'winner_rank', 'winner_points', 'loser_rank', 'loser_points'])
matches['weight'] = 1

G = nx.from_pandas_edgelist(matches.groupby([matches.winner_name, matches.loser_name]).sum(
).reset_index(), 'winner_name', 'loser_name', edge_attr=True)

# dodavanje atributa cvorovima

for node in G.nodes():
    turniri = matches[(matches['winner_name'] == node) |
                      (matches['loser_name'] == node)]
    turniri = turniri.groupby(by=['tourney_name'])
    G.nodes[node]['state'] = players[players['name'] == node]['state'].iloc[0]
    G.nodes[node]['rank'] = int(
        players[players['name'] == node]['rank'].iloc[0])
    G.nodes[node]['tourney_num'] = len(turniri.groups.keys())
    G.nodes[node]['rank_c']=0 if G.nodes[node]['rank']<150 else 1

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
plt.xlabel('ATP rang')
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
plt.xlabel('ATP rang')
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
plt.xlabel('ATP rang')
plt.ylabel('Stepen cvora')


# ego mreze

ego_mrezaNDJ = nx.ego_graph(G, 'Novak Djokovic')
ego_mrezaRF = nx.ego_graph(G, 'Roger Federer')
ego_mrezaRN = nx.ego_graph(G, 'Rafael Nadal')
nx.write_gml(ego_mrezaNDJ, "Novak2020.gml")
nx.write_gml(ego_mrezaRF, "Federer2020.gml")
nx.write_gml(ego_mrezaRN, "Nadal2020.gml")

# VELIKA TROJKA EGO UNIJA
velika_trojka_ego_pom = nx.compose(ego_mrezaNDJ, ego_mrezaRF)
velika_trojka_ego = nx.compose(velika_trojka_ego_pom, ego_mrezaRN)
nx.write_gml(velika_trojka_ego, "velika_trojka_ego2020.gml")

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

# distribucija broja tenisera u odnosu na broj mečeva koji su odigrali
""" plt.figure()
degrees = [G.degree(n, weight="weight") for n in G.nodes()]
plt.hist(degrees)
plt.title('Distribucija broja tenisera u odnosu na broj mečeva koji su odigrali') """

# distribucija broja turnira u odnosu na podlogu i godinu održavanja
# distribucija broja mečeva u odnosu na podlogu i godinu održavanja

nx.write_gml(G, 'mreza2020.gml')
plt.show()
