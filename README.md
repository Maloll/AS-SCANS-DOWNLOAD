# AS-SCANS-DOWNLOAD

Un outil simple en ligne de commande (CLI) pour naviguer et télécharger rapidement des scans directement depuis **Anime-Sama**.

## 🚀 Fonctionnalités
Ce tool te permet de :
* **Rechercher** un manga/manwha directement dans ton terminal.
* **Naviguer** dans la liste des chapitres disponibles.
* **Télécharger une plage de chapitres** : Tu donnes le chapitre de début, le chapitre de fin, et le script s'occupe du reste.
* (Les chapitres sont sauvegarder au format **.png**, sous la forme d'une longue et unique image, ce qui rends les scans lisible sur mobile comme sur desktop)

## 🛠️ Utilisation
1. Lance le script.
2. Tape le nom du manga/manhwa que tu cherches.
3. Sélectionne le manga/manhwa dans la liste.
4. Indique la plage de chapitres à récupérer (ex : du chapitre 10 au 25).
5. Les chapitres sont téléchargés en long **.png** et triés par dossier.


## ❓ Comment ça marche
1. Le script vérifie le chemin (path) de téléchargement et lance la recherche.
2. L'utilisateur choisit le manga/manhwa, la saison et la plage de chapitres.
3. Le script télécharge toutes les images de chaque chapitre et les range dans des dossiers séparés.
4. Une fois qu'un chapitre est entièrement téléchargé, un script qui fusionne toutes les pages d'un chapitre en une seule se lance en arrière-plan avec **subprocess**.
5. Le script supprime les téléchargements temporaires et ne laisse que les chapitres finis.
---

## 📦 Installation

### 1. Cloner le projet
```bash
git clone [https://github.com/maloll/AS-SCANS-DOWNLOAD.git](https://github.com/maloll/AS-SCANS-DOWNLOAD.git)
cd AS-SCANS-DOWNLOAD
```

## 2. Télécharger les dépendances 
```bash
pip install requests beautifulsoup4 numpy opencv-python
```