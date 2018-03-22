import concatenator
import scraper

zoom = 6  # on a scale of 0 to 7 (1km/pixel : 6)
years = ["2012", "2016"]  # 2012 or 2016

for year in years:
    folder_name = "tiles_" + str(year) + "_zoom" + str(zoom)
    scraper.scrape(year, zoom, folder_name)
    concatenator.concat(folder_name)
    # TODO : resize png
    # TODO : read png as a matrix, compare to GWP
