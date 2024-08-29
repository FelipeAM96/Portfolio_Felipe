# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#Avoir les packages rasterio, tkinter, os, glob et numpy instalé  

import os
import glob
import numpy as np
import rasterio
from rasterio.crs import CRS
import tkinter
from tkinter.filedialog import askdirectory
import scipy.ndimage

# Définition des dossiers de travail avec boite de dialogue
path_Formosat = tkinter.filedialog.askdirectory(title="Répertoire où se situent les images")
path_save = tkinter.filedialog.askdirectory(title="Répertoire de sauvegarde des NDVI")

# Rajout du caractère / à la fin de la chaine de caractère des path
path_Formosat += "/"
path_save += "/"

os.chdir(path_Formosat)

files = glob.glob(path_Formosat + "*.tif")

for i in range(0, len(files)):
    print("Image : ", files[i])
    
    src = rasterio.open(os.path.join(path_Formosat, files[i])) #B
            
    # Calculs en important les données dans des variables séparées et en changeant de type de données
    pir = src.read(7).astype('float32')
    rouge = src.read(5).astype('float32')
    vert = src.read(4).astype('float32')
    bd = src.read(6).astype('float32')
    
    #Autoriser la division par 0 et calculer les indices
    np.seterr(divide='ignore', invalid='ignore')
    
    #Calcules des Indices
    ndvi = (pir - rouge) / (pir + rouge).astype('float32')
    ndre = (pir - bd) / (pir + bd).astype('float32')
    ndwi = (vert - pir) / (vert + pir).astype('float32')   
    savi = ((pir - rouge) / (pir + rouge + 0.5)*1.5).astype('float32')  
    
    # Transform values that are 0 with all neighboring values also equal to 0 within a 5-pixel distance into No Data
    mask = scipy.ndimage.binary_erosion(ndvi == 0, structure=np.ones((2, 2))).astype(ndvi.dtype)
    ndvi = np.where(mask, np.nan, ndvi)
    
    mask = scipy.ndimage.binary_erosion(ndre == 0, structure=np.ones((2, 2))).astype(ndre.dtype)
    ndre = np.where(mask, np.nan, ndre)
    
    mask = scipy.ndimage.binary_erosion(ndwi == 0, structure=np.ones((2, 2))).astype(ndwi.dtype)
    ndwi = np.where(mask, np.nan, ndwi)
    
    mask = scipy.ndimage.binary_erosion(savi == 0, structure=np.ones((2, 2))).astype(savi.dtype)
    savi = np.where(mask, np.nan, savi)

    
    # ECRITURE DU FICHIER DE SORTIE
    output_dir = os.path.join(path_save, 'Resultats_Indices')
    os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist
    
    base_name = os.path.splitext(os.path.basename(files[i]))[0]
    
    ## Création des metadonnées de l'image de sortie
    # NDVI
    # ---------------------------------------------------------------------------
    ndviImage = rasterio.open(os.path.join(output_dir, base_name + "_NDVI.tiff"), 'w',
                            driver='Gtiff',
                            width=src.width, 
                            height=src.height,
                            count=1,
                            crs=src.crs,
                            transform=src.transform,
                            dtype='float32'
                            )
    ndviImage.write(ndvi, 1)
    ndviImage.close()
    
    # NDRE
    # ---------------------------------------------------------------------------
    ndreImage = rasterio.open(os.path.join(output_dir, base_name + "_NDRE.tiff"), 'w',
                            driver='Gtiff',
                            width=src.width, 
                            height=src.height,
                            count=1,
                            crs=src.crs,
                            transform=src.transform,
                            dtype='float32'
                            )
    ndreImage.write(ndre, 1)
    ndreImage.close()
    
    # NDWI
    # ---------------------------------------------------------------------------
    ndwiImage = rasterio.open(os.path.join(output_dir, base_name + "_NDWI.tiff"), 'w',
                            driver='Gtiff',
                            width=src.width, 
                            height=src.height,
                            count=1,
                            crs=src.crs,
                            transform=src.transform,
                            dtype='float32'
                            )
    ndwiImage.write(ndwi, 1)
    ndwiImage.close()
    
    # SAVI
    # ---------------------------------------------------------------------------
    saviImage = rasterio.open(os.path.join(output_dir, base_name + "_SAVI.tiff"), 'w',
                            driver='Gtiff',
                            width=src.width, 
                            height=src.height,
                            count=1,
                            crs=src.crs,
                            transform=src.transform,
                            dtype='float32'
                            )
    saviImage.write(savi, 1)
    saviImage.close()