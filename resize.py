
from PIL import Image
import os, sys

path = "D:/SelfdrivingCar-main/data/images/"
dirs = os.listdir( path )

def crop():
    for item in dirs:
        if os.path.isfile(path+item):
            im = Image.open(path+item)
            f, e = os.path.splitext(path+item)
            im = im.crop((0, 350, 1600, 900))
            im = im.resize((480,277), Image.ANTIALIAS)
            im.save("D:/SelfdrivingCar-main/data/resized/" + 'rb'+ item)

crop()