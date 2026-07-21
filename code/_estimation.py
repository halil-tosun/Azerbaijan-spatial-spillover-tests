"""
Shared two-way fixed-effects estimation routines used across multiple scripts.

All estimation in this replication package is implemented directly in NumPy/
SciPy (no specialized econometrics package), following the two-way
fixed-effects (within-transformation) approach described in Section 2.4 of
the manuscript. See docs/CODEBOOK.md for the full estimation description.
"""
import numpy as np
import pandas as pd
from scipy import stats as st
from _paths import TREATED, ADJACENT_1ST_ORDER, ADJACENT_2ND_ORDER, POST_YEAR_CUTOFF


def build_panel(efficiency_col='vrs_bc', data_path=None):
    """Load the district-year efficiency panel and attach treatment/adjacency
    indicators used throughout the analysis."""
    df = pd.read_csv(data_path)
    df = df.dropna(subset=[efficiency_col]).copy()
    df['post'] = (df['year'] >= POST_YEAR_CUTOFF).astype(int)
    df['treated_post'] = df['region'].isin(TREATED).astype(int) * df['post']
    df['adj1_post'] = df['region'].isin(ADJACENT_1ST_ORDER).astype(int) * df['post']
    df['adj2_post'] = df['region'].isin(ADJACENT_2ND_ORDER).astype(int) * df['post']
    return df


def demean_twfe(df, cols, unit_col='region', time_col='year'):
    """Within-transformation (two-way demeaning) for the specified columns."""
    d = df.copy()
    for col in cols:
        dm = d.groupby(unit_col)[col].transform('mean')
        ym = d.groupby(time_col)[col].transform('mean')
        gm = d[col].mean()
        d[col + '_dm'] = d[col] - dm - ym + gm
    return d


def twfe_cluster_robust(df, ycol, xcols, cluster_col='region'):
    """Two-way fixed-effects OLS via within-transformation, with cluster-robust
    (sandwich) standard errors clustered on `cluster_col`."""
    d = demean_twfe(df, [ycol] + xcols)
    X = np.column_stack([np.ones(len(d))] + [d[c + '_dm'].values for c in xcols])
    Y = d[ycol + '_dm'].values
    beta, *_ = np.linalg.lstsq(X, Y, rcond=None)
    resid = Y - X @ beta
    n, k = X.shape
    clusters = d[cluster_col].values
    uniq = np.unique(clusters)
    nc = len(uniq)
    XtX_inv = np.linalg.inv(X.T @ X)
    meat = np.zeros((k, k))
    for c in uniq:
        m = clusters == c
        s = X[m].T @ resid[m]
        meat += np.outer(s, s)
    dof_corr = (nc / (nc - 1)) * ((n - 1) / (n - k))
    vcov = dof_corr * XtX_inv @ meat @ XtX_inv
    se = np.sqrt(np.diag(vcov))
    return {
        'beta': beta, 'se': se, 'n': n, 'n_clusters': nc,
        'X': X, 'Y': Y, 'clusters': clusters, 'resid': resid,
        'XtX_inv': XtX_inv, 'dof_corr': dof_corr,
    }


def wild_cluster_bootstrap(df, ycol, xcols, target_idx, cluster_col='region', B=4999, seed=123):
    """Restricted wild cluster bootstrap (WCR, Rademacher weights) for the
    coefficient at position `target_idx` (0=intercept, 1=first xcol, ...)."""
    fit = twfe_cluster_robust(df, ycol, xcols, cluster_col)
    X, Y, clusters = fit['X'], fit['Y'], fit['clusters']
    n, k = X.shape
    uniq = np.unique(clusters)
    nc = len(uniq)

    restricted_cols = [i for i in range(k) if i != target_idx]
    X_r = X[:, restricted_cols]
    beta_r, *_ = np.linalg.lstsq(X_r, Y, rcond=None)
    resid_r = Y - X_r @ beta_r

    rng = np.random.default_rng(seed)
    t_boot = np.zeros(B)
    t_obs = fit['beta'][target_idx] / fit['se'][target_idx]

    for b in range(B):
        weights = {c: rng.choice([-1, 1]) for c in uniq}
        w_vec = np.array([weights[c] for c in clusters])
        y_star = X_r @ beta_r + resid_r * w_vec
        beta_b, *_ = np.linalg.lstsq(X, y_star, rcond=None)
        resid_b = y_star - X @ beta_b
        meat_b = np.zeros((k, k))
        for c in uniq:
            m = clusters == c
            s = X[m].T @ resid_b[m]
            meat_b += np.outer(s, s)
        vcov_b = fit['dof_corr'] * fit['XtX_inv'] @ meat_b @ fit['XtX_inv']
        se_b = np.sqrt(vcov_b[target_idx, target_idx])
        t_boot[b] = beta_b[target_idx] / se_b

    p_wcr = np.mean(np.abs(t_boot) >= np.abs(t_obs))
    tcrit_wcr = np.percentile(np.abs(t_boot), 95)
    coef = fit['beta'][target_idx]
    se = fit['se'][target_idx]
    ci_wcr = (coef - tcrit_wcr * se, coef + tcrit_wcr * se)
    return {'coef': coef, 'se': se, 't_obs': t_obs, 'p_wcr': p_wcr, 'ci_wcr': ci_wcr}


def randomization_inference(df, ycol, treated_col, adjacent_set, donor_pool, cluster_col='region',
                             n_perm=2000, seed=2024):
    """Fisher-style permutation test: reassign the adjacency label to random
    draws from the donor pool, holding the treated group fixed."""

    def get_adj_coef(adj_set):
        d = df.copy()
        d['adjacent_post_tmp'] = d[cluster_col].isin(adj_set).astype(int) * d['post']
        fit = twfe_cluster_robust(d, ycol, [treated_col, 'adjacent_post_tmp'], cluster_col)
        return fit['beta'][2]

    observed = get_adj_coef(adjacent_set)
    rng = np.random.default_rng(seed)
    placebo = np.zeros(n_perm)
    for i in range(n_perm):
        fake = rng.choice(donor_pool, size=len(adjacent_set), replace=False)
        placebo[i] = get_adj_coef(list(fake))
    p_ri = np.mean(np.abs(placebo) >= np.abs(observed))
    pctile = (placebo < observed).mean() * 100
    return {'observed': observed, 'placebo': placebo, 'p_ri': p_ri, 'percentile': pctile}
