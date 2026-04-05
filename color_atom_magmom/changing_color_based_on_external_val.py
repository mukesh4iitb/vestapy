import os
import re
import time


import numpy as np
import matplotlib
matplotlib.use('Agg')  # non-GUI backend
import matplotlib.pyplot as plt
from matplotlib import colors


from matplotlib.colors import SymLogNorm
#norm = SymLogNorm(linthresh=0.01, linscale=1.0, vmin=data.min(), vmax=data.max())

class ExponentialNorm(colors.Normalize):
    def __call__(self, value, clip=None):
        normed = (value - self.vmin)/(self.vmax - self.vmin)
        return (np.exp(normed) - 1)/(np.e - 1)

#exp_norm = ExponentialNorm(vmin=data.min(), vmax=data.max())



def converting_values_to_colors(filename, plot_colors=False):
    # external value data
    vals = np.loadtxt(filename).reshape(-1)

    # Choose colormap
    cmap = plt.colormaps['rainbow']
    
    # Automatically determine normalization range
    
    if np.all(vals < 0):
        vmin, vmax = -1.0, 0.0
        norm = plt.Normalize(vmin=vmin, vmax=vmax)
    elif np.all(vals > 0):
        vmin, vmax = 0.0, 1.0
        norm = plt.Normalize(vmin=vmin, vmax=vmax)
    else:
        vmin, vmax = -1.0, 1.0
        #norm = ExponentialNorm(vmin=vals.min(), vmax=vals.max())
        #norm = SymLogNorm(linthresh=0.01, linscale=1.0, vmin=vals.min(), vmax=vals.max())
        norm = colors.PowerNorm(gamma=0.5, vmin=vals.min(), vmax=vals.max())
    
    # Convert to RGBA
    rgba = cmap(norm(vals))
    
    # Extract RGB and scale to 0–255
    rgb_255 = (rgba[:, :3] * 255).astype(np.uint8)
    #print(rgb_255)
    
    # Plot as a color column
    if plot_colors:
        # Create figure & axes
        fig, ax = plt.subplots(figsize=(6, 3))
        
        # Plot data as a vertical strip and get the image object
        im = ax.imshow(vals.reshape(-1, 1), cmap=cmap, norm=norm, aspect='auto')
        
        # Add colorbar attached to the same axes
        cbar = fig.colorbar(im, ax=ax, orientation='vertical')
        #cbar.set_label('Value')
        # Add min and max labels manually
        cbar.ax.text(0.5, -0.02, f"{min(vals):.3f}", ha='center', va='top', transform=cbar.ax.transAxes)
        cbar.ax.text(0.5, 1.02, f"{max(vals):.3f}", ha='center', va='bottom', transform=cbar.ax.transAxes)
        
        plt.savefig("color_legend.png")
        plt.close()

    return rgb_255
    
converting_values_to_colors("ext.txt", plot_colors=True)



def Modifying_SITET_atoms_color_with_external_values(filename, external_value_filename):
    """
    1         C1  0.7700 180  86  32 128  73  41 214  0

    index,  symbols-elementIndex, atomic radius, R, G B (color of atoms), R B G (color of polyhedra = color of atoms (default)), alpha of polyhedra, L (which determine whether symbols-index should be shown or not. 0 shown, 1=not shown)
    
    These are includes in the following dictionary as modifying_SITET() function argument:
    
    sitet_properties = {
        "C":  {"radius": 1, "acolor": (1,1,1), "pcolor": (1,1,1), "alpha": 0.4, "L": 0},
        "N":  {"radius": 2, "acolor": (2,3,1), "pcolor": (2,3,1), "alpha": 0.4, "L": 0},
        "Co": {"radius": 3, "acolor": (2,2,2), "pcolor": (2,2,2), "alpha": 0.4, "L": 0},
        "S":  {"radius": 4, "acolor": (2,1,5), "pcolor": (2,1,5), "alpha": 0.4, "L": 0}
    }
    Note: Everything is not required to provide here. One provide few elements or few properties like radius etc. It will only change the given properties
    """

    with open(filename, 'r') as file:
        lines = file.readlines()
    
    rgb_255=converting_values_to_colors(external_value_filename)
    #print(rgb_255)
    
    start_bound_modifying = False
    bound_modified_lines = []




    for line in lines:
        words = line.split()
        if words and words[0] == "SITET":
            start_bound_modifying = True
            
            bound_modified_lines.append(line)
            continue
    
        if start_bound_modifying:
            if words and words[:5] == ['0', '0', '0', '0', '0']: # Stop modifying at "0 0 0 0"
                start_bound_modifying = False
            
                
            if len(words) > 6:
                #print(words)
                words[3], words[4], words[5] = rgb_255[int(words[0])-1]
                line = "{:>2}{:>11}{:>8}{:>4}{:>4}{:>4}{:>4}{:>4}{:>4}{:>4}{:>3}\n".format(*words)
                #print(line)
    
        bound_modified_lines.append(line)
    with open(filename, 'w') as file:
        file.writelines(bound_modified_lines)

#Modifying_SITET_atoms_color_with_external_values()
Modifying_SITET_atoms_color_with_external_values("POSCAR.vesta", "ext.txt")

