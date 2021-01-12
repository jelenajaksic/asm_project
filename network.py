import networkx as nx
import pandas
import matplotlib.pyplot as plt

df2018 = pandas.read_csv('data/final2020.csv')

G=nx.from_pandas_edgelist(df2018, 'winner_name', 'loser_name', edge_attr=True)

nx.draw(G, with_labels=True)

plt.show()