import numpy as np
from lib.bird import Bird
import random
import json

class GeneticAlgorithm():
    def __init__(self, GEN_SIZE, WIDTH, HEIGHT):
        self.GEN_SIZE = GEN_SIZE
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
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
        child = Bird(self.WIDTH,self.HEIGHT, bird.brain.copy()) # create a new bird with the the last bird brain
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


    def saveBird(self,birds):
        saveinfo = birds[0].brain
        dict = {
                "weights_ih" : saveinfo.weights_ih.tolist(),
                "weights_ho" : saveinfo.weights_ho.tolist(),
                "bias_h" : saveinfo.bias_h.tolist(),
                "bias_o" : saveinfo.bias_o.tolist(),
        }
        # Writing JSON data
        with open("FlappyGame/BestBirdBrain.json", 'w') as f:
            json.dump(dict, f, indent = 4)


    def readBird(self):
        with open("FlappyGame/BestBirdBrain.json", "r") as f:
            jsonData = json.load(f)
        return jsonData
