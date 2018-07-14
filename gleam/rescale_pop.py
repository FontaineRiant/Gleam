import rasterio
import numpy as np

directory = '../data/lightpop_merged/'

divide_pop_by = 4

input_files = ['2015_brazil.tif', '2015_colombia.tif', '2015_safrica_namibia.tif', '2015_south_america.tif']

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
