import pickle
import csv

# parameters
year_from = '2008'
year_to = '2013'

# loads preprocessed data
countries = pickle.load(open( "stats.pickle", "rb" ))

stats_by_country = {}

# get light sum for each year
for country, years in countries.items():
    for year in years:
        if year_from == year[-4:] or year_to == year[-4:]:
            if country not in stats_by_country:
                stats_by_country[country] = {'country':country}
            stats_by_country[country][year[-4:]] = years[year]['sum']

# compute deltas
for country in stats_by_country:
    if stats_by_country[country][year_from] == 0:
        stats_by_country[country]['delta'] = float('inf')
    else:
        stats_by_country[country]['delta'] = stats_by_country[country][year_to] / stats_by_country[country][year_from]

# write to csv
with open('lightdeltas.csv', 'w', newline='') as csvfile:
    fieldnames = ['country', year_from, year_to, 'delta']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',', quotechar='"')

    writer.writeheader()
    for country in stats_by_country:
        writer.writerow(stats_by_country[country])