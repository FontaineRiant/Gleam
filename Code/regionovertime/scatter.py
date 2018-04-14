import matplotlib.pyplot as plt
import pickle
import csv

# charge les données préprocessed
countries = pickle.load(open( "stats.pickle", "rb" ))
plt.rcParams["figure.figsize"] = (15,10)

graphs = {}

# charge les csv (format : [pays, année, _ , valeur])
graphs['population'] = []
with open('../../Data/population_per_country.csv', 'rt') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        if row: 
            graphs['population'].append(row)
            
graphs['gdp'] = []
with open('../../Data/gdp_per_country.csv', 'rt') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        if row: 
            graphs['gdp'].append(row)

graphs['energy'] = []
with open('../../Data/electricity_consumption_per_country.csv', 'rt') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        if row: 
            graphs['energy'].append(row)

for k, g in graphs.items() :
    g.pop(0)

    valuesX = []
    valuesY = []

    for country, years in countries.items():
        for year in years:
            for row in g:
                if row[0] == country and row[1] == year[-4:]:
                    valuesX.append(float(row[3]))
                    valuesY.append(years[year]['sum']) # disponibles : 'mean', 'std', 'median', 'sum'
                    break
        
    fig = plt.figure()
    ax1 = plt.subplot(1, 1, 1)

    #plt.xscale('log')
    #plt.yscale('log')
    ax1.scatter(valuesX, valuesY, alpha=0.2)
    ax1.set(xlabel=k, ylabel='Light')
    ax1.grid()

    fig.savefig("scatters/" + k + "-light.png")

    plt.close(fig)

print('plots done !')
