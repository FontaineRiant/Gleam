
# créé des scatterplots à partir du fichier stats.pickle et des données csv

import matplotlib.pyplot as plt
import pickle
import csv
import numpy as np

logscale = True
graph_year = '2013'

# charge les données préprocessed
countries = pickle.load(open( "stats.pickle", "rb" ))
plt.rcParams["figure.figsize"] = (15,10)

csv_data = {}

# charge les csv (format : [pays, année, _ , valeur])
csv_data['population'] = []
with open('../../Data/population_per_country.csv', 'rt') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        if row: 
            csv_data['population'].append(row)
            
csv_data['gdp'] = []
with open('../../Data/gdp_per_country.csv', 'rt') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        if row: 
            csv_data['gdp'].append(row)

csv_data['energy'] = []
with open('../../Data/electricity_consumption_per_country.csv', 'rt') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        if row: 
            csv_data['energy'].append(row)

# parcours les datasets csv
for k, g in csv_data.items() :
    g.pop(0)

    valuesX = []
    valuesY = []
    valuesZ = []

    # parcours les données de lumière par pays
    for country, years in countries.items():
        # parcours les données du pays par année
        for year in years:
            if not year[-4:] == graph_year:
                continue
            # cherche la ligne du csv correspondant au pays
            for row in g:
                if row[0] == country and row[1] == year[-4:]:
                    valuesX.append(float(row[3]))
                    valuesY.append(years[year]['sum']) # disponibles : 'mean', 'std', 'median', 'sum'
                    valuesZ.append(years[year]['ECONOMY'])
                    break
                
    # normalize Z
    #valuesZ = np.array(valuesZ).astype(np.float)
    #valuesZ = (valuesZ - np.amin(valuesZ)) / (np.amax(valuesZ) - np.amin(valuesZ))
    
    fig = plt.figure()
    ax1 = plt.subplot(1, 1, 1)

    if logscale:
        plt.xscale('log')
        plt.yscale('log')
    
    uniqueZ = list(set(valuesZ))
    colors = [plt.cm.jet(float(i[0])/7) for i in sorted(uniqueZ)]
    
    #ax1.scatter(valuesX, valuesY, alpha=1.0, c=valuesZ)
    for i, u in enumerate(sorted(uniqueZ)):
        xi = [valuesX[j] for j  in range(len(valuesX)) if valuesZ[j] == u]
        yi = [valuesY[j] for j  in range(len(valuesY)) if valuesZ[j] == u]
        ax1.scatter(xi, yi, c=colors[i], label=str(u))
    
    ax1.set(xlabel=k, ylabel='Light')
    ax1.legend()
    ax1.grid()

    fig.savefig("scatters/" + str(k) + "-light.png")

    plt.close(fig)
    print(str(k)+" pearson coefficient : \n"+str(np.corrcoef(valuesX, valuesY)))

print('plots done !')
