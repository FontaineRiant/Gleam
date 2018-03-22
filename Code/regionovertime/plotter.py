from rasterstats import zonal_stats, point_query
import os
import pickle

# valid country list : https://unstats.un.org/unsd/methodology/m49/
country = 'France'
stats = {}
stats[country] = {}

for entry in os.scandir('raster'):
    filename, *_, extension = entry.name.split(".")
    if extension != 'tif':
        continue

    global_stats = zonal_stats('borders/ne_10m_admin_0_countries.shp', entry.path,
                               stats="min max mean count sum std median majority minority unique range",
                               all_touched=True,
                               geojson_out=True)


    for c in global_stats:
        if c['properties']['NAME'] == country:
            stats[country][filename] = c['properties']
            break
    print(filename + " done")

pickle.dump(stats, open("stats.p", "wb" ) )

print(stats[country])
