"""
Anna Spiro and Charlotte Gray
Main: used for testing and data analysis
"""

from Person import Person
from Graph import Graph

import random
import pandas as pd
import networkx as nx
from copy import deepcopy
import numpy as np

# variables
num_students = 2275
num_close = 4
num_tang = 5

#constants
PROB_CLOSE = .174
PROB_TANG = .031
MEAN_SYMPTOMATIC = 4.98
STANDARD_DEV_SYMPTOMATIC = 4.83

# build social_graph from Prof. Dash NSCI 0401 social network data (for comparison)
social_ids_dict = {}
df = pd.read_excel('anonymous_classnetwork.xlsx')

for index, row in df.iterrows():

    if not pd.isnull(row[0]):

        current_id = int(row[0])

        if current_id not in social_ids_dict.keys():
            social_ids_dict[current_id] = Person({})

        for j in range(1, len(row)):

            if not pd.isnull(row[j]):

                contact_id = int(row[j])

                if contact_id not in social_ids_dict[
                    current_id].contacts.keys():  # not already a contact (repeats?)
                    social_ids_dict[current_id].contacts[contact_id] = PROB_CLOSE  # add contact

                if contact_id not in social_ids_dict.keys():  # initialize
                    social_ids_dict[contact_id] = Person({})

                if current_id not in social_ids_dict[contact_id].contacts.keys():
                    social_ids_dict[contact_id].contacts[current_id] = PROB_CLOSE

social_graph = Graph(social_ids_dict)
social_graph.ids_dict[1].get_covid(MEAN_SYMPTOMATIC, STANDARD_DEV_SYMPTOMATIC)  # give one person covid
social_graph.ids_dict[1].patient_zero = True
social_pos = nx.spring_layout(social_graph.networkx_graph())



def get_stats(healthy, asymptomatic, quarantined):
    """
    Takes in healthy, asymptomatic, quarantined from run_simulation
    return np arrays: graph stats is stats of [healthy, asymptomatic, quarantined] from first run
    """

    graph_stats = np.array([healthy[0], asymptomatic[0], quarantined[0]]) # stats for the first run (that we save the graphs for)
    average_stats = [np.mean(np.array(healthy), axis=0), np.mean(np.array(asymptomatic), axis=0), np.mean(np.array(quarantined), axis=0)]
    standard_devs = [np.std(np.array(healthy), axis=0), np.std(np.array(asymptomatic), axis=0), np.std(np.array(quarantined), axis=0)]

    return graph_stats, average_stats, standard_devs


days = 7
runs = 1000
fraction_tested_per_day = 21
results = run_simulation(random_graph, runs, days, fraction_tested_per_day, MEAN_SYMPTOMATIC, STANDARD_DEV_SYMPTOMATIC, False)

graphs = results[0]
first_graph = graphs[0]
last_graph = graphs[days]
first_graph.show_graph(PROB_CLOSE, PROB_TANG, random_pos)
last_graph.show_graph(PROB_CLOSE, PROB_TANG, random_pos)

healthy = results[1]
asymptomatic = results[2]
quarantined = results[3]

np.savetxt('full_healthy.csv', np.array(healthy), delimiter=',')
np.savetxt('full_asymptomatic.csv', np.array(asymptomatic), delimiter=',')
np.savetxt('full_quarantined.csv', np.array(quarantined), delimiter=',')

stats = get_stats(healthy, asymptomatic, quarantined)
graph_stats = stats[0]
average_stats = stats[1]
standard_devs = stats[2]

np.savetxt('graph_stats.csv', graph_stats, delimiter=',')
np.savetxt('average_stats.csv', average_stats, delimiter=',')
np.savetxt('standard_devs.csv', standard_devs, delimiter=',')
