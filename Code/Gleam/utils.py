import numpy as np


def preprocess(raster, tile_size, offset, ignore_empty_tiles=True):
    matrix_x = raster.read(1)
    matrix_y = raster.read(2)

    tiles_x = []
    tiles_y = []
    y = 0
    while y + tile_size < matrix_x.shape[1]:
        x = 0
        while x + tile_size < matrix_x.shape[0]:
            pop = np.sum(matrix_y[x: x + tile_size, y: y + tile_size])
            if pop > 0 or not ignore_empty_tiles:
                tiles_x.append(matrix_x[x: x + tile_size, y: y + tile_size])
                tiles_y.append(pop)

            x += offset
        y += offset
    return np.array(tiles_x), np.array(tiles_y)
