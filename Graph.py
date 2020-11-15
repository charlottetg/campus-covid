import networkx as nx
import matplotlib.pyplot as plt
import scipy
import random
from Person import Person
from random import choice
import numpy as np
import math as math

class Graph:

    def __init__(self, ids_dict):
        self.ids_dict = ids_dict
        self.day = 0

    # used to be in show_graph
    def networkx_graph(self):
        ids_dict = self.ids_dict
        g = nx.Graph()
        people_map = self.ids_dict
        people_ids = people_map.keys()

        # nodes
        labels = {}
        for person_id in people_ids:
            g.add_node(person_id)
            labels[person_id] = person_id # this is silly, take out later

        # edges
        for person_id in people_ids:
            current_contacts = people_map[person_id].contacts
            for contact in current_contacts:
                g.add_edge(person_id, contact, weight = current_contacts[contact])
        return g


    # display graph using networkx
    # g is networkx graph
    def show_graph(self, prob_close, prob_tang, g, pos):

        people_map = self.ids_dict

        healthy = [person_id for person_id in g.nodes() if people_map[person_id].state == -1]
        asymptomatic = [person_id for person_id in g.nodes() if people_map[person_id].state >= 0]
        quarantined = [person_id for person_id in g.nodes() if people_map[person_id].state == -2]
        patient_zero = [ person_id for person_id in g.nodes() if people_map[person_id].patient_zero]

        # nodes
        nx.draw_networkx_nodes(g, pos, nodelist= healthy, node_size=20, node_color="green")
        nx.draw_networkx_nodes(g, pos, nodelist= asymptomatic, node_size=20, node_color="red")
        nx.draw_networkx_nodes(g, pos, nodelist= patient_zero, node_size=20, node_color="purple")
        nx.draw_networkx_nodes(g, pos, nodelist= quarantined, node_size=20, node_color="blue")

        # labels
        #nx.draw_networkx_labels(g, pos, labels, font_size = 16)

        # make edges (something up here)
        close_contacts = [(u, v) for (u, v, d) in g.edges(data=True) if d["weight"] == prob_close]
        tang_contacts = [(u, v) for (u, v, d) in g.edges(data=True) if d["weight"] == prob_tang]
        dangerous_contacts = [(u, v) for (u, v, d) in g.edges(data=True) if people_map[u].state >= 0 or people_map[v].state >= 0]

        # draw edges
        #nx.draw_networkx_edges(g, pos, edgelist= tang_contacts, width=.5)
        #nx.draw_networkx_edges(g, pos, edgelist= close_contacts, width=1)
        #nx.draw_networkx_edges(g, pos, edgelist = dangerous_contacts, width=1, edge_color="red")

        plt.show()



    # to be called on self and an asymptomatic person: probabalistically gives covid to their contacts
    def individual_spread(self, spreader_id, mean_symptomatic, standard_dev_symptomatic):
        contacts = self.ids_dict[spreader_id].contacts
        for person_id in contacts:
            if self.ids_dict[person_id].state == -1: # healthy, susceptible
                transmission_prob = contacts[person_id]

                # if edge is traveled
                if random.choices([True, False], weights = [transmission_prob, (1 - transmission_prob)])[0]: # returns a list with one element
                    self.ids_dict[person_id].get_covid(mean_symptomatic, standard_dev_symptomatic)
                    print(str(person_id) + " got covid from " + str(spreader_id))


    # what happens to the graph every time step
    def graph_spread(self, mean_symptomatic, standard_dev_symptomatic):

        print("day " + str(self.day))
        # make a list of people ids who start off asymptomatic
        current_spreaders = []
        for person_id in self.ids_dict:
            if self.ids_dict[person_id].state >= 0: # asymptomatic
                self.ids_dict[person_id].state -= 1 # decrease by 1
                current_spreaders.append(person_id)

            if self.ids_dict[person_id].state == 0: # now showing symptoms
                self.ids_dict[person_id].state = -2 # quarantine (still spread this time step, but not after)
                print(str(person_id) + " showed symptoms and quarantined")

        for spreader in current_spreaders:
            self.individual_spread(spreader, mean_symptomatic, standard_dev_symptomatic)

        # keep track of day
        self.day += 1

    # for testing
    def print_contacts_info(self):
        people_map = self.ids_dict
        people_ids = people_map.keys()

        for person_id in self.ids_dict.keys():
            print("person " + str(person_id) + " :" + str(self.ids_dict[person_id].contacts))


    # also for testing (redundant with next functions)
    def print_stats(self):
        healthy = [person_id for person_id in self.ids_dict.keys() if self.ids_dict[person_id].state == -1]
        asymptomatic = [person_id for person_id in self.ids_dict.keys() if self.ids_dict[person_id].state >= 0]
        quarantined = [person_id for person_id in self.ids_dict.keys() if self.ids_dict[person_id].state == -2]

        print("day " + str(self.day))
        print("healthy: " + str(len(healthy)))
        print("asymptomatic: " + str(len(asymptomatic)))
        print("quarantined: " + str(len(quarantined)))
        print("\n")


    def num_healthy(self):
        return len([person_id for person_id in self.ids_dict.keys() if self.ids_dict[person_id].state == -1])

    def num_asymptomatic(self):
        return len([person_id for person_id in self.ids_dict.keys() if self.ids_dict[person_id].state >= 0])

    def num_quarantined(self):
        return len([person_id for person_id in self.ids_dict.keys() if self.ids_dict[person_id].state == -2])


    # dynamic test a list of people_ids
    def dynamic_test(self, ids_to_test):
        for id in ids_to_test:
            person = self.ids_dict[id]
            if person.get_tested():
                print(str(id) + " tested positive and quarantined")
            else:
                print(str(id) + " tested negative")

    def add_contacts(self, num_contacts, prob_contacts, num_students):

        ids_dict = self.ids_dict
        num_chosen = {}  # keep track of how many added for each students (needed?)
        at_contacts_max = set()

        for i in range(1, num_students + 1):  # for all of the students

            if i not in ids_dict.keys():
                ids_dict[i] = Person(
                    {})  # initialize person object with empty contacts (unless they've already been initialized)

            if i not in num_chosen.keys():
                num_chosen[i] = 0

            # don't choose yourself, don't add someone if they're already a contact, don't choose someone who already has max num contacts
            contact_options = set(range(1, num_students + 1)) - {i} - set(ids_dict[i].contacts.keys()) - at_contacts_max
            contacts_remaining = num_contacts - num_chosen[i]  # how many still left to choose

            if contacts_remaining > 0:

                if len(
                        contact_options) < contacts_remaining:  # math doesn't work out, but still need to add more contacts!
                    all_contact_options = set(range(1, num_students + 1)) - {i} - set(ids_dict[i].contacts.keys())
                    chosen_contacts = random.sample(list(all_contact_options), contacts_remaining)

                else:
                    chosen_contacts = random.sample(list(contact_options), contacts_remaining)  # choose contacts

                num_chosen[i] += contacts_remaining  # increment count for i

                # add contact and probability for current person
                # also make current person the contact of all chosen contacts
                # check if either current person or contact now have max number of contacts
                for contact in chosen_contacts:
                    ids_dict[i].contacts[contact] = prob_contacts

                    if num_chosen[i] == num_contacts:  # at max
                        at_contacts_max.add(i)

                    if contact not in ids_dict.keys():  # need to intialize new contact as their own person
                        ids_dict[contact] = Person({})

                    if contact not in num_chosen.keys():
                        num_chosen[contact] = 0

                    ids_dict[contact].contacts[i] = prob_contacts  # so that contacts are mutual
                    num_chosen[contact] += 1  # increment count for contact

                    if num_chosen[i] == num_contacts:  # at max
                        at_contacts_max.add(contact)
