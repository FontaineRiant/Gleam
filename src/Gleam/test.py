import rasterio
import numpy as np
import keras.models as models
import sys
from utils import preprocess

dataset = '../../data/lightpop_merged/2015_brazil.tif'
input_tile_size = 32

if len(sys.argv) < 2:
    print('Missing argument : use model as argument ("models/2018-06-18_18-18-40.h5" for example)')
    exit(0)

print('loading model')
arg = sys.argv[1].strip('-\x93\x96')
cnn = models.load_model(arg)

print('opening raster')

raster = rasterio.open(dataset)
testX, testY = preprocess(raster, input_tile_size, 8)
raster.close()
testX = np.expand_dims(testX, axis=3)

print('mean pop in tiles : ' + str(np.mean(testY)))
print('pop standard deviation in tiles : ' + str(np.std(testY)))

print('testing ...')

evaluation = cnn.evaluate(testX, testY, verbose=2, batch_size=1024)
evaluation = dict(zip(cnn.metrics_names, evaluation))

print('Mean squared error (loss) = ' + str(evaluation['mean_squared_error']))
print('Mean absolute error (loss) = ' + str(evaluation['mean_absolute_error']))
print('Sum of absolute errors (loss) = ' + str(evaluation['mean_absolute_error'] * len(testY)))

print('done !')