import urllib
import datetime

image = urllib.URLopener()

date = datetime.date(2016, 12, 1)
# while date != datetime.date(2018, 2, 21):
#    image.retrieve("https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/VIIRS_SNPP_DayNightBand_ENCC/default/"
#                   + date.strftime('%Y-%m-%d') + "/500m/5/4/20.png", "tiles/" + date.strftime('%Y-%m-%d') + ".png")
#    date += datetime.timedelta(days=1)
#    print("fetched " + date.strftime('%Y-%m-%d') + ".png")

x = 0
y = 0
zoom = 1
looping = True
while looping:
    try:
        print("retrieving ...")
        image.retrieve("https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/VIIRS_Night_Lights/default/"
                       "2016-01-01/500m/" + str(zoom) + "/" + str(y) + "/" + str(x) + ".png",
                       "tiles/" + str(x) + "-" + str(y) + ".png")
    except IOError:
        print("end of line")
        ++y
        x = 0
        try:
            print("retrieving new line")
            image.retrieve("https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/VIIRS_Night_Lights/default/"
                           "2016-01-01/500m/" + str(zoom) + "/" + str(y) + "/" + str(x) + ".png",
                           "tiles/" + str(x) + "-" + str(y) + ".png")
        except IOError:
            print("end of row and map")
            looping = False
    ++x
print("done")
