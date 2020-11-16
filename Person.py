import numpy as np
import math as math

class Person:

    def __init__(self, contacts):
        self.contacts = contacts # dictionary with friends as keys

        # this encodes their state (-1 = healthy, >= 0 = asymptomatic (how many days before symptomatic), -2 = quarantined)
        self.state = -1

        self.patient_zero = False # can take this out later

    def get_covid(self, mean_symptomatic, standard_dev_symptomatic):

        # randomly sample from distribution to get # time steps before symptomatic
        if (self.state == -1):
            self.state = math.floor(np.random.normal(mean_symptomatic, standard_dev_symptomatic))

    # return true if person is asymptomatic
    def get_tested(self):
        if (self.state >= 0): # asymptomatic
            self.state = -2
            return True # I think this is a weird structure
