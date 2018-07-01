import rasterio
import numpy as np
import keras.layers.core as core
import keras.layers.convolutional as conv
import keras.models as models
from keras import optimizers
import time
import keras.callbacks
from utils import preprocess
from keras import regularizers

dataset = '../../data/lightpop_merged/2000_usa.tif'
input_tile_size = 32

print('opening raster')

raster = rasterio.open(dataset)
trainX, trainY = preprocess(raster, input_tile_size, 8)
raster.close()
weights = trainY
trainX = np.expand_dims(trainX, axis=3)

img_count, img_rows, img_cols, img_channel_count = trainX.shape
print('image shape : ' + str(trainX.shape))

print('configuring cnn')

nb_epoch = 1000

# last filter makes the input layer for the last perceptron bigger
nb_filters_1 = 32
nb_filters_2 = 32
nb_filters_3 = 64
kernel_size = (3, 3)

cnn = models.Sequential()
cnn.add(conv.Convolution2D(filters=nb_filters_1, kernel_size=kernel_size, activation="relu", padding='same',
                           input_shape=(img_rows, img_cols, img_channel_count)))

cnn.add(conv.Convolution2D(filters=nb_filters_2, kernel_size=kernel_size, activation="relu", padding='same',
                           input_shape=(img_rows, img_cols, img_channel_count)))
						   
cnn.add(conv.MaxPooling2D(strides=(2, 2)))

cnn.add(conv.Convolution2D(filters=nb_filters_3, kernel_size=kernel_size, activation="relu", padding='same',
                           input_shape=(img_rows, img_cols, img_channel_count)))

cnn.add(conv.MaxPooling2D(strides=(2, 2)))

cnn.add(core.Flatten())
cnn.add(core.Dropout(0.2))
cnn.add(core.Dense(256))
cnn.add(core.Dense(1))

cnn.summary()
cnn.compile(loss="mean_squared_error", optimizer=optimizers.Adam(lr=0.01, decay=0.0), metrics=["mse", "mae"])

# logs for tensorboard
time = time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime())
tensorboard = keras.callbacks.TensorBoard(log_dir="logs/" + str(time))

# checkpoints
checkpoint = keras.callbacks.ModelCheckpoint('models/' + str(time) + '.h5', save_weights_only=False)

# reduce learning rate when we stopped learning anything
rlrp = keras.callbacks.ReduceLROnPlateau(monitor='loss', factor=0.5, patience=15, verbose=1, mode='auto', min_lr=0.00001)

print('training')

cnn.fit(trainX, trainY, batch_size=1024, epochs=nb_epoch, verbose=2, callbacks=[tensorboard, checkpoint, rlrp],
        sample_weight=None)

cnn.save('models/' + str(time) + '.h5')

print('model saved to models/' + time + '.h5')
print('logs saved to logs/' + time)

print('done !')
