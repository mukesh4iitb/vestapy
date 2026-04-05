import numpy as np

def reciprocal_lattice(a, b, c):
    """Compute reciprocal lattice vectors."""
    v = np.dot(a, np.cross(b, c))
    a_star = 2 * np.pi * np.cross(b, c) / v
    b_star = 2 * np.pi * np.cross(c, a) / v
    c_star = 2 * np.pi * np.cross(a, b) / v
    return a_star, b_star, c_star

def make_scene_matrix(a, b, c, view='a'):
    """
    Constructs the SCENE rotation matrix for viewing along 'a', 'b', 'c', 'a*', 'b*', or 'c*'.
    
    Parameters:
        a, b, c : np.ndarray
            Lattice vectors as 3-element arrays.
        view : str
            Which direction to view along: 'a', 'b', 'c', 'a*', 'b*', or 'c*'.
    
    Returns:
        scene : np.ndarray
            4x4 SCENE matrix suitable for VESTA.
    """
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)
    c = np.array(c, dtype=float)
    
    # Calculate reciprocal lattice vectors
    a_star, b_star, c_star = reciprocal_lattice(a, b, c)
    
    if view == 'a':
        z = a / np.linalg.norm(a)
        x_proj = b - np.dot(b, z) * z
        x = x_proj / np.linalg.norm(x_proj)
        y = np.cross(z, x)
    elif view == 'b':
        z = b / np.linalg.norm(b)
        x_proj = c - np.dot(c, z) * z
        x = x_proj / np.linalg.norm(x_proj)
        y = np.cross(z, x)
    elif view == 'c':
        z = c / np.linalg.norm(c)
        x_proj = a - np.dot(a, z) * z
        x = x_proj / np.linalg.norm(x_proj)
        y = np.cross(z, x)
    elif view == 'a*':
        z = a_star / np.linalg.norm(a_star)
        x_proj = b_star - np.dot(b_star, z) * z
        x = x_proj / np.linalg.norm(x_proj)
        y = np.cross(z, x)
    elif view == 'b*':
        z = b_star / np.linalg.norm(b_star)
        x_proj = c_star - np.dot(c_star, z) * z
        x = x_proj / np.linalg.norm(x_proj)
        y = np.cross(z, x)
    elif view == 'c*':
        z = c_star / np.linalg.norm(c_star)
        x_proj = a_star - np.dot(a_star, z) * z
        x = x_proj / np.linalg.norm(x_proj)
        y = np.cross(z, x)
    else:
        raise ValueError('view must be "a", "b", "c", "a*", "b*", or "c*"')

    # Stack as columns: x, y, z
    R = np.column_stack([x, y, z])
    scene = np.eye(4)
    scene[:3, :3] = R
    return scene.T  # VESTA expects the transpose

# Example usage:
# a = [a_x, a_y, a_z]
# b = [b_x, b_y, b_z]
# c = [c_x, c_y, c_z]
# scene_matrix = make_scene_matrix(a, b, c, view='b*')



a = [13.6800219299413364,   -0.1286632048488978,    0.0176988603057369]
b = [-6.9513628983464244,   11.9305489972695877,   -0.0312093214987958]
c = [ 0.0363222249194201,   -0.0139817097582095,   21.8106145823089577]



# Example usage:
# a, b, c = np.array([a_x, a_y, a_z]), np.array([b_x, b_y, b_z]), np.array([c_x, c_y, c_z])
print(make_scene_matrix(a, b, c, view='a'))
print(make_scene_matrix(a, b, c, view='b'))
print(make_scene_matrix(a, b, c, view='c'))

print(make_scene_matrix(a, b, c, view='a*'))
print(make_scene_matrix(a, b, c, view='b*'))
print(make_scene_matrix(a, b, c, view='c*'))
