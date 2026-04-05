import os
import re
import time
import pyautogui
import subprocess
import numpy as np


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
        location = pyautogui.locateOnScreen("/home/singh21m/.pfunctions/vestapy/save_button.png", confidence=0.7, grayscale=True)
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
        location = pyautogui.locateOnScreen("/home/singh21m/.pfunctions/vestapy/replace_button.png", confidence=0.7, grayscale=True)
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




def Modifying_SBOND(filename, sbond_properties):
    """
    This function select only atoms inside the boundary. 
    SBOND
     1     C     N    0.00000    1.79202  0  0  1  0  0  0.250  2.000  42 199  82
    {:>3}{:>6}{:>6}{:>11}{:>11}{:>3}{:>3}{:>3}{:>3}{:>3}{:>7}{:>7}{:>4}{:>4}{:>4}\n".format(*words)

     index, first atom, second, min-bond, max-bond, search-mode, boundary-mode, search-by-label, show-polyhedra, bond-style, radious (cylinder), width (line), R, G, B (bond color)



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
                #print(words)
                elem1 = words[1] #re.match(r"([A-Za-z]", words[2])
                elem2 = words[2] #re.match(r"([A-Za-z]", words[3])
                #print(elem1, elem2)
                bond1 = '{}-{}'.format(elem1, elem2)
                bond2 = '{}-{}'.format(elem2, elem1)

                #if (bond1 or bond2) in sbond_properties.keys():
                if bond1 in sbond_properties.keys() or bond2 in sbond_properties.keys():
                    #print(symbol)
                    sbond_prop = sbond_properties[bond1]
                    if "min-bond" in sbond_prop.keys():
                        words[3] = sbond_prop["min-bond"]
                    if "max-bond" in sbond_prop.keys():
                        words[4] = sbond_prop["max-bond"]
                    if "search-mode" in sbond_prop.keys():
                        words[5] = sbond_prop["search-mode"]
                    if "boundary-mode" in sbond_prop.keys():
                        words[6] = sbond_prop["boundary-mode"]
                    if "search-by-label" in sbond_prop.keys():
                        words[7] = sbond_prop["search-by-label"]
                    if "show-polyhedra" in sbond_prop.keys():
                        words[8] = sbond_prop["show-polyhedra"]
                    if "bond-style" in sbond_prop.keys():
                        words[9] = sbond_prop["bond-style"]
                    if "radius" in sbond_prop.keys():
                        words[10] = sbond_prop["radius"]  # cylinderical radious of bond.
                    if "width" in sbond_prop.keys():
                        words[11] = sbond_prop["width"]
                    if "bcolor" in sbond_prop.keys():
                        words[12], words[13], words[14] = sbond_prop['bcolor']

                #print(len(words))
                line = "{:>3}{:>6}{:>6}{:>11}{:>11}{:>3}{:>3}{:>3}{:>3}{:>3}{:>7}{:>7}{:>4}{:>4}{:>4}\n".format(*words)

        sbond_modified_lines.append(line)

    with open(filename, 'w') as file:
        file.writelines(sbond_modified_lines)

## Usage:
# sbond_properties = {
# "Al-S":  {"max-bond": 2.66646},
# "S-S":  {"max-bond": 2.6}
# }

# Modifying_SBOND("reoriented_Al2S12_pbe_1.out.vesta")


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


## rotating around lattice vector directions and reciprocal vector directions

def normalize(v):
    return v / np.linalg.norm(v)

def scene_direction(c, a, b):
    z_hat = normalize(c)
    a_perp = a - np.dot(a, z_hat) * z_hat
    if np.linalg.norm(a_perp) < 1e-8:
        a_perp = b - np.dot(b, z_hat) * z_hat
    x_hat = normalize(a_perp)
    y_hat = np.cross(z_hat, x_hat)

    SCENE = np.eye(4)
    SCENE[0, :3] = x_hat
    SCENE[1, :3] = y_hat
    SCENE[2, :3] = z_hat
    return SCENE

def reciprocal_lattice(a, b, c, two_pi=True):
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)
    c = np.array(c, dtype=float)

    volume = np.dot(a, np.cross(b, c))
    if abs(volume) < 1e-10:
        raise ValueError("Lattice vectors are linearly dependent")

    factor = 2.0 * np.pi if two_pi else 1.0

    a_star = factor * np.cross(b, c) / volume
    b_star = factor * np.cross(c, a) / volume
    c_star = factor * np.cross(a, b) / volume

    return a_star, b_star, c_star

def a_view(a_vec, b_vec, c_vec):
    return scene_direction(a_vec, b_vec, c_vec)

def b_view(a_vec, b_vec, c_vec):
    return scene_direction(b_vec, c_vec, a_vec)

def c_view(a_vec, b_vec, c_vec):
    return scene_direction(c_vec, a_vec, b_vec)

def astar_view(a_vec, b_vec, c_vec):
    astar_vec, bstar_vec, cstar_vec = reciprocal_lattice(a_vec, b_vec, c_vec)
    return scene_direction(astar_vec, bstar_vec, cstar_vec)

def bstar_view(a_vec, b_vec, c_vec):
    astar_vec, bstar_vec, cstar_vec = reciprocal_lattice(a_vec, b_vec, c_vec)
    return scene_direction(bstar_vec, cstar_vec, astar_vec)

def cstar_view(a_vec, b_vec, c_vec):
    astar_vec, bstar_vec, cstar_vec = reciprocal_lattice(a_vec, b_vec, c_vec)
    return scene_direction(cstar_vec, astar_vec, bstar_vec)

def Rotating_along_lattice_and_reciprocal_axis_directions(filename, view="c"):
    """
    filename, a meaning rotating vesta filename along "a" direction
    """
    with open(filename, 'r') as file:
        lines = file.readlines()

    start_SCENE_modifying = False
    SCENE_modified_lines = []

    lattice_param = False
    lattice_matrix = False
#    LMATRIX
# 0.500000  0.866025  0.000000  0.000000
#-0.866025  0.500000  0.000000  0.000000
# 0.000000  0.000000  1.000000  0.000000
# 0.000000  0.000000  0.000000  1.000000

    LM=[]
    lattice_matrix_rows_counter = 0
    for line in lines:
        if "LMATRIX" in line:
            lattice_matrix=True
            lattice_matrix_rows_counter = 0
            continue
        if lattice_matrix and len(line.split())==4:
            LM.append(list(map(float, line.split())))
            lattice_matrix_rows_counter +=1
            if lattice_matrix_rows_counter == 3:
                lattice_matrix=False
        #print("LM", LM)
        if "CELLP" in line:
            lattice_param=True
        if lattice_param and len(line.split())==6:
            a, b, c, alpha, beta, gamma = list(map(float, line.split()))
            lattice_param=False

            alpha, beta, gamma = np.deg2rad([alpha, beta, gamma])
            a_vec = np.array([a, 0.0, 0.0])

            # b in x-y plane
            b_x = b * np.cos(gamma)
            b_y = b * np.sin(gamma)
            b_vec = np.array([b_x, b_y, 0.0])

            # c vector
            c_x = c * np.cos(beta)
            c_y = c * (np.cos(alpha) - np.cos(beta) * np.cos(gamma)) / np.sin(gamma)
            # z-component from Pythagoras
            c_z = np.sqrt(c**2 - c_x**2 - c_y**2)
            c_vec = np.array([c_x, c_y, c_z])
            ## lower triangular matrix
            # Convert to radians
            #alpha, beta, gamma = np.deg2rad([alpha, beta, gamma])

            ## c vector (along z)
            #c_vec = np.array([0.0, 0.0, c])

            ## b vector (in y–z plane)
            #b_z = b * np.cos(alpha)
            #b_y = b * np.sin(alpha)
            #b_vec = np.array([0.0, b_y, b_z])

            ## a vector (general)
            #a_z = a * np.cos(beta)
            #a_y = (a * b * np.cos(gamma) - a_z * b_z) / b_y
            #a_x = np.sqrt(a**2 - a_y**2 - a_z**2)

            #a_vec = np.array([a_x, a_y, a_z])
            LM_rot = np.array(LM)[:, :-1]
            #print(LM_rot.shape)
            a_vec = LM_rot@a_vec
            b_vec = LM_rot@b_vec
            c_vec = LM_rot@c_vec
            #a_vec = np.array([6.1682281540000004,  -10.6836845599999997,    0.0000000000000000])
            #b_vec = np.array([6.1682281540000004,   10.6836845599999997,    0.0000000000000000])
            #c_vec = np.array([0.0000000000000000,    0.0000000000000000,   20.0000000000000000])

            print("lattice vectors:", a_vec, b_vec, c_vec)
            if view == "a":
                scene_matrix = a_view(a_vec, b_vec, c_vec)
            elif view == "b":
                scene_matrix = b_view(a_vec, b_vec, c_vec)
            elif view == "c":
                scene_matrix = c_view(a_vec, b_vec, c_vec)
            elif view == "a*":
                scene_matrix = astar_view(a_vec, b_vec, c_vec)
            elif view == "b*":
                scene_matrix = bstar_view(a_vec, b_vec, c_vec)
            elif view == "c*":
                scene_matrix = cstar_view(a_vec, b_vec, c_vec)

    #print("scene matrix:",scene_matrix)
    start_SCENE_modifying = False
    scene_row_counter = 0
    for line in lines:
        if "SCENE" in line:
            start_SCENE_modifying = True
            SCENE_modified_lines.append(line)
            continue

        if start_SCENE_modifying and len(line.split())==4:
            sc0, sc1, sc2, sc3 = scene_matrix[scene_row_counter]
            line="{}    {}   {}   {}\n".format(sc0, sc1, sc2, sc3)
            SCENE_modified_lines.append(line)
            scene_row_counter += 1
            if scene_row_counter == 4:
                start_SCENE_modifying = False
        else:
            SCENE_modified_lines.append(line)
    with open(filename, 'w') as file:
        file.writelines(SCENE_modified_lines)

#Rotating_along_lattice_and_reciprocal_axis_directions("sorted_N4_graphene_doped_43_K2S4_scc.vesta", view='a')




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
        Modifying_COMPS(filename, comps=0)

        #sitet_properties = {
        #   "Al":  {"acolor": (184, 5, 183)},
        #    "N":  {"acolor": (116, 131, 209)},
        #    "K":  {"acolor": (204, 28, 204)},
        #    "S":  {"acolor": (225, 255, 0)},
        #    "Fe":  {"acolor": (171, 27, 31)},
        #    "Co":  {"acolor": (25, 25, 193)},
        #    "Ni":  {"acolor": (67, 210, 213)},
        #}

        #Modifying_SITET(filename, sitet_properties)
        #sbond_properties = {"S-S":  {"max-bond": 2.6}}
       
        Modifying_SBOND(filename, sbond_properties={"C-N":{"boundary-mode":0}, "C-C":{"boundary-mode":0}})

        
        #Zooming_VestaPlot(filename, scale=2.2)
     #Shifting_and_zooming_Vestaplot(filename, shift_str="-0.450  -0.007", scale=1.866)
        Rotating_along_lattice_and_reciprocal_axis_directions(filename)
    ### Step-3: Convert vesta2tif file: 
    ### converting vesta2tif file
    for vest in vesta_files:
        print("Vesta2tif: {}".format(vest))
        filename = vest.split("/")[-1]
        path = "/".join(vest.split("/")[:-1])
        os.chdir(path)
        Vesta2tif(vest)

