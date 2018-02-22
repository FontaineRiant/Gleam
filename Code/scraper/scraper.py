import urllib
import datetime

image = urllib.URLopener()

date = datetime.date(2016, 12, 1)
while date != datetime.date(2018, 2, 21):
    image.retrieve("https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/VIIRS_SNPP_DayNightBand_ENCC/default/"
                   + date.strftime('%Y-%m-%d') + "/500m/5/4/20.png", "tiles/" + date.strftime('%Y-%m-%d') + ".png")
    date += datetime.timedelta(days=1)
    print("fetched " + date.strftime('%Y-%m-%d') + ".png")

print("done")
