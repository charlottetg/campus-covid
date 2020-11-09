from flask import Flask, request, jsonify
from Person import Person
from Graph import Graph
import random
app = Flask(__name__)

@app.route("/<id>")
def persondata(id):
    iid = int(id)
    p = Person([[iid, 0],[iid, -1],[2,.5],[3,.5]])
    if (p.state==-1):
        return "person " + id + " is healthy!"
    else:
        return jsonify(p.contacts)

@app.route("/")
def testing():
    g = working_graph_creator(10, 1, 2, .174, .031)
    gstatus = {}
    for k in g.adjacency_list:
        gstatus[k] = g.adjacency_list[k].state
    return jsonify(gstatus)

@app.route("/<day>")
def time(day):
    return "it is now day: " + day


def working_graph_creator(students, close, tang, prob_close, prob_tang):
    # build a people map
    adjacency_list = {}

    # create a new person object, add it to adjacency_list (associated with ID)
    for i in range(1, students + 1):  # for all of the students

        relationships = []

        # can eventually exclude i
        total_contacts = random.sample(range(1, students + 1), tang + close)

        for j in range(tang + close):
            if (j < close):  # first add close contacts
                relationships.append([total_contacts[j], prob_close])
            else:
                relationships.append([total_contacts[j], prob_tang])

        adjacency_list[i] = Person(relationships)

    adjacency_list[1].get_covid()  # give one person covid
    adjacency_list[1].patient_zero = True

    # create graph instance
    return Graph(adjacency_list)




if __name__ == "__main__":
    app.run(debug=True)