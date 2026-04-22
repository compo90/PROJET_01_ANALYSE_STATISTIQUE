# Post LinkedIn — PROJET 01

> Prêt à copier-coller. Adapte les liens GitHub / LinkedIn avant publication.
> Trois variantes : (1) court, (2) long pédagogique, (3) anglais court.

---

## 🇫🇷 Variante 1 — Court (idéal pour feed)

📊 Jour ~86/100 — Projet 01 de mon portfolio Data Science est en ligne.

**Analyse Statistique Complète sur 50 000 observations boursières** 🏦

Parce que tout projet ML réussi commence par une base statistique solide, j'ai décomposé les 6 piliers indispensables sur un dataset synthétique de marchés financiers (34 variables, 6 secteurs) :

1️⃣ Statistique univariée (tendance, dispersion, outliers MAD vs IQR vs Z-score)
2️⃣ Distributions (Normale vs Student-t, stylized facts, fat tails kurtosis=6.4)
3️⃣ Échantillonnage et biais (TCL, bootstrap, biais de survie)
4️⃣ Statistique bivariée (Pearson, Spearman, régression)
5️⃣ Tests bivariés (ANOVA, Kruskal, Chi² + tailles d'effet)
6️⃣ PCA (réduction de dimension, cercle des corrélations)

**Leçon clé** : avec 50K observations, *tout* devient statistiquement significatif. Il faut **toujours coupler p-value et taille d'effet** (Cohen's d, eta², V de Cramer).

🔗 Code GitHub : [lien]
📓 Notebook + rapport PDF + page HTML interactive dans le repo

Next : Projet 02 — Détection de fraude Mobile Money 🛡️

#DataScience #Python #Statistics #Finance #100DaysOfML #Portfolio #Dakar

---

## 🇫🇷 Variante 2 — Long pédagogique (carrousel-ready)

📊 **Projet 01 / 20 — Analyse Statistique Complète sur Marchés Financiers**

Pourquoi *encore* un projet sur les statistiques ?

Parce que je vois trop de tutoriels ML qui sautent cette étape. On importe pandas, on lance un `train_test_split`, on balance un XGBoost. Et on se demande pourquoi les résultats en production divergent du validation set.

➜ La réponse est quasi toujours dans la statistique descriptive qu'on n'a pas faite.

Alors j'ai construit un dataset synthétique de **50 000 observations boursières × 34 variables** (6 secteurs : Tech, Finance, Énergie, Santé, Consommation, Industrie) et j'ai déroulé les 6 piliers :

**1️⃣ Univariée**
— Kurtosis du rendement journalier = 6.4 → fat tails bien présentes.
— La méthode **MAD** détecte 0.19 % d'outliers, le **Z-score** en détecte 1 %. Sur fat-tailed, le Z-score se plante.

**2️⃣ Distributions**
— Student-t (df=6.14) bat la Normale sur AIC : -252 038 vs -248 193.
— Les 4 tests de normalité rejettent H0 (Shapiro, KS, Jarque-Bera, Anderson) → mais c'est attendu avec n=50K.

**3️⃣ Échantillonnage & biais**
— TCL vérifié empiriquement : σ des moyennes = σ_population/√n à 1 % près.
— Biais de survie quantifié : ignorer les actifs en défaut gonfle les performances (classique des backtests).

**4️⃣ Bivariée**
— Plus forte corrélation : volatilité ↔ bêta (ρ=0.33). Logique : un bêta élevé amplifie les mouvements.
— Les ratios fondamentaux (PER, ROE) sont quasi indépendants des rendements journaliers → leur pouvoir est long terme.

**5️⃣ Tests bivariés**
— Chi² Secteur × Bourse : p=0.014 (significatif !) mais V de Cramer=0.013 (négligeable).
— **C'est LE piège avec les grands échantillons** : toujours coupler p-value et taille d'effet.

**6️⃣ PCA**
— 15 variables → PC1 = axe "Risque marché" (volatilité+bêta), PC2 = "Sentiment" (VIX+sentiment), PC3 = "Valorisation" (PER+PBR).

---

**Les 4 livrables du projet** :
📓 Notebook Jupyter pédagogique (toutes les étapes expliquées)
📦 Scripts Python modulaires (src/ réutilisable)
📄 Rapport PDF de synthèse (10 pages)
🌐 Page HTML interactive avec onglets et SVG

**Stack** : Python · pandas · scipy · statsmodels · scikit-learn

🔗 GitHub : [lien]

Feedback bienvenu — ce projet est la fondation des suivants (Projet 02 = fraude Mobile Money, Projet 03 = scoring crédit Transpa Guinée).

#DataScience #Statistics #Python #Finance #QuantitativeAnalysis #100DaysOfML #Portfolio #MachineLearning #Dakar #Senegal

---

## 🇬🇧 Variante 3 — English short

📊 Portfolio Project 01 is live:

**End-to-end Statistical Analysis on 50k Financial Observations**

Before any ML model, solid statistical foundations. I broke down the 6 essential pillars on a synthetic stock market dataset (34 variables, 6 sectors):

1. Univariate (central tendency, outliers — MAD beats Z-score on fat-tailed data)
2. Distributions (Student-t beats Normal on AIC, kurtosis excess = 6.4)
3. Sampling & bias (CLT validated, survivorship bias quantified)
4. Bivariate (Pearson, Spearman, simple regression)
5. Hypothesis testing (ANOVA, Chi² + **effect sizes**)
6. PCA (risk / sentiment / valuation factors)

**Key lesson**: with 50k obs, EVERYTHING becomes statistically significant. Always pair p-values with effect sizes (Cohen's d, η², Cramer's V).

🔗 Full code on GitHub: [link]

#DataScience #Python #Statistics #Finance #MachineLearning #Portfolio

---

## Hashtags par plateforme

**LinkedIn** : #DataScience #Python #Statistics #Finance #100DaysOfML #Portfolio #Dakar #QuantitativeAnalysis #MachineLearning #OpenToWork

**Facebook** : #DataScience #Python #Statistiques #Finance #Projet #Dakar #Senegal

**TikTok / Reels** : #DataScience #Python #Stats #FinTech #100JoursML #Dakar #DataTok #QuantFinance

**YouTube (description vidéo)** :
- Tags : data science, python, statistics tutorial, pandas, scipy, pca, fat tails, stock market, portfolio project, 100 days of ML
