import rasterio
import numpy as np
import keras.models as models
import sys

input_tile_size = 32
outputs_per_tile = 1


def preprocess(raster, tile_size):
    matrix_x = raster.read(1)
    matrix_y = raster.read(2)

    tiles_x = []
    tiles_y = []
    y = 0
    while y + tile_size < matrix_x.shape[1]:
        x = 0
        while x + tile_size < matrix_x.shape[0]:
            pop = np.sum(matrix_y[x: x + tile_size, y: y + tile_size])
            if pop > 0:
                tiles_x.append(matrix_y[x: x + tile_size, y: y + tile_size])
                tiles_y.append(pop)

            x += 8
        y += 8
    return np.array(tiles_x), np.array(tiles_y)


if len(sys.argv) < 2:
    print('Missing argument : use model name as argument ("2018-06-18_18-18-40.h5" for example)')
    exit(0)

print('loading model')
arg = sys.argv[1].strip('-\x93\x96')
cnn = models.load_model('models/' + arg)

print('opening raster')

testX, testY = preprocess(rasterio.open('../../Data/lightpop_merged/2005.tif'), input_tile_size)
testX = np.expand_dims(testX, axis=3)

print('mean pop in tiles : ' + str(np.mean(testY)))
print('pop standard deviation in tiles : ' + str(np.std(testY)))

print('testing ...')

evaluation = cnn.evaluate(testX, testY, verbose=2, batch_size=2048)

print(dict(zip(cnn.metrics_names, evaluation)))

print('done !')
