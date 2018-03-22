import numpy as np

rowcount = 2
colcount = 4

width = 43200
height = 17400

tilewidth = 10800
tileheight = 10200

year = '2015'

array = np.zeros(shape=(height, width))
for row in range(0, rowcount):
    for col in range(0, colcount):
        print("parsing file " + str(1 + col + row * colcount))
        
        ascii_grid = np.loadtxt(
                "gpw-v4-population-count-adjusted-to-2015-unwpp-country-totals-rev10_" + year + "_30_sec_asc"
                "/gpw_v4_population_count_adjusted_to_2015_unwpp_country_totals_rev10_" + year + "_30_sec_" + str(
                1 + col + row * colcount) + ".asc", skiprows=6)
        
        for (x, y), value in np.ndenumerate(ascii_grid):
            if value == -9999:
                value = -1
            if not(y % 10 or x % 10):
                print(x + col * tilewidth, y + row * tileheight)
            array[x + col * tilewidth][y + row * tileheight] = value


np.save("gwp_" + year + ".npy", array)

print("done")
