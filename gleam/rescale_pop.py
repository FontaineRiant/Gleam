import rasterio
import numpy as np

## PARAMETERS ##
directory = '../data/lightpop_merged/'

input_files = ['2015_portugal.tif']

divide_pop_by = 4
################

for input_file in input_files:
    reference = rasterio.open(directory + input_file)
    profile = reference.profile

    # write to output file
    with rasterio.open(directory + 'adj_' + input_file, 'w', **profile) as dst:
        dst.write(reference.read(1).astype(rasterio.float32), 1)
        dst.write(reference.read(2).astype(rasterio.float32) / divide_pop_by, 2)
    reference.close()

    print('converted ' + input_file)

print('done !')
