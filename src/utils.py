"""
utils.py — Fungsi helper reusable untuk proyek analisis e-commerce
Mata Kuliah: Data Science | Tema: E-Business
"""

import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from pathlib import Path

# ─────────────────────────────────────────────
# KONFIGURASI VISUAL
# ─────────────────────────────────────────────

PALETTE = ["#264653", "#2a9d8f", "#e9c46a", "#f4a261", "#e76f51",
           "#023e8a", "#0077b6", "#0096c7", "#00b4d8", "#48cae4"]

FIGURES_DIR = Path(__file__).resolve().parent.parent / "reports" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)


def set_style():
    """Set global matplotlib/seaborn style untuk seluruh proyek."""
    sns.set_theme(style="whitegrid", palette=PALETTE)
    plt.rcParams.update({
        "figure.dpi": 120,
        "figure.facecolor": "white",
        "axes.facecolor": "#f9f9f9",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "font.family": "sans-serif",
        "axes.titlesize": 14,
        "axes.titleweight": "bold",
        "axes.labelsize": 11,
    })


# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────

def load_all_excel(folder: str, pattern: str = "*.xlsx") -> pd.DataFrame:
    """
    Membaca semua file Excel dalam folder dan menggabungkannya.

    Parameters
    ----------
    folder : str
        Path folder yang berisi file Excel.
    pattern : str
        Pola glob untuk filter file (default: '*.xlsx').

    Returns
    -------
    pd.DataFrame
        DataFrame gabungan dari semua file.
    """
    files = glob.glob(os.path.join(folder, "**", pattern), recursive=True)
    files = [f for f in files if not os.path.basename(f).startswith("~$")]

    if not files:
        raise FileNotFoundError(f"Tidak ada file ditemukan di: {folder}")

    df_list = []
    errors = []
    for f in sorted(files):
        try:
            df = pd.read_excel(f)
            df["_source_file"] = os.path.basename(f)
            df_list.append(df)
        except Exception as e:
            errors.append((f, str(e)))

    if errors:
        print(f"[WARN] Gagal membaca {len(errors)} file:")
        for f, e in errors:
            print(f"   - {os.path.basename(f)}: {e}")

    combined = pd.concat(df_list, ignore_index=True)
    print(f"[OK] Berhasil load {len(df_list)} file | Total baris: {len(combined):,}")
    return combined


# ─────────────────────────────────────────────
# STATISTIKA DESKRIPTIF
# ─────────────────────────────────────────────

def summarize_numeric(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ringkasan statistik deskriptif lengkap untuk kolom numerik.

    Returns
    -------
    pd.DataFrame
        Tabel dengan: count, mean, median, modus, std, min, Q1, Q3, max, skewness, kurtosis.
    """
    num_cols = df.select_dtypes(include="number").columns.tolist()
    rows = []
    for col in num_cols:
        s = df[col].dropna()
        mode_val = s.mode()
        rows.append({
            "Kolom": col,
            "Count": int(s.count()),
            "Mean": round(s.mean(), 2),
            "Median": round(s.median(), 2),
            "Modus": round(mode_val.iloc[0], 2) if len(mode_val) > 0 else None,
            "Std Dev": round(s.std(), 2),
            "Min": round(s.min(), 2),
            "Q1 (25%)": round(s.quantile(0.25), 2),
            "Q3 (75%)": round(s.quantile(0.75), 2),
            "Max": round(s.max(), 2),
            "Skewness": round(s.skew(), 3),
            "Kurtosis": round(s.kurtosis(), 3),
        })
    return pd.DataFrame(rows).set_index("Kolom")


def frequency_table(series: pd.Series, top_n: int = None) -> pd.DataFrame:
    """
    Membuat tabel distribusi frekuensi dari sebuah Series kategorikal.

    Parameters
    ----------
    series : pd.Series
        Kolom kategorikal.
    top_n : int, optional
        Ambil N teratas saja.

    Returns
    -------
    pd.DataFrame
        Tabel dengan frekuensi absolut, relatif (%), dan kumulatif (%).
    """
    counts = series.value_counts()
    if top_n:
        counts = counts.head(top_n)
    total = counts.sum()
    rel = (counts / total * 100).round(2)
    cumulative = rel.cumsum().round(2)
    return pd.DataFrame({
        "Frekuensi": counts.values,
        "Persentase (%)": rel.values,
        "Kumulatif (%)": cumulative.values
    }, index=counts.index)


def detect_outliers_iqr(series: pd.Series) -> dict:
    """
    Deteksi outlier menggunakan metode IQR (Interquartile Range).

    Returns
    -------
    dict
        Q1, Q3, IQR, batas bawah, batas atas, jumlah outlier, persentase.
    """
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    outliers = series[(series < lower) | (series > upper)]
    return {
        "Q1": round(q1, 2),
        "Q3": round(q3, 2),
        "IQR": round(iqr, 2),
        "Batas Bawah": round(lower, 2),
        "Batas Atas": round(upper, 2),
        "Jumlah Outlier": len(outliers),
        "Persentase Outlier (%)": round(len(outliers) / len(series) * 100, 2),
    }


# ─────────────────────────────────────────────
# VISUALISASI
# ─────────────────────────────────────────────

def save_fig(filename: str):
    """Simpan figure ke folder reports/figures/."""
    path = FIGURES_DIR / filename
    plt.savefig(path, bbox_inches="tight", dpi=150)
    print(f"[SAVED] Figure disimpan: {path}")


def fmt_rupiah(x, pos=None):
    """Formatter angka ke format Rupiah singkat (K/M/B)."""
    if x >= 1e9:
        return f"Rp {x/1e9:.1f}B"
    elif x >= 1e6:
        return f"Rp {x/1e6:.1f}M"
    elif x >= 1e3:
        return f"Rp {x/1e3:.1f}K"
    return f"Rp {x:.0f}"


def plot_bar(series: pd.Series, title: str, xlabel: str, ylabel: str,
             filename: str = None, color: str = "#2a9d8f",
             horizontal: bool = False, top_n: int = None):
    """Bar chart generik dengan style konsisten."""
    set_style()
    if top_n:
        series = series.head(top_n)

    fig, ax = plt.subplots(figsize=(10, 5))
    if horizontal:
        series[::-1].plot(kind="barh", ax=ax, color=color)
        ax.set_xlabel(ylabel)
        ax.set_ylabel(xlabel)
    else:
        series.plot(kind="bar", ax=ax, color=color)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        plt.xticks(rotation=30, ha="right")

    ax.set_title(title)
    plt.tight_layout()
    if filename:
        save_fig(filename)
    plt.show()


def plot_pie(series: pd.Series, title: str, filename: str = None, top_n: int = 5):
    """Pie chart generik."""
    set_style()
    data = series.head(top_n)
    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(
        data.values,
        labels=data.index,
        autopct="%1.1f%%",
        colors=PALETTE[:len(data)],
        startangle=140,
        wedgeprops={"edgecolor": "white", "linewidth": 2}
    )
    for at in autotexts:
        at.set_fontsize(10)
    ax.set_title(title, fontsize=14, fontweight="bold")
    plt.tight_layout()
    if filename:
        save_fig(filename)
    plt.show()


def plot_line(series: pd.Series, title: str, ylabel: str,
              filename: str = None, rupiah: bool = False):
    """Line chart untuk tren waktu."""
    set_style()
    fig, ax = plt.subplots(figsize=(14, 5))
    series.plot(ax=ax, marker="o", color="#2a9d8f", linewidth=2, markersize=5)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel("")
    ax.grid(True, alpha=0.3)
    if rupiah:
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_rupiah))
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    if filename:
        save_fig(filename)
    plt.show()


def plot_histogram(series: pd.Series, title: str, xlabel: str,
                   filename: str = None, bins: int = 30, rupiah: bool = False):
    """Histogram + KDE."""
    set_style()
    fig, ax = plt.subplots(figsize=(10, 5))
    series_clean = series.dropna()
    ax.hist(series_clean, bins=bins, color="#264653", alpha=0.7,
            edgecolor="white", density=True)
    series_clean.plot.kde(ax=ax, color="#e76f51", linewidth=2)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Densitas")
    if rupiah:
        ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmt_rupiah))
    plt.tight_layout()
    if filename:
        save_fig(filename)
    plt.show()


def plot_boxplot(df: pd.DataFrame, cols: list, title: str, filename: str = None):
    """Boxplot untuk deteksi outlier."""
    set_style()
    fig, axes = plt.subplots(1, len(cols), figsize=(5 * len(cols), 5))
    if len(cols) == 1:
        axes = [axes]
    for ax, col in zip(axes, cols):
        data = df[col].dropna()
        ax.boxplot(data, patch_artist=True,
                   boxprops={"facecolor": "#2a9d8f", "alpha": 0.7},
                   medianprops={"color": "#e76f51", "linewidth": 2},
                   flierprops={"marker": "o", "markersize": 3, "alpha": 0.4})
        ax.set_title(col, fontsize=11)
        ax.set_ylabel("Nilai")
    fig.suptitle(title, fontsize=14, fontweight="bold")
    plt.tight_layout()
    if filename:
        save_fig(filename)
    plt.show()
