################################################################################
#
# LOGISTICS
#
#    Sumedh Pranab Sen
#    NetID: XYZ000000
#
# DESCRIPTION
#
#    MNIST image classification with an xNN written and trained in Python
#
# INSTRUCTIONS
#
#    1. Go to Google Colaboratory: https://colab.research.google.com/notebooks/welcome.ipynb
#    2. File - New Python 3 notebook
#    3. Cut and paste this file into the cell (feel free to divide into multiple cells)
#    4. Runtime - Run all
#
# NOTES
#
#    1. This does not use PyTorch, TensorFlow or any other xNN library
#
#    2. Include a short summary here in nn.py of what you did for the neural
#       network portion of code
#
#    3. Include a short summary here in cnn.py of what you did for the
#       convolutional neural network portion of code
#
#    4. Include a short summary here in extra.py of what you did for the extra
#       portion of code
#
################################################################################

"""# Artificial Neural Network without Tensorflow, Keras, PyTorch
---
### Features

1.   This code doesn't use libraries like Tensorflow, Keras or PyTorch
2.   This code is flexible. Which means, you can add layers very easily and efficiently, without worrying about backpropagation and weight updation for each layer.
Like: 


```
nw = Network()
nw.add(Dense(input_size = 784, output_size = 1000, lr = 0.01, activation = "relu"))
```


3. Back Propagation happens automatically, for any number of layers. 
4. Data automatically passed between layers. Output of one layer is correctly passed as input to next layer.
5. Shows a minimal animated progress bar during each epoch. (Doesn't work on Colab)


```
Epoch: 0/5
############################################################ <--(The progress bar)
Validating the model...
Time taken: 20.49 sec
Time per input: 0.023 sec
Average training loss: 1.747
Validation Accuracy 0.81
=================================================================================
```
6. Follows an Object Oriented approach :)
"""

################################################################################
#
# IMPORT
#
################################################################################
import os.path
import urllib.request
import gzip
import time
import math
import numpy             as np
import matplotlib.pyplot as plt
import seaborn as sns

################################################################################
#
# PARAMETERS
#
################################################################################
# data
DATA_NUM_TRAIN         = 60000
DATA_NUM_TEST          = 10000
DATA_CHANNELS          = 1
DATA_ROWS              = 28
DATA_COLS              = 28
DATA_CLASSES           = 10
DATA_URL_TRAIN_DATA    = 'http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz'
DATA_URL_TRAIN_LABELS  = 'http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz'
DATA_URL_TEST_DATA     = 'http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz'
DATA_URL_TEST_LABELS   = 'http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz'
DATA_FILE_TRAIN_DATA   = 'train_data.gz'
DATA_FILE_TRAIN_LABELS = 'train_labels.gz'
DATA_FILE_TEST_DATA    = 'test_data.gz'
DATA_FILE_TEST_LABELS  = 'test_labels.gz'

# display
DISPLAY_ROWS   = 8
DISPLAY_COLS   = 4
DISPLAY_COL_IN = 10
DISPLAY_ROW_IN = 25
DISPLAY_NUM    = DISPLAY_ROWS*DISPLAY_COLS

################################################################################
#
# DATA
#
################################################################################

 # download
if (os.path.exists(DATA_FILE_TRAIN_DATA)   == False):
    urllib.request.urlretrieve(DATA_URL_TRAIN_DATA,   DATA_FILE_TRAIN_DATA)
if (os.path.exists(DATA_FILE_TRAIN_LABELS) == False):
    urllib.request.urlretrieve(DATA_URL_TRAIN_LABELS, DATA_FILE_TRAIN_LABELS)
if (os.path.exists(DATA_FILE_TEST_DATA)    == False):
    urllib.request.urlretrieve(DATA_URL_TEST_DATA,    DATA_FILE_TEST_DATA)
if (os.path.exists(DATA_FILE_TEST_LABELS)  == False):
    urllib.request.urlretrieve(DATA_URL_TEST_LABELS,  DATA_FILE_TEST_LABELS)

 # training data
 # unzip the file, skip the header, read the rest into a buffer and format to NCHW
file_train_data   = gzip.open(DATA_FILE_TRAIN_DATA, 'r')
file_train_data.read(16)
buffer_train_data = file_train_data.read(DATA_NUM_TRAIN*DATA_ROWS*DATA_COLS)
train_data        = np.frombuffer(buffer_train_data, dtype=np.uint8).astype(np.float32)
train_data        = train_data.reshape(DATA_NUM_TRAIN, 1, DATA_ROWS, DATA_COLS)
 
 
# training labels
# unzip the file, skip the header, read the rest into a buffer and format to a vector
file_train_labels   = gzip.open(DATA_FILE_TRAIN_LABELS, 'r')
file_train_labels.read(8)
buffer_train_labels = file_train_labels.read(DATA_NUM_TRAIN)
train_labels        = np.frombuffer(buffer_train_labels, dtype=np.uint8).astype(np.int32)
 
 # testing data
 # unzip the file, skip the header, read the rest into a buffer and format to NCHW
file_test_data   = gzip.open(DATA_FILE_TEST_DATA, 'r')
file_test_data.read(16)
buffer_test_data = file_test_data.read(DATA_NUM_TEST*DATA_ROWS*DATA_COLS)
test_data        = np.frombuffer(buffer_test_data, dtype=np.uint8).astype(np.float32)
test_data        = test_data.reshape(DATA_NUM_TEST, 1, DATA_ROWS, DATA_COLS)
 
 # testing labels
 # unzip the file, skip the header, read the rest into a buffer and format to a vector
file_test_labels   = gzip.open(DATA_FILE_TEST_LABELS, 'r')
file_test_labels.read(8)
buffer_test_labels = file_test_labels.read(DATA_NUM_TEST)
test_labels        = np.frombuffer(buffer_test_labels, dtype=np.uint8).astype(np.int32)
 
# debug
# print(train_data.shape)   # (60000, 1, 28, 28)
# print(train_labels.shape) # (60000,)
# print(test_data.shape)    # (10000, 1, 28, 28)
# print(test_labels.shape)  # (10000,)

################################################################################
#
# YOUR CODE GOES HERE
#
################################################################################

class SuperLayer:
    """
    class SuperLayer
    ----------------
    
    Includes activation functions and derivative functions that will be used by 
    all types of layers (Eg. Dense). Only 3 activation functions are defined here, for
    the sake of this assignment, however, all the 7 activation functions can be written
    here and this class will be extended by all the other layer classes.
    """

    def relu(self,x):
        """
        Performs the relu activation function.
        If element is <= 0, return 0, else return the element

        Input:
        -----
        x: numpy.ndarray

        Output:
        ------
        x: numpy.ndarray
        """
        for i in range(len(x[0])):
            x[0][i] = max(x[0][i], 0)
        return x

    def softmax(self,x):
        """
        Performs the softmax activation function.
        Turns a vector of K real numbers to a vector of K real numbers, each between 0 and 1
        that sum to 1.
        
        Input:
        -----
        x: numpy.ndarray
        
        Output:
        ------
        x: numpy.ndarray            
        """
        e_x = np.exp(x)
        e_y = e_x.sum(axis=1)
        return e_x / e_y
    
    def linear(self,x):
        """
        Performs the linear activation function
        Returns the input without any modification
        
        Input:
        -----
        x: numpy.ndarray
        
        Output:
        ------
        x: numpy.ndarray
        """
        return x

    
    def relu_der(self,x):
        """
        Calculates derivative of relu, used in error back propagation
        If element is <= 0, return 0, else return 1
        
        Input:
        -----
        x: numpy.ndarray
        
        Output:
        ------
        x: numpy.ndarray
        """
        temp = np.array([])
        for i in x[0]:
            if i <= 0:
                temp = np.append(temp,0)
            else:
                temp = np.append(temp,1)
        return temp.reshape(1,len(x[0]))

class Flatten:
    """
    Class used to represent a flat input
    
    Parameters:
    -----------
        name: str
            Used for identification and displaying layer information
        normalize: int
            Used for normalizing the input. Default = 1 (No normalization)
        data: numpy.ndarray 
            Holds the 2D array to be flattened
        prev: Flatten or Dense 
            Specifies the layer before this layer
        next: Flatten or Dense
            Specifies the layer after this layer
    """
    def __init__(self,name = "Flatten",normalize = 1):
        self.name = name
        self.normalize = normalize
        self.data = None
        self.prev = None
        self.next = None
    
    def compute(self):
        """
        Normalizes and converts a 2D array to a 1D array.
        
        Input:
        -----
        data: numpy.matrix
        
        Output:
        ------
        _: numpy.ndarray     
        """
        rows = self.data.shape[1]
        cols = self.data.shape[2]
        return np.matrix.flatten(self.data/self.normalize).reshape(1,rows*cols)
    
    def backprop(self,bp_data):
        """
        Doesnt have any use in Flatten. Written to maintain uniformity between classes
        """
        return bp_data
    
    def update_wt(self):
        """
        Doesnt have any use in Flatten. Written to maintain uniformity between classes
        """
        pass

class Dense(SuperLayer):
    """
    Class used to represent a fully connected layer
    
    Parameters:
    -----------
    name: str
        Used for identification and displaying layer information.
    input_size: int
        Size of the input data. Used to initialize weight matrix.
    output_size: int
        Size of the output data. Used to initialize weight matrix and bias.
    weight: numpy.matrix
        Weights initialzed to random numbers between -0.25, 0.25.
    bias: numpy.ndarray
        Bias values initialized to random numbers between -0.25, 0.25.
    data: numpy.ndarray 
        Holds the data to work upon.
    net: numpy.ndarray 
        Holds the net output produced by multiplying data and weights.
    activation: str
        Specifies the activation function for the layer. Default = "linear"
    output: numpy.ndarray 
        Holds the output produced after applying the activation function.
    prev: Flatten or Dense 
        Specifies the layer before this layer.
    next: Flatten or Dense
        Specifies the layer after this layer.
    lr: double
        Learning rate for the layer. Default = 0.01. 
    delta_wt: numpy.ndarray
        This is used while back propagation to update weights of the layer. Automatically calculated during backpropagation.
    """
    
    def __init__(self,input_size,output_size,lr = 0.01,activation = 'linear',name = "Dense"):
        self.name = name
        self.input_size = input_size
        self.output_size = output_size
        self.weight = np.random.uniform(-0.25,0.25,size = (input_size,output_size))
        self.bias = np.random.uniform(-0.25,0.25,size = (1,output_size))
        self.data = None
        self.net = None
        self.activation = activation
        self.output = None
        self.prev = None
        self.next = None
        self.lr = lr
        self.delta_wt = None

    def compute(self):
        """
        Multiplies the input data with the layer's weights, adds layer's bias and applies the 
        specified activation function. Returns the output as np.ndarray, that serves as the input
        for next layer, or is the final output of the network
        
        Input:
        ------
        data: numpy.ndarray
        
        Output:
        ------
        self.output: numpy.ndarray
        """
        self.net = np.dot(self.data,self.weight)+self.bias
        
        #Checks the activation function specified and calls the appropriate method
        if self.activation == "relu":
            self.output = self.relu(self.net)
        elif self.activation == "softmax":
            self.output = self.softmax(self.net)
        elif self.activation == "linear":
            self.output = self.linear(self.net)
        return self.output

    def backprop(self,bp_data):
        """
        Automatically performs the backpropagation. Takes in a parameter bp_data which is the errors backpropagated for
        layers after this layer. Also calculates new bp_data, which will be used by layer before this layer.
        
        Input:
        -----
        bp_data: numpy.ndarray
            Data from succeeding layers used for back propagation.
            
        Output:
        -------
        bp_data: numpy.ndarray
            Updated input array "bp_data" that will be used by preceeding layers in the network during backpropagation.
        """
        if not self.next: #last layer
            self.delta_wt = np.dot(self.data.T, bp_data)
            return bp_data #no modifications made to bp_data.
        else: #not last layer
            
            #Split the main backpropagation formula into 2 terms t1 and t2 for simplicity.
            t1 = np.dot(self.data.T, self.relu_der(self.net))
            t2 = np.dot(bp_data, self.next.weight.T)
            self.delta_wt = np.multiply(t1, t2)
            
            #Calculating the new bp_data, that will be used by the preceeding layers. New bp_data will include both the 
            #bp_data this layer received from the succeeding layers, and some data from this layer. Split into 2 terms
            #t1 and t2 for simplicity
            t1 = np.multiply(self.next.weight, self.relu_der(self.net).T)
            t2 = bp_data
            bp_data = np.dot(t2, t1.T)
            return bp_data

    def update_wt(self):
        """
        Updates the weight of the layer after each backpropagation
        
        """
        self.weight = self.weight - np.multiply(self.delta_wt, self.lr)

class Network:
    """
    Class to manage  addition of layers, training and testing data in a Neural Network. 
    Defines the architecture of the xNN
    
    Parameters:
    -----------
    layers: list
        Holds a list of all layers in the Neural Network
    ypred: numpy.ndarray 
        Predictions made by the network on test data (xtest)
    curr: Flatten or Dense
        Points to the current layer in the network. This is used to specify the preceeding and succeeding layers of any layer
    out: numpy.ndarray
        Holds the final output of the network
    epoch_loss: list
        Holds the average losses per epoch for all epochs
    epoch_acc: list
        Holds the accuracy per epoch for all epochs
    epoch_time: list
        Holds the time taken per epoch for all epochs
    """
    
    def __init__(self):
        np.random.seed(0)
        self.layers = []
        self.ypred = None
        self.curr = None
        self.out = None
        self.epoch_acc = []
        self.epoch_loss = []
        self.epoch_time = []
    def add(self,layer):
        """
        Adds a new layer to the neural network. Sets the previous and next layer of each layer. 
        When adding the 1st layer, self.curr is set to None. So for the 1st layer, performing
        layer.prev = self.curr will set the layer's previous layer as None, which is how it should be
        After adding the 1st layer, self.curr is set to the 1st layer, and so, when you add 2nd and subsequent
        layers, the previous layer will be correctly set.
        
        Input:
        -----
        layer: Dense or Flatten
            Object of class Dense or Flatten
            
        Output:
        -------
            None
        """
        self.layers.append(layer)
        layer.prev = self.curr
        self.curr = layer
        if layer.prev:
            layer.prev.next = layer
        

    def fit(self,x,y,epochs = 1, validation_split = 0.0):
        """
        Performs forward pass, backpropagation, weightupdation for all layers, for the entire dataset.
        Repeats the process for the number of epochs set by the user. Epochs is set 1 by default.
        
        Input:
        -----
        x: numpy.matrix
            Independent variables of the data.
        y: numpy.matrix
            Dependent variables of the data (Usually the class names)
        epochs: int
            Number of times data should be fit.
        validation_split: double
            The percentage of training data that should be reserved for validation. 
            Data is not shuffled and the trailing "validation_split"% of data is reserved 
            for validation.
            
        Output:
        -------
            None
            
        """
        if validation_split != 0.0:
            split = int((1-validation_split) * x.shape[0])
            val_x = x[split:]
            val_y = y[split:]
            x = x[:split]
            y = y[:split]
        
        print("\nBeginning Training...")
        print("=================================================================================")
        print("Number of epochs: "+str(epochs))
        print("Training dataset size: "+str(x.shape[0]))
        if validation_split != 0.0:
            print("Validation dataset size: "+str(val_x.shape[0])+"\n")
        #One hot encoding of the class labels
        ohe_labels = np.zeros((y.size,y.max()+1))
        ohe_labels[np.arange(y.size),y] = 1
        
        total_start = time.time()        
        for e in range(epochs):
            print("Epoch: "+str(e)+"/"+str(epochs))
            start = time.time()
            temp_error = 0
            progress = "###" #shows a progress bar. Only for asthetics
            for i in range(x.shape[0]):
                #Performs forward pass, backpropagation, weight updation for each data sample and records cummulative 
                #loss for all data samples.
                
                #Forward Pass
                data = x[i,:,:,:]
                for layer in self.layers:
                    #Set the input data for each layer, call the corresponding layer's compute() 
                    #method and pass the data to it. Passing data is redundant.
                    layer.data = data
                    data = layer.compute()
                    
                self.out = data
                
                #Calculating cummulative loss for each epoch
                temp_error += self.lossfunction(ohe_labels[i], self.out)
            
                #Displaying the progress bar
                if i % (x.shape[0]//20) == 0:
                    print(progress,end = "\r")
    
                #Backpropagation
                bp_data = self.out - ohe_labels[i]
                for layer in self.layers[::-1]:
                    #Starting from the last layer, pass the calculated bp_data to backdrop(). This method
                    #returns an updated bp_data, which serves as an input to the next layer.
                    bp_data = layer.backprop(bp_data)
    
                #Weight Updation
                for layer in self.layers:
                    layer.update_wt()
            
            #Recording average loss for each epoch
            self.epoch_loss.append(temp_error / x.shape[0])
            
            if validation_split != 0.0:
                print("\nValidating the model...")
                val_y_pred = self.predict(val_x)
                val_acc = self.accuracy(val_y_pred,val_y.tolist())
                self.epoch_acc.append(val_acc)
                
            #Recording time taken for each epoch
            end = time.time()
            self.epoch_time.append((end-start))
            
                
            print("Time taken: "+str(round(end-start,2))+" sec")
            print("Time per input: "+str(round((end-start)/x.shape[0],3))+" sec")
            print("Average training loss: "+str(round(temp_error/x.shape[0],3)))
            if validation_split != 0.0:
                print("Validation Accuracy "+str(val_acc))
            print("=================================================================================\n")


        self.plot(self.epoch_loss,"Loss","Epoch v/s Loss")
        self.plot(self.epoch_acc,"Accuracy","Epoch v/s Accuracy")
        print("Time taken: "+str(round(time.time()-total_start,2))+" sec")
    
    def predict(self,x):
        """
        Uses the trained neural network and predicts the output for each input sample
        
        Input:
        -----
        x: numpy.matrix
            Independent variables of the test data.
            
        Output:
        -------
        y_pred: list
            List of predictions for each input data sample 
        """
        y_pred = []
        progress = "---" #shows a progress bar. Only for asthetics
        for i in range(x.shape[0]):
            #Displaying the progress bar
            if i % (x.shape[0]//20) == 0:
                print(progress,end = "\r")
                
            data = x[i]
            #Forward Pass
            for layer in self.layers:
                #Set the input data for each layer, call the corresponding layer's compute() 
                #method and pass the data to it. Passing data is redundant.
                layer.data = data
                data = layer.compute()
                
            #Recording the class with highest probability
            y_pred.append(np.argmax(data,axis = 1)[0])   

        self.ypred =  y_pred
        return y_pred
    
    def accuracy(self,pred,true):
        """
        Calculates the accuracy of the predicted classes by comparing them to true classes
        
        Input:
        -----
        pred: list
            Predicted values
        true: list
            True values
            
        Output:
        -------
        acc: double
            Accuracy of the predicted classes.
        """
        if len(pred) != len(true):
            raise Exception("Unequal lengths: "+str(len(pred))+"!="+str(len(true)))
            return 0
        if type(pred).__name__ != "list" or type(true).__name__ != "list":
            raise Exception("Unsupported data types. Please pass both parameters as lists")
            return 0
        acc = 0
        for i in range(len(pred)):
            if pred[i] == true[i]:
                acc += 1
        return acc / len(pred)
    
    def plot(self,x,label,title):
        plt.figure()
        sns.lineplot(x = range(len(x)),y = x)
        plt.legend(labels=[label])
        plt.ylabel(label)
        plt.xlabel("Epoch")
        plt.title(title)

    def lossfunction(self,true,pred):
        """
        Calculates the loss using cross entropy
        
        Input:
        -----
        pred: numpy.ndarray
            Predicted values
        true: list
            True values
        
        Outut:
        ------
        error double
            loss calculated using cross entropy
        """
        error = 0
        for i in range(len(true)):
            error -= (true[i] * np.log2(pred[0][i]))
        return error
    
    def describe(self):
        print("Layer Type\tInput\tOutput\tMACs")
        print("=============================================================")
        for layer in self.layers:
            ltype = layer.name
            try:
                ipsize = str(layer.input_size)
                opsize = str(layer.output_size)
                macs = str(layer.input_size*layer.output_size)
            except AttributeError:
                ipsize = "--"
                opsize = "--"
                macs = "--"
            print(ltype+"\t\t"+ipsize+"\t  "+opsize+"\t  "+macs)
        print("=============================================================")

nw = Network()
flat = Flatten(normalize = 255)
l1 = Dense(784, 1000, 0.01, "relu")
l2 = Dense(1000, 100,0.01, "relu")
l3 = Dense(100, 10,0.01, "softmax")
nw.add(flat)
nw.add(l1)
nw.add(l2)
nw.add(l3)
nw.describe()
nw.fit(x = train_data, y = train_labels, epochs = 5, validation_split = 0.10)
y_pred = nw.predict(test_data)

fin_accuracy = nw.accuracy(y_pred,test_labels[:100].tolist())
print("Final accuracy: "+str(fin_accuracy))

fig = plt.figure(figsize=(DISPLAY_COL_IN, DISPLAY_ROW_IN))
ax  = []
for i in range(DISPLAY_NUM):
    img = test_data[i, :, :, :].reshape((DATA_ROWS, DATA_COLS))
    ax.append(fig.add_subplot(DISPLAY_ROWS, DISPLAY_COLS, i + 1))
    ax[-1].set_title('True: ' + str(test_labels[i]) + ' xNN: ' + str(y_pred[i]))
    plt.imshow(img, cmap='Greys')
plt.show()
