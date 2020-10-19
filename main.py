import networkx as nx
import matplotlib.pyplot as plt
import scipy
import random
from random import choice
import numpy as np


# people constants
MEAN_SYMPTOMATIC = 6 # 6 days on average
STANDARD_DEV_SYMPTOMATIC = 1.2 # can change this later

# graph constants
NUM_STUDENTS = 20
NUM_CLOSE = 1
PROB_CLOSE = 2 # will eventually want to make this a probability
NUM_TANG = 5
PROB_TANG = 1


class Person:

    def __init__(self, contacts):
        self.state = "healthy"
        self.contacts = contacts

        # how many days before a person is symptomatic: initalize as -1
        self.before_symptomatic = -1

    def get_covid(self):
        # change state to infected asymptomatic
        self.state = "asymptomatic"

        # randomly sample from disrubtion to get # time steps before symptomatic
        self.before_symptomatic = np.random.normal(MEAN_SYMPTOMATIC, STANDARD_DEV_SYMPTOMATIC)

    def get_tested(self):
        if (self.state == "asymptomatic"):
            self.state = "quarantined"

class Graph:
    def __init__(self):
        close_data = [NUM_CLOSE, PROB_CLOSE]
        tang_data = [NUM_TANG, PROB_TANG]

        # initialize graph
        g_basic = nx.Graph()

        # initialize node infos: dumb! slow!
        people = {}

        for i in range(1, NUM_STUDENTS+1): #for all of the students
            #if they are not already in the graph?
            """
            if i in people:
                #they're someone's close contact already! whose?
                print('already a contact?')
            """
            g_basic.add_node(i) #add them to the networkx graph

            # add contact edges
            # tangential contacts
            tang_contacts = random.sample(range(1, NUM_STUDENTS+1), tang_data[0])

            # close contacts
            close_contacts = random.sample(range(1, NUM_STUDENTS+1), close_data[0])
            #for each of their close contacts, we gotta do something here!

            contacts = [(tang_data[1], tang_contacts), (close_data[1], close_contacts)]
            people[i] = Person(contacts)


        # add edges
        for i in range(1, NUM_STUDENTS+1):
            for pair in people[i].contacts:
                # print(pair)
                risk = pair[0]
                contacts = pair[1]
                for contact in contacts:
                    g_basic.add_edge(i, contact, weight = risk)


        # code for testing

        #testing the viewing by giving 5 random people covid
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

Graph()
