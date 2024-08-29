# -*- coding: utf-8 -*-
"""
Créé le vendredi 26 mai 2023 à 15h35
"""

import rasterio
from rasterio.warp import reproject
import numpy
from rasterio.enums import Resampling
from tkinter import Tk, filedialog
import os

# Ouvrir la fenêtre de dialogue pour sélectionner le fichier d'entrée
root = Tk()
root.withdraw()
input_file = filedialog.askopenfilename(title="Sélectionnez le fichier TIF d'entrée")

# Vérifier si le fichier a été sélectionné
if not input_file:
    print("Aucun fichier sélectionné.")
    exit()

# Ouvrir le fichier d'entrée
with rasterio.open(input_file) as src:
    # Définir la fenêtre de dialogue pour sélectionner le dossier de sortie
    output_dir = filedialog.askdirectory(title="Sélectionnez le dossier de sortie")

    # Vérifier si le dossier a été sélectionné
    if not output_dir:
        print("Aucun dossier de sortie sélectionné.")
        exit()

    # Définir le chemin complet pour le fichier de sortie
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = os.path.join(output_dir, base_name + "_Reechantillon.tif")

    # Définir l'échelle de rééchantillonnage souhaitée
    facteur_echelle = 2  # Facteur d'échelle de 0,5 pour réduire de moitié

    # Calculer les nouvelles dimensions
    nouvelle_largeur = int(src.width * facteur_echelle)
    nouvelle_hauteur = int(src.height * facteur_echelle)

    # Définir les options de rééchantillonnage
    options_reechantillonnage = {
        'width': nouvelle_largeur,
        'height': nouvelle_hauteur,
        'transform': src.transform * src.transform.scale(facteur_echelle, facteur_echelle)
    }

    # Créer un tableau vide pour stocker l'image rééchantillonnée
    image_reechantillonnee = numpy.zeros((src.count, nouvelle_hauteur, nouvelle_largeur), dtype=src.dtypes[0])

    # Réaliser le rééchantillonnage
    for i in range(src.count):
        reproject(
            source=rasterio.band(src, i+1),
            destination=image_reechantillonnee[i],
            src_transform=src.transform,
            src_crs=src.crs,
            dst_transform=options_reechantillonnage['transform'],
            dst_crs=src.crs,
            resampling=Resampling.bilinear
        )

    # Enregistrer le fichier de sortie
    profile = src.profile
    profile.update(**options_reechantillonnage)
    
# Calculer les limites du bounding box des valeurs non nulles
indices_non_nuls = numpy.nonzero(image_reechantillonnee != 0)
min_ligne = numpy.min(indices_non_nuls[1])
max_ligne = numpy.max(indices_non_nuls[1])
min_colonne = numpy.min(indices_non_nuls[2])
max_colonne = numpy.max(indices_non_nuls[2])

# Ajuster les dimensions et la transformation en fonction du bounding box
nouvelle_largeur = max_colonne - min_colonne + 1
nouvelle_hauteur = max_ligne - min_ligne + 1
options_reechantillonnage['width'] = nouvelle_largeur
options_reechantillonnage['height'] = nouvelle_hauteur
options_reechantillonnage['transform'] = rasterio.transform.from_origin(
    options_reechantillonnage['transform'].xoff + min_colonne * options_reechantillonnage['transform'].a,
    options_reechantillonnage['transform'].yoff + min_ligne * options_reechantillonnage['transform'].e,
    options_reechantillonnage['transform'].a,
    options_reechantillonnage['transform'].e
)

# Recadrer l'image rééchantillonnée en fonction du bounding box
image_reechantillonnee = image_reechantillonnee[:, min_ligne:max_ligne+1, min_colonne:max_colonne+1]

# Mettre à jour les profils avec les nouvelles dimensions
profile['width'] = nouvelle_largeur
profile['height'] = nouvelle_hauteur

# Enregistrer le fichier de sortie
with rasterio.open(output_file, 'w', **profile) as dst:
    dst.write(image_reechantillonnee)

print("Rééchantillonnage terminé. Le fichier a été enregistré sous:", output_file)
