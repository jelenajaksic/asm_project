import networkx as nx
import pandas
import matplotlib.pyplot as plt

df2018 = pandas.read_csv('data/final2020.csv')

df2018 = df2018.drop(columns=['tourney_name','surface','tourney_level','date','winner_id','winner_state','loser_id','loser_state','winner_rank','winner_points','loser_rank','loser_points'])
df2018['weight']=1

G=nx.from_pandas_edgelist(df2018.groupby([df2018.winner_name, df2018.loser_name]).sum().reset_index(), 'winner_name', 'loser_name', edge_attr=True)

print(G['Novak Djokovic'])
print(G.nodes)

#nx.write_gexf(G, "test2020.gexf")


nx.draw(G, with_labels=True)