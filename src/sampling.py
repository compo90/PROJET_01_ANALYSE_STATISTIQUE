"""
Partie 3 — Échantillonnage et Biais
===================================

- Théorème Central Limite (simulation)
- Échantillonnage aléatoire simple vs stratifié
- Biais de sélection / survie / look-ahead
- Bootstrap et intervalles de confiance
"""

from __future__ import annotations

import numpy as np
import pandas as pd


# -----------------------------------------------------------------------------
# Théorème Central Limite — simulation
# -----------------------------------------------------------------------------
def simuler_tcl(
    population: np.ndarray,
    taille_echantillon: int = 30,
    n_repetitions: int = 2000,
    seed: int = 42,
) -> np.ndarray:
    """Tire n_repetitions échantillons de taille_echantillon et renvoie les moyennes."""
    rng = np.random.default_rng(seed)
    population = population[~np.isnan(population)]
    moyennes = np.empty(n_repetitions)
    for i in range(n_repetitions):
        ech = rng.choice(population, size=taille_echantillon, replace=False)
        moyennes[i] = ech.mean()
    return moyennes


def comparer_tcl(population: np.ndarray, tailles: list[int] = [5, 30, 100, 500]) -> pd.DataFrame:
    """Compare l'effet de la taille d'échantillon sur la distribution des moyennes."""
    rows = []
    mu_pop = np.nanmean(population)
    sigma_pop = np.nanstd(population, ddof=1)
    for n in tailles:
        moyennes = simuler_tcl(population, taille_echantillon=n)
        rows.append({
            "n":                       n,
            "moyenne_des_moyennes":    float(moyennes.mean()),
            "ecart_type_des_moyennes": float(moyennes.std(ddof=1)),
            "ecart_type_theorique":    float(sigma_pop / np.sqrt(n)),
            "moyenne_population":      float(mu_pop),
        })
    return pd.DataFrame(rows)


# -----------------------------------------------------------------------------
# Échantillonnage : simple vs stratifié
# -----------------------------------------------------------------------------
def echantillon_simple(df: pd.DataFrame, taille: int, seed: int = 42) -> pd.DataFrame:
    """Échantillon aléatoire simple sans remise."""
    return df.sample(n=taille, random_state=seed)


def echantillon_stratifie(
    df: pd.DataFrame,
    col_strate: str,
    taille: int,
    seed: int = 42,
) -> pd.DataFrame:
    """Échantillonnage stratifié proportionnel sur col_strate."""
    props = df[col_strate].value_counts(normalize=True)
    out_parts = []
    rng = np.random.default_rng(seed)
    for strate, prop in props.items():
        n_strate = max(1, int(round(taille * prop)))
        sous_pop = df[df[col_strate] == strate]
        if len(sous_pop) == 0:
            continue
        idx = rng.choice(sous_pop.index, size=min(n_strate, len(sous_pop)), replace=False)
        out_parts.append(df.loc[idx])
    return pd.concat(out_parts).sample(frac=1, random_state=seed)


def comparer_echantillonnages(
    df: pd.DataFrame,
    col_strate: str,
    col_mesure: str,
    taille: int = 500,
    n_repetitions: int = 200,
    seed: int = 42,
) -> pd.DataFrame:
    """Compare variance des estimations moyenne selon méthode d'échantillonnage."""
    rng = np.random.default_rng(seed)
    mu_pop = df[col_mesure].mean()

    moy_simple, moy_strat = [], []
    for i in range(n_repetitions):
        s = df.sample(n=taille, random_state=rng.integers(1, 10**6))
        moy_simple.append(s[col_mesure].mean())
        e = echantillon_stratifie(df, col_strate, taille, seed=int(rng.integers(1, 10**6)))
        moy_strat.append(e[col_mesure].mean())

    return pd.DataFrame([
        {"methode": "Aleatoire simple",  "biais": np.mean(moy_simple) - mu_pop, "variance": np.var(moy_simple, ddof=1)},
        {"methode": "Stratifie",         "biais": np.mean(moy_strat)  - mu_pop, "variance": np.var(moy_strat,  ddof=1)},
    ])


# -----------------------------------------------------------------------------
# Biais de sélection / survie / look-ahead
# -----------------------------------------------------------------------------
def biais_survie(df: pd.DataFrame, col_defaut: str, col_mesure: str) -> dict:
    """Quantifie l'écart entre estimation sur 'survivants' et population totale."""
    pop_all = df[col_mesure].mean()
    pop_surv = df.loc[df[col_defaut] == 0, col_mesure].mean()
    return {
        "moyenne_population":   float(pop_all),
        "moyenne_survivants":   float(pop_surv),
        "biais_absolu":         float(pop_surv - pop_all),
        "biais_relatif_pct":    float((pop_surv - pop_all) / pop_all * 100) if pop_all else np.nan,
    }


def biais_selection(df: pd.DataFrame, col_cible: str, filtre_mask: pd.Series) -> dict:
    """Compare moyenne filtrée vs non filtrée — illustre le biais de sélection."""
    return {
        "n_population":         int(len(df)),
        "n_filtre":             int(filtre_mask.sum()),
        "moyenne_pop":          float(df[col_cible].mean()),
        "moyenne_selection":    float(df.loc[filtre_mask, col_cible].mean()),
        "ecart":                float(df.loc[filtre_mask, col_cible].mean() - df[col_cible].mean()),
    }


# -----------------------------------------------------------------------------
# Bootstrap
# -----------------------------------------------------------------------------
def bootstrap_ic(
    x: np.ndarray,
    statistic=np.mean,
    n_boot: int = 2000,
    alpha: float = 0.05,
    seed: int = 42,
) -> dict:
    """Intervalle de confiance bootstrap (percentile) pour une statistique."""
    rng = np.random.default_rng(seed)
    x = x[~np.isnan(x)]
    n = len(x)
    boot_stats = np.empty(n_boot)
    for i in range(n_boot):
        sample = rng.choice(x, size=n, replace=True)
        boot_stats[i] = statistic(sample)
    lo, hi = np.quantile(boot_stats, [alpha / 2, 1 - alpha / 2])
    return {
        "statistic_obs":     float(statistic(x)),
        "ic_inf":            float(lo),
        "ic_sup":            float(hi),
        "niveau_confiance":  1 - alpha,
        "se_bootstrap":      float(boot_stats.std(ddof=1)),
    }
