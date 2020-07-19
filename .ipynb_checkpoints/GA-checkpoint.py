"""
Daniel Maidment
maidment.daniel@gmail.com
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib
import time
import pandas as pd
import scipy.io
import scipy.signal as signal
import scipy.linalg as linalg
import warnings
from numpy import pi
from numpy import cos
from numpy import sin
from numpy import log10
from numpy import log
from numpy import real
from numpy import imag
from numpy import sqrt
from numpy import e
from numpy import abs
from numpy import angle
from numpy.fft import fft
from numpy.fft import ifft
from numpy.fft import fftshift
from numpy import min
from numpy import max
from numpy import sum
from numpy.linalg import norm
from numpy import dot

######################################################"""
#turns off automatic plt.plot display, use plt.show()  to re-enable
plt.ioff()
#Turn off pesky from Future Warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


def cal_pop_fitness(equation_inputs, pop):
     # Calculating the fitness value of each solution in the current population.
     # The fitness function calculates the sum of products between each input
     # and its corresponding weight.
     fitness = np.sum(pop*equation_inputs, axis=1)
     return fitness

def select_mating_pool(pop, fitness, num_parents):

    # Selecting the best individuals in the current generation as parents
    # for producing the offspring of the next generation.

    #generate empty parent population array
    parents = np.empty((num_parents, pop.shape[1]))

    #iterate through the number of parents
    for parent_num in range(num_parents):
        #find which memper had max fitness
        max_fitness_idx = np.where(fitness == np.max(fitness))
        max_fitness_idx = max_fitness_idx[0][0]

        #choose the individual from the previous population with the maximum
        #fitness to be a parent for the next generation.
        parents[parent_num, :] = pop[max_fitness_idx, :]

        #set the current maximum fitness to be some small value so that on the
        #next iteration of the loop the next best individual will be selected
        #i.e. take this one out of the running
        fitness[max_fitness_idx] = -99999999999
    return parents

def crossover(parents, offspring_size):

    offspring = np.empty(offspring_size)
    # The point at which crossover takes place between two parents.
    #Usually, it is at the center.
    crossover_point = int(offspring_size[1]/2)

    for k in range(offspring_size[0]):
        # Index of the first parent to mate.
        parent1_idx = k%parents.shape[0]
        # Index of the second parent to mate.
        parent2_idx = (k+1)%parents.shape[0]
        # The new offspring will have its first half of its genes taken from the first parent.
        offspring[k, 0:crossover_point] = parents[parent1_idx, 0:crossover_point]
        # The new offspring will have its second half of its genes taken from the second parent.
        offspring[k, crossover_point:] = parents[parent2_idx, crossover_point:]
    return offspring

def mutation(offspring_crossover):

    # Mutation changes a single gene in each offspring randomly.

    for idx in range(offspring_crossover.shape[0]):

        # The random value to be added to the gene.

        random_value = np.random.uniform(-1.0, 1.0, 1)

        offspring_crossover[idx, 4] = offspring_crossover[idx, 4] + random_value

    return offspring_crossover

