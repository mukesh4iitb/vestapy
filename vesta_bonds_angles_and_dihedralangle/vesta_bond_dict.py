# Creating a dictionary based on vesta_bond.txt file (this file is part of vesta software).

bond_dict = {}

with open("vesta_bond.txt") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue  # skip comments and empty lines

        parts = line.split()
        index, a, b, dist = parts[0], parts[1], parts[2], float(parts[3])

        # create the dictionary.
        bond_dict[(a, b)] = dist
