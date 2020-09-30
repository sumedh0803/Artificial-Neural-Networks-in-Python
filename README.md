# Artificial Neural Network without Tensorflow, Keras, PyTorch
---
### Features
0.   Designed an Artificial Neural Network in Python, using numpy library. The ANN had 1 input layer, 2 hidden layers and 1 output layer, and was trained on the MNIST handwritten      digit dataset. Achieved an accuracy of 97%
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
