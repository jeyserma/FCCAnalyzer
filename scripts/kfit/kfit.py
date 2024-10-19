from sympy import *
import numpy as np
from numpy.linalg import multi_dot, inv


"""
This class performs a kinematic fit on set of parameters given a set of
measured parameters and analytical constraints. The derivatives of the
constraint vector are computed analytically. The minimisation is performed
using iteratively the Lagrange multiplier method using definitions and
conventions from : https://arxiv.org/pdf/1911.10200.pdf
"""

class KinematicFit:
    def __init__(self, variables, constraints):

        """ vector of variables a of size n """
        self.variables = variables

        """ vector of constraints H(a) of size r """
        self.constraints = constraints

        """ compute matrix of dHi/daj expressions of size (r x n) """
        self.constraints_derivatives = self.compute_constraints_derivative(constraints, variables)

        """ fit parameters """
        self.iterations = 100  # how many loops
        self.maxchisqdiff = 1.e-06 # criterion for convergence
        self.weight = 1. # for linear constraints use w = 1, smaller for higher


    """ compute matrix of dHi/daj expressions of size (r x n) """
    def compute_constraints_derivative(self, constraints, variables):
        dconstraints = []
        # these are expressions
        for i in range(len(constraints)):
            dH_i = []
            for j in range(len(variables)):
                constrain_derivative = Derivative(constraints[i], variables[j]).doit()
                dH_i.append(constrain_derivative)
            dconstraints.append(dH_i)
        return dconstraints

    """ print expressions of constraints """
    def print_constraints(self):
        r = len(self.constraints)
        for i in range(r):
            print(i, "constraint expression : {}".format(constraints[i]))

    """ print expressions of constraints """
    def print_constraints_derivatives(self):
        r = len(self.constraints)
        n = len(self.variables)
        for i in range(r):
            for j in range(n):
                print("dH{}/d{} = {}".format(i+1,self.variables[j], self.constraints_derivatives[i][j]))

    """ create mapping between symbols and value """
    def evaluate_variables(self, a):
        sub_list = []
        rows = a.shape[0]
        for i in range(rows):
            sub_list.append((self.variables[i],a[i][0]))
        return sub_list


    """ evaluate vector of constraints """
    def evaluate_constraints(self, replacements):
        d = np.zeros((len(self.constraints),1))
        for i in range(d.shape[0]):
            Hi = self.constraints[i]
            d[i][0] = Hi.subs(replacements)
        return d

    """ evaluate vector of constraints """
    def evaluate_constraint_derivative(self, replacements):
        D = np.zeros((len(self.constraints),len(self.constraints_derivatives[0])))
        for i in range(D.shape[0]):
            for j in range(D.shape[1]):
                dHi_dxj = self.constraints_derivatives[i][j]
                D[i][j] = dHi_dxj.subs(replacements)
        return D

    """ run kinematic fit """
    def results(self, a0, Va0, options):

        # initialize options
        self.iterations   = options[0]
        self.maxchisqdiff = options[1]
        self.weight       = options[2]

        ## start minimisation here
        converged=False
        i=0
        chisqrd=0.
        chisqrd_last=0.

        n = len(self.variables)

        # check that a and V have correct sizes
        if a0.shape[0] != n or a0.shape[1] != 1:
            print('Wrong size of a0. Need a numpy array of size ({},{})'.format(n,1))
            exit()

        if Va0.shape[0] != n or Va0.shape[1] != n:
            print('Wrong size of Va0. Need a numpy array of size ({},{})'.format(n,n))
            exit()

        # initialise variables and covariance matrix
        a = a0
        Va = Va0

        # iteratively solve
        while not converged and i < self.iterations:

            symb_to_val = self.evaluate_variables(a)
            d = self.evaluate_constraints(symb_to_val)
            D = self.evaluate_constraint_derivative(symb_to_val)
            DT = np.transpose(D)
            VD = inv(multi_dot([D, Va, DT]))
            Lambda = VD.dot(d) ## fix me: could be as well V * (d+D*delta_a)
            LambdaT = np.transpose(Lambda)
            delta_a = - self.weight * multi_dot([Va, DT, Lambda])
            delta_a_T = np.transpose(delta_a)
            # fitted values and new covariance matrix
            a = a + delta_a
            Va = Va - Va * DT * VD * D * Va * self.weight
            #chisqrd = np.trace(Va)
            chisqrd = multi_dot([delta_a_T, inv(Va), delta_a]) + 2*LambdaT.dot(d + D.dot(delta_a))

            if i==0: firstchisqrd = chisqrd
            i += 1

            if abs(chisqrd - chisqrd_last) < self.maxchisqdiff:
                 converged=True # good enough fit

        return (a, Va, chisqrd_last, i)