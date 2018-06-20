import rasterio
import numpy as np
import keras.layers.core as core
import keras.layers.convolutional as conv
import keras.models as models
from keras import optimizers
import time
import keras.callbacks

input_tile_size = 32
outputs_per_tile = 1


def preprocess(raster, tile_size):
    matrix_x = raster.read(1)
    matrix_y = raster.read(2)

    tiles_x = []
    tiles_y = []
    weights = []
    y = 0
    while y + tile_size < matrix_x.shape[1]:
        x = 0
        while x + tile_size < matrix_x.shape[0]:
            pop = np.sum(matrix_y[x: x + tile_size, y: y + tile_size])
            if pop > 0:
                tiles_x.append(matrix_y[x: x + tile_size, y: y + tile_size])
                tiles_y.append(pop)
                weights.append(pop)

            x += 8
        y += 8
    return np.array(tiles_x), np.array(tiles_y), np.array(weights)


print('opening raster')

trainX, trainY, weights = preprocess(rasterio.open('../../Data/lightpop_merged/2000.tif'), input_tile_size)
trainX = np.expand_dims(trainX, axis=3)

img_count, img_rows, img_cols, img_channel_count = trainX.shape
print('image shape : ' + str(trainX.shape))

print('configuring cnn')

nb_epoch = 50

# last filter makes the input layer for the last perceptron bigger
nb_filters_1 = 32
nb_filters_2 = 32
nb_conv_1 = 3
nb_conv_2 = 3

cnn = models.Sequential()
cnn.add(conv.Convolution2D(filters=nb_filters_1, kernel_size=(nb_conv_1, nb_conv_1), activation="relu", padding='same',
                           input_shape=(img_rows, img_cols, img_channel_count)))
cnn.add(conv.MaxPooling2D(strides=(2, 2)))

cnn.add(conv.Convolution2D(filters=nb_filters_2, kernel_size=(nb_conv_2, nb_conv_2), activation="relu", padding='same'))
cnn.add(conv.MaxPooling2D(strides=(2, 2)))

cnn.add(core.Flatten())
cnn.add(core.Dropout(0.2))
cnn.add(core.Dense(32))
cnn.add(core.Dense(1))

cnn.summary()
cnn.compile(loss="mean_squared_error", optimizer=optimizers.Adam(lr=0.001), metrics=["mse", "mae"])

# logs for tensorboard
time = time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime())
tensorboard = keras.callbacks.TensorBoard(log_dir="logs/" + str(time))

# checkpoints
checkpoint = keras.callbacks.ModelCheckpoint('models/' + str(time) + '.h5', save_weights_only=False)

# reduce learning rate when we stopped learning anything
keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=10, verbose=1, mode='min', min_lr=0.0001)

print('training')

cnn.fit(trainX, trainY, batch_size=8, epochs=nb_epoch, verbose=2, callbacks=[tensorboard, checkpoint],
        sample_weight=weights)

cnn.save('models/' + str(time) + '.h5')

print('model saved to models/' + time)
print('logs saved to logs/' + time)

print('done !')
