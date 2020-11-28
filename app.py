from flask import Flask, request, jsonify, render_template
from Person import Person
from Graph import Graph
import pandas as pd
import random
from pyvis.network import Network
app = Flask(__name__)


@app.route("/<day>")
def testofPyvis(day):
    g = Network()
    g.add_node(0, label="0")
    for i in range(1, int(day)):
        g.add_node(i, label=str(i))
        g.add_edge(i, i-1)
        #g.add_node(1, label="b")
    #g.add_edge(0, 1)
    strin = "templates/" + day + ".html"
    g.show(strin)
    return render_template(day+".html")
    #return render_template(strin)


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
