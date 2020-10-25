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
NUM_CLOSE = 2
PROB_CLOSE = .174 # will eventually want to make this a probability
NUM_TANG = 5
PROB_TANG = .031 # will eventually want to make this a probability

# build a people map
adjacency_list = {}

# create a new person object, add it to adjacency_list (associated with ID)
for i in range(1, NUM_STUDENTS+1): #for all of the students

    relationships = []

    # can eventually exclude i
    total_contacts = random.sample(range(1, NUM_STUDENTS+1), NUM_TANG + NUM_CLOSE)

    for j in range(NUM_TANG + NUM_CLOSE):
        if (j < NUM_CLOSE): # first add close contacts
            relationships.append([total_contacts[j], PROB_CLOSE])
        else:
            relationships.append([total_contacts[j], PROB_TANG])

    adjacency_list[i] = Person(relationships)

    adjacency_list[1].get_covid() # give one person covid

# create graph instance
graph = Graph(adjacency_list)

graph.graph_spread()
graph.graph_spread()
graph.graph_spread()

graph.show_graph()
