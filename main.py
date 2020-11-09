
import random


from Person import Person
from Graph import Graph

# graph constants
NUM_STUDENTS = 10
NUM_CLOSE = 1
NUM_TANG = 2
PROB_CLOSE = .174
PROB_TANG = .031


# build a people map
adjacency_list = {}

# create a new person object, add it to adjacency_list (associated with ID)
for i in range(1, NUM_STUDENTS+1): #for all of the students

    relationships = []

    # can eventually exclude i
    total_contacts = random.sample(range(1, NUM_STUDENTS+1), NUM_TANG + NUM_CLOSE)

    for j in range(NUM_TANG + NUM_CLOSE):
        if (j < NUM_CLOSE): # first add close contacts
            relationships.append([total_contacts[j], PROB_CLOSE])
        else:
            relationships.append([total_contacts[j], PROB_TANG])

    adjacency_list[i] = Person(relationships)

adjacency_list[1].get_covid() # give one person covid
adjacency_list[1].patient_zero = True

# create graph instance
graph = Graph(adjacency_list)


for i in range(7):
    graph.graph_spread()
    graph.dynamic_test([random.randint(1,NUM_STUDENTS)])

graph.print_stats()
graph.show_graph()
