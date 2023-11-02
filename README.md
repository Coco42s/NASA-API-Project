# NASA API Request

## Description
Cette application a été créé dans le cadre d'un projets en cours de NSI
Cette application Python permet aux utilisateurs d'interagir avec l'API de la NASA pour récupérer des informations sur les rover martien, image du jour et d'autre sujet . Les utilisateurs peuvent adresser des requêtes à l'API de la NASA et recevoir diverses données, telles que des images, des faits astronomiques, etc.

---

## Features

- **NASA API Integration**: L'application s'intègre parfaitement à l'API de la NASA pour récupérer des données en temps réel.
- **User-Friendly**: Interface simple et facile à utiliser pour effectuer des requêtes API.
- **Customization**: Les utilisateurs peuvent personnaliser leurs demandes pour spécifier le type d'informations qu'ils souhaitent récupérer.

---

## Installation

Avant de commencer l'utilisation de l'application, veuillez suivre ces étapes préalables :

### 1. Vérifier l'installation de Python 3.11

Assurez-vous que Python 3.11 est installé sur votre machine.

### 2. Installation de la police de caractères

Dans le dossier `font` :
- **Windows:**
    - Double-cliquez sur la police de caractères.
    - Cliquez sur "Installer" dans la nouvelle fenêtre.
- **Mac OS:**
    - Ouvrez Font Book.
    - Accédez à la section "Utilisateur".
    - Cliquez sur "+".
    - Recherchez la police dans le dossier de l'application (`source de l'application/font`).
    - Cliquez sur "Ouvrir".

### 3. Installation de FFmpeg

Installez [FFmpeg](https://ffmpeg.org/download.html) sur votre système.

### 4. Installation de pkg-config

Installez `pkg-config` sur votre système.
- **Windows**
   1. Installez MSYS2 à partir du site officiel : [MSYS2](https://www.msys2.org/)
   2. Après l'installation, ouvrez le terminal MSYS2 et mettez à jour le système de paquets en utilisant les commandes suivantes :

```bash
   pacman -Syu
```

   3. Ensuite, installez pkg-config en utilisant la commande suivante :

```bash
   pacman -S mingw-w64-x86_64-pkg-config
```

- **Linux**
   1. Installer `pkg-config` sur linux via un terminals
```bash
sudo apt-get install pkg-config
```

### 5. Lancer setup_lib

Exécutez le script `setup_lib` qui installera toutes les bibliothèques nécessaires au bon fonctionnement de l'application. 

**IMPORTANT : NE PAS ARRÊTER MÊME S'IL Y A UNE ERREUR.**

```bash
python lib\setup_lib.py
```

### 6. Assurez-vous que le dossier 'assets' contient les sous-dossiers suivants :

S'ils ne sont pas présents, veuillez les créer.

1. 'APOD'
2. 'EPIC'
3. 'MRP'

### 7. Vérifiez également la présence du fichier 'icons8-nasa-16.png' dans le dossier 'assets'.

S'il n'est pas présent, veuillez mettre en commentaire les lignes 35, 36 et 37.

### 8. Clé API NASA

Veuillez mètre votre clé d'api a la ligne 29
Vous pouvez vous procurer une clé d'API sur le site d'api de la NASA [API_NASA](https://api.nasa.gov/)

---

## Lancement de l'Application

Pour lancer l'application, suivez ces étapes simples :

1. Assurez-vous d'avoir suivi les étapes d'installation décrites précédemment.

2. Ouvrez un terminal ou une ligne de commande.

3. Accédez au dossier source de l'application.

4. Exécutez le fichier `NASA_API_Requests.py` avec Python.

```bash
    python NASA_API_Requests.py
```

5. L'interface utilisateur de l'application devrait s'ouvrir, vous permettant de commencer à explorer les fonctionnalités de la NASA API.

**Note :** Assurez-vous que toutes les dépendances sont correctement installées avant de lancer l'application.
**Note :** Tout les date doit être noter sous la forme YYYY-MM-DD.

N'hésitez pas à explorer et à apprécier les merveilles de l'univers avec NASA API Request !

---

## Créateur

Ce projet a été créé par [Molines Corentin]().

---

## Problèmes Connus

Actuellement, le projet présente certains problèmes connus que nous travaillons activement à résoudre. Si vous rencontrez l'un de ces problèmes, veuillez consulter les solutions provisoires recommandées ou attendre la prochaine mise à jour du projet.

1. **Video APOD : [La video avance trop vite]**
   - *Solution provisoire : Ne rien faire sa gène pas le code.*

2. **changement d'interfaces (RARE) : [lor du changement de une api a EPIC quand elle est petit il se peut que python prène les devent et ne télécharge pas le fichier d'information en premier et sa fais une ereur car le fichier est incoplait]**
   -*solution provisoir : ne pas changer vers EPIC quand sais le première mise en petit format*

N'hésitez pas à [Me contacter](Contact) si vous rencontrez d'autres problèmes non répertoriés ici.

---

## Fonctionnalités

Découvrez les fonctionnalités clés offertes par notre projet :

1. **Intégration NASA API :**
   - Accédez aux dernières données de l'Agence spatiale américaine pour explorer des informations sur l'espace, les planètes, et bien plus encore.

2. **Interface Utilisateur Conviviale :**
   - Profitez d'une interface utilisateur intuitive, permettant une interaction aisée avec les fonctionnalités de l'application.

3. **Personnalisation des Requêtes :**
   - Personnalisez vos requêtes pour spécifier les types d'informations que vous souhaitez obtenir de l'API de la NASA.

4. **Compatibilité Multiplateforme :**
   - Utilisez l'application sur divers systèmes d'exploitation, offrant une flexibilité d'utilisation.

5. **Documentation Complète :**
   - Consultez une documentation détaillée pour faciliter l'installation, la configuration, et l'utilisation de l'application.

Explorez ces fonctionnalités pour tirer le meilleur parti de l'expérience offerte par notre projet.

---

## Licence

Ce projet est sous licence GNU General Public License (GPL) - voir le fichier [LICENSE](LICENSE) pour plus de détails.

La licence GPL est une licence open source qui garantit que le logiciel est librement accessible, modifiable et distribuable par quiconque. Assurez-vous de lire et de comprendre les termes de la licence avant d'utiliser, copier, modifier ou distribuer ce logiciel.

---

## Contact

Si vous avez des questions, des commentaires ou des suggestions, n'hésitez pas à nous contacter. Nous sommes là pour vous aider !

- **Adresse e-mail :** [corentrain7@gmal.com](mailto:corentrain7@gmal.com)

Nous sommes reconnaissants de votre intérêt pour notre projet et sommes impatients de vous entendre !

---