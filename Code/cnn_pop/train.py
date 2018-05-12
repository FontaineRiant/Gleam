
import pandas as pd
import rasterio
import matplotlib.pyplot as plt
import numpy as np
import keras.layers.core as core
import keras.layers.convolutional as conv
import keras.models as models
import keras.utils.np_utils as kutils

input_tile_size = 32
outputs_per_tile = 1

def normalize(array):
    array = np.array(array).astype('float32')
    array = (array - np.amin(array)) / (np.amax(array) - np.amin(array))
    return array

def tile(matrix, tile_size):
    y = 0
    tiles = []
    while (y + tile_size < matrix.shape[1]):
        x = 0
        while(x + tile_size < matrix.shape[0]):
            tiles.append(matrix[x: x + tile_size, y: y + tile_size])
            x += tile_size
        y += tile_size
    tiles = np.array(tiles)
    return tiles[:100]

print('opening raster')

train = rasterio.open('../../Data/lightpop_merged/2000_subset.tif')
trainX = np.expand_dims(tile(normalize(train.read(1)), input_tile_size), axis=3)
trainY = np.expand_dims(np.mean(tile(normalize(train.read(2)), input_tile_size), axis=2), axis=3)

test = rasterio.open('../../Data/lightpop_merged/2005_subset.tif')
testX = np.expand_dims(tile(normalize(test.read(1)), input_tile_size), axis=3)
testY = np.expand_dims(np.mean(tile(normalize(test.read(2)), input_tile_size), axis=2), axis=3)

print(trainX.shape)
img_count, img_rows, img_cols, img_channel_count = trainX.shape
print('image shape : ' + str(trainX.shape))

print('configuring cnn')

nb_epoch = 1 # Change to 100

batch_size = 1


# last filter makes the input layer for the last perceptron bigger
nb_filters_1 = 2
nb_filters_2 = 64
nb_conv_1 = 5
nb_conv_2 = 4

cnn = models.Sequential()
cnn.add(conv.Convolution2D(filters=nb_filters_1, kernel_size=(nb_conv_1, nb_conv_1), activation="relu", border_mode='same',
    input_shape=(img_rows, img_cols, img_channel_count)))
#cnn.add(conv.MaxPooling2D(strides=(2,2)))

#cnn.add(conv.Convolution2D(filters=nb_filters_2, kernel_size=(nb_conv_2, nb_conv_2), activation="relu", border_mode='same'))
#cnn.add(conv.MaxPooling2D(strides=(2,2)))

#cnn.add(core.Dropout(0.2))
cnn.add(core.Dense(1))

cnn.summary()
cnn.compile(loss="mean_squared_error", optimizer="adam", metrics=["mse"])

print('training')

cnn.fit(trainX, trainY, batch_size=batch_size, epochs=nb_epoch, verbose=1)

cnn.save('model.h5')

print('done !')
