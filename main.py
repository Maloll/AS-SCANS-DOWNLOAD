import json
from os import system
import os
from AS_scrap_utils import *
from Download import DownloadChap
import shutil
import time
import json

search_url = "https://anime-sama.to/catalogue/?type[]=Scans&search="


def choose_path():
    base_path = input("Veuillez ajoutez un chemin de téléchargement \n(ex : \"C:/Users/user1/Documents/Scans\"): ")
    data = {"download_path": f"{base_path}"}
    with open("settings.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

if not os.path.exists("settings.json") :
    choose_path()

if os.path.exists("settings.json"):
    with open("settings.json", "r") as f :
        jsonData = json.load(f)
        base_path = jsonData['download_path']
        if not os.path.exists(base_path):
            choose_path()


system('cls')
search = input("Recherche : ")
system('cls')
recherches = recherche(f"{search_url}{search}")

if len(recherches) == 1:
    choix_scan = 1
elif len(recherches) < 1:
    print("Aucun résultat")
    exit()
else:
    choix_scan = int(input("Choix Scan : "))
if choix_scan:
    system('cls')
    scan = recherches[choix_scan - 1]
    les_seasons = seasons(scan['lien'])
    if len(les_seasons) == 1:
        choix_saison = 1
    else:
        choix_saison = int(input("Choix saison : "))
    while not choix_saison and choix_saison == 0:
        choix_saison = int(input("Choix saison : "))
    if choix_saison:
        system('cls')
        lien = les_seasons[choix_saison - 1]['lien']
        nomOeuvre = getNomOeuvre(lien)
    chapValide = False
    while not chapValide :
        system('cls')
        b, c = nbPages(nomOeuvre, 1)
        print(f"Choix : {nomOeuvre} - Nombre de chapitres : {c}")
        choix_chapitre_d = int(input("Chapitre Début : "))
        choix_chapitre_f = int(input("Chapitre Fin : "))
        couleur = input("Couleurs ? (O/N): ")
        if couleur.lower() == "o":
            q = 8
        else:
            q = 25
        if choix_chapitre_d and verifChap(nomOeuvre,choix_chapitre_d) and choix_chapitre_d != 0:
                chapValide = True
                system('cls')
                for i in range(choix_chapitre_d, choix_chapitre_f + 1):
                    DownloadChap(nomOeuvre, i, base_path)
                time.sleep(2)
                print("Nettoyage des téléchargements...")
                for i in range(choix_chapitre_d, choix_chapitre_f + 1):
                    chemin = f"{base_path}\\{nomOeuvre.strip()}\\{i}"
                    shutil.rmtree(chemin)