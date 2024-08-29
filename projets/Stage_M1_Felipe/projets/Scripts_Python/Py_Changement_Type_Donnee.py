# -*- coding: utf-8 -*-
"""
Créé le vendredi 26 mai 2023 à 16h00
"""

import numpy as np
import tifffile as tif
from tkinter import Tk, filedialog
import rasterio
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
    # Charger les données de l'image
    input_data = src.read()
    input_data_float32 = input_data.astype(np.float32)

    # Définir la fenêtre de dialogue pour sélectionner le dossier de sortie
    output_dir = filedialog.askdirectory(title="Sélectionnez le dossier de sortie")

    # Vérifier si le dossier a été sélectionné
    if not output_dir:
        print("Aucun dossier de sortie sélectionné.")
        exit()

    # Définir le chemin complet pour le fichier de sortie
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = os.path.join(output_dir, base_name + "_Retype.tif")

    # Copier le profil du fichier d'entrée vers le fichier de sortie
    profile = src.profile

    # Mettre à jour le profil avec le nouveau type de données
    profile['dtype'] = 'float32'

    # Enregistrer le fichier de sortie
    with rasterio.open(output_file, 'w', **profile) as dst:
        dst.write(input_data_float32)

print("Resampling terminé. Le fichier a été enregistré sous:", output_file)
