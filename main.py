# for testing

import random
import pandas as pd
import networkx as nx
from copy import deepcopy

from Person import Person
from Graph import Graph

# var
num_students = 20
num_close = 4
num_tang = 10

#constants
PROB_CLOSE = .174
PROB_TANG = .031
MEAN_SYMPTOMATIC = 6
STANDARD_DEV_SYMPTOMATIC = 1.2

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
    Runs a simulated spread, returns [graphs, single_stats, average_stats]
    graphs is array of networkx graphs for each day of the simulation *for the first run*
    single_stats is a 2D array of population [healthy, asymptomatic, quarantined] for each day *for the first run*
    average_stats is a 2D array of population [healthy, asymptomatic, quarantined] for each day *on average*

    note: all_contacts is a Boolean
    """

    healthy = [0] * days
    asymptomatic = [0] * days
    quarantined = [0] * days

    graphs = []

    for i in range(num_runs):
        current_run_graph = deepcopy(graph)

        for j in range(days):
            current_run_graph.graph_spread(mean_symptomatic, standard_dev_symptomatic)
            people_to_test = random.sample(list(range(1, num_students)), round(num_students / fraction_tested_per_day))
            current_run_graph.dynamic_test(people_to_test, all_contacts, PROB_CLOSE)

            healthy[j] += current_run_graph.num_healthy()
            asymptomatic[j] += current_run_graph.num_asymptomatic()
            quarantined[j] += current_run_graph.num_quarantined()

            if i == 0: # only save first run graphs
                current_day_graph = deepcopy(current_run_graph).networkx_graph() # want as a networkx graph
                graphs.append(current_day_graph) # kind of weird, but works!

                if j == days - 1: # last day of first run, save single_stats
                    single_stats = deepcopy([healthy, asymptomatic, quarantined])

    averaged_healthy = [ x / num_runs for x in healthy]
    averaged_asymptomatic = [ x / num_runs for x in asymptomatic]
    averaged_quarantined = [ x / num_runs for x in quarantined]

    average_stats = [averaged_healthy, averaged_asymptomatic, averaged_quarantined]

    return graphs, single_stats, average_stats


results = run_simulation(random_graph, 2, 3, 20, MEAN_SYMPTOMATIC, STANDARD_DEV_SYMPTOMATIC, False)
graphs = results[0]
single_stats = results[1]
average_stats = results[2]

"""
for graph in graphs:
    graph.print_stats()
"""

print("single stats = " + str(single_stats))
print("average stats = " + str(average_stats))
