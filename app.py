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


#constants
PROB_CLOSE = .174
PROB_TANG = .031
MEAN_SYMPTOMATIC = 4.98
STANDARD_DEV_SYMPTOMATIC = 4.83

# def single_simulation(graph, fraction_tested_per_day):
#     """
#     runs a simulated spread on :param graph:. tests according to :param fraction_tested_per_day:.
#     :return: days.
#     days[i] is a set of the info you need for day i. it includes:
#         - people: [covid, quarantined, safe] lists of their ids.
#         - log: array of strings that reflect covid trasmissions
#
#     This is for DRAWING the simulation in a way that is informative. This is not for the cumulative averaging type stuff.
#     Edges from people with covid to their contacts will be colored reddish, showing the people that are at risk.
#     """
#     #day zero: everyone is safe.
#     #day one: person has covid. 1 person should have covid, their contacts get marked at_risk.
#     for j in range(10):
#         graph.graph_spread(MEAN_SYMPTOMATIC, STANDARD_DEV_SYMPTOMATIC)
#
#         current_run_graph.graph_spread(mean_symptomatic, standard_dev_symptomatic)
#         people_to_test = random.sample(list(range(1, num_students)), round(num_students / fraction_tested_per_day))
#         current_run_graph.dynamic_test(people_to_test, all_contacts, PROB_CLOSE)
#
#         current_healthy.append(current_run_graph.num_healthy())
#         current_asymptomatic.append(current_run_graph.num_asymptomatic())
#         current_quarantined.append(current_run_graph.num_quarantined())

def run_simulation(graph, num_runs, days, fraction_tested_per_day, mean_symptomatic, standard_dev_symptomatic, all_contacts, num_students=20):
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
    graphs = [graph]

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
    #
    # a simulation consists of:
    #        -   a set of relationships within the graph
    #        -   a set of peoples statuses for each day
    # so maybe we want a set of simulations?


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
def formpage():
    return render_template("form.html")

@app.route("/action_page.php")
def takingformdata():
    num_tang = int(request.args.get('t'))
    num_close = int(request.args.get('c'))
    num_students = int(request.args.get('s'))

    campus = Graph({}) #campus object
    campus.add_contacts(num_close, PROB_CLOSE, num_students)
    campus.add_contacts(num_tang, PROB_TANG, num_students)

    net = Network().from_nx(campus.networkx_graph()) #pyvis Network version of the campus with no info on who has covid or not
    net.save_graph("templates/campus.html")
    return render_template('campus.html') #if we had an array with the list of everyone daily statuses, we could

    campus.ids_dict[1].get_covid(MEAN_SYMPTOMATIC, STANDARD_DEV_SYMPTOMATIC)  # give one person covid
    campus.ids_dict[1].patient_zero = True
    random_pos = nx.spring_layout(campus.networkx_graph())

    results = run_simulation(campus, 2, 3, 21, MEAN_SYMPTOMATIC, STANDARD_DEV_SYMPTOMATIC, False, num_students)
    """
    for i in range(4):
        net = Network()
        net.from_nx(results[0][i])
        address = "templates/"+str(i)+".html"
        net.write_html(address)
        """
    return render_template('singlesimulation.html')
    #so now, for each graph what do we do?
    #each of the graphs wil


@app.route("/<template>")
def templatedebug(template):
    return render_template(template+'.html')


if __name__ == "__main__":
    app.run(debug=True)
