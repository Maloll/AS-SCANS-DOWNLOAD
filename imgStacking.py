import cv2
import numpy as np
from AS_scrap_utils import nbPages
import sys

if len(sys.argv) > 2:
    nomOeuvre = sys.argv[1]
    chapitre = sys.argv[2]
    q = int(sys.argv[3])
    chemain = sys.argv[4]


pages, chap = nbPages(nomOeuvre, chapitre)
nomOeuvre = nomOeuvre.strip()
path1 = f"{chemain}/{nomOeuvre}/{chapitre}/1.jpg"
img1 = cv2.imread(path1)
liste = []
liste.append(img1)
for i in range(2, pages + 1):
    path2 = f"{chemain}/{nomOeuvre}/{chapitre}/{i}.jpg"
    img2 = cv2.imread(path2)
    if img1 is None or img2 is None:
        print("Path Error !!!")
    else:
        if img1.shape[1] != img2.shape[1]:
            larg = img1.shape[1]
            ratio = larg / img2.shape[1]
            haut = int(ratio * img2.shape[0])
            img2 = cv2.resize(img2, (larg, haut))
        liste.append(img2)
img_stack = np.vstack(liste)
img_f = (img_stack // q) * q
success, buffer = cv2.imencode("blup.png", img_f, [cv2.IMWRITE_PNG_COMPRESSION, 5])
if success:
    with open(f"{chemain}/{nomOeuvre}/{chapitre}.png", "wb") as f:
        f.write(buffer)
    print(f"Sauvegarde du chapitre {chapitre} réussie !")
else:
    print(f"Erreur lors de la sauvegarde du chapitre {chapitre}")