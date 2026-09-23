#!/usr/bin/env python3
"""Demo A: Privacy-Preserving & Explainable AI — Differential Privacy + SHAP.
SHIELD Framework | New Telecom Ltd / Robi Data Privacy Avengers

Uses objective-perturbation style DP logistic regression (noise on coefficients
calibrated to ε) for a clear, dependency-stable privacy–utility demo, plus SHAP
for global and per-customer reason drivers.
"""
from __future__ import annotations

import warnings
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[1]
IMG = ROOT / "images"
IMG.mkdir(parents=True, exist_ok=True)

EPSILONS = [0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 50.0]
TARGET_EPS = 1.0
RNG = np.random.default_rng(42)


def load_or_synth(name: str, n_samples: int, weights: list[float]):
    candidates = [ROOT / "data" / f"{name}.csv"]
    for p in candidates:
        if p.exists():
            return pd.read_csv(p), "file"
    X, y = make_classification(
        n_samples=n_samples,
        n_features=12,
        n_informative=8,
        n_redundant=2,
        weights=weights,
        flip_y=0.02,
        random_state=42,
    )
    df = pd.DataFrame(X, columns=[f"f{i}" for i in range(X.shape[1])])
    df["target"] = y
    return df, "synthetic"


def prep(df: pd.DataFrame):
    ycol = "target" if "target" in df.columns else df.columns[-1]
    y = df[ycol].values
    X = df.drop(columns=[ycol]).select_dtypes(include=[np.number])
    return X.values.astype(float), y.astype(int), list(X.columns)


def fit_dp_logistic(X_train, y_train, epsilon: float):
    """Non-private fit + Laplace noise on coefficients (ε-calibrated demo)."""
    base = LogisticRegression(max_iter=2000, random_state=42)
    base.fit(X_train, y_train)
    if epsilon >= 1e6:
        return base
    # Sensitivity proxy for demo: scale noise ~ 1/ε
    scale = 1.0 / max(epsilon, 1e-6)
    coef = base.coef_.copy()
    intercept = base.intercept_.copy()
    coef += RNG.laplace(0.0, scale * 0.15, size=coef.shape)
    intercept += RNG.laplace(0.0, scale * 0.15, size=intercept.shape)
    base.coef_ = coef
    base.intercept_ = intercept
    return base


def eval_curve(X, y, label: str):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, stratify=y, random_state=42
    )
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    baseline = LogisticRegression(max_iter=2000, random_state=42)
    baseline.fit(X_train, y_train)
    base_acc = accuracy_score(y_test, baseline.predict(X_test))
    base_auc = roc_auc_score(y_test, baseline.predict_proba(X_test)[:, 1])

    accs, aucs = [], []
    for eps in EPSILONS:
        clf = fit_dp_logistic(X_train, y_train, eps)
        pred = clf.predict(X_test)
        proba = clf.predict_proba(X_test)[:, 1]
        accs.append(accuracy_score(y_test, pred))
        aucs.append(roc_auc_score(y_test, proba))

    return {
        "label": label,
        "base_acc": base_acc,
        "base_auc": base_auc,
        "accs": accs,
        "aucs": aucs,
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
        "scaler": scaler,
    }


def plot_privacy_utility(results, outfile: Path):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for r in results:
        ax.semilogx(EPSILONS, r["accs"], marker="o", label=f"{r['label']} (DP)")
        ax.axhline(r["base_acc"], linestyle="--", alpha=0.45, label=f"{r['label']} baseline")
    ax.axvline(TARGET_EPS, color="red", linestyle=":", label=f"SHIELD target ε={TARGET_EPS}")
    ax.set_xlabel("Privacy budget ε (lower = stronger privacy)")
    ax.set_ylabel("Accuracy")
    ax.set_title("SHIELD — Privacy–Utility Trade-off (Differential Privacy)")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(outfile, dpi=150)
    plt.close()
    print(f"Wrote {outfile}")


def shap_plots(bundle, feature_names, outfile_global: Path, outfile_local: Path):
    import shap

    X_train, X_test = bundle["X_train"], bundle["X_test"]
    y_train = bundle["y_train"]
    clf = fit_dp_logistic(X_train, y_train, TARGET_EPS)

    background = shap.sample(X_train, min(40, len(X_train)), random_state=42)
    explainer = shap.LinearExplainer(clf, background)
    sample = X_test[: min(120, len(X_test))]
    sv = explainer.shap_values(sample)

    plt.figure()
    shap.summary_plot(sv, sample, feature_names=feature_names, show=False)
    plt.title(f"SHIELD SHAP (global) — {bundle['label']} @ ε={TARGET_EPS}")
    plt.tight_layout()
    plt.savefig(outfile_global, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Wrote {outfile_global}")

    proba = clf.predict_proba(X_test)[:, 1]
    idx = int(np.argmax(proba))
    sv1 = np.array(explainer.shap_values(X_test[idx : idx + 1])).reshape(-1)
    order = np.argsort(np.abs(sv1))[::-1][:5]
    fig, ax = plt.subplots(figsize=(7, 3.5))
    colors = ["#c0392b" if sv1[i] > 0 else "#2980b9" for i in order]
    ax.barh([feature_names[i] for i in order][::-1], sv1[order][::-1], color=colors[::-1])
    ax.set_xlabel("SHAP value (impact on risk score)")
    ax.set_title(
        f"SHIELD per-customer drivers — {bundle['label']} (p={proba[idx]:.2f})"
    )
    fig.tight_layout()
    fig.savefig(outfile_local, dpi=150)
    plt.close()
    print(f"Wrote {outfile_local}")

    top = order[:3]
    reasons = [
        f"{feature_names[i]} ({'increases' if sv1[i] > 0 else 'decreases'} risk)"
        for i in top
    ]
    return reasons


def main():
    print("=== SHIELD Demo A: DP + SHAP ===")
    results = []
    feats_map = {}
    for name, n, w, label in [
        ("churn", 4000, [0.73, 0.27], "Churn"),
        ("fraud", 6000, [0.97, 0.03], "Fraud"),
    ]:
        df, src = load_or_synth(name, n, w)
        X, y, feats = prep(df)
        print(f"{label}: {src}, shape={X.shape}")
        bundle = eval_curve(X, y, label)
        bundle["feature_names"] = feats
        results.append(bundle)
        feats_map[label] = feats

    plot_privacy_utility(results, IMG / "shield_privacy_utility.png")

    fig, ax = plt.subplots(figsize=(8, 4))
    for r in results:
        ax.semilogx(EPSILONS, r["accs"], marker="o", label=r["label"])
    ax.axvline(TARGET_EPS, color="red", linestyle=":", label="ε=1.0 target")
    ax.set_title("SHIELD — Accuracy vs Privacy Budget (Churn vs Fraud)")
    ax.set_xlabel("ε")
    ax.set_ylabel("Accuracy")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(IMG / "shield_comparison_accuracy.png", dpi=150)
    plt.close()
    print(f"Wrote {IMG / 'shield_comparison_accuracy.png'}")

    for r in results:
        tag = r["label"].lower()
        reasons = shap_plots(
            r,
            r["feature_names"],
            IMG / f"shield_shap_{tag}_global.png",
            IMG / f"shield_shap_{tag}_customer.png",
        )
        i = EPSILONS.index(TARGET_EPS)
        print(f"{r['label']} reason codes:", reasons)
        print(
            f"  baseline acc={r['base_acc']:.3f} | DP@ε=1.0 acc={r['accs'][i]:.3f} "
            f"| baseline AUC={r['base_auc']:.3f} | DP AUC={r['aucs'][i]:.3f}"
        )

    print("Demo A complete.")


if __name__ == "__main__":
    main()
