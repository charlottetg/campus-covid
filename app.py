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
    print(g)
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
                        social_ids_dict[current_id].contacts[contact_id] = PROB_CLOSE  # add contact

                    if contact_id not in social_ids_dict.keys():  # initialize
                        social_ids_dict[contact_id] = Person({})

                    if current_id not in social_ids_dict[contact_id].contacts.keys():
                        social_ids_dict[contact_id].contacts[current_id] = PROB_CLOSE

    social_graph = Graph(social_ids_dict)
    social_graph.ids_dict[1].get_covid(MEAN_SYMPTOMATIC, STANDARD_DEV_SYMPTOMATIC)  # give one person covid
    social_graph.ids_dict[1].patient_zero = True

    print(len(social_graph.ids_dict))

    # originally in show_graph (to keep pos consistent)
    social_pos = nx.spring_layout(social_graph.networkx_graph())
    social_graph.show_graph(PROB_CLOSE, PROB_TANG, social_graph.networkx_graph(), social_pos)


    """
    # create graph with random close + tang contacts
    random_graph = Graph({})
    random_graph.add_contacts(NUM_CLOSE, PROB_CLOSE, NUM_STUDENTS)
    random_graph.add_contacts(NUM_TANG, PROB_TANG, NUM_STUDENTS)
    random_graph.ids_dict[1].get_covid(MEAN_SYMPTOMATIC, STANDARD_DEV_SYMPTOMATIC)  # give one person covid
    random_graph.ids_dict[1].patient_zero = True

    # originally in show_graph (to keep pos consistent)
    random_pos = nx.spring_layout(random_graph.networkx_graph())
    random_graph.show_graph(PROB_CLOSE, PROB_TANG, random_graph.networkx_graph(), random_pos)
    """

    # one week
    for i in range(7):
        #random_graph.graph_spread(MEAN_SYMPTOMATIC, STANDARD_DEV_SYMPTOMATIC)
        social_graph.graph_spread(MEAN_SYMPTOMATIC, STANDARD_DEV_SYMPTOMATIC)

        people_to_test = random.sample(list(range(1, NUM_STUDENTS)), round(NUM_STUDENTS / 21))

        #random_graph.dynamic_test(people_to_test)
        social_graph.dynamic_test(people_to_test)


    #random_graph.show_graph(PROB_CLOSE, PROB_TANG, random_graph.networkx_graph(), random_pos)
    #random_graph.print_stats()
    #random_graph.print_contacts_info()

    social_graph.show_graph(PROB_CLOSE, PROB_TANG, social_graph.networkx_graph(), social_pos) #we don't want to use nx in the back end
    social_graph.print_stats()
    #social_graph.print_contacts_info()



if __name__ == "__main__":
    app.run(debug=True)
