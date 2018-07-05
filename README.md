# La Terre de nuit vue de l'espace

Ce projet a été réalisé dans le cadre d'un travail de bachelor de la HEIG-VD.
Il s'agit d'une collection ne notebooks ayant servi à explorer différentes données géographiques, et permettant
d'entraîner un réseau de neurones à convolutions capable de prédire la répartition de la population d'une région
à partir d'une image satellite de celle-ci.

# Installation

Sur Windows, certains paquets scientifiques ne sont pas compatibles. Il s'agit de shapely, gdal, fiona et rasterio.
Il est nécessaire de les télécharger et les installer manuellement depuis https://www.lfd.uci.edu/~gohlke/pythonlibs/.

Sur tous les systèmes d'exploitation, il faut ensuite lancer la commande :

'''
pip install -r src/requirements.txt
'''

(optionnel) Pour activer le calcul sur GPU, suivre le [tutoriel de Tensorflow](https://www.tensorflow.org/install/).

# Utilisation

TODO : fix paths

# Notebooks
Chaque notebook se trouve dans le répertoire src/ puis dans un dossier du même nom que le notebook.

## country_stats
Cet ensemble de scripts permet d'extraire la somme de luminosité émise pour chaque pays, et de mettre ces données
en relation avec diverses données par pays à l'aide de graphes.

## gleam
Ce notebook effectue un prétraitement sur une image satellite et une grille de population pour entraîner un
réseau de neurones et prédire la répartition de la population à partir d'une autre image satellite.

## rastercomparator
Ce notebook peut mettre en relation deux rasters pour en tirer un nuage de point des valeurs de chaque pixel sur les
deux rasters, ainsi que compiler la différence entre ces deux rasters afin de visualiser la différence d'une année à
l'autre par exemple.

## viirs_extractor
Ce notebook répond au besoin spécique d'extraire les données très volumineuses de la NOAA et d'en faire la médiane pour
chaque année.