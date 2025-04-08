# Exemple de résultat des matchs de la champion league après le tirage aléatoire

<p align="center">
  <img src="https://github.com/user-attachments/assets/1dfbbda6-df37-482b-9601-25b7da3ea446" />
</p>

# Consignes du tirage

Les équipes sont répartis en 4 chapeaux de 9 équipes.<br>
Chaque équipe :

- Affrontera 8 équipes au total donc deux par chapeau

- 2 équipes par chapeau, l’un à domicile(home) et l’autre à l’extérieur(away).

- Aucune équipe de son championnat(du meme pays)

- 2 équipes maximum du même championnat.

- le choix des matchs est aléatoire

- le tirage final est generé dans un format pdf pour visualiser le resultat du tirage

# utilisation du projet

1. ## Créer le venv(environnement virtuel)

```cmd
   python3.11 -m venv venv
   ou
   py3.11 -m venv venv
```

2. ## Activer l'environnement virtuel

```cmd
   # windows:
   venv/Scripts/activate
   # mac ou linux:
   source venv/bin/activate
```

3. ## Installer toutes les dependances

```cmd
 pip install -r requirements.txt
```

4. ## Placer vous à la racine du projet et lancez le tirage<br>
   Rassure vous que python est accecible en ligne de commande et executez la commande ci-dessous

```cmd
   # mac ou linux
   python3.11 main.py

   # windows
   py3.11 main.py
```

si vous utilisez un editeur de code comme vscode vous pouvez vous placez dans le fichier `main.py` et lancer la commande depuis en haut à droite de l'éditeur.

5. ## Voir les resultats

   Une fois le tirage effectué, regardé dans le dossier data vous aller apercevoir un fichier tirage.pdf qui contient le resultat du tirage.<br>
   ouvrer le fichier pdf avec votre lecteur pdf et visualisez les matchs

6. ## Comprendre le principe de generation de la maquette

   Si vous voulez comprendre le principe de génération de la maquette, vous pouvez dans le dossier `data` ouvrir le fichier `images/skeleton_model_pdf.png`

7. ## Comprendre le principe pour générer le tirage<br>
   Si vous voulez comprendre le principe du code ou si vous avez des questions, vous pouvez me contactez directement sur [LinkedIn](https://www.linkedin.com/in/ulrich-chokomeny/).
