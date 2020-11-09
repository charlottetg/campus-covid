from flask import Flask, request, jsonify
from Person import Person
app = Flask(__name__)

@app.route("/<id>")
def persondata(id):
    #id = int(id)
    p = Person([[id, 0],[id, -1],[2,.5],[3,.5]])
    if (p.state==-1):
        return "person " + id + " is healthy!"
    else:
        return jsonify(p.contacts)

@app.route("/<day>")
def time(day):
    return "it is now day: " + day

if __name__ == "__main__":
    app.run(debug=True)