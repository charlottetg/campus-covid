# for testing

import random
import pandas as pd
import networkx as nx
from copy import deepcopy
import numpy as np

from Person import Person
from Graph import Graph

# var
num_students = 20
num_close = 4
num_tang = 10

#constants
PROB_CLOSE = .174
PROB_TANG = .031
MEAN_SYMPTOMATIC = 4.98
STANDARD_DEV_SYMPTOMATIC = 4.83

# build social_graph from Dash data
"""
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
"""

# create graph with randomly assigned (mutual) close and tang contacts
random_graph = Graph({})
random_graph.add_contacts(num_close, PROB_CLOSE, num_students)
random_graph.add_contacts(num_tang, PROB_TANG, num_students)
random_graph.ids_dict[1].get_covid(MEAN_SYMPTOMATIC, STANDARD_DEV_SYMPTOMATIC)  # give one person covid
random_graph.ids_dict[1].patient_zero = True
random_pos = nx.spring_layout(random_graph.networkx_graph())


def run_simulation(graph, num_runs, days, fraction_tested_per_day, mean_symptomatic, standard_dev_symptomatic, all_contacts):
    """
    Runs a simulated spread, returns [graphs, healthy, asymptomatic, quarantined]
    graphs is array of networkx graphs for each day of the simulation *for the first run*
    note: all_contacts is a Boolean
    """

    # dimensions of these will be (num_rows, days)
    healthy = []
    asymptomatic = []
    quarantined = []

    # this will be a 1D array
    graphs = []

    for i in range(num_runs):
        current_run_graph = deepcopy(graph)

        # 1D arrays of length j
        current_healthy = [num_students-1]
        current_asymptomatic = [1]
        current_quarantined = [0]

        for j in range(days):
            current_run_graph.graph_spread(mean_symptomatic, standard_dev_symptomatic)
            people_to_test = random.sample(list(range(1, num_students)), round(num_students / fraction_tested_per_day))
            current_run_graph.dynamic_test(people_to_test, all_contacts, PROB_CLOSE)

            current_healthy.append(current_run_graph.num_healthy())
            current_asymptomatic.append(current_run_graph.num_asymptomatic())
            current_quarantined.append(current_run_graph.num_quarantined())

            if i == 0: # only save first run graphs
                current_day_graph = deepcopy(current_run_graph).networkx_graph() # want as a networkx graph
                graphs.append(current_day_graph) # kind of weird, but works!

        healthy.append(current_healthy)
        asymptomatic.append(current_asymptomatic)
        quarantined.append(current_quarantined)

    return graphs, healthy, asymptomatic, quarantined


def get_stats(healthy, asymptomatic, quarantined):
    """
    Takes in healthy, asymptomatic, quarantined from run_simulation
    return np arrays: graph stats is stats of [healthy, asymptomatic, quarantined] from first run
    """

    graph_stats = np.array([healthy[0], asymptomatic[0], quarantined[0]]) # stats for the first run (that we save the graphs for)
    average_stats = [np.mean(np.array(healthy), axis=0), np.mean(np.array(asymptomatic), axis=0), np.mean(np.array(quarantined), axis=0)]
    standard_devs = [np.std(np.array(healthy), axis=0), np.std(np.array(asymptomatic), axis=0), np.std(np.array(quarantined), axis=0)]

    return graph_stats, average_stats, standard_devs


results = run_simulation(random_graph, 2, 3, 21, MEAN_SYMPTOMATIC, STANDARD_DEV_SYMPTOMATIC, False)
graphs = results[0]
healthy = results[1]
asymptomatic = results[2]
quarantined = results[3]

print(np.array(healthy))
print(np.array(asymptomatic))
print(np.array(quarantined))

stats = get_stats(healthy, asymptomatic, quarantined)
graph_stats = stats[0]
average_stats = stats[1]
standard_devs = stats[2]

print(graph_stats)
print(average_stats)
print(standard_devs)
