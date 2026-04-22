"""
Générateur de dataset synthétique - Marchés Financiers
=======================================================

Produit un dataset réaliste de 50 000 observations x 30 variables
sur des actifs boursiers multi-secteurs. Injecte des propriétés
statistiques réalistes : fat tails, corrélations sectorielles,
volatility clustering, valeurs manquantes contrôlées.

Usage:
    python src/data_generator.py
"""

from __future__ import annotations

import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta


# -----------------------------------------------------------------------------
# Paramètres globaux
# -----------------------------------------------------------------------------
SEED = 42
N_ROWS = 50_000

SECTEURS = {
    "Tech":         {"vol_annuelle": 0.35, "rendement_annuel": 0.14, "beta": 1.30},
    "Finance":      {"vol_annuelle": 0.28, "rendement_annuel": 0.09, "beta": 1.10},
    "Energie":      {"vol_annuelle": 0.32, "rendement_annuel": 0.07, "beta": 1.05},
    "Sante":        {"vol_annuelle": 0.22, "rendement_annuel": 0.10, "beta": 0.85},
    "Consommation": {"vol_annuelle": 0.20, "rendement_annuel": 0.08, "beta": 0.75},
    "Industrie":    {"vol_annuelle": 0.24, "rendement_annuel": 0.08, "beta": 0.95},
}

BOURSES = ["NYSE", "NASDAQ", "EURONEXT", "LSE", "TSX"]
RATINGS = ["AAA", "AA", "A", "BBB", "BB", "B", "CCC"]


# -----------------------------------------------------------------------------
# Génération
# -----------------------------------------------------------------------------
def generate_dataset(n_rows: int = N_ROWS, seed: int = SEED) -> pd.DataFrame:
    """Génère un DataFrame synthétique de marchés financiers."""
    rng = np.random.default_rng(seed)

    # 1. Métadonnées actifs
    secteurs = list(SECTEURS.keys())
    secteur_col = rng.choice(secteurs, size=n_rows, p=[0.22, 0.18, 0.15, 0.15, 0.15, 0.15])
    bourse_col = rng.choice(BOURSES, size=n_rows, p=[0.30, 0.30, 0.15, 0.15, 0.10])

    # Un ticker par ligne (simulé, 4 lettres)
    tickers = np.array([
        "".join(rng.choice(list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"), size=4))
        for _ in range(n_rows)
    ])

    # 2. Dates (séries temporelles échelonnées)
    start_date = datetime(2015, 1, 1)
    offsets = rng.integers(low=0, high=365 * 9, size=n_rows)
    dates = [start_date + timedelta(days=int(o)) for o in offsets]

    # 3. Vecteur de paramètres par ligne (dépendant du secteur)
    vol_annuelle = np.array([SECTEURS[s]["vol_annuelle"] for s in secteur_col])
    rend_annuel = np.array([SECTEURS[s]["rendement_annuel"] for s in secteur_col])
    beta_sect = np.array([SECTEURS[s]["beta"] for s in secteur_col])

    # 4. Prix et rendements — modèle log-normal + fat tails Student-t
    # Prix: distribution log-normale (propriété classique des actifs)
    prix_init = np.exp(rng.normal(loc=4.0, scale=0.8, size=n_rows))  # ~50 USD médian
    prix_init = np.clip(prix_init, 1.0, 5000.0)

    # Rendement journalier: mix gaussien + heavy-tailed Student-t (df=5)
    # 85% gaussien, 15% fat-tailed pour reproduire stylized facts
    mask_fat = rng.random(n_rows) < 0.15
    vol_journaliere = vol_annuelle / np.sqrt(252)
    rend_moy_journalier = rend_annuel / 252

    rend_gauss = rng.normal(loc=rend_moy_journalier, scale=vol_journaliere, size=n_rows)
    rend_student = rng.standard_t(df=5, size=n_rows) * vol_journaliere * 1.4
    rendement_jour = np.where(mask_fat, rend_student, rend_gauss)

    # Rendement log
    rendement_log = np.log1p(rendement_jour)

    # Prix de clôture
    prix_cloture = prix_init * (1 + rendement_jour)
    prix_ouverture = prix_init * (1 + rng.normal(0, vol_journaliere * 0.3, n_rows))
    prix_haut = np.maximum(prix_ouverture, prix_cloture) * (1 + np.abs(rng.normal(0, vol_journaliere * 0.5, n_rows)))
    prix_bas = np.minimum(prix_ouverture, prix_cloture) * (1 - np.abs(rng.normal(0, vol_journaliere * 0.5, n_rows)))

    # 5. Volume (log-normal)
    volume = np.exp(rng.normal(loc=14.0, scale=1.3, size=n_rows)).astype(np.int64)

    # 6. Capitalisation (log-normal, corrélée au prix)
    market_cap_m = prix_cloture * np.exp(rng.normal(loc=3.5, scale=1.2, size=n_rows))

    # 7. Volatilité réalisée (20 jours) — heavy tail
    volatilite_20j = np.abs(rng.normal(vol_journaliere, vol_journaliere * 0.4, n_rows))
    volatilite_20j += rng.exponential(scale=vol_journaliere * 0.3, size=n_rows)

    # 8. Ratios fondamentaux
    per = np.abs(rng.normal(loc=20, scale=12, size=n_rows))
    per = np.clip(per, 3, 150)
    pbr = np.abs(rng.normal(loc=2.5, scale=1.8, size=n_rows))
    pbr = np.clip(pbr, 0.3, 15)
    roe = rng.normal(loc=0.12, scale=0.09, size=n_rows)  # Return on Equity
    roa = rng.normal(loc=0.06, scale=0.05, size=n_rows)  # Return on Assets
    debt_equity = np.abs(rng.normal(loc=1.2, scale=0.9, size=n_rows))
    dividend_yield = np.abs(rng.normal(loc=0.025, scale=0.02, size=n_rows))

    # 9. Beta (corrélé au secteur, avec bruit)
    beta = beta_sect + rng.normal(0, 0.15, n_rows)

    # 10. Indicateurs techniques
    rsi = np.clip(rng.normal(loc=50, scale=18, size=n_rows), 0, 100)
    macd = rng.normal(loc=0, scale=2.5, size=n_rows)
    moy_mobile_50 = prix_cloture * (1 + rng.normal(0, 0.05, n_rows))
    moy_mobile_200 = prix_cloture * (1 + rng.normal(0, 0.10, n_rows))
    bollinger_width = np.abs(rng.normal(loc=0.04, scale=0.02, size=n_rows))

    # 11. Sentiment marché (-1 à 1)
    sentiment = np.clip(rng.normal(loc=0.05, scale=0.4, size=n_rows), -1, 1)

    # 12. Variables macroéconomiques (identiques par date approx, bruit faible)
    taux_central = 0.02 + 0.03 * np.sin(np.array(offsets) / 365) + rng.normal(0, 0.002, n_rows)
    inflation = 0.025 + 0.02 * np.sin(np.array(offsets) / 180) + rng.normal(0, 0.003, n_rows)
    vix = np.abs(rng.normal(loc=18, scale=7, size=n_rows)) + 5 * np.abs(sentiment)

    # 13. Note de crédit
    rating = rng.choice(RATINGS, size=n_rows, p=[0.05, 0.10, 0.20, 0.30, 0.20, 0.10, 0.05])

    # 14. Ancienneté (années depuis IPO)
    anciennete = np.abs(rng.normal(loc=15, scale=12, size=n_rows))
    anciennete = np.clip(anciennete, 0.5, 80)

    # 15. Employés (proxy taille) — corrélé à market cap
    employes = (market_cap_m * rng.lognormal(mean=0, sigma=0.4, size=n_rows)).astype(np.int64)
    employes = np.clip(employes, 50, 500_000)

    # 16. Flag défaut récent (rare, ~2%)
    defaut_recent = rng.random(n_rows) < 0.02

    # 17. Pays de siège
    pays = rng.choice(
        ["USA", "France", "Allemagne", "UK", "Canada", "Japon", "Chine"],
        size=n_rows,
        p=[0.45, 0.08, 0.08, 0.12, 0.07, 0.10, 0.10]
    )

    # -----------------------------------------------------------------------
    # Assemblage DataFrame
    # -----------------------------------------------------------------------
    df = pd.DataFrame({
        "date":            dates,
        "ticker":          tickers,
        "secteur":         secteur_col,
        "bourse":          bourse_col,
        "pays":            pays,
        "rating":          rating,
        "anciennete":      np.round(anciennete, 1),
        "employes":        employes,
        "prix_ouverture":  np.round(prix_ouverture, 2),
        "prix_haut":       np.round(prix_haut, 2),
        "prix_bas":        np.round(prix_bas, 2),
        "prix_cloture":    np.round(prix_cloture, 2),
        "volume":          volume,
        "market_cap_m":    np.round(market_cap_m, 2),
        "rendement_jour":  np.round(rendement_jour, 6),
        "rendement_log":   np.round(rendement_log, 6),
        "volatilite_20j":  np.round(volatilite_20j, 5),
        "beta":            np.round(beta, 3),
        "per":             np.round(per, 2),
        "pbr":             np.round(pbr, 2),
        "roe":             np.round(roe, 4),
        "roa":             np.round(roa, 4),
        "debt_equity":     np.round(debt_equity, 3),
        "dividend_yield":  np.round(dividend_yield, 4),
        "rsi":             np.round(rsi, 1),
        "macd":            np.round(macd, 3),
        "moy_mobile_50":   np.round(moy_mobile_50, 2),
        "moy_mobile_200":  np.round(moy_mobile_200, 2),
        "bollinger_width": np.round(bollinger_width, 4),
        "sentiment":       np.round(sentiment, 3),
        "taux_central":    np.round(taux_central, 4),
        "inflation":       np.round(inflation, 4),
        "vix":             np.round(vix, 2),
        "defaut_recent":   defaut_recent.astype(int),
    })

    # Injection contrôlée de valeurs manquantes (~1.5 %) sur quelques variables
    for col in ["per", "pbr", "roe", "sentiment"]:
        mask_nan = rng.random(n_rows) < 0.015
        df.loc[mask_nan, col] = np.nan

    return df


def main():
    out_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "stock_market_dataset.csv")

    print(f"[INFO] Generation de {N_ROWS:,} observations...")
    df = generate_dataset()
    df.to_csv(out_path, index=False)

    print(f"[OK] Dataset sauvegarde : {out_path}")
    print(f"[INFO] Shape : {df.shape}")
    print(f"[INFO] Taille : {os.path.getsize(out_path) / 1e6:.2f} MB")
    print(f"\n[APERCU]\n{df.head(3)}")
    print(f"\n[TYPES]\n{df.dtypes}")


if __name__ == "__main__":
    main()
