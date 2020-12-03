from flask import Flask, request, jsonify, render_template
from Person import Person
from Graph import Graph
from copy import deepcopy
import pandas as pd
import random
from pyvis.network import Network
import networkx as nx
app = Flask(__name__)

# var
num_students = 20
num_close = 4
num_tang = 10

#constants
PROB_CLOSE = .174
PROB_TANG = .031
MEAN_SYMPTOMATIC = 4.98
STANDARD_DEV_SYMPTOMATIC = 4.83

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


@app.route("/")
def simulationsetup():


    random_graph = Graph({})
    random_graph.add_contacts(num_close, PROB_CLOSE, num_students)
    random_graph.add_contacts(num_tang, PROB_TANG, num_students)
    random_graph.ids_dict[1].get_covid(MEAN_SYMPTOMATIC, STANDARD_DEV_SYMPTOMATIC)  # give one person covid
    random_graph.ids_dict[1].patient_zero = True
    random_pos = nx.spring_layout(random_graph.networkx_graph())


    results = run_simulation(random_graph, 2, 3, 21, MEAN_SYMPTOMATIC, STANDARD_DEV_SYMPTOMATIC, False)
    #now we have pathways to get to different days?

    #user input tells us which day(results, __) to return
    return day(results, 1)

def day(results, i):
    daygraph = Network()
    daygraph.from_nx(results[0][i])
    daygraph.show("templates/"+str(i) + ".html")
    return render_template(str(i)+".html")

"""
@app.route("/<id>")
def persondata(id):
    iid = int(id)
    p = Person([[iid, 0],[iid, -1],[2,.5],[3,.5]])
    if (p.state==-1):
        return "person " + id + " is healthy!"
    else:
        return jsonify(p.contacts)

@app.route("/<day>")
def time(day):
    return "it is now day: " + day

"""


if __name__ == "__main__":
    app.run(debug=True)
