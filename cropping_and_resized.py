import os
import numpy as np
import cv2
from PIL import Image

def functions():
    """Return a list of public functions in this module."""
    import inspect
    return sorted([
        name for name, obj in globals().items()
        if inspect.isfunction(obj) and not name.startswith("_")
    ])


def croping_image_using_px_py_h_w(file, px, py, h, w):
    """
    file: name of being cropped.
    px, py: are pixel of image, which can be found with GIMP.
    w, h : width and height of image, which again can be found using GIMP.

    Note: In my experience, cv2 is good with croping file, while PIL is good with resizing.
    """
    img = cv2.imread("{}".format(file))

    #px, py = 1019, 321
    #w, h = 1875, 1452

    x1, y1 = px, py
    x2, y2 = x1+w, y1+h

    # Define crop area (y1:y2, x1:x2)
    cropped = img[y1: y2, x1:x2]

    # Save cropped image
    cropped_name=file.split(".tif")[0]+"_man_cropped.tif"
    cv2.imwrite("{}".format(cropped_name), cropped)

#croping_image_using_px_py_h_w("e01_man_cropping.tif", px=1019, py=321, w=1875, h=1452)

# Load the image
#for file in [ "CONTCAR_Li2S_cropped.tif", "CONTCAR_Li1_cropped.tif","CONTCAR_Li2_cropped.tif","CONTCAR_Li3_cropped.tif","CONTCAR_Li4_cropped.tif","POSCAR_Li1_cropped.tif","POSCAR_Li2_cropped.tif","POSCAR_Li3_cropped.tif","POSCAR_Li4_cropped.tif" ]:


def resizing_image_using_width_height_dip(file, width_in, height_in, dpi=600):
    """
    width_in, height_in : width, and height of final image, which can be directly taken from PPT size.
    dpi = with value of 600, it seems to be good. So, I will stick with it, unless, something, I need to change drastically.

    Note: In my experience, cv2 is good with croping file, while PIL is good with resizing.
    """

    # target size in inches
    #width_in = 1.85
    #height_in = 1.42

    # convert to pixels
    target_w = int(width_in * dpi)
    target_h = int(height_in * dpi)

    img = Image.open(file)
    w, h = img.size

    # Compute scale factor so that the **larger dimension** fits the target
    scale = max(target_w / w, target_h / h)

    # New dimensions that preserve aspect ratio
    width_px = int(w * scale)
    height_px = int(h * scale)


    img = Image.open("{}".format(file))
    resized = img.resize((width_px, height_px), Image.LANCZOS)


    resized_name=file.split("_cropped.tif")[0]+"_resized.tif"
    resized.save(resized_name, dpi=(dpi,dpi))

#resizing_image_using_width_height_dip("e01_man_cropping_man_cropped.tif", width_in=1.85, height_in=1.42, dpi=600)

def crop_by_color(file, border=5, bg_color=(255, 255, 255)):
    """
    Crop an image based on presence of color (non-background)
    :param file: image
    :param border: Border in pixels to leave around the object
    :param bg_color: Background color (default white)
    :return: Cropped image
    """
    # Read image
    img = cv2.imread(file, cv2.IMREAD_UNCHANGED)

    # Create a mask where non-background pixels are 1
    mask = cv2.inRange(img, np.array([0,0,0]), np.array([254,254,254]))
    # For colored images, mask will pick anything not pure white

    # Find coordinates of non-zero pixels
    coords = cv2.findNonZero(mask)  # returns N x 1 x 2 array
    if coords is None:
        print(f"No non-background pixels found in {file}")
        return img

    # Get bounding rectangle
    x, y, w, h = cv2.boundingRect(coords)

    # Add border and clip to image size
    x1 = max(x - border, 0)
    y1 = max(y - border, 0)
    x2 = min(x + w + border, img.shape[1])
    y2 = min(y + h + border, img.shape[0])

    cropped = img[y1:y2, x1:x2]
    
    # Save cropped image
    cropped_name=file.split(".tif")[0]+"_cc_cropped.tif"
    cv2.imwrite("{}".format(cropped_name), cropped)
    return cropped


#cropped_img = crop_by_color("e02_cc_cropping.tif", border=20)



