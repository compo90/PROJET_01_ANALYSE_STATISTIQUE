![Image Alt](https://github.com/compo90/PROJET_01_ANALYSE_STATISTIQUE/blob/be439a44ac0d885b9236d06726f96f3ac8c4a6d4/PHOTO%20AFFICHE.png
)
# PROJET 01 — Analyse Statistique Complète sur Données Financières

> **Projet éducatif** : les fondamentaux statistiques appliqués aux marchés financiers.
> **Auteur** : Aboubacar COMPO — Data Scientist  (Dakar, Sénégal)
> **Contexte** : Challenge 100 jours ML — Projet 01 du portfolio

---

## Objectif

Démontrer, de bout en bout et sur un dataset synthétique réaliste de **50 000 observations x 30 variables**, les 6 piliers de l'analyse statistique indispensables à tout projet Data Science réussi.

La statistique est la **fondation** : avant tout modèle ML, il faut savoir décrire, questionner et comprendre les données.

---

## Dataset synthétique — Marchés Financiers

- **50 000 lignes** (observations quotidiennes agrégées sur plusieurs actifs)
- **30 variables** couvrant 6 secteurs (Tech, Finance, Énergie, Santé, Consommation, Industrie)
- Variables : prix, rendements log, volatilité, volume, capitalisation, ratios fondamentaux (P/E, P/B, ROE, Beta), indicateurs techniques (RSI, MACD, moyennes mobiles), sentiment marché, macro (taux, inflation)
- Génération contrôlée : distributions normales, lognormales, heavy-tailed (Student), corrélations sectorielles injectées

Fichier : `data/stock_market_dataset.csv`

---

## Structure du repo

```
PROJET_01_ANALYSE_STATISTIQUE/
├── README.md
├── data/
│   └── stock_market_dataset.csv         # dataset synthétique généré
├── src/                                  # modules Python réutilisables
│   ├── data_generator.py                 # génération du dataset
│   ├── univariate.py                     # Partie 1
│   ├── distributions.py                  # Partie 2
│   ├── sampling.py                       # Partie 3
│   ├── bivariate.py                      # Partie 4
│   ├── tests.py                          # Partie 5
│   └── pca_analysis.py                   # Partie 6
├── notebooks/
│   └── PROJET_01_Analyse_Statistique.ipynb
├── outputs/
│   ├── figures/                          # PNG générés
│   └── report/                           # rapport PDF
├── projet_interactif.html                # artefact HTML partageable
└── requirements.txt
```

---

## Les 6 Parties

### Partie 1 — Statistique Univariée
Tendance centrale (moyenne, médiane, mode), dispersion (écart-type, IQR, CV), forme (asymétrie, kurtosis), visualisations (histogramme, boxplot, violin), détection d'outliers (IQR, Z-score, MAD).

### Partie 2 — Distributions de Probabilité
Fit des distributions (Normale, LogNormale, Student-t), test de normalité (Shapiro-Wilk, Kolmogorov-Smirnov, Jarque-Bera), QQ-plots, stylized facts des rendements financiers (fat tails, volatility clustering).

### Partie 3 — Échantillonnage et Biais
Théorème Central Limite illustré par simulation, échantillonnage aléatoire simple vs stratifié, biais de sélection / survie / look-ahead, bootstrap et intervalles de confiance.

### Partie 4 — Statistique Bivariée
Corrélations (Pearson, Spearman, Kendall), scatter plots, heatmap de corrélation sectorielle, régression linéaire simple, coefficient de détermination R².

### Partie 5 — Tests Bivariés Complets
Tests paramétriques (t-test, ANOVA), non-paramétriques (Mann-Whitney, Kruskal-Wallis), test du Chi² d'indépendance, tests de corrélation, **calcul des tailles d'effet** (Cohen's d, eta², Cramer's V).

### Partie 6 — Statistique Multivariée (PCA)
Standardisation, décomposition en composantes principales, scree plot, variance expliquée cumulée, cercle des corrélations, biplot, interprétation économique des facteurs.

---

## Stack technique

- **Python 3.10+**
- `pandas`, `numpy` — manipulation
- `scipy.stats` — tests statistiques
- `matplotlib`, `seaborn` — visualisations
- `scikit-learn` — PCA et standardisation
- `statsmodels` — régression, tests avancés

---

## Installation et exécution

```bash
# 1. Cloner le repo
git clone https://github.com/<votre_user>/PROJET_01_ANALYSE_STATISTIQUE.git
cd PROJET_01_ANALYSE_STATISTIQUE

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Générer le dataset
python src/data_generator.py

# 4. Lancer le notebook
jupyter notebook notebooks/PROJET_01_Analyse_Statistique.ipynb
```

---

## Livrables

- Notebook Jupyter pédagogique bilingue
- Scripts modulaires réutilisables
- Rapport PDF synthèse
- Artefact HTML interactif (onglets + SVG)

---

## Auteur et contact

**Aboubacar COMPO**
Ingénieur Télécoms — Administrateur Réseaux/Systèmes en reconversion Data Science
Dakar, Sénégal
[LinkedIn](https://www.linkedin.com/) · [GitHub](https://github.com/)

---

*Projet 01/20 — Roadmap Challenge 100 jours ML*
*License : MIT — Réutilisation libre à des fins pédagogiques*
