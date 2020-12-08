"""
Anna Spiro and Charlotte Gray
"""
import requests
from flask import Flask, request, jsonify, render_template
import numpy as np
from Graph import Graph
from copy import deepcopy
import pandas as pd
import random
from pyvis.network import Network
import networkx as nx
app = Flask(__name__)

#constants
PROB_CLOSE = .174
PROB_TANG = .031
MEAN_SYMPTOMATIC = 4.98
STANDARD_DEV_SYMPTOMATIC = 4.83

def single_simulation(campus, id, tests):
    """
    :param graph: campus!
    :param id: id of person to get first covid
    :return: [array of pyvis networks, array of logs]
    """
    students = len(campus.ids_dict)
    networks = []
    networks.append(campus.pyvis_graph())

    d = 1
    campus.ids_dict[1].get_covid(MEAN_SYMPTOMATIC, STANDARD_DEV_SYMPTOMATIC)  # give one person covid
    networks.append(campus.pyvis_graph())
    asymptomatic = campus.asymptomatic()
    quarantined = campus.quarantined()

    while campus.num_asymptomatic()>0:
        d +=1
        asymptomatic += campus.asymptomatic()
        quarantined += campus.quarantined()
        campus.graph_spread(MEAN_SYMPTOMATIC, STANDARD_DEV_SYMPTOMATIC)
        people_to_test = random.sample(list(range(1, students)), tests)
        campus.dynamic_test(people_to_test, False, PROB_CLOSE)
        networks.append(campus.pyvis_graph())

    asymptomatic = np.unique(asymptomatic)
    quarantined = np.unique(quarantined)
    summary = "This outbreak, from the first case to the final case being caught, lasted a total of " + str(d) + " days. Over the course of the outbreak, the college administered "
    summary += "T"
    summary += " tests. " + str(len(asymptomatic)) + " out of " + str(students) + " students contracted covid during the outbreak. " + str(len(quarantined)) + " students had to quarantine at some point during the oubreak. That makes for a total of " + str(7*len(quarantined)) + " days spent in quarantine by students."

    """
    net.save_graph("templates/campus.html")
    return render_template('campus.html')
    """
    for i in range(0, len(networks)):
        networks[i].save_graph("static/"+ str(i)+".html")
    return render_template("singlesimulation.html", story=summary, clogs=campus.log_arrays(), t=d, networks=networks)

def run_simulation(graph, num_runs, days, daily_tests, all_contacts):
    """
    Runs multiple iterations of a simulated spread, returns [healthy, asymptomatic, quarantined]
    note: all_contacts is a Boolean
    """
    num_students = len(graph.ids_dict)
    # dimensions of these will be (num_rows, days)
    healthy = []
    asymptomatic = []
    quarantined = []

    for i in range(num_runs):
        current_run_graph = deepcopy(graph)

        # 1D arrays of length j
        current_healthy = [num_students-1]
        current_asymptomatic = [1]
        current_quarantined = [0]

        for j in range(days):
            current_run_graph.graph_spread(MEAN_SYMPTOMATIC, STANDARD_DEV_SYMPTOMATIC)
            people_to_test = random.sample(list(range(1, num_students)), daily_tests)
            current_run_graph.dynamic_test(people_to_test, all_contacts, PROB_CLOSE)

            current_healthy.append(current_run_graph.num_healthy())
            current_asymptomatic.append(current_run_graph.num_asymptomatic())
            current_quarantined.append(current_run_graph.num_quarantined())

        healthy.append(current_healthy)
        asymptomatic.append(current_asymptomatic)
        quarantined.append(current_quarantined)

    return {"healthy stats:":healthy, "asymptomatic stats:":asymptomatic, "quarantined stats (grouped by day and run):":quarantined}


def get_stats(healthy, asymptomatic, quarantined):
    """
    Takes in healthy, asymptomatic, quarantined (all run data) from run_simulation
    return np arrays: graph stats is stats of [healthy, asymptomatic, quarantined] from first run
    """

    graph_stats = np.array([healthy[0], asymptomatic[0], quarantined[0]]) # stats for the first run (that we save the graphs for)
    average_stats = [np.mean(np.array(healthy), axis=0), np.mean(np.array(asymptomatic), axis=0), np.mean(np.array(quarantined), axis=0)]
    standard_devs = [np.std(np.array(healthy), axis=0), np.std(np.array(asymptomatic), axis=0), np.std(np.array(quarantined), axis=0)]

    return graph_stats, average_stats, standard_devs


@app.route('/', methods=['GET', 'POST']) #credit to www.realpython.com tutorial for http routing in python
def home():
    errors = []
    results = {}
    if request.method == "POST":
        try:
            url = request.form['url'] #url the user entered
            r = requests.get(url)
            print(r.text)
        except:
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )
    return render_template('form.html', errors=errors, results=results)


@app.route("/action_page.php")
def takingformdata():
    num_tang = int(request.args.get('t'))
    num_close = int(request.args.get('c'))
    num_students = int(request.args.get('s'))
    tested_daily= int(request.args.get('tests'))
    num_runs = int(request.args.get('mode'))

    campus = Graph({})  # campus object
    campus.add_contacts(num_close, PROB_CLOSE, num_students)
    campus.add_contacts(num_tang, PROB_TANG, num_students)

    if num_runs > 1: #if we're doing multiple simulations and getting aggregate data
        campus.ids_dict[1].get_covid(MEAN_SYMPTOMATIC, STANDARD_DEV_SYMPTOMATIC)  # give one person covid
        campus.ids_dict[1].patient_zero = True
        return jsonify(run_simulation(campus, num_runs, 7, tested_daily, False))

    else:
        return single_simulation(campus, 1, tested_daily)



@app.route('/<day>', methods=['GET'])
def uglytemplateday(day):
    if request.method == "GET":
            return render_template(day+'.html')


if __name__ == "__main__":
    app.run(debug=True)
