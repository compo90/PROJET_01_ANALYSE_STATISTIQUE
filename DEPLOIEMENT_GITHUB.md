# Guide de déploiement GitHub — PROJET 01

> Guide pas à pas pour publier le projet sur GitHub depuis ta machine (Windows / Linux / Mac).
> Le dossier est prêt : README, code, notebook exécuté, rapport PDF, page HTML, post LinkedIn.

---

## Étape 0 — Vérifier que git est installé

Ouvre un terminal (PowerShell, CMD, bash) et tape :

```bash
git --version
```

Si git n'est pas installé :
- **Windows** : https://git-scm.com/download/win
- **Mac** : `brew install git`
- **Linux** : `sudo apt install git`

Première configuration (une seule fois par machine) :

```bash
git config --global user.name "Aboubacar COMPO"
git config --global user.email "abccompo90@gmail.com"
git config --global init.defaultBranch main
```

---

## Option A — Ligne de commande (recommandée)

### 1. Se placer dans le dossier du projet

```bash
cd "MON PORTOFOLIO/PROJET_01_ANALYSE_STATISTIQUE"
```

(Adapte selon le chemin réel sur ta machine.)

### 2. Initialiser le dépôt local

```bash
git init -b main
git add .
git status
```

`git status` doit lister tous tes fichiers (README, src/, notebooks/, outputs/, data/, etc.).

### 3. Premier commit

```bash
git commit -m "feat: projet 01 analyse statistique complete sur marches financiers

- Dataset synthetique 50k observations x 34 variables (6 secteurs)
- 6 parties : univariee, distributions, echantillonnage, bivariee, tests, PCA
- Scripts modulaires Python (src/)
- Notebook Jupyter pedagogique execute
- Rapport PDF de synthese (10 pages)
- Page HTML interactive avec SVG
- Post LinkedIn bilingue (FR/EN)"
```

### 4. Créer le dépôt sur GitHub.com

1. Va sur https://github.com/new
2. Nom suggéré : `portfolio-ds-01-analyse-statistique` (ou `projet-01-analyse-statistique-finance`)
3. Description : `Analyse statistique complete sur 50k observations boursieres — 6 piliers du data scientist (univariee, distributions, echantillonnage, bivariee, tests, PCA).`
4. **Public** (c'est ton portfolio)
5. **NE COCHE PAS** "Add a README", "Add .gitignore", "Choose a license" — on a déjà les fichiers localement
6. Clique **Create repository**

### 5. Lier le dépôt local au dépôt distant

GitHub te donne les commandes. Copie-colle :

```bash
git remote add origin https://github.com/<TON-USERNAME>/portfolio-ds-01-analyse-statistique.git
git push -u origin main
```

Remplace `<TON-USERNAME>` par ton pseudo GitHub.

### 6. Authentification

La première fois, GitHub demande un **Personal Access Token** (pas ton mot de passe).

Pour en créer un :
1. https://github.com/settings/tokens → `Generate new token (classic)`
2. Nom : `cli-portfolio`
3. Expiration : 90 jours (ou plus)
4. Scopes : coche **repo** (suffisant pour push)
5. Génère et **copie le token** (tu ne le reverras plus)
6. Quand git demande le password, colle le token

Alternative plus propre : installer **GitHub CLI** (`gh auth login`) qui gère ça automatiquement.

---

## Option B — GitHub Desktop (interface graphique)

Si tu préfères cliquer plutôt que taper :

1. Télécharge GitHub Desktop : https://desktop.github.com/
2. Connecte-toi avec ton compte GitHub
3. **File → Add local repository** → sélectionne le dossier `PROJET_01_ANALYSE_STATISTIQUE`
4. GitHub Desktop propose d'initialiser un dépôt git → **Initialize**
5. Écris un message de commit dans la zone en bas à gauche (titre + description) → **Commit to main**
6. Clique **Publish repository** en haut → coche "Public" → **Publish repository**

C'est tout. Le projet est en ligne.

---

## Option C — GitHub CLI (`gh`) — pour utilisateurs avancés

Si tu as `gh` installé :

```bash
cd "MON PORTOFOLIO/PROJET_01_ANALYSE_STATISTIQUE"
git init -b main
git add .
git commit -m "feat: projet 01 analyse statistique"
gh repo create portfolio-ds-01-analyse-statistique --public --source=. --remote=origin --push
```

Une seule commande pour créer le dépôt distant et pousser. `gh auth login` au préalable si jamais.

---

## Après le push — actions à faire sur GitHub

### 1. Ajouter une description + topics

Sur la page du dépôt → roue crantée ⚙️ à côté de "About" :
- Description : `Analyse statistique complete sur marches financiers — 50k observations, 6 piliers DS`
- Website : laisse vide pour l'instant (ou pointe vers ton LinkedIn)
- Topics : `data-science` `python` `statistics` `finance` `pca` `pandas` `scipy` `portfolio` `100daysofml`

### 2. Vérifier le rendu du README

Le README.md s'affiche automatiquement sur la page d'accueil du repo. Vérifie que :
- Les sections sont lisibles
- Le dataset stats_data.json et les figures s'affichent correctement
- Les badges (si présents) ne sont pas cassés

### 3. Rendre le notebook visible

GitHub rend automatiquement les `.ipynb`. Clique sur `notebooks/PROJET_01_Analyse_Statistique.ipynb` → le notebook s'affiche avec toutes les sorties, graphiques inclus. ✅

### 4. Héberger la page HTML interactive (bonus)

Pour que `projet_interactif.html` soit accessible par URL :

1. Settings → Pages
2. Source : `Deploy from a branch`
3. Branch : `main` / root
4. Save

Dans ~2 minutes, la page est en ligne à :
```
https://<TON-USERNAME>.github.io/portfolio-ds-01-analyse-statistique/projet_interactif.html
```

Copie cette URL — tu pourras la partager sur LinkedIn.

---

## Mettre à jour le POST_LINKEDIN.md

Avant de publier sur LinkedIn, édite `POST_LINKEDIN.md` pour remplacer `[lien]` par la vraie URL GitHub :

```
🔗 Code GitHub : https://github.com/<TON-USERNAME>/portfolio-ds-01-analyse-statistique
🌐 Demo live  : https://<TON-USERNAME>.github.io/portfolio-ds-01-analyse-statistique/projet_interactif.html
```

---

## Taille du dataset (10.7 MB)

Le CSV `data/stock_market_dataset.csv` fait 10.7 MB → bien en-dessous de la limite GitHub de 100 MB, donc **pas besoin de Git LFS**.

Si un jour tu veux héberger un dataset > 100 MB, installe Git LFS :
```bash
git lfs install
git lfs track "*.csv"
git add .gitattributes
```

---

## Mises à jour futures

Après avoir modifié un fichier :

```bash
git add .
git commit -m "docs: ajout conclusion sur fat tails"
git push
```

---

## Checklist finale avant de partager sur LinkedIn

- [ ] Repo public et accessible depuis un navigateur en privé (test Incognito)
- [ ] README affiche correctement structure, description, comment lancer
- [ ] Notebook visible avec sorties sur GitHub
- [ ] PDF téléchargeable depuis `outputs/report/`
- [ ] Page HTML en ligne via GitHub Pages (optionnel)
- [ ] POST_LINKEDIN.md mis à jour avec les vrais liens
- [ ] Topics + description configurés sur le repo
- [ ] Toi-même en train de cloner le repo sur une autre machine pour vérifier qu'il marche

---

## En cas de pépin

| Erreur | Solution |
|---|---|
| `fatal: not a git repository` | `git init -b main` avant tout |
| `Authentication failed` | Utilise un Personal Access Token, pas ton mot de passe |
| `large files detected` | Installe Git LFS ou réduis le fichier |
| `remote origin already exists` | `git remote remove origin` puis re-add |
| `refusing to merge unrelated histories` | Ajoute `--allow-unrelated-histories` au pull |

---

**Ton projet est prêt à partir. Il te reste juste à copier-coller les commandes de l'Option A (ou suivre GitHub Desktop).**
