import networkx as nx
import matplotlib.pyplot as plt
import scipy
import random
from random import choice
import numpy as np
import math as math

class Person:

    def __init__(self, contacts):
        self.contacts = contacts # this is a 2D array [friend, weight]

        # how many days before a person is symptomatic:
        # this encodes their state (-1 = healthy, >= 0 = asymptomatic, -2 = quarantined)
        self.state = -1

        self.patient_zero = False # can take this out later

    def get_covid(self):

        # people constants (move these out?)
        MEAN_SYMPTOMATIC = 6 # 6 days on average
        STANDARD_DEV_SYMPTOMATIC = 1.2 # can change this later

        # randomly sample from disrubtion to get # time steps before symptomatic
        if (self.state == -1):
            self.state = math.floor(np.random.normal(MEAN_SYMPTOMATIC, STANDARD_DEV_SYMPTOMATIC))

    # returns true if self has it
    def get_tested(self):
        if (self.state >= 0): # asymptomatic
            self.state = -2
            return True # I think this is a weird structure