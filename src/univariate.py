"""
Partie 1 — Statistique Univariée
================================

Analyse variable par variable : mesures de tendance centrale,
dispersion, forme de la distribution, détection d'outliers.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats


# -----------------------------------------------------------------------------
# Tendance centrale et dispersion
# -----------------------------------------------------------------------------
def describe_numeric(series: pd.Series) -> dict:
    """Statistiques descriptives complètes d'une série numérique."""
    s = series.dropna()
    q1, q2, q3 = s.quantile([0.25, 0.50, 0.75])
    iqr = q3 - q1
    mean = s.mean()
    std = s.std(ddof=1)

    return {
        "n":              int(s.size),
        "moyenne":        float(mean),
        "mediane":        float(q2),
        "mode":           float(s.mode().iloc[0]) if not s.mode().empty else np.nan,
        "ecart_type":     float(std),
        "variance":       float(s.var(ddof=1)),
        "min":            float(s.min()),
        "max":            float(s.max()),
        "etendue":        float(s.max() - s.min()),
        "q1":             float(q1),
        "q3":             float(q3),
        "iqr":            float(iqr),
        "cv":             float(std / mean) if mean != 0 else np.nan,
        "asymetrie":      float(stats.skew(s)),
        "kurtosis":       float(stats.kurtosis(s)),  # Fisher: 0 = normale
        "mad":            float(stats.median_abs_deviation(s, scale="normal")),
    }


def describe_dataframe(df: pd.DataFrame, cols: list[str] | None = None) -> pd.DataFrame:
    """Applique describe_numeric sur plusieurs colonnes numériques."""
    if cols is None:
        cols = df.select_dtypes(include=np.number).columns.tolist()
    stats_list = []
    for c in cols:
        d = describe_numeric(df[c])
        d["variable"] = c
        stats_list.append(d)
    out = pd.DataFrame(stats_list).set_index("variable")
    return out


# -----------------------------------------------------------------------------
# Détection d'outliers
# -----------------------------------------------------------------------------
def outliers_iqr(series: pd.Series, k: float = 1.5) -> pd.Series:
    """Masque booléen des outliers selon la règle IQR (Tukey)."""
    s = series.dropna()
    q1, q3 = s.quantile([0.25, 0.75])
    iqr = q3 - q1
    lower, upper = q1 - k * iqr, q3 + k * iqr
    return (series < lower) | (series > upper)


def outliers_zscore(series: pd.Series, threshold: float = 3.0) -> pd.Series:
    """Masque des outliers via Z-score (sensible aux distributions non-normales)."""
    s = series.dropna()
    z = np.abs((series - s.mean()) / s.std(ddof=1))
    return z > threshold


def outliers_mad(series: pd.Series, threshold: float = 3.5) -> pd.Series:
    """Masque des outliers via MAD (robuste, préféré pour fat-tails)."""
    med = series.median()
    mad = stats.median_abs_deviation(series.dropna(), scale="normal")
    if mad == 0:
        return pd.Series(False, index=series.index)
    z_mod = 0.6745 * (series - med) / mad
    return np.abs(z_mod) > threshold


def outliers_summary(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    """Résumé comparatif des 3 méthodes de détection."""
    rows = []
    for c in cols:
        rows.append({
            "variable": c,
            "n_iqr":    int(outliers_iqr(df[c]).sum()),
            "n_zscore": int(outliers_zscore(df[c]).sum()),
            "n_mad":    int(outliers_mad(df[c]).sum()),
            "pct_iqr":  round(outliers_iqr(df[c]).mean() * 100, 2),
            "pct_mad":  round(outliers_mad(df[c]).mean() * 100, 2),
        })
    return pd.DataFrame(rows).set_index("variable")


# -----------------------------------------------------------------------------
# Analyse catégorielle univariée
# -----------------------------------------------------------------------------
def describe_categorical(series: pd.Series) -> pd.DataFrame:
    """Table fréquence / proportion pour variable catégorielle."""
    counts = series.value_counts(dropna=False)
    pct = series.value_counts(dropna=False, normalize=True) * 100
    return pd.DataFrame({"effectif": counts, "pourcentage": pct.round(2)})


def entropie_shannon(series: pd.Series) -> float:
    """Entropie de Shannon (base 2) — mesure de diversité."""
    p = series.value_counts(normalize=True, dropna=False).values
    return float(-np.sum(p * np.log2(p + 1e-12)))
