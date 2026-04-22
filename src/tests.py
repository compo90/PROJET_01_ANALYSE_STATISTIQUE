"""
Partie 5 — Tests Bivariés Complets
==================================

Tests paramétriques et non-paramétriques + tailles d'effet.

Règle de décision : p < 0.05 => on rejette H0.
Toujours coupler avec taille d'effet (significatif ≠ important).
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats


# -----------------------------------------------------------------------------
# Comparaison de 2 groupes
# -----------------------------------------------------------------------------
def t_test(x: pd.Series, y: pd.Series, equal_var: bool = False) -> dict:
    """t-test de Welch (equal_var=False par défaut)."""
    x, y = x.dropna().values, y.dropna().values
    stat, p = stats.ttest_ind(x, y, equal_var=equal_var)
    return {
        "test":             "Welch t-test" if not equal_var else "Student t-test",
        "stat":             float(stat),
        "p_value":          float(p),
        "moy_x":            float(x.mean()),
        "moy_y":            float(y.mean()),
        "diff":             float(x.mean() - y.mean()),
        "cohens_d":         cohens_d(x, y),
        "conclusion_5pct":  "H0 rejetée" if p < 0.05 else "H0 non rejetée",
    }


def mann_whitney(x: pd.Series, y: pd.Series) -> dict:
    """Test non paramétrique Mann-Whitney U (comparaison de distributions)."""
    x, y = x.dropna().values, y.dropna().values
    stat, p = stats.mannwhitneyu(x, y, alternative="two-sided")
    return {
        "test":             "Mann-Whitney U",
        "stat":             float(stat),
        "p_value":          float(p),
        "med_x":            float(np.median(x)),
        "med_y":            float(np.median(y)),
        "conclusion_5pct":  "H0 rejetée" if p < 0.05 else "H0 non rejetée",
    }


# -----------------------------------------------------------------------------
# Comparaison de k groupes
# -----------------------------------------------------------------------------
def anova(df: pd.DataFrame, col_num: str, col_cat: str) -> dict:
    """ANOVA one-way F-test + eta² (taille d'effet)."""
    groupes = [g[col_num].dropna().values for _, g in df.groupby(col_cat)]
    stat, p = stats.f_oneway(*groupes)

    # Eta² = SS_between / SS_total
    all_vals = np.concatenate(groupes)
    grand_mean = all_vals.mean()
    ss_between = sum(len(g) * (g.mean() - grand_mean) ** 2 for g in groupes)
    ss_total = np.sum((all_vals - grand_mean) ** 2)
    eta2 = ss_between / ss_total if ss_total > 0 else np.nan

    return {
        "test":            "ANOVA one-way",
        "F":               float(stat),
        "p_value":         float(p),
        "eta2":            float(eta2),
        "eta2_interpret":  interpret_eta2(eta2),
        "n_groupes":       len(groupes),
        "conclusion_5pct": "H0 rejetée" if p < 0.05 else "H0 non rejetée",
    }


def kruskal_wallis(df: pd.DataFrame, col_num: str, col_cat: str) -> dict:
    """Kruskal-Wallis (équivalent non-paramétrique ANOVA)."""
    groupes = [g[col_num].dropna().values for _, g in df.groupby(col_cat)]
    stat, p = stats.kruskal(*groupes)
    return {
        "test":            "Kruskal-Wallis",
        "H":               float(stat),
        "p_value":         float(p),
        "n_groupes":       len(groupes),
        "conclusion_5pct": "H0 rejetée" if p < 0.05 else "H0 non rejetée",
    }


# -----------------------------------------------------------------------------
# Indépendance entre 2 catégorielles
# -----------------------------------------------------------------------------
def chi2_independance(df: pd.DataFrame, col_a: str, col_b: str) -> dict:
    """Chi² d'indépendance + V de Cramer (taille d'effet)."""
    ct = pd.crosstab(df[col_a], df[col_b])
    chi2, p, dof, expected = stats.chi2_contingency(ct)
    n = ct.values.sum()
    r, c = ct.shape
    cramers_v = np.sqrt(chi2 / (n * (min(r, c) - 1))) if min(r, c) > 1 else np.nan
    return {
        "test":               "Chi2 d'independance",
        "chi2":               float(chi2),
        "p_value":            float(p),
        "ddl":                int(dof),
        "cramers_v":          float(cramers_v),
        "cramers_interpret":  interpret_cramers(cramers_v),
        "conclusion_5pct":    "H0 rejetée" if p < 0.05 else "H0 non rejetée",
    }


# -----------------------------------------------------------------------------
# Tailles d'effet
# -----------------------------------------------------------------------------
def cohens_d(x: np.ndarray, y: np.ndarray) -> float:
    """d de Cohen — taille d'effet standardisée entre 2 moyennes."""
    nx, ny = len(x), len(y)
    pooled_sd = np.sqrt(((nx - 1) * np.var(x, ddof=1) + (ny - 1) * np.var(y, ddof=1)) / (nx + ny - 2))
    return float((x.mean() - y.mean()) / pooled_sd) if pooled_sd > 0 else 0.0


def interpret_cohens_d(d: float) -> str:
    d = abs(d)
    if d < 0.2:  return "negligeable"
    if d < 0.5:  return "faible"
    if d < 0.8:  return "moyen"
    return "fort"


def interpret_eta2(eta2: float) -> str:
    if eta2 < 0.01: return "negligeable"
    if eta2 < 0.06: return "faible"
    if eta2 < 0.14: return "moyen"
    return "fort"


def interpret_cramers(v: float) -> str:
    if np.isnan(v): return "n/a"
    if v < 0.1:     return "negligeable"
    if v < 0.3:     return "faible"
    if v < 0.5:     return "moyen"
    return "fort"


# -----------------------------------------------------------------------------
# Rapport de batterie
# -----------------------------------------------------------------------------
def batterie_tests_bivaries(df: pd.DataFrame, col_num: str, col_cat: str) -> pd.DataFrame:
    """Applique ANOVA + Kruskal-Wallis sur un couple num × cat."""
    tests = [anova(df, col_num, col_cat), kruskal_wallis(df, col_num, col_cat)]
    return pd.DataFrame(tests)
