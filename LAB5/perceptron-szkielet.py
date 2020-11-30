'''
Plik zawiera szkielet programu, który definiuje i trenuje perceptron prosty.

Uzupełnić program o:
- wczytanie danych treningowych z pliku CSV,
- zainicjowanie wag losowymi wartościami,
- przeprowadzenie treningu perceptronu metodą gradientową,
- przeprowadzenie testu perceptronu.

Program należy wykorzystać do nauczenia perceptronu dodawania w zakresie [0,1].
'''

import csv
from numpy import tanh, power
import random


def read_input_data(filename):
    '''
    Reads input data (train / test) from a CSV file.
    Input:
        filename - CSV file name (string)
    CSV file format:  
        input1, input2, ..., output
                        ...
                        ...  
    Returns: 
        Nin - number of inputs of the perceptron (int)
        X - input training data (list)
        Y - output (expected) training data (list)
    '''

    Nin = 2
    X = []
    Y = []

    file = open(filename, 'r')
    data = csv.reader(file, delimiter=",", quoting=csv.QUOTE_NONNUMERIC)

    for line in data:
        X.append(line[0:Nin])
        Y.append(line[Nin])

    file.close()
    return Nin, X, Y


def initialize_weights(Nin):
    '''
    Initialize weights with a random numbers from range [0,1).
    Input:
        Nin - number of inputs of the perceptron (int)
    Output:
        Randomly initialized weights (list of Nin size)
    '''

    w = []
    for i in range(Nin):
        w.append(random.random())

    return w


def f(x):
    return tanh(x)


def fprim(x):
    return 1 - power(tanh(x), 2)


def sum_weight(X, W):
    sum_w = 0

    for i in range(len(X)):
        for j in range(len(W)):
            sum_w += W[j] * X[i][j]

    return sum_w


def train(epochs, X, Y, weights, eta):
    '''
    Trains the simple perceptron using the gradient method.
    Plots the RMSE.
    Inputs:
        epochs - number of training iterations (int > 0)
        X - training (input) vector (list)
        Y - training (output) vector (list)
        weights - initial weights (list)
        eta - learning rate (0-1]
    Returns:
        weights - optimized weights (list)
    '''   

    # For each epoch:
    #   For each training data (pair X,Y):
    #       Calculate output Yout
    #       Use Yout to calculate error
    #       Adjust weights using the gradient formula
    #       Calculate ans store the RMSE (root mean squared error)
    # Plot the RMSE(epoch)

    for epoch in range(epochs):
        error = 0
        sumW = float(sum_weight(X, weights))
        for i in range(len(X)):
            out = f(sumW)
            error += pow(Y[i] - out, 2)
            for j in range(Nin):
                weights[j] += eta * fprim(sumW) * (Y[i] - out) * X[i][j]

    return weights


def test(filename, weights):
    '''
    Test ot the trained perceptron by propagating the test data.
    Input:
        filename - CSV file name (string)
        weights - trained weights (list)
    CSV file format:  
        input1, input2, ..., expected_output
                        ...
                        ...  
    Returns: 
        Y - output testing results (list)
        Yexpected - output expected results (list)
        
    '''
    Y = []
    Nin, Xtest, Ytest = read_input_data(filename)

    for i in range(len(Xtest)):
        sumW = 0
        for j in range(Nin):
            sumW += weights[j] * Xtest[i][j]

        Y.append(f(sumW))


    return Y, Ytest

    
if __name__ == '__main__':    
    '''
     Simple perceptron

                 Yout
                  ^
                  |
                  O
                / | \         weights: weights[]
              Nin inputs
    '''

    # Get the train data
    Nin, Xtrain, Ytrain = read_input_data("train_data.csv")

    # Initialize weights
    weights = initialize_weights(Nin)
    
    # Train of the perceptron
    epochs = 10000
    eta = 0.7
    weights = train(epochs, Xtrain, Ytrain, weights, eta)

    # Test of the perceptron with the trained weights
    Yout, Yexpected = test("test_data.csv", weights)
    print("Results:", Yout)
    print("Expected results:", Yexpected)

