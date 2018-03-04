import urllib.request as ur
import os


def scrape(year, zoom, folder_name):

    image_retriever = ur.URLopener()

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    x = 0
    y = 0
    looping = True
    while looping:
        try:
            print("retrieving " + str(x) + "_" + str(y) + "...")
            image_retriever.retrieve(
                "https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/VIIRS_Night_Lights/default/"
                + year + "-01-01/500m/" + str(zoom) + "/" + str(y) + "/" + str(x) + ".png",
                folder_name + "/%03d" % x + "-%03d" % y + ".png")
        except IOError:
            print("end of line")
            y += 1
            x = 0
            try:
                print("retrieving new line")
                image_retriever.retrieve(
                    "https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/VIIRS_Night_Lights/default/"
                    + year + "-01-01/500m/" + str(zoom) + "/" + str(y) + "/" + str(x) + ".png",
                    folder_name + "/%03d" % x + "-%03d" % y + ".png")
            except IOError:
                print("end of row and map")
                looping = False
        x += 1

    print("year " + year + ", zoom " + str(zoom) + ": scraping done")
