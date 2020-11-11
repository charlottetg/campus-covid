from flask import Flask, request, jsonify
from Person import Person
from Graph import Graph
import pandas as pd
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
    g = graph_from_data(10, 1, 2, .174, .031, 6, 1.2)
    #print(g)
    return ""

@app.route("/<day>")
def time(day):
    return "it is now day: " + day


def graph_from_data(students, close, tang, prob_close, prob_tang, mean_symptomatic, standard_dev_symptomatic):
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
                        social_ids_dict[current_id].contacts[contact_id] = prob_close  # add contact

                    if contact_id not in social_ids_dict.keys():  # initialize
                        social_ids_dict[contact_id] = Person({})

                    if current_id not in social_ids_dict[contact_id].contacts.keys():
                        social_ids_dict[contact_id].contacts[current_id] = prob_close

    print(len(social_ids_dict))
    social_graph = Graph(social_ids_dict)
    social_graph.ids_dict[1].get_covid(mean_symptomatic, standard_dev_symptomatic)  # give one person covid
    social_graph.ids_dict[1].patient_zero = True

    # create graph with random close + tang contacts
    random_graph = Graph({})
    random_graph.add_contacts(close, prob_close, students)
    random_graph.add_contacts(tang, prob_tang, students)
    random_graph.ids_dict[1].get_covid(mean_symptomatic, standard_dev_symptomatic)  # give one person covid
    random_graph.ids_dict[1].patient_zero = True

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

    # social_graph.show_graph(prob_close, prob_tang) #we don't want to use nx in the back end
    social_graph.print_stats()
    # social_graph.print_contacts_info()

if __name__ == "__main__":
    app.run(debug=True)
