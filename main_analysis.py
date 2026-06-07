"""
main_analysis.py — Script utama analisis e-commerce (entry point)
Jalankan: python main_analysis.py

Script ini menjalankan seluruh pipeline analisis secara berurutan:
1. Load & merge semua file Excel
2. Data cleaning
3. Statistika deskriptif
4. Visualisasi (9 chart)
"""

import os
import sys
import glob
import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

warnings.filterwarnings('ignore')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.utils import (
    load_all_excel, set_style, summarize_numeric,
    frequency_table, detect_outliers_iqr,
    plot_bar, plot_pie, plot_line, plot_histogram, fmt_rupiah
)

# ──────────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────────
CLEAN_FOLDER = os.path.join('temp_data', 'Clean_Dataset', 'CLEAN')
PROCESSED_DIR = os.path.join('data', 'processed')
FIGURES_DIR = os.path.join('reports', 'figures')

os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(FIGURES_DIR, exist_ok=True)
set_style()

PALETTE = ["#264653", "#2a9d8f", "#e9c46a", "#f4a261", "#e76f51",
           "#023e8a", "#0077b6", "#0096c7", "#00b4d8", "#48cae4"]


def save_fig(filename):
    path = os.path.join(FIGURES_DIR, filename)
    plt.savefig(path, bbox_inches='tight', dpi=150)
    print(f'  💾 Figure disimpan: {path}')


# ──────────────────────────────────────────────
# STEP 1: LOAD DATA
# ──────────────────────────────────────────────
print('\n' + '='*55)
print('  STEP 1: LOAD DATA')
print('='*55)

df = load_all_excel(CLEAN_FOLDER)
df.to_csv(os.path.join(PROCESSED_DIR, 'all_months_clean.csv'), index=False)
print(f'  [OK] Data mentah disimpan ke: {PROCESSED_DIR}/all_months_clean.csv')


# ──────────────────────────────────────────────
# STEP 2: DATA CLEANING
# ──────────────────────────────────────────────
print('\n' + '='*55)
print('  STEP 2: DATA CLEANING')
print('='*55)

df_clean = df.copy()

# Hapus duplikat
before = len(df_clean)
df_clean.drop_duplicates(subset='order_id', keep='first', inplace=True)
print(f'  [1] Duplikat dihapus: {before - len(df_clean):,} baris')

# Konversi datetime
df_clean['Waktu Pesanan Dibuat'] = pd.to_datetime(
    df_clean['Waktu Pesanan Dibuat'], errors='coerce'
)

# Konversi numerik
num_cols = [
    'total_qty', 'total_weight_gr', 'Total Diskon',
    'Ongkos Kirim Dibayar oleh Pembeli',
    'Estimasi Potongan Biaya Pengiriman',
    'Total Pembayaran', 'Perkiraan Ongkos Kirim'
]
for col in num_cols:
    df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')

# Normalisasi status
df_clean['Status Pesanan'] = df_clean['Status Pesanan'].str.strip()
df_clean.loc[
    df_clean['Status Pesanan'].str.contains('Pesanan diterima', na=False),
    'Status Pesanan'
] = 'Pesanan Diterima'
df_clean['Status Pesanan'] = df_clean['Status Pesanan'].replace(
    {'Telah Dikirim': 'Sedang Dikirim'}
)

# Fitur turunan waktu
df_clean['Tahun'] = df_clean['Waktu Pesanan Dibuat'].dt.year
df_clean['Bulan'] = df_clean['Waktu Pesanan Dibuat'].dt.month
df_clean['Nama_Bulan'] = df_clean['Waktu Pesanan Dibuat'].dt.strftime('%Y-%m')
df_clean['Hari_Minggu'] = df_clean['Waktu Pesanan Dibuat'].dt.day_name()
df_clean['Jam'] = df_clean['Waktu Pesanan Dibuat'].dt.hour
df_clean['Alasan Pembatalan'] = df_clean['Alasan Pembatalan'].fillna('Tidak Dibatalkan')

df_clean.to_csv(os.path.join(PROCESSED_DIR, 'all_months_cleaned.csv'), index=False)
print(f'  [OK] Data bersih: {len(df_clean):,} baris, {len(df_clean.columns)} kolom')
print(f'  [OK] Disimpan ke: {PROCESSED_DIR}/all_months_cleaned.csv')


# ──────────────────────────────────────────────
# STEP 3: STATISTIKA DESKRIPTIF
# ──────────────────────────────────────────────
print('\n' + '='*55)
print('  STEP 3: STATISTIKA DESKRIPTIF')
print('='*55)

summary = summarize_numeric(df_clean)
print(summary.to_string())

tp = df_clean['Total Pembayaran']
print(f'\n  📊 Total Pembayaran:')
print(f'     Mean   : Rp {tp.mean():,.0f}')
print(f'     Median : Rp {tp.median():,.0f}')
print(f'     Std    : Rp {tp.std():,.0f}')
print(f'     Total  : Rp {tp.sum():,.0f}')

print(f'\n  📊 Tabel Frekuensi: Status Pesanan')
print(frequency_table(df_clean['Status Pesanan']).to_string())

print(f'\n  📊 Tabel Frekuensi: Metode Pembayaran')
print(frequency_table(df_clean['Metode Pembayaran']).to_string())

print(f'\n  📊 Tabel Frekuensi: Provinsi (Top 10)')
print(frequency_table(df_clean['Provinsi'], top_n=10).to_string())

print(f'\n  📊 Deteksi Outlier: Total Pembayaran')
outlier_info = detect_outliers_iqr(df_clean['Total Pembayaran'].dropna())
for k, v in outlier_info.items():
    print(f'     {k}: {v:,}' if isinstance(v, (int, float)) else f'     {k}: {v}')


# ──────────────────────────────────────────────
# STEP 4: VISUALISASI
# ──────────────────────────────────────────────
print('\n' + '='*55)
print('  STEP 4: VISUALISASI (9 CHART)')
print('='*55)

# ── VIZ 1: Tren Bulanan
print('\n  [1] Tren Penjualan Bulanan...')
monthly = df_clean.groupby('Nama_Bulan').agg(
    Jumlah_Transaksi=('order_id', 'count'),
    Total_Pendapatan=('Total Pembayaran', 'sum')
).sort_index()

fig, axes = plt.subplots(2, 1, figsize=(15, 10))
axes[0].plot(monthly.index, monthly['Total_Pendapatan'], marker='o', color='#2a9d8f', linewidth=2.5)
axes[0].fill_between(monthly.index, monthly['Total_Pendapatan'], alpha=0.1, color='#2a9d8f')
axes[0].set_title('Tren Total Pendapatan Bulanan', fontweight='bold')
axes[0].set_ylabel('Total Pendapatan (Rp)')
axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(fmt_rupiah))
axes[0].grid(True, alpha=0.3)
plt.setp(axes[0].xaxis.get_majorticklabels(), rotation=45, ha='right')
axes[1].bar(monthly.index, monthly['Jumlah_Transaksi'], color='#264653', alpha=0.8)
axes[1].set_title('Tren Jumlah Transaksi Bulanan', fontweight='bold')
axes[1].set_ylabel('Jumlah Transaksi')
plt.setp(axes[1].xaxis.get_majorticklabels(), rotation=45, ha='right')
plt.tight_layout()
save_fig('04_tren_bulanan.png')
plt.close()

# ── VIZ 2: Status Pesanan
print('  [2] Distribusi Status Pesanan...')
status = df_clean['Status Pesanan'].value_counts()
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
axes[0].barh(status.index, status.values, color=PALETTE[:len(status)])
axes[0].set_title('Distribusi Status Pesanan', fontweight='bold')
wedges, texts, autotexts = axes[1].pie(
    status.values, labels=status.index, autopct='%1.1f%%',
    colors=PALETTE[:len(status)], wedgeprops={'edgecolor': 'white', 'linewidth': 2}
)
axes[1].set_title('Proporsi Status Pesanan', fontweight='bold')
plt.tight_layout()
save_fig('04_status_pesanan.png')
plt.close()

# ── VIZ 3: Metode Pembayaran
print('  [3] Metode Pembayaran...')
payment = df_clean['Metode Pembayaran'].value_counts()
top5 = payment.head(5)
others = payment.iloc[5:].sum()
pie_data = pd.concat([top5, pd.Series({'Lainnya': others})])
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
axes[0].barh(payment.head(8).index[::-1], payment.head(8).values[::-1],
             color=PALETTE[:8], alpha=0.85)
axes[0].set_title('Top 8 Metode Pembayaran', fontweight='bold')
axes[1].pie(pie_data.values, labels=pie_data.index, autopct='%1.1f%%',
            colors=PALETTE[:len(pie_data)], wedgeprops={'edgecolor': 'white'})
axes[1].set_title('Proporsi Metode Pembayaran', fontweight='bold')
plt.tight_layout()
save_fig('04_metode_pembayaran.png')
plt.close()

# ── VIZ 4: Provinsi
print('  [4] Top 10 Provinsi...')
province = df_clean.groupby('Provinsi').agg(
    Jumlah=('order_id', 'count'), Pendapatan=('Total Pembayaran', 'sum')
).sort_values('Jumlah', ascending=False).head(10)
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
axes[0].barh(province.index[::-1], province['Jumlah'][::-1], color=PALETTE[:10])
axes[0].set_title('Top 10 Provinsi (Jumlah Transaksi)', fontweight='bold')
axes[1].barh(province.index[::-1], province['Pendapatan'][::-1], color='#0077b6')
axes[1].set_title('Top 10 Provinsi (Pendapatan)', fontweight='bold')
axes[1].xaxis.set_major_formatter(mticker.FuncFormatter(fmt_rupiah))
plt.tight_layout()
save_fig('04_provinsi_top10.png')
plt.close()

# ── VIZ 5: Kategori Produk
print('  [5] Kategori Produk Terlaris...')
category = df_clean['product_categories'].value_counts().head(15)
fig, ax = plt.subplots(figsize=(12, 7))
ax.barh(category.index[::-1], category.values[::-1], color=PALETTE * 2, alpha=0.85)
ax.set_title('Top 15 Kategori Produk Terlaris', fontweight='bold')
ax.set_xlabel('Jumlah Transaksi')
plt.tight_layout()
save_fig('04_kategori_produk.png')
plt.close()

# ── VIZ 6: Distribusi Nilai Transaksi
print('  [6] Distribusi Nilai Transaksi...')
tp_trimmed = df_clean['Total Pembayaran'].dropna()
tp_trimmed = tp_trimmed[tp_trimmed < tp_trimmed.quantile(0.99)]
fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(tp_trimmed, bins=40, color='#264653', alpha=0.75, edgecolor='white', density=True)
tp_trimmed.plot.kde(ax=ax, color='#e76f51', linewidth=2.5)
ax.set_title('Distribusi Total Pembayaran (≤ P99)', fontweight='bold')
ax.set_xlabel('Total Pembayaran (Rp)')
ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmt_rupiah))
plt.tight_layout()
save_fig('04_distribusi_nilai.png')
plt.close()

# ── VIZ 7: Korelasi
print('  [7] Heatmap Korelasi...')
corr_cols = ['total_qty', 'total_weight_gr', 'Total Diskon',
             'Ongkos Kirim Dibayar oleh Pembeli',
             'Estimasi Potongan Biaya Pengiriman',
             'Total Pembayaran', 'Perkiraan Ongkos Kirim']
corr_matrix = df_clean[corr_cols].corr()
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='RdYlGn',
            mask=mask, ax=ax, vmin=-1, vmax=1, linewidths=0.5)
ax.set_title('Matriks Korelasi Variabel Numerik', fontweight='bold')
plt.tight_layout()
save_fig('03_korelasi_heatmap.png')
plt.close()

# ── VIZ 8: Pola Temporal
print('  [8] Pola Temporal (Jam & Hari)...')
hourly = df_clean.groupby('Jam').size()
day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
day_labels = ['Senin','Selasa','Rabu','Kamis','Jumat','Sabtu','Minggu']
daily = df_clean.groupby('Hari_Minggu').size().reindex(day_order)
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].bar(hourly.index, hourly.values, color='#2a9d8f', alpha=0.8)
axes[0].set_title('Distribusi Pesanan per Jam', fontweight='bold')
axes[1].bar(day_labels, daily.values, color='#e9c46a', alpha=0.8)
axes[1].set_title('Distribusi Pesanan per Hari', fontweight='bold')
plt.tight_layout()
save_fig('03_pola_temporal.png')
plt.close()

# ── VIZ 9: Outlier Boxplot
print('  [9] Boxplot Outlier...')
cols_box = ['Total Pembayaran', 'total_qty', 'Total Diskon']
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
colors_box = ['#2a9d8f', '#264653', '#e9c46a']
for ax, col, color in zip(axes, cols_box, colors_box):
    ax.boxplot(df_clean[col].dropna(), patch_artist=True,
               boxprops={'facecolor': color, 'alpha': 0.7},
               medianprops={'color': '#e76f51', 'linewidth': 2.5},
               flierprops={'marker': 'o', 'markersize': 2, 'alpha': 0.3})
    ax.set_title(col, fontweight='bold')
fig.suptitle('Boxplot Deteksi Outlier', fontsize=14, fontweight='bold')
plt.tight_layout()
save_fig('03_boxplot_outlier.png')
plt.close()


# ──────────────────────────────────────────────
# STEP 5: SUMMARY
# ──────────────────────────────────────────────
print('\n' + '='*55)
print('  RINGKASAN HASIL ANALISIS')
print('='*55)
print(f'  Total Transaksi    : {len(df_clean):,}')
print(f'  Total Pendapatan   : Rp {df_clean["Total Pembayaran"].sum():,.0f}')
print(f'  Rata-rata/Transaksi: Rp {df_clean["Total Pembayaran"].mean():,.0f}')
print(f'  Metode Bayar Terpop: {df_clean["Metode Pembayaran"].value_counts().idxmax()}')
print(f'  Provinsi Terbanyak : {df_clean["Provinsi"].value_counts().idxmax()}')
print(f'  Kategori Terlaris  : {df_clean["product_categories"].value_counts().idxmax()}')
print(f'\n  📁 Figures tersimpan di: {FIGURES_DIR}/')
figs = sorted(glob.glob(os.path.join(FIGURES_DIR, '*.png')))
for f in figs:
    print(f'     [OK] {os.path.basename(f)}')
print(f'\n  [OK] Analisis selesai!\n')
