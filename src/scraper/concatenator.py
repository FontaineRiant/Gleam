import os
from PIL import Image


def concat(tiles_directory):
    def get_tile_x_y(filename):
        filename = filename.split(".")[0]
        return filename.split("-")

    maxX, maxY = get_tile_x_y(sorted(os.scandir(tiles_directory), key=lambda entry: entry.name)[-1].name)

    tiles_dimensions = ()
    extension = ""
    for entry in os.scandir(tiles_directory):
        tiles_dimensions = Image.open(entry.path).size
        _, extension = entry.name.split(".")
        break

    merged = Image.new("RGB", (int(maxX) * tiles_dimensions[0], int(maxY) * tiles_dimensions[1]), color="black")

    for entry in os.scandir(tiles_directory):
        x, y = get_tile_x_y(entry.name)
        merged.paste(Image.open(entry.path), (tiles_dimensions[0] * int(x), tiles_dimensions[1] * int(y)))

    merged.save(tiles_directory + "." + extension)
    print(tiles_directory + ": concat done")


