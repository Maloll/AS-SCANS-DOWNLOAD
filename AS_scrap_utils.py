import re
import requests
from bs4 import BeautifulSoup


def nettoyage(title):
    # nettoie le titre pour les noms de dossiers
    name = title.lower().replace(" ", "_")
    return "".join(c for c in name if c.isalnum() or c == "_")

def est_le_bon_pannel(tag):
    # verifie si la div contient le script des scans
    return tag.name == "div" and tag.find("script", recursive=False) is not None

def recherche(search_url):
    # lance la recherche sur le catalogue
    reponse = requests.get(search_url)
    soup = BeautifulSoup(reponse.text, 'html.parser')
    cartes = soup.find_all('div', class_='catalog-card')
    data = []
    nb = 1
    for carte in cartes:
        genres = "Non spécifié"
        info_rows = carte.find_all('div', class_='info-row')
        for row in info_rows:
            label = row.find('span', class_='info-label').get_text(strip=True)
            if label == "Genres":
                genres = row.find('p', class_='info-value').get_text(strip=True)
        titre = carte.find('h2').get_text(strip=True)
        item = {
            "titre": titre,
            "lien": carte.find('a')['href'],
            "image": carte.find('img')['src'],
            "genres": genres,
            "synopsis": carte.find('div', class_='synopsis-content').get_text(strip=True)
        }
        print(f"{nb:2}   titre : {titre}")
        nb += 1
        data.append(item)
    return data

def seasons(url_choix):
    # recupere les differentes saisons ou arcs dispos
    reponse = requests.get(url_choix)
    soup = BeautifulSoup(reponse.text, 'html.parser')
    titre_oeuvre = soup.find('h4', id="titreOeuvre").get_text(strip=True)
    pannels = soup.find_all(est_le_bon_pannel)
    seasons = []
    i = 1
    print(f"Saisons trouvées sur {titre_oeuvre} : ")
    for pannel in pannels:
        script = pannel.find('script').get_text(strip=True)
        if "panneauScan" in script:
            found = re.findall(r'panneauScan\("(.*?)",\s*"(.*?)"\)', script)
            for titre, url in found:
                if titre != "nom":
                    print(f"  {i:3} - {titre:40}")
                    lien = f"{url_choix.rstrip('/')}/{url.rstrip('/')}"
                    seasons.append({"titre": titre, "lien": f"{lien}"})
                    i += 1
    return seasons

def nbEpisodes(url_saison):
    # recupere la liste des episodes si applicable
    reponse = requests.get(f"{url_saison}/episodes.js")
    lecteurs = re.findall(r"var (.*?) = \[(.*?)\];", reponse.text, re.DOTALL)
    if lecteurs:
        print(f"nb lecteurs trouvé : {len(lecteurs)}")
        
        for lecteur in lecteurs:
            if "https://video.sibnet.ru/" in lecteur[1]:
                return re.findall(r"\'https://(.*?)\'", lecteur[1], re.DOTALL)
    return []

def download(reponse, titre):
    # sauvegarde le contenu binaire en jpg
    with open(f"{titre}.jpg", "wb") as fichier:
        fichier.write(reponse.content)
    #print(f"Page {titre} enregistré")

def nbPages(Oeuvre, chapitre):
    # interroge l api pour le nombre de pages
    try:
        api = "https://anime-sama.to/s2/scans/get_nb_chap_et_img.php"
        settings = {"oeuvre" : f"{Oeuvre}"}
        reponse = requests.get(api, params=settings)
        if reponse:
            json_data = reponse.json()
            return json_data[f'{chapitre}'], len(json_data)
    except : return "erreur", "erreur"
    
def getNomOeuvre(url):
    # recupere le titre propre de l oeuvre
    reponse = requests.get(url)
    soup = BeautifulSoup(reponse.text, 'html.parser')
    return soup.find('h3', id="titreOeuvre").get_text(strip=False)

def verifChap(nomOeuvre, chapitre):
    # verifie si le chapitre existe sur le serveur
    base_url = f"https://anime-sama.to/s2/scans/{nomOeuvre}/"
    url = f"{base_url}{chapitre}/1.jpg"
    if requests.head(url).status_code == 200:
        return True
    return False