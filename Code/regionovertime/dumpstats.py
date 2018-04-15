from rasterstats import zonal_stats, point_query
import os
import pickle

stats = {}

# valid country list : https://unstats.un.org/unsd/methodology/m49/

for entry in os.scandir('../../Data/lightrasters_noaa'):
    filename, *_, extension = entry.name.split(".")
    if extension != 'tif':
        continue

    global_stats = zonal_stats('../../Data/borders/ne_10m_admin_0_countries.shp', entry.path,
                               stats="mean sum std median",
                               all_touched=True,
                               geojson_out=True)

    for c in global_stats:
        print(c['properties']['ECONOMY'])
        name = c['properties']['NAME_SORT']

        if name is None:
            name = c['properties']['NAME']
        
        if name not in stats:
            stats[name] = {}
        
        stats[name][filename] = c['properties']
            
    print(filename + " done")

pickle.dump(stats, open("stats.pickle", "wb" ))
print("all done !")
