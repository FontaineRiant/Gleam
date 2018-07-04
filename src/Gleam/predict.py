import math

import rasterio
import numpy as np
import keras.models as models
import sys
from utils import preprocess_predict

filename = '2015_south_america.tif'
dataset_folder = '../../data/lightpop_merged/'
dataset = dataset_folder + filename
input_tile_size = 32

if len(sys.argv) < 2:
    print('Missing argument : use model as argument ("models/2018-06-18_18-18-40.h5" for example)')
    exit(0)

print('loading model')
arg = sys.argv[1].strip('-\x93\x96')
cnn = models.load_model(arg)

print('opening raster')

raster = rasterio.open(dataset)
band = raster.read(1)
profile = raster.profile
profile.update(count=1)
width, height = raster.width, raster.height
testX = preprocess_predict(raster, input_tile_size)
raster.close()
testX = np.expand_dims(testX, axis=3)

print('generating raster')

predicted_tiles = cnn.predict(testX, verbose=0)

tiles_x = []
predicted_raster = np.zeros(shape=(raster.height, raster.width))
y = 0
pred_index = 0
while y + input_tile_size < width:
    x = 0
    while x + input_tile_size < height:
        in_tile = band[x: x + input_tile_size, y: y + input_tile_size]
        if np.max(in_tile) <= 0:
            predicted_raster[x: x + input_tile_size, y: y + input_tile_size] = 0
        else:
            weights = in_tile / np.max(in_tile)  # normalize visible light between 0 and 1 to avoid overflows
            weights = np.exp(weights) - 1  # visible light is perceived logarithmically => counteract with exp
            weights = weights / np.sum(weights)  # the sum of all weights must be 1
            predicted_raster[x: x + input_tile_size, y: y + input_tile_size] = predicted_tiles[pred_index] * weights

        pred_index += 1
        x += input_tile_size
    y += input_tile_size

predicted_raster = np.array(predicted_raster)

with rasterio.open('predictions/' + filename, 'w', **profile) as dst:
    dst.write(predicted_raster.astype(rasterio.float32), 1)

print('done !')
