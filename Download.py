import re
import requests
from bs4 import BeautifulSoup
from AS_scrap_utils import download, nbPages
import os
from concurrent.futures import ThreadPoolExecutor
import base64

def images_to_html(chemin_chap, nbPages, nomOeuvre, numChapitre, chemin_save):
    html = []
    with open("css.txt","r") as f:
        css = f.read()
        html.append(css)
    for i in range(1, nbPages+1):
        with open(f"{chemin_chap}/{i}.jpg", "rb") as f:
            data =  base64.b64encode(f.read()).decode('utf-8')
        html.append(f'<img src="data:image/webp;base64,{data}">\n')
    html.append("</div>")
    with open(f"{chemin_save}/{nomOeuvre} - {numChapitre}.html", "w") as f :
        for lines in html :
            f.write(lines)

def DownloadChap(nomOeuvre, chapitre, base_path) :
    base_url = f"https://anime-sama.to/s2/scans/{nomOeuvre}/"
    url_chapitre = f"{base_url}{chapitre}/"
    pages, chapitres = nbPages(f"{nomOeuvre}", f"{chapitre}")

    nomOeuvre = nomOeuvre.strip()
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    if not os.path.exists(f"{base_path}/{nomOeuvre}"):
        os.makedirs(f"{base_path}/{nomOeuvre}")
    if not os.path.exists(f"{base_path}/{nomOeuvre}/{chapitre}"):
        os.makedirs(f"{base_path}/{nomOeuvre}/{chapitre}")
    chemin = f"{base_path}/{nomOeuvre}/{chapitre}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    def toute_les_img(i):
        url = f"{url_chapitre}{i}.jpg"
        reponse = requests.get(url, headers=headers)
        download(reponse, f"{chemin}/{i}")

    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(toute_les_img, range(1, pages + 1))
    
    images_to_html(chemin,pages,nomOeuvre,(chapitre - 1),f"{base_path}/{nomOeuvre}")
    print(f"Chapitre : {chapitre} Téléchargé")