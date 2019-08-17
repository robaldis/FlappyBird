import numpy as np
from random import *
import math
import scipy.special


def matrixAdd(a, b):
    for i in range((np.size(a, 0))):
        for j in range(np.size(a, 1)):
            a[i][j] += b[i][j]

class NeuralNetwrok (object):

    def __init__(self,input_nodes,hidden_nodes, output_nodes,lr, oldBrain = None):
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes

        if (oldBrain != None):
            self.weights_ih = oldBrain.weights_ih
            self.weights_ho = oldBrain.seights_ho
            self.bias_h = oldbrain.bias_h
            self.bias_o = oldbrain.bias_o


        else:
            # Make the weights between the input and hidden and hidden and output
            self.weights_ih = np.ndarray(shape = (self.hidden_nodes, self.input_nodes))
            self.weights_ho = np.ndarray(shape = (self.output_nodes, self.hidden_nodes))
            # randomise the weights
            self.weights_ih = self.randomWeights(self.weights_ih)
            self.weights_ho = self.randomWeights(self.weights_ho)

            # Create the bias arrays
            self.bias_h = np.ndarray(shape = (self.hidden_nodes,1))
            self.bias_o = np.ndarray(shape = (self.output_nodes, 1))
            self.bias_h = self.randomWeights(self.bias_h)
            self.bias_o = self.randomWeights(self.bias_o)


        self.lr = lr

        # activation function is the sigmoid function
        self.activation_function = lambda x: scipy.special.expit(x)

        pass


    def predict(self, inputArray):
        # convert inputs list to 2d array
        input = np.array(inputArray, ndmin=2).T

        # Calculate singnals into the hidden layer
        hiddenInput = np.dot(self.weights_ih, input)
        hiddenInput = hiddenInput + self.bias_h
        hiddenOutput = self.activation_function(hiddenInput)
        # hiddenOutput = matrix.transpose(hiddenOutput)


        # Calclate signals into the final layer
        finalInput = np.dot(self.weights_ho, hiddenOutput)
        finalInput = finalInput + self.bias_o
        finalOutput = self.activation_function(finalInput)

        for i in range((np.size(finalOutput, 0))):
            for j in range(np.size(finalOutput, 1)):
                finalOutput[i][j] = round(finalOutput[i][j], 2)


        # Sending it back to the caller
        return finalOutput

    def gradientDecent(self, inputArray, targetArray):

        # convert inputs list to 2d array
        input = np.array(inputArray, ndmin=2).T

        # Calculate singnals into the hidden layer
        hiddenInput = np.dot(self.weights_ih, input)
        hiddenInput = hiddenInput + self.bias_h
        hiddenOutput = self.activation_function(hiddenInput)
        # hiddenOutput = matrix.transpose(hiddenOutput)

        # Calclate signals into the final layer
        finalInputs = np.dot(self.weights_ho, hiddenOutput)
        finalInputs = finalInputs + self.bias_o
        finalOutputs = self.activation_function(finalInputs)

        target = np.array(targetArray, ndmin=2).T

        # Calculate the errors for the output layer
        outputErrors = target - finalOutputs
        outputGradiants = finalOutputs * (1- finalOutputs)
        outputGradiants = outputGradiants * outputErrors
        outputGradiants = outputGradiants * self.lr

        # Calclate deltas
        hidden_T = np.matrix.transpose(hiddenOutput)
        weights_ho_deltas = outputGradiants * hidden_T

        # Change the weights by the deltas
        self.weights_ho += weights_ho_deltas
        # Change the bias with the gradiant
        self.bias_o += outputGradiants

        # Calculate the hidden layer errors
        who_T = np.matrix.transpose(self.weights_ho)
        hiddenErrors = who_T * outputErrors

        # Hidden layer gradiant
        hiddenGradiants = hiddenOutput * ( 1 - hiddenOutput)
        hiddenGradiants = hiddenGradiants * hiddenErrors
        hiddenGradiants = hiddenGradiants * self.lr

        # Calculate deltas
        input_t = np.matrix.transpose(input)
        weights_ih_deltas = hiddenGradiants * input_t

        # change the weights by the deltas
        self.weights_ih += weights_ih_deltas
        # Change the bias with the gradiant
        self.bias_h += hiddenGradiants



    def copy(self):

        tempBrain = NeuralNetwrok(self.input_nodes, self.hidden_nodes, self.output_nodes, self)
        return tempBrain

    def mutate(self, list, probability):
        # # Mutation changes a single gene in each offspring randomly.
        # for idx in range(weight.shape[0]):
        #     for idy in range (weight.shape[1]):
        #         r = random()
        #         if (r < rate):
        #             # The random value to be added to the gene.
        #             random_value = uniform(-1.0, 1.0)
        #
        #             weight[idx, idy] = weight[idx, idy] + (random_value * 0.01)
        #
        # # return weight

        temp = list   # Cast to numpy array
        shape = temp.shape       # Store original shape
        temp = temp.flatten()    # Flatten to 1D
        num_to_change = int(len(temp) * probability)
        inds = np.random.choice(
            temp.size, size=num_to_change)   # Get random indices
        # multiply weights by random # from -2 to 2)
        temp[inds] = temp[inds] + np.random.uniform(-0.01, 0.01, size=num_to_change)
        # temp[inds] = np.random.uniform(-1, 1, size=num_to_change)

        temp = temp.reshape(shape)                     # Restore original shape
        return temp


    def randomWeights(self, n):
        for i in range(np.size(n, 0)):
            for j in range(np.size(n, 1)):
                n[i][j] = uniform(-1,1)
        return n
