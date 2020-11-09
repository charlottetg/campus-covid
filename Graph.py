import networkx as nx
import matplotlib.pyplot as plt
import scipy
import random
from random import choice
import numpy as np
import math as math

class Graph:

    def __init__(self, adjacency_list):
        self.adjacency_list = adjacency_list
        self.day = 0


    # display graph using networkx
    def show_graph(self):

        # eventually take these out
        PROB_CLOSE = .174
        PROB_TANG = .031

        g = nx.Graph()
        people_map = self.adjacency_list
        people_ids = people_map.keys()

        # nodes
        labels = {}
        for person_id in people_ids:
            g.add_node(person_id)
            labels[person_id] = person_id # this is silly, take out later

        # edges
        for person_id in people_ids:
            for contact in people_map[person_id].contacts:
                g.add_edge(person_id, contact[0], weight = contact[1])

        healthy = [person_id for person_id in g.nodes() if people_map[person_id].state == -1]
        asymptomatic = [person_id for person_id in g.nodes() if people_map[person_id].state >= 0]
        quarantined = [person_id for person_id in g.nodes() if people_map[person_id].state == -2]
        patient_zero = [ person_id for person_id in g.nodes() if people_map[person_id].patient_zero]

        pos = nx.circular_layout(g)  # positions for all nodes

        # nodes
        nx.draw_networkx_nodes(g, pos, nodelist= healthy, node_size=250, node_color="green")
        nx.draw_networkx_nodes(g, pos, nodelist= asymptomatic, node_size=250, node_color="red")
        nx.draw_networkx_nodes(g, pos, nodelist= patient_zero, node_size=250, node_color="purple")
        nx.draw_networkx_nodes(g, pos, nodelist= quarantined, node_size=250, node_color="blue")

        # labels
        nx.draw_networkx_labels(g, pos, labels, font_size = 16)

        # make edges (something up here)
        close_contacts = [(u, v) for (u, v, d) in g.edges(data=True) if d["weight"] == PROB_CLOSE]
        tang_contacts = [(u, v) for (u, v, d) in g.edges(data=True) if d["weight"] == PROB_TANG]
        dangerous_contacts = [(u, v) for (u, v, d) in g.edges(data=True) if people_map[u].state >= 0 or people_map[v].state >= 0]

        # draw edges
        nx.draw_networkx_edges(g, pos, edgelist= tang_contacts, width=1)
        nx.draw_networkx_edges(g, pos, edgelist= close_contacts, width=2)
        nx.draw_networkx_edges(g, pos, edgelist = dangerous_contacts, width=1, edge_color="red")

        plt.show()


    # to be called on self and an asymptomatic person: probabalistically gives covid to their contacts
    def individual_spread(self, spreader_id):
        for contact in self.adjacency_list[spreader_id].contacts:
            if self.adjacency_list[contact[0]].state == -1: # healthy, susceptible
                transmission_prob = contact[1]

                # if edge is traveled
                if random.choices([True, False], weights = [transmission_prob, (1 - transmission_prob)])[0]: # returns a list with one element
                    self.adjacency_list[contact[0]].get_covid()
                    print(str(contact[0]) + " got covid from " + str(spreader_id))


    # what happens to the graph every time step
    def graph_spread(self):

        print("day " + str(self.day))
        # make a list of people ids who start off asymptomatic
        current_spreaders = []
        for person_id in self.adjacency_list.keys():
            if self.adjacency_list[person_id].state >= 0: # asymptomatic
                self.adjacency_list[person_id].state -= 1 # decrease by 1
                current_spreaders.append(person_id)

            if self.adjacency_list[person_id].state == 0: # now showing symptoms
                self.adjacency_list[person_id].state = -2 # quarantine (still spread this time step, but not after)
                print(str(person_id) + " showed symptoms and quarantined")

        for spreader in current_spreaders:
            self.individual_spread(spreader)

        # keep track of day
        self.day += 1

    # for testing
    def print_contacts_info(self):
        people_map = self.adjacency_list
        people_ids = people_map.keys()

        for person_id in self.adjacency_list.keys():
            print("person " + str(person_id) + " :" + str(self.adjacency_list[person_id].contacts))


    # also for testing (redundant with next functions)
    def print_stats(self):
        healthy = [person_id for person_id in self.adjacency_list.keys() if self.adjacency_list[person_id].state == -1]
        asymptomatic = [person_id for person_id in self.adjacency_list.keys() if self.adjacency_list[person_id].state >= 0]
        quarantined = [person_id for person_id in self.adjacency_list.keys() if self.adjacency_list[person_id].state == -2]

        print("day " + str(self.day))
        print("healthy: " + str(len(healthy)))
        print("asymptomatic: " + str(len(asymptomatic)))
        print("quarantined: " + str(len(quarantined)))
        print("\n")


    def num_healthy(self):
        return len([person_id for person_id in self.adjacency_list.keys() if self.adjacency_list[person_id].state == -1])

    def num_asymptomatic(self):
        return len([person_id for person_id in self.adjacency_list.keys() if self.adjacency_list[person_id].state >= 0])

    def num_quarantined(self):
        return len([person_id for person_id in self.adjacency_list.keys() if self.adjacency_list[person_id].state == -2])


    # dynamic test a list of people_ids
    def dynamic_test(self, ids_to_test):
        for id in ids_to_test:
            person = self.adjacency_list[id]
            if person.get_tested():
                print(str(id) + " tested positive and quarantined")
            else:
                print(str(id) + " tested negative")
