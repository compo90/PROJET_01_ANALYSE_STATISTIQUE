"""
Partie 6 — Statistique Multivariée : Analyse en Composantes Principales
=======================================================================

Réduction de dimension, visualisation d'un espace multivarié,
identification de structures latentes dans les données financières.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


# -----------------------------------------------------------------------------
# Préparation
# -----------------------------------------------------------------------------
def preparer_donnees_pca(df: pd.DataFrame, cols: list[str]) -> tuple[pd.DataFrame, StandardScaler]:
    """Drop NA + standardise (moyenne=0, sd=1) — pré-requis PCA."""
    X = df[cols].dropna()
    scaler = StandardScaler()
    X_std = scaler.fit_transform(X)
    return pd.DataFrame(X_std, columns=cols, index=X.index), scaler


# -----------------------------------------------------------------------------
# PCA
# -----------------------------------------------------------------------------
def pca_complete(X_std: pd.DataFrame, n_components: int | None = None) -> dict:
    """Exécute une PCA et retourne tous les éléments utiles."""
    if n_components is None:
        n_components = X_std.shape[1]
    pca = PCA(n_components=n_components)
    scores = pca.fit_transform(X_std)

    variance_expl = pca.explained_variance_ratio_
    variance_cum = np.cumsum(variance_expl)

    # Loadings = corrélations entre var originales et composantes
    loadings = pd.DataFrame(
        pca.components_.T * np.sqrt(pca.explained_variance_),
        index=X_std.columns,
        columns=[f"PC{i+1}" for i in range(n_components)],
    )

    scores_df = pd.DataFrame(
        scores,
        index=X_std.index,
        columns=[f"PC{i+1}" for i in range(n_components)],
    )

    return {
        "pca":               pca,
        "scores":            scores_df,
        "loadings":          loadings,
        "variance_expl":     variance_expl,
        "variance_cum":      variance_cum,
        "eigenvalues":       pca.explained_variance_,
    }


def seuil_kaiser(eigenvalues: np.ndarray) -> int:
    """Nombre de composantes à retenir (critère Kaiser : eigenvalue > 1)."""
    return int(np.sum(eigenvalues > 1))


def nb_axes_variance(variance_cum: np.ndarray, seuil: float = 0.80) -> int:
    """Nombre de composantes pour atteindre seuil % de variance cumulée."""
    return int(np.searchsorted(variance_cum, seuil) + 1)


# -----------------------------------------------------------------------------
# Contributions et qualité de représentation
# -----------------------------------------------------------------------------
def contributions_variables(loadings: pd.DataFrame) -> pd.DataFrame:
    """Contribution (%) de chaque variable à chaque composante."""
    contrib = (loadings ** 2)
    contrib = contrib.div(contrib.sum(axis=0), axis=1) * 100
    return contrib.round(2)


def cos2_variables(loadings: pd.DataFrame) -> pd.DataFrame:
    """Qualité de représentation (cos²) : somme = 1 sur toutes composantes."""
    cos2 = loadings ** 2
    cos2 = cos2.div(cos2.sum(axis=1), axis=0)
    return cos2.round(3)


# -----------------------------------------------------------------------------
# Interprétation automatique
# -----------------------------------------------------------------------------
def interpreter_axes(loadings: pd.DataFrame, seuil_loading: float = 0.5, top_n: int = 5) -> pd.DataFrame:
    """Pour chaque composante : variables majoritaires (loading | > seuil)."""
    rows = []
    for comp in loadings.columns:
        s = loadings[comp].abs().sort_values(ascending=False)
        top = s.head(top_n)
        significatives = top[top > seuil_loading]
        signes = loadings.loc[significatives.index, comp].round(2).to_dict()
        rows.append({
            "composante": comp,
            "n_variables_significatives": len(significatives),
            "variables_et_signes": signes,
        })
    return pd.DataFrame(rows)
