# for testing

import random
from random import choice
import numpy as np
import pandas as pd

from Person import Person
from Graph import Graph

# constants
NUM_STUDENTS = 10
NUM_CLOSE = 2
NUM_TANG = 1
NUM_STUDENTS = 157
NUM_CLOSE = 4
NUM_TANG = 10
PROB_CLOSE = .174
PROB_TANG = .031
MEAN_SYMPTOMATIC = 6
STANDARD_DEV_SYMPTOMATIC = 1.2


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

print(len(social_graph.ids_dict))


# create graph with random close + tang contacts
random_graph = Graph({})
random_graph.add_contacts(NUM_CLOSE, PROB_CLOSE, NUM_STUDENTS)
random_graph.add_contacts(NUM_TANG, PROB_TANG, NUM_STUDENTS)
random_graph.ids_dict[1].get_covid(MEAN_SYMPTOMATIC, STANDARD_DEV_SYMPTOMATIC)  # give one person covid
random_graph.ids_dict[1].patient_zero = True

"""
# one week
for i in range(7):
    # random_graph.graph_spread(MEAN_SYMPTOMATIC, STANDARD_DEV_SYMPTOMATIC)
    social_graph.graph_spread(mean_symptomatic, standard_dev_symptomatic)

    people_to_test = random.sample(list(range(1, students)), round(students / 21))

    # random_graph.dynamic_test(people_to_test)
    social_graph.dynamic_test(people_to_test)

# random_graph.show_graph(PROB_CLOSE, PROB_TANG)
# random_graph.print_stats()
# random_graph.print_contacts_info()
"""

#social_graph.show_graph(PROB_CLOSE, PROB_TANG) #we don't want to use nx in the back end
#social_graph.print_stats()
social_graph.print_contacts_info()
