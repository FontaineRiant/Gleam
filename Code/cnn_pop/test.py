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
    return tiles

print('loading model')
cnn = models.load_model('model.h5')

print('opening raster')

train = rasterio.open('../../Data/lightpop_merged/2000_subset.tif')
trainX = np.expand_dims(tile(train.read(1), input_tile_size), axis=3)
trainY = np.mean(tile(train.read(2), input_tile_size), axis=(1, 2))

test = rasterio.open('../../Data/lightpop_merged/2005_subset.tif')
testX = np.expand_dims(tile(test.read(1), input_tile_size), axis=3)
testY = np.mean(tile(test.read(2), input_tile_size), axis=(1, 2))

print('testing ...')

evaluation = cnn.evaluate(testX, testY, verbose=1)

print(dict(zip(cnn.metrics_names, evaluation)))

predictedY = cnn.predict(testX)

print('done !')
