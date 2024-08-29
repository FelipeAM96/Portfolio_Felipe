# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 10:59:27 2023

@author: restit
"""

import numpy as np
import matplotlib.pyplot as plt

# Données
a = -0.646363
b = 1.311645
meanX = 0.757526
meanY = 0.347242
sdX = 0.166277
sdY = 0.277549
correlation = 0.785797
significance = 16085589.320067

# Générer les points pour la ligne de régression
x_vals = np.linspace(meanX - 3*sdX, meanX + 3*sdX, 100)
y_vals = a + b * x_vals

# Créer l'équation de la régression
equation = f'Équation'

# Tracer les points de données et la ligne de régression
plt.figure(figsize=(10, 6))
plt.scatter(x_vals, y_vals, color='red', label='Régression Linéaire')
plt.scatter(meanX, meanY, color='blue', label='Point Moyen')
plt.errorbar(meanX, meanY, xerr=sdX, yerr=sdY, linestyle='', color='blue', capsize=5)
plt.plot(x_vals, y_vals, color='red', linestyle='dashed', label='Ligne de Régression')
plt.xlabel('IV1')
plt.ylabel('IV2')
plt.title('Graphique de Régression Linéaire (IV1 - IV2)')
plt.legend(loc='upper left')

# Ajouter les informations dans une boîte placée dans le coin inférieur droit du graphique
info_text = f'Corrélation (R) : {correlation:.4f}\nSignificativité (F) : {significance:.4f}\nInclinaison (b) : {b:.6f}\nIntercept (a) : {a:.6f}\n{equation} : y = {a:.4f} + {b:.6f} * x'
plt.text(0.98, 0.02, info_text, transform=plt.gca().transAxes, bbox=dict(boxstyle='round,pad=0.5', edgecolor='black', facecolor='white'), horizontalalignment='right', verticalalignment='bottom')

plt.grid()

plt.show()