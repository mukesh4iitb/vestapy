import os
import re
import time
import pyautogui
import subprocess


import numpy as np
import matplotlib
matplotlib.use('Agg')  # non-GUI backend
import matplotlib.pyplot as plt
from matplotlib import colors


def Formating_Line(line):
    
    char_split = re.split(r'[^\s]+', line)
    space_len = [len(ch) for ch in char_split[:-1]]
    space_split = line.split()
    str_len =[len(sp) for sp in space_split]
    
    # print(space_len)
    # print(str_len)
    tot_len=[]
    for i in range(len(space_len)):
        tot_len.append(space_len[i]+str_len[i])
    
    format_line=[]
    for i in range(len(tot_len)):
        format_line.append(f"{{:>{tot_len[i]}}}")
    return "".join(format_line)+'\n'




def Vesta_Inp2_Out(filename, outfile_type='vesta'):
    filename_type = filename.split(".")[-1]
    outfile = filename.replace(filename_type, outfile_type)  # Change extension
    cmd = ["VESTA", "-nogui", "-i", filename, "-o", "option=cartesian", outfile]
    subprocess.run(cmd)


def Vesta2tif(filename):
    subprocess.Popen(["VESTA", filename], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(3)
    subprocess.run(['wmctrl', '-a', 'VESTA'])
    pyautogui.hotkey("alt", 'f')
    pyautogui.press(['down'] * 8)
    pyautogui.press('enter')
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press("backspace")
    pyautogui.write("{}_new.tif".format(filename.split(".vesta")[0]))
    time.sleep(1)

    MAX_TAB_TRIES = 3
    for _ in range(MAX_TAB_TRIES):
        location = pyautogui.locateOnScreen("/home/singh21m/Al2Sx/reoriented_Al2Sx/color_atom_magmom/save_button.png", confidence=0.7, grayscale=True)
        if location:
            print("Save button is now focused.")
            pyautogui.press('enter')
            found = True
            break
        else:
            pyautogui.press('tab')
            time.sleep(0.5)  # short pause to allow UI update
    time.sleep(1)

    try:
        location = pyautogui.locateOnScreen("/home/singh21m/Al2Sx/reoriented_Al2Sx/color_atom_magmom/replace_button.png", confidence=0.7, grayscale=True)
        if location:
            print("Replace button found. Clicking Enter")
            pyautogui.press('enter')
    except pyautogui.ImageNotFoundException:
        # Image not found, do nothing
        pass
    
    time.sleep(1)
    pyautogui.write('2')
    pyautogui.press(['tab']*2)
    pyautogui.press('enter')
    time.sleep(4)
    pyautogui.press('enter')
    time.sleep(1)
    subprocess.run(["pkill", "VESTA"])


def Vesta2tif0(filename):
    subprocess.Popen(["VESTA", "CONTCAR_Co_fix_new.vasp"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(3)
    subprocess.run(['wmctrl', '-a', 'VESTA'])
    pyautogui.hotkey("alt", 'f')
    pyautogui.press(['down'] * 8)
    pyautogui.press('enter')
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press("backspace")
    pyautogui.write("{}_new.tif".format(filename.split(".vesta")[0]))
    pyautogui.hotkey("shift", "tab")
    pyautogui.hotkey("shift", "tab")
    pyautogui.press("enter")
    pyautogui.press(['down'] * 5)
    pyautogui.press("enter")
    pyautogui.press(['tab']*4)
    pyautogui.press("enter")
    pyautogui.write('2')
    time.sleep(1)
    pyautogui.press(['tab']*2)
    pyautogui.press('enter')
    time.sleep(4)
    pyautogui.press('enter')

    time.sleep(1)
    subprocess.run(["pkill", "VESTA"])


"""
this function need to be checked.


def open_vesta_and_export_image(file_path, output_file):
    # Open VESTA via the command line or shortcut (use os or subprocess)
    # Example: os.system("path_to_vesta_executable POSCAR")
    subprocess.run(["VESTA", "POSCAR"])

    # Let VESTA open
    time.sleep(5)

    # Open the file (use "File" -> "Open" or directly open from command line)
    pyautogui.hotkey('ctrl', 'o')  # Simulate Ctrl + O for 'Open'
    time.sleep(1)
    pyautogui.typewrite(file_path)  # Type the file path
    pyautogui.press('enter')  # Press Enter to open the file
    time.sleep(3)

    # Go to Edit -> Bonds -> uncheck "Don't search outside the cell"
    pyautogui.hotkey('alt', 'e')  # Open the Edit menu
    time.sleep(1)
    pyautogui.press('b')  # Select Bonds
    time.sleep(1)
    pyautogui.press('enter')  # Enter to go to the Bonds options

    # Click to uncheck "Don't search outside the cell"
    # You would need to move the mouse to the exact position or use image recognition
    # to click the checkbox.
    # Example using pyautogui locateOnScreen to find an image of the checkbox
    checkbox_location = pyautogui.locateOnScreen('checkbox_image.png')
    pyautogui.click(checkbox_location)
    time.sleep(1)

    # Export image to tif file
    pyautogui.hotkey('alt', 'f')  # Open File menu
    pyautogui.press('e')  # Press Export (based on the keyboard shortcut)
    pyautogui.typewrite(output_file)  # Type output file path
    pyautogui.press('enter')  # Press Enter to save the image
    time.sleep(2)

    # Close VESTA or perform other steps if necessary

if __name__ == "__main__":
    # Call the function for multiple files
  #  file_paths = ["path_to_POSCAR_1", "path_to_POSCAR_2"]  # Example file paths
  #  output_paths = ["output_1.tif", "output_2.tif"]  # Corresponding output paths
  #  
  #  for file_path, output_file in zip(file_paths, output_paths):
  #      open_vesta_and_export_image(file_path, output_file)

  #  file_paths=["/home/singh21m/CMU/data/KS/pri_Co_sulphides"]
  #  output_paths=["out.tif"]
    open_vesta_and_export_image("/home/singh21m/CMU/data/KS/pri_Co_sulphides", "out.tif")

"""




def Modifying_SBOND(filename):
    """
    This function select only atoms inside the boundary. 
    SBOND
     1     C     N    0.00000    1.79202  0  0  1  0  0  0.250  2.000  42 199  82

     index, first atom, second, min-bond, max-bond, search mode, boundary mode, search by label, show polyhedra, bond-style, radious (cylinder), width (line), R, G, B (bond color)



    Note: If periodic atoms are not suitable shown in the vesta, it can be increased by 0.05 or 0.1 with modifying_BOUND().
    """
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    start_sbond_modifying = False
    sbond_modified_lines = []

    for line in lines:
        words = line.split()
        if words and words[0] == "SBOND":
            start_sbond_modifying = True
            sbond_modified_lines.append(line)
            continue

        if start_sbond_modifying:
            if words and words[:4] == ['0', '0', '0', '0']: # Stop modifying at "0 0 0 0"
                start_sbond_modifying = False
            
            if len(words) > 6:  # Ensure there are at least 7 columns
                words[6] = '0'  # Replace 7th column with 0
                #print(words)
                line = "{:>3}{:>6}{:>6}{:>11}{:>11}{:>3}{:>3}{:>3}{:>3}{:>3}{:>7}{:>7}{:>4}{:>4}{:>4}\n".format(*words)

        sbond_modified_lines.append(line)

    with open(filename, 'w') as file:
        file.writelines(sbond_modified_lines)

## Usage:
#modifying_SBOND("CONTCAR_Co_fix_new0.vesta", "CONTCAR_Co_fix_new1.vesta")

def Modifying_BOUND(filename, dw):
    """
    this function modify boundary of cell.
    """
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    start_bound_modifying = False
    bound_modified_lines = []


    for line in lines:
        words = line.split()
        if words and words[0] == "BOUND":
            start_bound_modifying = True
            bound_modified_lines.append(line)
            continue

        if start_bound_modifying:
            if words and words[:5] == ['0', '0', '0', '0', '0']:
                # Stop modifying at "0 0 0 0"
                start_bound_modifying = False

            #words[6] = '0'  # Replace 7th column with 0
            if len(words) == 6:
                for i in range(0,6,2):
                    words[i] = float(words[i])-dw
                    words[i+1] = float(words[i+1])+dw
                #print(words)
                line = "{:>8}{:>9}{:>10}{:>9}{:>10}{:>9}\n".format(*words)

        bound_modified_lines.append(line)

    with open(filename, 'w') as file:
        file.writelines(bound_modified_lines)

## Usage:
#modifying_BOUND("CONTCAR_Co_fix_new1.vesta", "CONTCAR_Co_fix_new2.vesta", dw=0.05)

def Modifying_UCLOP(filename, line_style=0, line_cell=1, line_width=1, R=0, G=0, B=0):
    """
     0   2  2.000   0   0   0
    """
    ucolp={}
    ucolp[line_style] = line_style
    ucolp[line_cell]  = line_cell
    ucolp[line_width]  = line_width
    ucolp[R] = R
    ucolp[G] = G
    ucolp[B] = B
    
    with open(filename, 'r') as file:
        lines = file.readlines()
        
        for i in range(len(lines) - 1):
            if "UCOLP" in lines[i]:  # If UCOLP is found in the current line
                ucolp_line = lines[i + 1].strip().split()  # Take the next line
                print("UCOLP Before:", ucolp_line)
                for j, key in enumerate(ucolp.keys()):
                    ucolp_line[j] = str(ucolp[key])
                print("UCOLP After:", lines[i+1])
                #lines[i+1] = " ".join(ucolp_line)+'\n'
                lines[i+1] = "{:>4}{:>4}{:>7}{:>4}{:>4}{:>4}\n".format(*ucolp_line)
                
        with open(filename, 'w') as file:
            file.writelines(lines)


## Usage:
#modifying_UCLOP("CONTCAR_Co_fix_new2.vesta", "CONTCAR_Co_fix_new3.vesta",  line_width=2)



def Modifying_SITET(filename, sitet_properties):
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
                match = re.match(r"([A-Za-z]+)(\d+)", words[1])
                symbol, index = match.group(1), match.group(2)
                if symbol in sitet_properties.keys():
                    #print(symbol)
                    sitet_prop = sitet_properties[symbol]
                    if "radius" in sitet_prop.keys():
                        words[2] = sitet_prop["radius"]
                    if "acolor" in sitet_prop.keys():
                        words[3], words[4], words[5] = sitet_prop["acolor"]
                    if "pcolor" in sitet_prop.keys():
                        words[6], words[7], words[8] = sitet_prop["pcolor"]
                    if "alpha" in sitet_prop.keys():
                        words[9] = sitet_prop["alpha"]
                    if "L" in sitet_prop.keys():
                        words[10] = sitet_prop["L"]
                        
                line = "{:>2}{:>11}{:>8}{:>4}{:>4}{:>4}{:>4}{:>4}{:>4}{:>4}{:>3}\n".format(*words)
                #print(line)
    
        bound_modified_lines.append(line)
    with open(filename, 'w') as file:
        file.writelines(bound_modified_lines)

### Usage:
#sitet_properties = {
#    "C": {"acolor": (217, 101, 33)},
#    "N": {"acolor": (116, 131, 209)},
#    "Co":{"acolor": (204, 28, 204)},
#    "S": {"acolor": (255, 208, 0)}
#}
#
#modifying_SITET("CONTCAR_Co_fix_new3.vesta", "CONTCAR_Co_fix_new4.vesta", sitet_properties)


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
        norm = SymLogNorm(linthresh=0.01, linscale=1.0, vmin=vals.min(), vmax=vals.max())
        #norm = colors.PowerNorm(gamma=0.5, vmin=vals.min(), vmax=vals.max())
    
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


#converting_values_to_colors("ext_values.txt", plot_colors=True)

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
                words[3], words[4], words[5] = rgb_255[int(words[0])-1]        
                line = "{:>2}{:>11}{:>8}{:>4}{:>4}{:>4}{:>4}{:>4}{:>4}{:>4}{:>3}\n".format(*words)
                #print(line)
    
        bound_modified_lines.append(line)
    with open(filename, 'w') as file:
        file.writelines(bound_modified_lines)

#Modifying_SITET_atoms_color_with_external_values("example_atom_color_change.vesta", "ext_values.txt")



def Modifying_COMPS(filename, comps=1):
    """
    This modifying the presence and absence of axis.
    comps=0 -> absence of axis
    comps=1 -> presence of axis
    
    usage:
    #modifying_COMPS("Al2S12_b3lyp_13_CONTCAR.vesta", comps=0)
    """

    with open(filename, 'r') as file:
        lines = file.readlines()

        for i in range(len(lines) - 1):
            if "COMPS" in lines[i]:
                lines[i]="COMPS {}\n".format(comps)
        with open(filename, 'w') as file:
            file.writelines(lines)



def Zooming_VestaPlot(filename, scale=1.5):
    """
    this part of SCENE, which is last line of it.
    4+2+1= 7th line
    """
    with open(filename, 'r') as file:
        lines = file.readlines()

        for i in range(len(lines) - 1):
            if "SCENE" in lines[i]:  # If UCOLP is found in the current line
                zscale = lines[i + 7]  # Take 7th line which is zooming index
                print("Zoom scale Before:", zscale)
                zscale = scale
                print("Zoom scale After:", zscale)
                lines[i+7] = "{:>4}\n".format(zscale)

        with open(filename, 'w') as file:
            file.writelines(lines)


def Shifting_And_Zooming_VestaPlot(filename, shift_str='0.00  0.00', scale=1.5):
    """
    this part of SCENE, which is last line of it.
    4+2+1= 7th line
    """
    with open(filename, 'r') as file:
        lines = file.readlines()

        for i in range(len(lines) - 1):
            if "SCENE" in lines[i]:  # If UCOLP is found in the current line
                lines[i+5] = shift_str  # shifting
                print("Zoom scale Before:", lines[i+7])
                lines[i+7] = "{:>4}\n".format(scale)  #zooming
                print("Zoom scale After:", lines[i+7])

        with open(filename, 'w') as file:
            file.writelines(lines)




def VestaInpFileCollector(startswith="", endswith=".vasp"):
    """
    VestaInp are those type of files, which can be opened in vesta such as .vasp, .cif, .xyz etc.
    """

    drct=os.getcwd()
    inp_files = []
    
    for path, dirs, files in os.walk("."):
        path = os.path.relpath(path, ".")
    
        for file0 in files:
            if file0.startswith(startswith) and file0.endswith(endswith):
                inp_files.append(os.path.join(drct, path, file0))
    
    return inp_files

def VestaFileCollector(startswith="", endswith="vesta"):
    drct=os.getcwd()
    vesta_files = []
    
    for path, dirs, files in os.walk("."):
        path = os.path.relpath(path, ".")
    
        for file0 in files:
            if file0.startswith(startswith) and file0.endswith(endswith):
                vesta_files.append(os.path.join(drct, path, file0))
    
    return vesta_files


if __name__ == "__main__":
    #print("yes")
    
    #inp_files=VestaInpFileCollector(startswith="", endswith=".xyz")
    #print(contcar_files())
    vesta_files=VestaFileCollector()
    #print(vesta_files())

    ### testing file
    #contcar_files = ['/home/mukesh/CMU/data/KS/pri_sulphides/CONTCAR_pri_S8.vasp']
    #vesta_files = ['/home/mukesh/CMU/data/KS/pri_sulphides/CONTCAR_pri_S8.vesta']
    
    ### Step-1: Convert Vasp2vesta file: 
    ### converting vasp2vesta file
    #for inp in inp_files:
    #    print("vasp2vesta: {}".format(inp))
    #    filename = inp.split("/")[-1]
    #    path = "/".join(inp.split("/")[:-1])
    #    os.chdir(path)
    #    Vesta_Inp2_Out(filename)

    ## Step-2: modify vesta files: 
    for vest in vesta_files:
        print("Modifying: {}".format(vest))
        filename = vest.split("/")[-1]
        path = "/".join(vest.split("/")[:-1])
        os.chdir(path)

    #    Modifying_SBOND(filename)
    #    Modifying_BOUND(filename, dw=0.05)
    #    Modifying_UCLOP(filename, line_width=2)
    #    Modifying_COMPS(filename, comps=0)

    #    sitet_properties = {
    #       "Al":  {"acolor": (184, 5, 183)},
    #    #    "N":  {"acolor": (116, 131, 209)},
    #    #    "K":  {"acolor": (204, 28, 204)},
    #    #    "S":  {"acolor": (225, 255, 0)},
    #    #    "Fe":  {"acolor": (171, 27, 31)},
    #    #    "Co":  {"acolor": (25, 25, 193)},
    #    #    "Ni":  {"acolor": (67, 210, 213)},
    #    }

    #    Modifying_SITET(filename, sitet_properties)
        Modifying_SITET_atoms_color_with_external_values("example_atom_color_change.vesta", "ext_values.txt")
        
        #Zooming_plot(filename, scale=2.5)
     #Shifting_and_zooming_plot(filename, shift_str="-0.450  -0.007", scale=1.866)

    ### Step-3: Convert vesta2tif file: 
    ### converting vesta2tif file
    for vest in vesta_files:
        print("Vesta2tif: {}".format(vest))
        filename = vest.split("/")[-1]
        path = "/".join(vest.split("/")[:-1])
        os.chdir(path)
        Vesta2tif(vest)

