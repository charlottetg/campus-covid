import networkx as nx
import matplotlib.pyplot as plt
import scipy
import random
from random import choice
import numpy as np

class Person:

    def __init__(self, contacts):
        self.contacts = contacts # this is a 2D array [friend, weight]

        # how many days before a person is symptomatic:
        # this encodes their state (-1 = healthy, >= 0 = asymptomatic, -2 = quarantined)
        self.before_symptomatic = -1

    def get_covid(self):

        # people constants (move these out?)
        MEAN_SYMPTOMATIC = 6 # 6 days on average
        STANDARD_DEV_SYMPTOMATIC = 1.2 # can change this later

        # randomly sample from disrubtion to get # time steps before symptomatic
        if (self.before_symptomatic == -1):
            self.before_symptomatic = np.random.normal(MEAN_SYMPTOMATIC, STANDARD_DEV_SYMPTOMATIC)

    def get_tested(self):
        if (self.before_symptomatic >= 0 ): # asymptomatic
            self.before_symptomatic = -2
            return True # do something
        if (self.before_symptomatic == -1 or self.before_symptomatic == -2): # healthy or in quarantine
            return False # do nothing

    """
    def spread_covid(self):
        for
    """


class Graph:

    def __init__(self, adjacency_list):
        self.adjacency_list = adjacency_list

    """
    # every time step
    def graph_spread(self):

        for person_id in self.adjacency_list.keys():
            person = adjacency_list[person_id]
            if person.before_symptomatic > 0: # asymptomatic! danger!
                person.before_symptomatic -= 1 # decrease by 1


        np.random.choice([])

    def dynamic_test(self, people_to_test):

        return discovered_positives

    """

    # display graph using networkx
    def show_graph(self):

        PROB_CLOSE = 2 # will eventually want to make this a probability
        PROB_TANG = 1 # will eventually want to make this a probability

        g = nx.Graph()
        people_map = self.adjacency_list
        people_ids = people_map.keys()

        # nodes
        for person_id in people_ids:
            g.add_node(person_id)

        # edges
        for person_id in people_ids:
            for contact in people_map[person_id].contacts:
                g.add_edge(person_id, contact[0], weight = contact[1])

        healthy = [ person_id for person_id in g.nodes() if people_map[person_id].before_symptomatic == -1]
        asymptomatic = [ person_id for person_id in g.nodes() if people_map[person_id].before_symptomatic >= 0]
        quarantined = [ person_id for person_id in g.nodes() if people_map[person_id].before_symptomatic == -2]

        pos = nx.circular_layout(g)  # positions for all nodes

        # nodes
        nx.draw_networkx_nodes(g, pos, nodelist= healthy, node_size=50, node_color="green")
        nx.draw_networkx_nodes(g, pos, nodelist= asymptomatic, node_size=50, node_color="red")
        nx.draw_networkx_nodes(g, pos, nodelist= quarantined, node_size=50, node_color="black")

        # make edges
        close_contacts = [(u, v) for (u, v, d) in g.edges(data=True) if d["weight"] == PROB_CLOSE]
        tang_contacts = [(u, v) for (u, v, d) in g.edges(data=True) if d["weight"] == PROB_TANG]
        dangerous_contacts = [(u, v) for (u, v, d) in g.edges(data=True) if people_map[u].before_symptomatic >= 0 or people_map[v].before_symptomatic >= 0]

        # draw edges
        nx.draw_networkx_edges(g, pos, edgelist=tang_contacts, width=1)
        nx.draw_networkx_edges(g, pos, edgelist=close_contacts, width=2)
        nx.draw_networkx_edges(g, pos, edgelist = dangerous_contacts, width=1, edge_color="red")

        plt.show()
