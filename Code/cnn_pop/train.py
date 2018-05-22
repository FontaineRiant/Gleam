import pandas as pd
import rasterio
import matplotlib.pyplot as plt
import numpy as np
import keras.layers.core as core
import keras.layers.convolutional as conv
import keras.models as models
import keras.utils.np_utils as kutils
from keras import optimizers
from sklearn.utils import shuffle

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

print('opening raster')

train = rasterio.open('../../Data/lightpop_merged/2000_subset.tif')
trainX = np.expand_dims(tile(train.read(1), input_tile_size), axis=3)
trainY = np.mean(tile(train.read(2), input_tile_size), axis=(1, 2))

trainX, trainY = shuffle(trainX, trainY) # shuffle lists

print(trainX.shape)
img_count, img_rows, img_cols, img_channel_count = trainX.shape
print('image shape : ' + str(trainX.shape))

print('configuring cnn')

nb_epoch = 100

batch_size = 1 # nombre de mesures avant d'update les poids

# last filter makes the input layer for the last perceptron bigger
nb_filters_1 = 32
nb_filters_2 = 32
nb_conv_1 = 3
nb_conv_2 = 3

cnn = models.Sequential()
cnn.add(conv.Convolution2D(filters=nb_filters_1, kernel_size=(nb_conv_1, nb_conv_1), activation="relu", border_mode='same',
    input_shape=(img_rows, img_cols, img_channel_count)))
cnn.add(conv.MaxPooling2D(strides=(2,2)))

cnn.add(conv.Convolution2D(filters=nb_filters_2, kernel_size=(nb_conv_2, nb_conv_2), activation="relu", border_mode='same'))
cnn.add(conv.MaxPooling2D(strides=(2,2)))

cnn.add(core.Flatten())
cnn.add(core.Dropout(0.2))
cnn.add(core.Dense(32))
cnn.add(core.Dense(1))

cnn.summary()
cnn.compile(loss="mean_squared_error", optimizer=optimizers.Adam(lr=0.001), metrics=["mse", "mae"])

print('training')

hist = cnn.fit(trainX, trainY, batch_size=batch_size, epochs=nb_epoch, verbose=1)

cnn.save('model.h5')

plt.plot(hist.history["loss"])
plt.title("model loss")
plt.ylabel("loss")
plt.xlabel("epoch")
plt.legend(["train"], loc="upper left")
plt.savefig("epochs.png")

print('done !')
