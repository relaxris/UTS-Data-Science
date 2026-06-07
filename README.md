# 📊 Analisis Data E-Commerce — UTS Data Science

Proyek ini merupakan tugas UTS mata kuliah **Data Science** yang menganalisis data transaksi e-commerce (Shopee) dari Kaggle untuk periode **Desember 2023 – November 2025**.

---

## 🎯 Tujuan

Menganalisis pola penjualan, perilaku pembeli, distribusi geografis, dan tren pendapatan dari data e-commerce dengan menggunakan teknik-teknik data science: statistika deskriptif, eksplorasi data, dan visualisasi.

---

## 📁 Struktur Project

```
UTS-Data-Science/
├── data/
│   ├── raw/                         # Data mentah (tidak dimodifikasi)
│   ├── processed/                   # Data setelah cleaning & preprocessing
│   └── external/                    # Data pendukung dari sumber lain
│
├── notebooks/
│   ├── 01_data_understanding.ipynb  # Pengantar DS & pemahaman dataset
│   ├── 02_data_cleaning.ipynb       # Konsep statistika & pembersihan data
│   ├── 03_exploratory_analysis.ipynb# EDA, peringkasan, penyajian, sebaran
│   └── 04_visualization_report.ipynb# Visualisasi lengkap & insight bisnis
│
├── src/
│   └── utils.py                     # Fungsi helper yang dapat digunakan ulang
│
├── reports/
│   └── figures/                     # Output grafik & visualisasi
│
├── temp_data/                       # Dataset original (dari ekstraksi zip)
├── requirements.txt                 # Daftar dependensi Python
├── main_analysis.py                 # Script analisis utama (entry point)
└── README.md                        # Dokumentasi ini
```

---

## 🗄️ Dataset

- **Sumber**: Kaggle — Dataset E-Commerce Shopee Indonesia
- **Periode**: Desember 2023 – November 2025
- **Format**: Excel (.xlsx) per bulan, tersedia versi RAW dan CLEAN
- **Jumlah file**: 48 file Excel (24 CLEAN + 24 RAW_PUBLIC)

### Kolom Utama

| Kolom | Keterangan |
|---|---|
| `order_id` | ID unik setiap pesanan |
| `total_qty` | Jumlah item dalam pesanan |
| `total_weight_gr` | Berat total (gram) |
| `Total Diskon` | Diskon yang diterima (Rp) |
| `product_categories` | Kategori produk yang dibeli |
| `Status Pesanan` | Status akhir pesanan |
| `Metode Pembayaran` | Cara pembayaran (COD, ShopeePay, dll) |
| `Provinsi` | Provinsi tujuan pengiriman |
| `Total Pembayaran` | Nilai transaksi total (Rp) |
| `Waktu Pesanan Dibuat` | Timestamp pesanan |

---

## 🚀 Cara Menjalankan

### 1. Install dependensi
```bash
pip install -r requirements.txt
```

### 2. Jalankan notebook secara berurutan
```bash
jupyter notebook
```
Buka dan jalankan notebook dari `01_` hingga `04_` secara berurutan.

### 3. Atau jalankan script utama
```bash
python main_analysis.py
```

---

## 📓 Isi Notebook

### `01_data_understanding.ipynb`
- Pengantar Data Science (definisi, lifecycle, peran DS)
- Teknik pengumpulan data (sumber Kaggle, data sekunder)
- Load & merge semua file Excel
- Pemahaman awal struktur dataset

### `02_data_cleaning.ipynb`
- Konsep dasar statistika (populasi, sampel, skala pengukuran)
- Identifikasi & penanganan missing values
- Penghapusan duplikat
- Normalisasi tipe data & teks

### `03_exploratory_analysis.ipynb`
- Peringkasan data (mean, median, modus, std, quartile)
- Penyajian data (tabel distribusi frekuensi)
- Kualitas data (outlier, missing pattern)
- Pola sebaran (histogram, boxplot, skewness, kurtosis)
- Korelasi antar variabel

### `04_visualization_report.ipynb`
- Tren penjualan bulanan
- Distribusi status pesanan
- Top 10 provinsi transaksi
- Metode pembayaran
- Top kategori produk
- Distribusi nilai transaksi
- Insight & rekomendasi bisnis

---

## 👤 Informasi

- **Mata Kuliah**: Data Science
- **Sumber Data**: Kaggle (Dataset E-Commerce Shopee Indonesia)
- **Tema**: E-Business
