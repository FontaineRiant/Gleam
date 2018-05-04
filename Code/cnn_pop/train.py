# nécessite environ 10 Go de RAM disponible, peut prendre jusqu'à 1h

import pandas as pd
import rasterio
import matplotlib.pyplot as plt
import numpy as np
import keras.layers.core as core
import keras.layers.convolutional as conv
import keras.models as models
import keras.utils.np_utils as kutils

def normalize(array):
    array = np.array(array).astype(np.float)
    array = (array - np.amin(array)) / (np.amax(array) - np.amin(array))
    return array

print('opening raster')

train = rasterio.open('../../Data/lightpop_merged/2000_subset.tif')
trainX = normalize(train.read(1))
trainY = normalize(train.read(2))

test = rasterio.open('../../Data/lightpop_merged/2005_subset.tif')
testX = normalize(train.read(1))
testY = normalize(train.read(2))

print('configuring cnn')

nb_epoch = 1 # Change to 100

batch_size = 128
img_rows, img_cols = testX

# last filter makes the input layer for the last perceptron bigger
nb_filters_1 = 32
nb_filters_2 = 64
nb_conv_1 = 32
nb_conv_2 = 8

cnn = models.Sequential()

cnn.add(conv.Convolution2D(nb_filters_1, nb_conv_1, nb_conv_1,  activation="relu", input_shape=(img_rows, img_cols, 1), 
    border_mode='same'))
cnn.add(conv.Convolution2D(nb_filters_1, nb_conv_1, nb_conv_1, activation="relu", border_mode='same'))
cnn.add(conv.MaxPooling2D(strides=(2,2)))

cnn.add(conv.Convolution2D(nb_filters_2, nb_conv_2, nb_conv_2, activation="relu", border_mode='same'))
cnn.add(conv.Convolution2D(nb_filters_2, nb_conv_2, nb_conv_2, activation="relu", border_mode='same'))
cnn.add(conv.MaxPooling2D(strides=(2,2)))

cnn.add(core.Flatten())
cnn.add(core.Dropout(0.2))
cnn.add(core.Dense(4096, activation=None))

cnn.summary()
cnn.compile(loss="mean_squared_error", optimizer="adam", metrics=["mse"])

print('training')

cnn.fit(trainX, trainY, batch_size=batch_size, nb_epoch=nb_epoch, verbose=1)

yPred = cnn.predict_classes(testX)

np.savetxt('trained.csv', np.c_[range(1,len(yPred)+1),yPred], delimiter=',',
    header = 'ImageId,Label', comments = '', fmt='%d')

print('done !')
