import os
import rasterio
import numpy as np

monthly_dir = '../../data/lightrasters_noaa/monthly/'
yearly_dir = '../../data/lightrasters_noaa/'
window_size = 7500

output_files = {}

for filename in os.listdir(monthly_dir):
    if filename.endswith('.tif'):
        # get year and region of the observation
        year = filename[filename.find('-') + 1: filename.find('-') + 5]
        region = filename[filename.find('-') + 10: filename.find('-') + 17]

        if (year, region) not in output_files:
            output_files[(year, region)] = []
        # group files by same year and region
        output_files[(year, region)].append(filename)

print('fetched file names')

# iterate over windows of every raster of the same region/year to compute their median pixels
for (year, region), input_files in output_files.items():
    # get the metadat to be used for the output file (same as input)
    reference = rasterio.open(monthly_dir + input_files[0])
    profile = reference.profile
    dimensions = (reference.height, reference.width)
    reference.close()

    # initialize matrix for the output file
    raster = np.zeros(dimensions)

    y_offset = 0
    while y_offset < dimensions[1]:
        x_offset = 0
        while x_offset < dimensions[0]:
            windows = []
            for input_file in input_files:
                with rasterio.open(monthly_dir + input_file) as src:
                    windows.append(src.read(1, window=((x_offset, x_offset + window_size),
                                                       (y_offset, y_offset + window_size))))

            # compute mediant for each point between windows, store result to raster
            raster[x_offset: x_offset + window_size, y_offset: y_offset + window_size] = np.median(windows, axis=0)
            x_offset += window_size
        y_offset += window_size

    # write to output file
    with rasterio.open(yearly_dir + year + '_' + region + '.tif', 'w', **profile) as dst:
        dst.write(raster.astype(rasterio.float32), 1)

    print('generated ' + year + '_' + region + '.tif')
    # remove monthly observations files
    for input_file in input_files:
        os.remove(monthly_dir + input_file)

print('done !')
