import numpy as np
from bird import Bird
import random

class GeneticAlgorithm():
    def __init__(self, GEN_SIZE):
        self.GEN_SIZE = GEN_SIZE
        pass

    # Normalize the fitness
    # set the fitness to between 0 and 1
    def normalize(self, birds):
        for i in range(len(birds)):
            birds[i].score = pow(birds[i].score, 2)

    # Get the fitness of the bird
    # How well they done in the generation
    def calculateFitness(self, savedBirds):
        sum = 0
        for bird in savedBirds:
            sum += bird.score

        for bird in savedBirds:
            bird.fitness = bird.score / sum

    # Pick one of the birds from the savedBirds list
    # This is done with probability acording to the fitness
    def pickOne(self, savedBirds):
        fitness = 0
        index = 0
        bird = None
        r = random.random()
        while (r >  0):
            r = r - savedBirds[index].fitness
            index += 1

        # Go back one to get the index you want
        index -= 1
        bird = savedBirds[index]
        child = Bird(WIDTH,HEIGHT, bird.brain.copy()) # create a new bird with the the last bird brain
        # Mutate the childs brain
        child.mutate(0.2) # the probability that the weight will mutate
        return child # Return the child to add it to the list

    # Create a new generation
    def nextGeneration(self, savedBirds, birds):

        self.normalize(savedBirds) # normalize fitness
        self.calculateFitness(savedBirds) # calculate how well the bird performed

        # Make a new generation
        for i in range(self.GEN_SIZE):
            birds.append(self.pickOne(savedBirds)) # create a new list of birds

        return birds
