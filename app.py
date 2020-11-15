from flask import Flask, request, jsonify, render_template
from Person import Person
from Graph import Graph
import pandas as pd
import random
app = Flask(__name__)

@app.route("/")
def testin():
    return render_template('hello.html')

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






if __name__ == "__main__":
    app.run(debug=True)
