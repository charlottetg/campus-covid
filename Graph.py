"""
Anna Spiro and Charlotte Gray
Graph Class
"""

from Person import Person
import networkx as nx
import matplotlib.pyplot as plt
import scipy
import random
from random import choice
import numpy as np
import math as math

class Graph:
    """
    A class used to represent a graph of Person objects.
    Attributes
    __________
    ids_dict: dict
        contains people's IDs as (integer) keys and the associated Person objects as values
    day: int
        represents the number of days since the first COVID-19 case
    log: list
        list of strings that are a written description of what has happened to Person objects in the graph throughout the COVID-19 spread
    Methods
    _______
    networkx_graph
        Return a Networkx graph of the given Graph Object.
    show_graph
        Display a Networkx graph with node and edge colors representing COVID-19 states and edge weights representing contact types.
    individual_spread
        Probabalistically spreads COVID-19 from an asymptomatic person to their contacts.
    graph_spread
        To be called on a Graph every time step: increment day and spread covid from infected individuals.
    num_healthy
        Return number of healthy Person objects in a graph.
    num_asymptomatic
        Return number of asymptomatic Person objects in a graph.
    num_quarantined
        Return number of quarantined Person objects in a graph.
    dynamic_test
        Test a list of Person IDs, contact trace if a positive case is found.
    add_contacts
        Add contacts with a given probabilty to Person objects in Graph such that contacts are mutual.
    print_contacts_info
        For testing purposes: print contact information.
    print_stats
        For testing purposes: print Graph stats.
    """

    def __init__(self, ids_dict):
        """
        Parameters
        __________
        ids_dict: dict
            contains people's IDs as (integer) keys and the associated Person objects as values
        """
        self.ids_dict = ids_dict
        self.day = 0
        self.log = []

    def networkx_graph(self):
        """ Return a Networkx graph of the given Graph Object.
        """
        g = nx.Graph()
        people_ids = self.ids_dict.keys()

        # add nodes
        for person_id in people_ids:
            g.add_node(person_id)

        # add edges
        for person_id in people_ids:
            current_contacts = self.ids_dict[person_id].contacts
            for contact in current_contacts:
                g.add_edge(person_id, contact, weight = current_contacts[contact])
        return g

    def show_graph(self, prob_close, prob_tang, pos):
        """ Display a Networkx graph with node and edge colors representing COVID-19 states and edge weights representing contact types.
        Parameters
        __________
        prob_close: float
            Transmission probability associated with a close contact
        prob_tang: float
            Transmission probability associated with a tangential contact
        pos: graph layout
            Layout of graph to show
        """

        g = self.networkx_graph()
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

        # edges
        close_contacts = [(u, v) for (u, v, d) in g.edges(data=True) if d["weight"] == prob_close]
        tang_contacts = [(u, v) for (u, v, d) in g.edges(data=True) if d["weight"] == prob_tang]
        dangerous_contacts = [(u, v) for (u, v, d) in g.edges(data=True) if people_map[u].state >= 0 or people_map[v].state >= 0]

        # draw edges
        nx.draw_networkx_edges(g, pos, edgelist= tang_contacts, width=.5)
        nx.draw_networkx_edges(g, pos, edgelist= close_contacts, width=.2)
        nx.draw_networkx_edges(g, pos, edgelist = dangerous_contacts, width=1, edge_color="red")

        plt.show()

    def individual_spread(self, spreader_id, mean_symptomatic, standard_dev_symptomatic):
        """ Probabalistically spreads COVID-19 from an asymptomatic person to their contacts.
        Parameters
        __________
        spreader_id: int
            ID of asymptomatic person
        mean_symptomatic: float
            Mean number of days until an individual becomes symptomatic
        standard_dev_symptomatic: float
            Standard deviation number of days until an individual becomes symptomatic
        """
        contacts = self.ids_dict[spreader_id].contacts
        for person_id in contacts:
            if self.ids_dict[person_id].state == -1: # healthy/susceptible
                transmission_prob = contacts[person_id]

                # if edge is traveled
                if random.choices([True, False], weights = [transmission_prob, (1 - transmission_prob)])[0]:
                    self.ids_dict[person_id].get_covid(mean_symptomatic, standard_dev_symptomatic)
                    self.log.append(str(person_id) + " got covid from " + str(spreader_id))

    def graph_spread(self, mean_symptomatic, standard_dev_symptomatic):
        """To be called on a Graph every time step: increment day and spread covid from infected individuals
        Parameters
        __________
        mean_symptomatic: float
            Mean number of days until an individual becomes symptomatic
        standard_dev_symptomatic: float
            Standard deviation number of days until an individual becomes symptomatic
        """

        self.log.append("day " + str(self.day)) #CAN I DO

        # make a list of IDs who start off asymptomatic
        current_spreaders = []
        for person_id in self.ids_dict:
            if self.ids_dict[person_id].state >= 0: # asymptomatic
                self.ids_dict[person_id].state -= 1 # decrease by 1
                current_spreaders.append(person_id)

            if self.ids_dict[person_id].state == 0: # now showing symptoms
                self.ids_dict[person_id].state = -2 # quarantine (still spread this time step, but not after)
                self.log.append(str(person_id) + " showed symptoms and quarantined")

        for spreader in current_spreaders:
            self.individual_spread(spreader, mean_symptomatic, standard_dev_symptomatic)

        # increment day
        self.day += 1

    def num_healthy(self):
        """Return number of healthy Person objects in a graph.
        """
        return len([person_id for person_id in self.ids_dict.keys() if self.ids_dict[person_id].state == -1])

    def num_asymptomatic(self):
        """Return number of asymptomatic Person objects in a graph.
        """
        return len([person_id for person_id in self.ids_dict.keys() if self.ids_dict[person_id].state >= 0])

    def num_quarantined(self):
        """Return number of quarantined Person objects in a graph.
        """
        return len([person_id for person_id in self.ids_dict.keys() if self.ids_dict[person_id].state == -2])


    def dynamic_test(self, ids_to_test, all_contacts, prob_close):
        """Test a list of people IDs, contact trace if a positive case is found.
        Parameters
        __________
        ids_to_test: list
            list of integers representing IDs to test
        all_contacts: Boolean
            whether to test all contacts or just close contacts: if True, contact trace all contacts
        """
        for id in ids_to_test:
            person = self.ids_dict[id]
            if person.get_tested(): # asymptomatic case found
                self.log.append(str(id) + " tested positive and quarantined")

                for contact_id in person.contacts:
                    if all_contacts: # contact trace tang contacts as well as close contacts
                        if self.ids_dict[contact_id].get_tested(): # tested positive
                            self.log.append(str(contact_id) + " tested positive and quarantined (from contact tracing)")
                        else:
                            self.log.append(str(contact_id) + " tested negative and quarantined (from contact tracing)")
                    else:
                        if person.contacts[contact_id] == prob_close: # only contact trace close contacts
                            if self.ids_dict[contact_id].get_tested(): # tested positive
                                self.log.append(str(contact_id) + " tested positive and quarantined (from contact tracing)")
                            else:
                                self.log.append(str(contact_id) + " tested negative and quarantined (from contact tracing)")
            else:
                self.log.append(str(id) + " tested negative")

    def add_contacts(self, num_contacts, prob_contacts, num_students):
        """Add contacts with a given probabilty to Person objects in Graph such that contacts are mutual.
        Parameters
        __________
        num_contacts: int
            number of contacts (of the given probability) to add for each Person
        prob_contacts: float
            probability (of transmission) of contacts being added
        num_students: int
            total number of students in Graph
        """

        ids_dict = self.ids_dict
        num_chosen = {}  # dictionary to keep track of how many contacts added for each Person
        at_contacts_max = set() # set students with max number of contacts

        for i in range(1, num_students + 1):  # for all students
            if i not in ids_dict.keys():
                ids_dict[i] = Person({})  # initialize person object with empty contacts (unless they've already been initialized)
            if i not in num_chosen.keys():
                num_chosen[i] = 0

            # don't choose yourself, don't add someone if they're already a contact, don't choose someone who already has max num contacts
            contact_options = set(range(1, num_students + 1)) - {i} - set(ids_dict[i].contacts.keys()) - at_contacts_max
            contacts_remaining = num_contacts - num_chosen[i]  # how many contacts still left to choose

            if contacts_remaining > 0:

                if len(contact_options) < contacts_remaining:  # the math doesn't work out, but we still need to add more contacts
                    all_contact_options = set(range(1, num_students + 1)) - {i} - set(ids_dict[i].contacts.keys()) # include students at max contacts
                    chosen_contacts = random.sample(list(all_contact_options), contacts_remaining)

                else:
                    chosen_contacts = random.sample(list(contact_options), contacts_remaining)

                num_chosen[i] += contacts_remaining  # increment count for i

                # add contact with transmission probability for current person
                # make current person the contact of all chosen contacts
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

                    if num_chosen[contact] == num_contacts:  # at max; recently changed from "i" to "contact"
                        at_contacts_max.add(contact)

    def print_contacts_info(self):
        """For testing purposes: print contact information.
        """
        for person_id in self.ids_dict.keys():
            print("person " + str(person_id) + " :" + str(self.ids_dict[person_id].contacts))

    def print_stats(self):
        """For testing purposes: print Graph stats.
        """
        healthy = [person_id for person_id in self.ids_dict.keys() if self.ids_dict[person_id].state == -1]
        asymptomatic = [person_id for person_id in self.ids_dict.keys() if self.ids_dict[person_id].state >= 0]
        quarantined = [person_id for person_id in self.ids_dict.keys() if self.ids_dict[person_id].state == -2]

        print("day " + str(self.day))
        print("healthy: " + str(len(healthy)))
        print("asymptomatic: " + str(len(asymptomatic)))
        print("quarantined: " + str(len(quarantined)))
        print("\n")
