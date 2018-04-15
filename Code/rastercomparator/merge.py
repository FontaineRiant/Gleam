from rasterstats import zonal_stats, point_query
import numpy as np

outputs = ['2000', '2005', '2010']

lightrasters = ['../../Data/lightrasters_noaa/F152000.v4b.avg_lights_x_pct.tif',
    '../../Data/lightrasters_noaa/F162005.v4b.avg_lights_x_pct.tif',
    '../../Data/lightrasters_noaa/F182010.v4b.avg_lights_x_pct.tif']

poprasters = ['../../Data/poprasters_sedac/gpw_v4_population_count_adjusted_to_2015_unwpp_country_totals_rev10_2000_30_sec.tif',
    '../../Data/poprasters_sedac/gpw_v4_population_count_adjusted_to_2015_unwpp_country_totals_rev10_2005_30_sec.tif',
    '../../Data/poprasters_sedac/gpw_v4_population_count_adjusted_to_2015_unwpp_country_totals_rev10_2010_30_sec.tif']

for output, lightraster, popraster in zip(outputs, lightrasters, poprasters):
    with rasterio.open(lightrasters[0]) as src0:
        meta = src0.meta
    
    meta.update(count = 2)

    # Read each layer and write it to stack
    with rasterio.open(output+'.tif', 'w', **meta) as dst:
        with rasterio.open(lightraster) as src:
            dst.write_band(1, src.read(1))
        with rasterio.open(popraster) as src:
            dst.write_band(2, src.read(1))

    #print("coeff "+ output +" : "+str(np.corrcoef(lr_values, pr_values)))