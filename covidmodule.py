import networkx as nx
import matplotlib.pyplot as plt
import scipy
import random
from random import choice
import numpy as np

class Person:

    def __init__(self, contacts):
        self.contacts = contacts # this is a 2D array [friend, weight]

        # how many days before a person is symptomatic:
        # this encodes their state (-1 = healthy, >= 0 = asymptomatic, -2 = quarantined)
        self.before_symptomatic = -1

    def get_covid(self):

        # people constants (move these out?)
        MEAN_SYMPTOMATIC = 6 # 6 days on average
        STANDARD_DEV_SYMPTOMATIC = 1.2 # can change this later

        # randomly sample from disrubtion to get # time steps before symptomatic
        if (self.before_symptomatic == -1):
            self.before_symptomatic = np.random.normal(MEAN_SYMPTOMATIC, STANDARD_DEV_SYMPTOMATIC)

    def get_tested(self):
        if (self.before_symptomatic >= 0 ): # asymptomatic
            self.before_symptomatic = -2
            return True # do something
        if (self.before_symptomatic == -1 or self.before_symptomatic == -2): # healthy or in quarantine
            return False # do nothing



class Graph:

    def __init__(self, adjacency_list):
        self.adjacency_list = adjacency_list

    """
    def covid_spread(self):


    def dynamic_test(self, people_to_test):

        return discovered_positives
    """
