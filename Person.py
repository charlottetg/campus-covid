"""
Anna Spiro and Charlotte Gray
Person Class
"""

import numpy as np
import math as math

class Person:
    """
    A class used to represent an individual Person and keep track of their contacts and state.
    This class is used in the Graph class as the basis for the graph model of campus.

    Attributes
    __________
    contacts: dict
        a person's contacts are (integer) keys, and the types of contact
        (quantified through transmission pobability) are (float) values
    state: int
        encodes a person's COVID-19 status:
        -1 = healthy, >= 0 = infected and asymptomatic, -2 = quarantined.
        For asymptomatic individuals, the integer represents the number of time steps
        before they will show symptoms.
    patient_zero: Boolean
        for visualization purposes, this keeps track of whether the individual
        is patient zero (True = yes, False = no)

    Methods
    _______
    get_covid
        If the individual is healthy, set their state to the number of time steps before they become symptomatic.
    get_tested
         If the individual is asymptomatic, set them to quarantine and return True.
    """

    def __init__(self, contacts):
        """
        Parameters
        __________
        contacts: dict
            A person's contacts are integer keys, and the types of contact
            (quantified through transmission pobability) are float values
        """
        self.contacts = contacts
        self.state = -1
        self.patient_zero = False

    def get_covid(self, mean_symptomatic, standard_dev_symptomatic):
        """ If the individual is healthy, set their state to the number of time steps before they become symptomatic.
        Parameters
        __________
        mean_symptomatic: float
            Mean number of days until an individual becomes symptomatic
        standard_dev_symptomatic: float
            Standard deviation number of days until an individual becomes symptomatic
        """
        # randomly sample from the distribution described by mean, standard deviation
        if (self.state == -1):
            self.state = math.floor(np.random.normal(mean_symptomatic, standard_dev_symptomatic))

    def get_tested(self):
        """ If the individual is asymptomatic, set them to quarantine and return True.
        """
        if (self.state >= 0): # the person is asymptomatic
            self.state = -2
            return True
