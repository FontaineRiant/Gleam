import rasterio
import numpy as np
import keras.models as models
import sys
from utils import preprocess

dataset = '../../Data/lightpop_merged/2005.tif'
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
testX, _ = preprocess(raster, input_tile_size, input_tile_size, ignore_empty_tiles=False)
testX = np.expand_dims(testX, axis=3)

print('generating raster')

predicted_tiles = cnn.predict(testX, verbose=0)

tiles_x = []
predicted_raster = np.zeros(shape=(raster.height, raster.width))
y = 0
pred_index = 0
while y + input_tile_size < raster.width:
    x = 0
    while x + input_tile_size < raster.height:
        in_tile = band[x: x + input_tile_size, y: y + input_tile_size]
        if np.max(in_tile) <= 0:
            predicted_raster[x: x + input_tile_size, y: y + input_tile_size] = 0
        else:
            tile = predicted_tiles[pred_index] * in_tile / (np.max(in_tile) * input_tile_size * input_tile_size + 1)
            predicted_raster[x: x + input_tile_size, y: y + input_tile_size] = tile

        pred_index += 1
        x += input_tile_size
    y += input_tile_size

predicted_raster = np.array(predicted_raster)

profile = raster.profile
profile.update(count=1)

with rasterio.open('predictions/2005.tif', 'w', **profile) as dst:
    dst.write(predicted_raster.astype(rasterio.float32), 1)
raster.close()

print('done !')
