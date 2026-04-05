import re
import ase.io
import numpy as np
from collections import defaultdict
from vesta_bond_dict import bond_dict


def get_bond_cutoff(elem1, elem2, delta=0.0):
    return bond_dict.get(tuple(sorted((elem1, elem2))), 0.0) + delta

#print(get_bond_cutoff('Yb', "Cl", delta=0.2))

def bond_distance(POS, idx1, idx2):
    pos1 = POS.positions[idx1]
    pos2 = POS.positions[idx2]
    dist = np.linalg.norm(np.array(pos1) - np.array(pos2))
    return dist

def angle_A_B_C(POS, idx1, idx2, idx3):
    pos1 = POS.positions[idx1]
    pos2 = POS.positions[idx2]
    pos3 = POS.positions[idx3]

    # Vectors AB and BC
    v1 = pos1 - pos2
    v2 = pos3 - pos2

    # Normalize vectors
    v1_norm = v1 / np.linalg.norm(v1)
    v2_norm = v2 / np.linalg.norm(v2)

    # Cosine of angle
    cos_theta = np.dot(v1_norm, v2_norm)
    cos_theta = np.clip(cos_theta, -1.0, 1.0)  # Avoid numerical errors

    # Angle in degrees
    angle = np.degrees(np.arccos(cos_theta))
    return angle


#def dihedral_angle_A_B_C_D(idx1, idx2, idx3, idx4):
#    p0 = POS.positions[idx1]
#    p1 = POS.positions[idx2]
#    p2 = POS.positions[idx3]
#    p3 = POS.positions[idx4]
#
#    # Bond vectors
#    b0 = p0 - p1
#    b1 = p2 - p1
#    b2 = p3 - p2
#
#    # Normalize b1
#    b1 /= np.linalg.norm(b1)
#
#    # Vectors normal to planes
#    n1 = np.cross(b0, b1)
#    n2 = np.cross(b1, b2)
#
#    # Normalize normals
#    n1 /= np.linalg.norm(n1)
#    n2 /= np.linalg.norm(n2)
#
#    # Compute angle using arctangent for correct sign
#    x = np.dot(n1, n2)
#    y = np.dot(np.cross(n1, n2), b1)
#
#    angle = np.degrees(np.arctan2(y, x))
#    return angle


def dihedral_angle_A_B_C_D(POS, idx1, idx2, idx3, idx4):
    p0 = POS.positions[idx1]
    p1 = POS.positions[idx2]
    p2 = POS.positions[idx3]
    p3 = POS.positions[idx4]

    # Bond vectors
    b0 = p0 - p1
    b1 = p2 - p1

    b2 = p1 - p2
    b3 = p3 - p2

    # Normalize b1
    b0 /= np.linalg.norm(b0)
    b1 /= np.linalg.norm(b1)
    b2 /= np.linalg.norm(b2)
    b3 /= np.linalg.norm(b3)

    # Vectors normal to planes
    n1 = np.cross(b0, b1)
    n2 = np.cross(b2, b3)

    n1 /= np.linalg.norm(n1)
    n2 /= np.linalg.norm(n2)
    cos_theta = np.dot(n1, n2)
    #cos_theta = np.clip(cos_theta, -1.0, 1.0)  # Avoid numerical errors

    # Angle in degrees
    dihedral = np.degrees(np.arccos(cos_theta))
    return dihedral

def creating_index_mapping_dict(POS):
    elements = POS.get_chemical_symbols()

    counter = defaultdict(int)
    vesta_index = []
    for elem in elements:
        counter[elem] += 1
        vesta_index.append(f"{elem}{counter[elem]}")
    
    python_index=[]
    for i, atom in enumerate(POS):
        python_index.append("{}{}".format(atom.symbol, i))
    
    python_index_2_vesta_index_dict = { p: v for p, v in zip(python_index, vesta_index) }
    vesta_index_2_python_index_dict = { v: p for v, p in zip(vesta_index, python_index)}

    return python_index_2_vesta_index_dict, vesta_index_2_python_index_dict


def Convert_Indices(mapping_dict, indices):
    if isinstance(indices[0], tuple):
        # Handle bond pairs, triples, quadruples
        return [tuple(mapping_dict.get(atom, atom) for atom in group) for group in indices]
    else:
        # Single list of atoms
        return [mapping_dict.get(atom, atom) for atom in indices]


def range_finder(dict_with_str_key_list_value):
    key_min_max_values = ''
    for key, values in dict_with_str_key_list_value.items():
        min_val = min(values)
        max_val = max(values)
        key_min_max_values += f"{key}: range={min_val:.3f}-{max_val:.3f}\n"
    return key_min_max_values



def get_tuples(POS, delta=0):
    
    bond_pairs = []
    for i, atom1 in enumerate(POS):
        elem1 = atom1.symbol
        pos1 = atom1.position
        for j, atom2 in enumerate(POS):
            elem2 = atom2.symbol
            pos2 = atom2.position
            if i >= j:
                continue
            dist = np.linalg.norm(np.array(pos1) - np.array(pos2))
            cutoff = get_bond_cutoff(elem1, elem2, delta=delta)
            #print(cutoff)
            if cutoff and dist <= cutoff:
                bond_pairs.append(("{}{}".format(elem1, i), "{}{}".format(elem2, j)))
    
    # Create adjacency list
    neighbors = defaultdict(set)
    for a, b in bond_pairs:
        neighbors[a].add(b)
        neighbors[b].add(a)
    
    bond_triples = []
    for center in neighbors:
        bonded = list(neighbors[center])
        for i in range(len(bonded)):
            for j in range(i + 1, len(bonded)):
                bond_triples.append((bonded[i], center, bonded[j]))
    
    
    bond_quadruples = []
    for b, c in bond_pairs:
        for a in neighbors[b] - {c}:
            for d in neighbors[c] - {b}:
                bond_quadruples.append((a, b, c, d))

    return bond_pairs, bond_triples, bond_quadruples



def get_bond_lengths(POS, bond_pairs):
    
    bond_lengths = {}
    bond_lengths_tuplewise = []
    for idx in bond_pairs:
        #print(idx)
        match1 = re.match(r'([A-Z][a-z]?)(\d+)', idx[0])
        elem1, idx1 = match1.groups()
        match2 = re.match(r'([A-Z][a-z]?)(\d+)', idx[1])
        elem2, idx2 = match2.groups()
    
        bond=bond_distance(POS, int(idx1), int(idx2))
        bond_lengths_tuplewise.append(bond)
        
        key = f"{elem1}-{elem2}"
        if key not in bond_lengths:
            bond_lengths[key] = [bond]
        else:
            bond_lengths[key].append(bond)

    return bond_lengths_tuplewise, bond_lengths


def get_bond_angles(POS, bond_triples):
    
    bond_angles = {}
    bond_angles_tuplewise = []
    
    for idx in bond_triples:
        match1 = re.match(r'([A-Z][a-z]?)(\d+)', idx[0])
        elem1, idx1 = match1.groups()
        match2 = re.match(r'([A-Z][a-z]?)(\d+)', idx[1])
        elem2, idx2 = match2.groups()
        match3 = re.match(r'([A-Z][a-z]?)(\d+)', idx[2])
        elem3, idx3 = match3.groups()
        
        angle=angle_A_B_C(POS, int(idx1), int(idx2), int(idx3))
        bond_angles_tuplewise.append(angle)
    
        key = f"{elem1}-{elem2}-{elem3}"
        if key not in bond_angles:
            bond_angles[key] = [angle]
        else:
            bond_angles[key].append(angle)
        #print(angle_A_B_C(int(idx1), int(idx2), int(idx3)))
        
    return bond_angles_tuplewise, bond_angles



def get_bond_dihedrals(POS, bond_quadruples):
    
    bond_dihedrals = {}
    bond_dihedrals_tuplewise = []
    
    for idx in bond_quadruples:
        match1 = re.match(r'([A-Z][a-z]?)(\d+)', idx[0])
        elem1, idx1 = match1.groups()
        match2 = re.match(r'([A-Z][a-z]?)(\d+)', idx[1])
        elem2, idx2 = match2.groups()
        match3 = re.match(r'([A-Z][a-z]?)(\d+)', idx[2])
        elem3, idx3 = match3.groups()
        match4 = re.match(r'([A-Z][a-z]?)(\d+)', idx[3])
        elem4, idx4 = match4.groups()
    
        diangle=dihedral_angle_A_B_C_D(POS, int(idx1), int(idx2), int(idx3), int(idx4))
        bond_dihedrals_tuplewise.append(diangle)
        
        key = f"{elem1}-{elem2}-{elem3}-{elem4}"
        if key not in bond_dihedrals:
            bond_dihedrals[key] = [diangle]
        else:
            bond_dihedrals[key].append(diangle)
        #print(dihedral_angle_A_B_C_D(int(idx1), int(idx2), int(idx3), int(idx4)))

    return bond_dihedrals_tuplewise, bond_dihedrals


## sometime, reading the xyz file, which has extraline at the end of file, causes erro
## I am using try-except block to avoid the same.


#try:
#    POS = ase.io.read("Al2S3.xyz", format="xyz")
#except ValueError:
#    # remove blank lines and retry
#    with open("Al2S3.xyz") as f:
#        lines = [l for l in f if l.strip()]
#    with open("Al2S3.xyz", "w") as f:
#        f.writelines(lines)
#    POS = ase.io.read("Al2S3.xyz", format="xyz")
#
#
#
#
#
#bond_pairs, bond_triples, bond_quadruples = get_tuples(POS)
#
#python_vesta_indices = creating_index_mapping_dict(POS)
#vesta_bond_pairs = Convert_Indices(python_vesta_indices[0], bond_pairs)
#vesta_bond_triples = Convert_Indices(python_vesta_indices[0], bond_triples)
#vesta_bond_quadruples = Convert_Indices(python_vesta_indices[0], bond_quadruples)
#
#
#
#bond_lengths = get_bond_lengths(POS, bond_pairs)
#
#for bp, bl in zip(vesta_bond_pairs, bond_lengths[0]):
#    print(bp, round(bl, 3))
#
#print(range_finder(bond_lengths[1]))


for file in [ "Al2S12_hse_1.out.xyz","Al2S12_pbe_1.out.xyz","Al2S18_hse_1.out.xyz","Al2S18_pbe_1.out.xyz","Al2S3_hse_1.out.xyz","Al2S3_pbe_1.out.xyz","Al2S6_hse_1.out.xyz","Al2S6_pbe_1.out.xyz" ]:
    print("**************{}************".format(file))
    POS = ase.io.read(file, format="xyz")
    bond_pairs, bond_triples, bond_quadruples = get_tuples(POS)
    
    python_vesta_indices = creating_index_mapping_dict(POS)
    vesta_bond_pairs = Convert_Indices(python_vesta_indices[0], bond_pairs)
    bond_lengths = get_bond_lengths(POS, bond_pairs)
    
    for bp, bl in zip(vesta_bond_pairs, bond_lengths[0]):
        print(bp, round(bl, 2))
    
    print(range_finder(bond_lengths[1]))

#print("bond-pairs (vesta-indices):", Convert_Indices(python_vesta_indices[0], bond_pairs))
#print("--"*20)
#print("bond-triples (vesta-indices):", Convert_Indices(python_vesta_indices[0], bond_triples))
#print("--"*20)
#print("bond-quadruples (vesta-indices):", Convert_Indices(python_vesta_indices[0], bond_quadruples))
#print("--"*20)

#print(get_bond_dihedrals(POS, bond_quadruples))
#bond_lengths = get_bond_lengths(POS, bond_pairs)
#bond_angles = get_bond_angles(POS, bond_triples)
#bond_dihedrals = get_bond_dihedrals(POS, bond_quadruples)

#print("bond-lenghts_tuplewise:", bond_lengths[0])
#print("--"*20)
#print("bond-angles_tuplewise:", bond_angles[0])
#print("--"*20)
#print("bond-dihedrals_tuplewise:", bond_dihedrals[0])
#print("--"*20)
#
#
#
#print("bond-lenghts:", bond_lengths[1])
#print("--"*20)
#print("bond-angles:", bond_angles[1])
#print("--"*20)
#print("bond-dihedrals:", bond_dihedrals[1])
#print("--"*20)
#
#
#range_finder(bond_lengths[1])
#print("--"*20)
#range_finder(bond_angles[1])
#print("--"*20)
#range_finder(bond_dihedrals[1])
#print("--"*20)
