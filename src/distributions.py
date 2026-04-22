"""
Partie 2 — Distributions de Probabilité
=======================================

Ajustement de lois (Normale, LogNormale, Student-t),
tests de normalité, QQ-plots, stylized facts des rendements.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats


# -----------------------------------------------------------------------------
# Ajustement de distributions
# -----------------------------------------------------------------------------
def fit_normale(x: np.ndarray) -> dict:
    """Paramètres MLE d'une Normale + log-vraisemblance + AIC/BIC."""
    x = x[~np.isnan(x)]
    mu, sigma = stats.norm.fit(x)
    ll = np.sum(stats.norm.logpdf(x, loc=mu, scale=sigma))
    k = 2
    aic = 2 * k - 2 * ll
    bic = k * np.log(len(x)) - 2 * ll
    return {"loi": "Normale", "mu": mu, "sigma": sigma, "loglik": ll, "aic": aic, "bic": bic, "k": k}


def fit_student(x: np.ndarray) -> dict:
    """Paramètres MLE d'une Student-t (3 paramètres: df, loc, scale)."""
    x = x[~np.isnan(x)]
    df_, loc_, scale_ = stats.t.fit(x)
    ll = np.sum(stats.t.logpdf(x, df=df_, loc=loc_, scale=scale_))
    k = 3
    aic = 2 * k - 2 * ll
    bic = k * np.log(len(x)) - 2 * ll
    return {"loi": "Student-t", "df": df_, "loc": loc_, "scale": scale_, "loglik": ll, "aic": aic, "bic": bic, "k": k}


def fit_lognormal(x: np.ndarray) -> dict:
    """Ajustement LogNormale (nécessite x > 0)."""
    x = x[~np.isnan(x) & (x > 0)]
    if len(x) == 0:
        return {"loi": "LogNormale", "erreur": "aucune valeur > 0"}
    shape, loc_, scale_ = stats.lognorm.fit(x, floc=0)
    ll = np.sum(stats.lognorm.logpdf(x, shape, loc=loc_, scale=scale_))
    k = 2
    aic = 2 * k - 2 * ll
    bic = k * np.log(len(x)) - 2 * ll
    return {"loi": "LogNormale", "shape": shape, "scale": scale_, "loglik": ll, "aic": aic, "bic": bic, "k": k}


def compare_distributions(x: np.ndarray) -> pd.DataFrame:
    """Compare plusieurs lois par AIC/BIC — meilleur = plus petit AIC."""
    results = []
    for fit_fn in [fit_normale, fit_student]:
        try:
            results.append(fit_fn(x))
        except Exception as e:
            results.append({"loi": fit_fn.__name__, "erreur": str(e)})
    if (x[~np.isnan(x)] > 0).all():
        try:
            results.append(fit_lognormal(x))
        except Exception as e:
            results.append({"loi": "LogNormale", "erreur": str(e)})
    return pd.DataFrame(results)


# -----------------------------------------------------------------------------
# Tests de normalité
# -----------------------------------------------------------------------------
def test_shapiro(x: np.ndarray, sample_size: int = 5000) -> dict:
    """Shapiro-Wilk (échantillonné si n > sample_size car test sensible sur n grand)."""
    x = x[~np.isnan(x)]
    if len(x) > sample_size:
        rng = np.random.default_rng(42)
        x = rng.choice(x, size=sample_size, replace=False)
    stat, p = stats.shapiro(x)
    return {"test": "Shapiro-Wilk", "stat": float(stat), "p_value": float(p), "H0_rejetee_5pct": bool(p < 0.05)}


def test_ks_normal(x: np.ndarray) -> dict:
    """Kolmogorov-Smirnov vs N(moyenne, std)."""
    x = x[~np.isnan(x)]
    mu, sigma = x.mean(), x.std(ddof=1)
    stat, p = stats.kstest(x, "norm", args=(mu, sigma))
    return {"test": "Kolmogorov-Smirnov", "stat": float(stat), "p_value": float(p), "H0_rejetee_5pct": bool(p < 0.05)}


def test_jarque_bera(x: np.ndarray) -> dict:
    """Jarque-Bera : test basé sur asymétrie + kurtosis."""
    x = x[~np.isnan(x)]
    stat, p = stats.jarque_bera(x)
    return {"test": "Jarque-Bera", "stat": float(stat), "p_value": float(p), "H0_rejetee_5pct": bool(p < 0.05)}


def test_anderson(x: np.ndarray) -> dict:
    """Anderson-Darling — plus sensible dans les queues."""
    x = x[~np.isnan(x)]
    res = stats.anderson(x, dist="norm")
    # Seuil 5 % = index 2
    crit_5 = res.critical_values[2]
    return {
        "test": "Anderson-Darling",
        "stat": float(res.statistic),
        "val_critique_5pct": float(crit_5),
        "H0_rejetee_5pct": bool(res.statistic > crit_5)
    }


def batterie_normalite(x: np.ndarray) -> pd.DataFrame:
    """Batterie complète de tests de normalité sur une série."""
    tests = [test_shapiro(x), test_ks_normal(x), test_jarque_bera(x), test_anderson(x)]
    return pd.DataFrame(tests)


# -----------------------------------------------------------------------------
# Stylized facts des rendements financiers
# -----------------------------------------------------------------------------
def stylized_facts(returns: pd.Series) -> dict:
    """Vérifie les 'stylized facts' classiques des rendements financiers :
    - asymétrie proche de 0 (voire négative)
    - kurtosis >> 3 (fat tails)
    - faible autocorrélation des rendements
    - forte autocorrélation des |rendements| (volatility clustering)
    """
    r = returns.dropna()
    return {
        "n":                     int(r.size),
        "moyenne":               float(r.mean()),
        "ecart_type":            float(r.std(ddof=1)),
        "asymetrie":             float(stats.skew(r)),
        "kurtosis_excess":       float(stats.kurtosis(r)),
        "autocorr_lag1":         float(r.autocorr(lag=1)),
        "autocorr_abs_lag1":     float(r.abs().autocorr(lag=1)),
        "autocorr_abs_lag5":     float(r.abs().autocorr(lag=5)),
        "fat_tails":             bool(stats.kurtosis(r) > 1.0),
        "volatility_clustering": bool(r.abs().autocorr(lag=1) > 0.05),
    }
