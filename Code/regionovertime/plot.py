import matplotlib.pyplot as plt
import pickle
import csv

yaxiss = ['sum'] # disponibles : 'mean', 'std', 'median'
countries = pickle.load(open( "stats.pickle", "rb" ))
plt.rcParams["figure.figsize"] = (15,10)

population = []
with open('../../Data/population_per_country.csv', 'rt') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        if row: 
            population.append(row)
            
gdp = []
with open('../../Data/gdp_per_country.csv', 'rt') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        if row: 
            gdp.append(row)

# remove headers
gdp.pop(0)    
population.pop(0)

for yaxis in yaxiss:
    for country, years in countries.items():
        x = []
        y1 = []
        y2 = []
        y3 = []
        
        for year in sorted(years):
            x.append(year[-4:])
            y1.append(years[year][yaxis])
            
            found = False
            for row in population:
                if row[0] == country and row[1] == year[-4:]:
                    y2.append(float(row[3]))
                    found = True
                    break
                
            if not found:
                y2.append(0)
            
            found = False
            for row in gdp:
                if row[0] == country and row[1] == year[-4:]:
                    y3.append(float(row[3]))
                    found = True
                    break
                
            if not found:
                y3.append(0)

        fig = plt.figure()
        ax1 = plt.subplot(3, 1, 1)
        ax1.plot(x, y1)
        ax1.set(xlabel='year', ylabel=yaxis, title='Light intensity (0-63) in ' + str(country) + ' from space')
        ax1.grid()

        ax2 = plt.subplot(3, 1, 2)
        ax2.plot(x, y2)
        ax2.set(xlabel='year', ylabel='population (thousands)', title='')
        ax2.grid()
        
        ax3 = plt.subplot(3, 1, 3)
        ax3.plot(x, y3)
        ax3.set(xlabel='year', ylabel='GDP', title='')
        ax3.grid()

        fig.savefig("plots/" + yaxis + "_" + str(country) + ".png")
        
        plt.close(fig)
print('plots done !')
