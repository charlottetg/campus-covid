import networkx as nx
import matplotlib.pyplot as plt
import scipy
import random
from random import choice
import numpy as np

from covidmodule import Person
from covidmodule import Graph

# graph constants
NUM_STUDENTS = 20
NUM_CLOSE = 1
PROB_CLOSE = 2 # will eventually want to make this a probability
NUM_TANG = 5
PROB_TANG = 1 # will eventually want to make this a probability

# build a people map
adjacency_list = {}

# create a new person object, add it to adjacency_list (associated with ID)
for i in range(1, NUM_STUDENTS+1): #for all of the students

    relationships = []

    # can eventually exclude i
    total_contacts = random.sample(range(1, NUM_STUDENTS+1), NUM_TANG + NUM_CLOSE)

    for j in range(NUM_TANG + NUM_CLOSE):
        if (j < NUM_CLOSE):
            relationships.append([total_contacts[j], PROB_CLOSE])
        else:
            relationships.append([total_contacts[j], PROB_TANG])

    adjacency_list[i] = Person(relationships)

# create graph instance
current_graph = Graph(adjacency_list)
print(current_graph)










"""
~graveyard~/testing code

# add edges
for i in range(1, NUM_STUDENTS+1):
    for pair in people[i].contacts:
        # print(pair)
        risk = pair[0]
        contacts = pair[1]
        for contact in contacts:
            g_basic.add_edge(i, contact, weight = risk)



g_basic = nx.Graph()
g_basic.add_node(i) #add them to the networkx graph


for i in random.sample(range(1, NUM_STUDENTS+1), 5):
    people[i].get_covid()

closecontacts = [(u, v) for (u, v, d) in g_basic.edges(data=True) if d["weight"] == 2 ]
tangentialcontacts = [(u, v) for (u, v, d) in g_basic.edges(data=True) if d["weight"] == 1 ]
dangerouscontacts = [(u, v) for (u, v, d) in g_basic.edges(data=True) if people[u].state!="healthy" or people[v].state!="healthy"]

safepeople = [ p for p in g_basic.nodes() if people[p].state=="healthy"]
unsafepeople = [ p for p in g_basic.nodes() if people[p].state=="asymptomatic"]
#drawing = nx.draw_networkx(g_basic, node_size = NODE_SIZES, with_labels = False)
#colors = nx.get_edge_attributes(g_basic,'color').values()
#weights = nx.get_edge_attributes(g_basic,'weight').values()

pos = nx.circular_layout(g_basic)  # positions for all nodes

# nodes
nx.draw_networkx_nodes(g_basic, pos, nodelist= safepeople, node_size=10, node_color="green")
nx.draw_networkx_nodes(g_basic, pos, nodelist= unsafepeople, node_size=20, node_color="red")


#nx.draw(g_basic, node_size = 10, edge_color=colors, width=list(weights))
nx.draw_networkx_edges(g_basic, pos, edgelist=tangentialcontacts, width=1)
nx.draw_networkx_edges(g_basic, pos, edgelist=closecontacts, width=2)
nx.draw_networkx_edges(g_basic, pos, edgelist = dangerouscontacts, width=1, edge_color="red", style = "dashed")

plt.show()
"""
