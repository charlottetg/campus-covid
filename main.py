import networkx as nx
import matplotlib.pyplot as plt
import scipy
import random
from random import choice

class Person:
    def __init__(self, contacts):
        self.state = "healthy"
        self.contacts = contacts
        self.before_symptomatic = -1

    def get_covid(self):
        # change state to infected asymptomatic
        self.state = "asymptomatic"

        # randomly pick int = # of time steps before symptomatic
        self.before_symptomatic = 5

    def get_tested(self):
        if (self.state == "asymptomatic"):
            self.state = "quarantined"

class Graph:
    def __init__(self):
        students = 20
        close = [1, 2]
        tangential = [5, 1]
        # initialize graph
        g_basic = nx.Graph()
        # initialize node infos: dumb! slow!
        people = {}

        for i in range(1, students+1): #for all of the students
            #if they are not already in the graph?
            """
            if i in people:
                #they're someone's close contact already! whose?
                print('already a contact?')
            """
            g_basic.add_node(i) #add them to the networkx graph

            # add contact edges
            # tangential contacts
            t = random.sample(range(1, students+1), tangential[0])

            # close contacts
            c = random.sample(range(1, students+1), close[0])
            #for each of their close contacts, we gotta do something here!

            contacts = [(tangential[1], t), (close[1], c)]
            people[i] = Person(contacts)



        # add edges
        for i in range(1, students+1):
            for pair in people[i].contacts:
                #print(pair)
                risk = pair[0]
                contacts = pair[1]
                for contact in contacts:
                    g_basic.add_edge(i, contact, weight = risk)


        #testing the viewing by giving 5 random people covid
        for i in random.sample(range(1, students+1), 5):
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
