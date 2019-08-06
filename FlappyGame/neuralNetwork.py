from numpy import *
from random import *
import math
import scipy.special


def matrixAdd(a, b):
    for i in range((size(a, 0))):
        for j in range(size(a, 1)):
            a[i][j] += b[i][j]

class NeuralNetwrok (object):

    def __init__(self,input_nodes,hidden_nodes, output_nodes,lr):
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes

        # Make the weights between the input and hidden and hidden and output
        self.weights_ih = ndarray(shape = (self.hidden_nodes, self.input_nodes))
        self.weights_ho = ndarray(shape = (self.output_nodes, self.hidden_nodes))
        # randomise the weights
        self.weights_ih = self.randomWeights(self.weights_ih)
        self.weights_ho = self.randomWeights(self.weights_ho)

        # Create the bias arrays
        self.bias_h = ndarray(shape = (self.hidden_nodes,1))
        self.bias_o = ndarray(shape = (self.output_nodes, 1))
        self.bias_h = self.randomWeights(self.bias_h)
        self.bias_o = self.randomWeights(self.bias_o)
        # self.bias_h = matrix.transpose(self.bias_h)
        # self.bias_o = matrix.transpose(self.bias_o)


        self.lr = lr

        # activation function is the sigmoid function
        self.activation_function = lambda x: scipy.special.expit(x)

        pass


    def feedForward(self, inputArray):
        # convert inputs list to 2d array
        input = array(inputArray, ndmin=2).T

        # Calculate singnals into the hidden layer
        hiddenInput = dot(self.weights_ih, input)
        hiddenInput = hiddenInput + self.bias_h
        hiddenOutput = self.activation_function(hiddenInput)
        # hiddenOutput = matrix.transpose(hiddenOutput)


        # Calclate signals into the final layer
        finalInput = dot(self.weights_ho, hiddenOutput)
        finalInput = finalInput + self.bias_o
        finalOutput = self.activation_function(finalInput)

        for i in range((size(finalOutput, 0))):
            for j in range(size(finalOutput, 1)):
                finalOutput[i][j] = round(finalOutput[i][j], 2)


        # Sending it back to the caller
        return finalOutput

    def gradientDecent(self, inputArray, targetArray):

        # convert inputs list to 2d array
        input = array(inputArray, ndmin=2).T

        # Calculate singnals into the hidden layer
        hiddenInput = dot(self.weights_ih, input)
        hiddenInput = hiddenInput + self.bias_h
        hiddenOutput = self.activation_function(hiddenInput)
        # hiddenOutput = matrix.transpose(hiddenOutput)

        # Calclate signals into the final layer
        finalInputs = dot(self.weights_ho, hiddenOutput)
        finalInputs = finalInputs + self.bias_o
        finalOutputs = self.activation_function(finalInputs)

        target = array(targetArray, ndmin=2).T

        # Calculate the errors for the output layer
        outputErrors = target - finalOutputs
        outputGradiants = finalOutputs * (1- finalOutputs)
        outputGradiants = outputGradiants * outputErrors
        outputGradiants = outputGradiants * self.lr

        # Calclate deltas
        hidden_T = matrix.transpose(hiddenOutput)
        weights_ho_deltas = outputGradiants * hidden_T

        # Change the weights by the deltas
        self.weights_ho += weights_ho_deltas
        # Change the bias with the gradiant
        self.bias_o += outputGradiants

        # Calculate the hidden layer errors
        who_T = matrix.transpose(self.weights_ho)
        hiddenErrors = who_T * outputErrors

        # Hidden layer gradiant
        hiddenGradiants = hiddenOutput * ( 1 - hiddenOutput)
        hiddenGradiants = hiddenGradiants * hiddenErrors
        hiddenGradiants = hiddenGradiants * self.lr

        # Calculate deltas
        input_t = matrix.transpose(input)
        weights_ih_deltas = hiddenGradiants * input_t

        # change the weights by the deltas
        self.weights_ih += weights_ih_deltas
        # Change the bias with the gradiant
        self.bias_h += hiddenGradiants




    def randomWeights(self, n):
        for i in range(size(n, 0)):
            for j in range(size(n, 1)):
                n[i][j] = uniform(-1,1)
        return n
