# nécessite environ 10 Go de RAM disponible, peut prendre jusqu'à 1h

import rasterio
import matplotlib.pyplot as plt
import numpy as np

logscale = False # needs probably more RAM than you can have, not recommended
year = '2000'

valuesX = []
valuesY = []
valuesZ = []

raster = rasterio.open('../../data/lightpop_merged/'+ year + '.tif')
valuesX = raster.read(1) # first band
valuesY = raster.read(2)

# normalize Z
#valuesZ = np.array(valuesZ).astype(np.float)
#valuesZ = (valuesZ - np.amin(valuesZ)) / (np.amax(valuesZ) - np.amin(valuesZ))
    
fig = plt.figure()
ax1 = plt.subplot(1, 1, 1)

if logscale:
    plt.xscale('log')
    plt.yscale('log')
ax1.scatter(valuesX, valuesY, alpha=0.01)
ax1.set(xlabel='?', ylabel='?')
ax1.grid()

if logscale:
    fig.savefig("scatters/" + year + "_logscale.png")
else:
    fig.savefig("scatters/" + year + ".png")

plt.close(fig)

print('plots done !')
