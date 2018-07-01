import rasterio
import numpy as np
import sys

dataset1 = '../../data/lightrasters_noaa/F101992.v4b.avg_lights_x_pct.tif'
dataset2 = '../../data/lightrasters_noaa/F182013.v4c.avg_lights_x_pct.tif'
out = '1992-2013.tif'

print('opening rasters')

raster1 = rasterio.open(dataset1)
raster2 = rasterio.open(dataset2)

print('generating raster')

raster3 = raster2.read(1) - raster1.read(1)

profile = raster1.profile
profile.update(count=1)

with rasterio.open(out, 'w', **profile) as dst:
    dst.write(raster3.astype(rasterio.float32), 1)
raster1.close()
raster2.close()
print('done !')
