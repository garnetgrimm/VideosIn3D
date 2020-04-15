import numpy as np
from PIL import Image
import glob
import os

folder = "anim"

files = glob.glob('anim/*')
for f in files:
    os.remove(f)

files = glob.glob('out/*')
for f in files:
    os.remove(f)

os.system("convert -coalesce ./g.gif anim/xx_%05d.png")

filelist = os.listdir(folder)
for fichier in filelist[:]: # filelist[:] makes a copy of filelist.
    if not(fichier.endswith(".png")):
        filelist.remove(fichier)

arrList = []
for imgName in filelist:
    img = Image.open(folder + "/" + imgName)
    arr = np.array(img)
    arrList.append(arr)


for frame in range(0, np.size(arrList[0],1)):
    newImg = np.zeros(( len(arrList), np.size(arrList[0],0), 3 ), dtype=np.uint8)
    for y in range(0, np.size(newImg, 0)):
        for x in range(0, np.size(newImg, 1)):
            newImg[y][x] = arrList[y][x][frame]
    new_im = Image.fromarray(newImg)
    new_im.save("out/frame"+str(frame)+".png")

os.system("convert -delay 10 -loop 0 out/*.png animation.gif")
files = glob.glob('out/*')
for f in files:
    os.remove(f)
