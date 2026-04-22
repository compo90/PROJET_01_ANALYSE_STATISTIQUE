"""
Partie 4 — Statistique Bivariée
===============================

Corrélations (Pearson, Spearman, Kendall), régression linéaire simple,
heatmaps corrélation, analyse numérique × catégorielle.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats


# -----------------------------------------------------------------------------
# Corrélations
# -----------------------------------------------------------------------------
def correlations_paire(x: pd.Series, y: pd.Series) -> pd.DataFrame:
    """Renvoie Pearson / Spearman / Kendall avec p-values."""
    mask = x.notna() & y.notna()
    x, y = x[mask], y[mask]

    rows = []
    for nom, fn in [
        ("Pearson",  stats.pearsonr),
        ("Spearman", stats.spearmanr),
        ("Kendall",  stats.kendalltau),
    ]:
        res = fn(x, y)
        # scipy >= 1.9 : res est un namedtuple (statistic, pvalue)
        r = res[0]
        p = res[1]
        rows.append({"methode": nom, "coefficient": float(r), "p_value": float(p), "n": int(len(x))})
    return pd.DataFrame(rows)


def matrice_correlation(
    df: pd.DataFrame,
    cols: list[str] | None = None,
    method: str = "pearson",
) -> pd.DataFrame:
    """Matrice de corrélation sur colonnes numériques."""
    if cols is None:
        cols = df.select_dtypes(include=np.number).columns.tolist()
    return df[cols].corr(method=method)


def top_correlations(corr: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Top n paires de variables les plus corrélées (en valeur absolue)."""
    c = corr.abs().where(np.triu(np.ones(corr.shape), k=1).astype(bool))
    s = c.stack().sort_values(ascending=False).head(n)
    out = pd.DataFrame({
        "var_1": [i[0] for i in s.index],
        "var_2": [i[1] for i in s.index],
        "corr_abs": s.values,
        "corr": [corr.loc[i[0], i[1]] for i in s.index],
    })
    return out


# -----------------------------------------------------------------------------
# Régression linéaire simple
# -----------------------------------------------------------------------------
def regression_simple(x: pd.Series, y: pd.Series) -> dict:
    """Régression linéaire OLS y = a + b*x (avec résidus, R2, p-value)."""
    mask = x.notna() & y.notna()
    x, y = x[mask].values, y[mask].values

    res = stats.linregress(x, y)
    y_pred = res.intercept + res.slope * x
    residuals = y - y_pred

    return {
        "intercept":     float(res.intercept),
        "pente":         float(res.slope),
        "r_value":       float(res.rvalue),
        "r_squared":     float(res.rvalue ** 2),
        "p_value":       float(res.pvalue),
        "stderr_pente":  float(res.stderr),
        "rmse":          float(np.sqrt(np.mean(residuals ** 2))),
        "mae":           float(np.mean(np.abs(residuals))),
        "n":             int(len(x)),
    }


# -----------------------------------------------------------------------------
# Numérique × Catégorielle — comparaison de groupes
# -----------------------------------------------------------------------------
def stats_par_groupe(df: pd.DataFrame, col_num: str, col_cat: str) -> pd.DataFrame:
    """Statistiques descriptives de col_num par niveaux de col_cat."""
    return (
        df.groupby(col_cat)[col_num]
        .agg(["count", "mean", "median", "std", "min", "max"])
        .round(4)
        .sort_values("mean", ascending=False)
    )


# -----------------------------------------------------------------------------
# Catégorielle × Catégorielle — table de contingence
# -----------------------------------------------------------------------------
def table_contingence(df: pd.DataFrame, col_a: str, col_b: str, normalize: bool = False) -> pd.DataFrame:
    """Table croisée entre 2 variables catégorielles."""
    return pd.crosstab(df[col_a], df[col_b], normalize=normalize)
