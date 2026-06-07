# 📘 PANDUAN LENGKAP UNTUK PEMULA
# Project Data Science: Analisis E-Commerce Shopee

---

## 🧭 DAFTAR ISI

1. [Apa itu project ini?](#1-apa-itu-project-ini)
2. [Peta File & Folder — Siapa Ngomong ke Siapa?](#2-peta-file--folder)
3. [Cara Menjalankan (Step by Step)](#3-cara-menjalankan)
4. [Penjelasan Setiap File](#4-penjelasan-setiap-file)
5. [Penjelasan Data (CSV) — Apa Arti Setiap Kolom?](#5-penjelasan-data)
6. [Kenapa Data Tidak Lengkap?](#6-kenapa-data-tidak-lengkap)
7. [Alur Kerja Kode dari Awal sampai Akhir](#7-alur-kerja-kode)
8. [Pertanyaan Umum (FAQ)](#8-faq)

---

## 1. APA ITU PROJECT INI?

Project ini adalah analisis data penjualan sebuah toko di **Shopee** selama ±2 tahun
(Desember 2023 – November 2025). Kita menggunakan Python untuk:

- **Membaca** ribuan baris data transaksi
- **Membersihkan** data yang kotor/tidak konsisten
- **Menghitung** statistik (rata-rata, median, dll)
- **Membuat grafik** untuk memahami pola penjualan

Bayangkan seperti membuat laporan penjualan toko, tapi dilakukan oleh komputer secara
otomatis untuk 20.848 transaksi sekaligus!

---

## 2. PETA FILE & FOLDER

Berikut gambaran LENGKAP bagaimana semua file saling berhubungan:

```
┌─────────────────────────────────────────────────────────────────┐
│                    ALUR DATA PROJECT                            │
│                                                                 │
│  temp_data/                                                     │
│  └─ Clean_Dataset/CLEAN/                                        │
│     ├─ JanuarySales2024_clean.xlsx  ──┐                        │
│     ├─ FebruarySales2024_clean.xlsx   │  24 file Excel         │
│     ├─ ... (22 file lain)             │  digabung jadi 1       │
│     └─ NovemberSales2025_clean.xlsx ──┘                        │
│                    │                                            │
│                    ▼  (dibaca oleh)                             │
│  src/utils.py  ◄──────────────────── fungsi load_all_excel()   │
│       │                                                         │
│       ▼  (menghasilkan)                                         │
│  data/processed/                                                │
│  ├─ all_months_clean.csv      ← data gabungan mentah           │
│  └─ all_months_cleaned.csv    ← data setelah dibersihkan       │
│                    │                                            │
│                    ▼  (dibaca oleh)                             │
│  notebooks/                                                     │
│  ├─ 01_data_understanding.ipynb   ← Pengenalan + Load Data     │
│  ├─ 02_data_cleaning.ipynb        ← Bersihkan Data             │
│  ├─ 03_exploratory_analysis.ipynb ← Analisis Mendalam          │
│  └─ 04_visualization_report.ipynb ← Buat 9 Grafik             │
│                    │                                            │
│                    ▼  (menghasilkan)                            │
│  reports/figures/                                               │
│  └─ *.png   ← 9 file gambar grafik hasil analisis              │
└─────────────────────────────────────────────────────────────────┘
```

### Intinya: Alur Data Sederhana

```
Excel per Bulan (24 file)
        ↓  digabung oleh utils.py
CSV Gabungan (1 file, 20.848 baris)
        ↓  dibaca oleh Notebook 01-04
Grafik & Statistik (9 gambar + angka-angka)
```

---

## 3. CARA MENJALANKAN

### ✅ PRASYARAT (Install Dulu)

Buka PowerShell / Terminal, lalu jalankan:

```powershell
pip install pandas numpy matplotlib seaborn openpyxl scipy jupyter
```

Atau pakai requirements.txt yang sudah ada:

```powershell
pip install -r requirements.txt
```

---

### 🅰️ CARA 1: Pakai Script Python (Paling Cepat)

Script ini menjalankan SEMUA analisis sekaligus dalam satu langkah.

**Langkah-langkah:**

```powershell
# 1. Buka folder project
cd "C:\Users\Riski\OneDrive\Desktop\Kuliah\DTS\UTS\UTS-Data-Science"

# 2. Jalankan script utama
$env:PYTHONIOENCODING='utf-8'
python main_analysis.py
```

**Apa yang terjadi saat dijalankan:**
```
STEP 1: LOAD DATA         ← Baca 24 file Excel, gabungkan
STEP 2: DATA CLEANING     ← Bersihkan data, tambah kolom baru
STEP 3: STATISTIKA        ← Hitung mean, median, dll
STEP 4: VISUALISASI       ← Buat 9 gambar grafik
```

**Hasil:** Folder `reports/figures/` akan berisi 9 file .png berupa grafik.

---

### 🅱️ CARA 2: Pakai Jupyter Notebook (Lengkap + Ada Penjelasannya)

Ini cara terbaik untuk belajar karena kamu bisa lihat penjelasan + kode + hasil
secara bersamaan.

**Langkah-langkah:**

```powershell
# 1. Buka folder project
cd "C:\Users\Riski\OneDrive\Desktop\Kuliah\DTS\UTS\UTS-Data-Science"

# 2. Buka Jupyter
jupyter notebook
```

**Yang terjadi:** Browser akan terbuka otomatis. Kamu akan lihat daftar file.

**Urutan notebook yang harus dijalankan:**

```
① Buka: notebooks/01_data_understanding.ipynb
   → Klik "Run All" atau tekan Shift+Enter di setiap cell
   → Ini akan menghasilkan: data/processed/all_months_clean.csv

② Buka: notebooks/02_data_cleaning.ipynb
   → Jalankan semua cell
   → Ini akan menghasilkan: data/processed/all_months_cleaned.csv

③ Buka: notebooks/03_exploratory_analysis.ipynb
   → Jalankan semua cell
   → Ini akan menghasilkan: 3 gambar grafik di reports/figures/

④ Buka: notebooks/04_visualization_report.ipynb
   → Jalankan semua cell
   → Ini akan menghasilkan: 6 gambar grafik tambahan
```

> ⚠️ PENTING: Harus berurutan! Notebook 02 membutuhkan output dari 01,
>             Notebook 03 membutuhkan output dari 02, dst.

---

## 4. PENJELASAN SETIAP FILE

### 📄 main_analysis.py
```
FUNGSI  : Script utama yang menjalankan seluruh analisis sekaligus
BAHASA  : Python
DIBACA  : Saat kamu jalankan "python main_analysis.py"
CARA    : Dia memanggil fungsi-fungsi dari src/utils.py
HASIL   : Data CSV di data/processed/ + Grafik di reports/figures/
```

### 📄 src/utils.py
```
FUNGSI  : Kumpulan "alat bantu" yang dipakai berulang-ulang
BAHASA  : Python
DIBACA  : Oleh main_analysis.py dan semua notebook
ISINYA  : Fungsi-fungsi seperti:
          - load_all_excel()   → membaca dan menggabungkan file Excel
          - summarize_numeric() → menghitung statistik deskriptif
          - frequency_table()  → membuat tabel distribusi frekuensi
          - detect_outliers_iqr() → mencari data ekstrim (outlier)
          - plot_bar()         → membuat grafik batang
          - plot_pie()         → membuat grafik lingkaran
          - plot_line()        → membuat grafik garis
          - fmt_rupiah()       → format angka jadi "Rp 50K"
```

### 📓 notebooks/01_data_understanding.ipynb
```
FUNGSI  : Notebook pertama — pengenalan dan load data
ISINYA  : - Teori: apa itu Data Science
          - Teori: lifecycle data science
          - Teori: teknik pengumpulan data (data dari Kaggle)
          - Kode : membaca 24 file Excel dan menggabungkannya
          - Kode : menampilkan 5 baris pertama & info dataset
HASIL   : data/processed/all_months_clean.csv (20.848 baris)
```

### 📓 notebooks/02_data_cleaning.ipynb
```
FUNGSI  : Notebook kedua — statistika dasar dan bersihkan data
ISINYA  : - Teori: populasi vs sampel
          - Teori: jenis variabel (nominal, ordinal, rasio, interval)
          - Teori: ukuran pemusatan (mean, median, modus)
          - Kode : hapus duplikat
          - Kode : perbaiki tipe data (tanggal, angka)
          - Kode : normalisasi teks Status Pesanan
          - Kode : tambah kolom Tahun, Bulan, Jam
HASIL   : data/processed/all_months_cleaned.csv (+ kolom baru)
```

### 📓 notebooks/03_exploratory_analysis.ipynb
```
FUNGSI  : Notebook ketiga — analisis mendalam
ISINYA  : - Tabel statistik: mean, median, modus, std, Q1, Q3
          - Tabel distribusi frekuensi semua kategori
          - Deteksi outlier menggunakan IQR
          - Histogram & KDE distribusi nilai transaksi
          - Heatmap korelasi antar variabel
          - Grafik pola per jam dan hari
HASIL   : 3 file gambar .png di reports/figures/
```

### 📓 notebooks/04_visualization_report.ipynb
```
FUNGSI  : Notebook keempat — visualisasi final dan insight
ISINYA  : 9 visualisasi lengkap:
          1. Tren pendapatan bulanan (garis)
          2. Tren jumlah transaksi bulanan (batang)
          3. Distribusi status pesanan (bar + pie)
          4. Metode pembayaran (bar + pie)
          5. Top 10 provinsi (horizontal bar)
          6. Top 15 kategori produk (horizontal bar)
          7. Distribusi nilai transaksi (histogram)
          8. Rata-rata transaksi per metode bayar
          9. Analisis retur (donut + bar)
          + Ringkasan insight dan rekomendasi bisnis
HASIL   : 6 file gambar .png di reports/figures/
```

### 📄 requirements.txt
```
FUNGSI  : Daftar library Python yang dibutuhkan
CARA    : pip install -r requirements.txt
ISI     : pandas, numpy, matplotlib, seaborn, openpyxl, scipy, jupyter
```

### 📄 README.md
```
FUNGSI  : Dokumentasi project (tampil di GitHub)
ISI     : Penjelasan project, cara install, cara jalankan
```

---

## 5. PENJELASAN DATA

### Apa itu file CSV?

CSV = Comma Separated Values. Ini seperti tabel Excel tapi disimpan sebagai
teks biasa. Setiap baris = 1 pesanan. Setiap kolom dipisah dengan koma.

### Contoh Satu Baris Data:

```
ORD_0000006, 2, 1000, 0, 0, Celengan, 1, Selesai, ...
```

Ini artinya:
- ID pesanan: ORD_0000006
- 2 item dibeli
- Berat total 1000 gram
- 0 item diretur
- Diskon Rp 0
- Kategori: Celengan
- 1 jenis kategori
- Status: Selesai

### Penjelasan Lengkap 18 Kolom Asli:

| # | Nama Kolom | Arti | Contoh Nilai |
|---|---|---|---|
| 1 | `order_id` | Nomor unik setiap pesanan | ORD_0000006 |
| 2 | `total_qty` | Berapa banyak barang dipesan | 2 (artinya 2 item) |
| 3 | `total_weight_gr` | Berat total pesanan dalam gram | 1000 (= 1 kg) |
| 4 | `total_returned_qty` | Berapa item yang dikembalikan | 0 (tidak ada retur) |
| 5 | `Total Diskon` | Potongan harga yang diterima (Rp) | 0 |
| 6 | `product_categories` | Kategori barang yang dibeli | Celengan |
| 7 | `num_product_categories` | Jumlah jenis kategori berbeda | 1 |
| 8 | `Status Pesanan` | Kondisi akhir pesanan | Selesai / Batal |
| 9 | `Alasan Pembatalan` | Jika batal, apa alasannya | Ubah Pesanan |
| 10 | `Opsi Pengiriman` | Jasa dan layanan kirim | Hemat Kargo-SPX Hemat |
| 11 | `Metode Pembayaran` | Cara bayar pembeli | COD / ShopeePay |
| 12 | `Kota/Kabupaten` | Kota tujuan pengiriman | KAB. BANDUNG |
| 13 | `Provinsi` | Provinsi tujuan | JAWA BARAT |
| 14 | `Ongkos Kirim Dibayar oleh Pembeli` | Biaya kirim dari pembeli (Rp) | 0 |
| 15 | `Estimasi Potongan Biaya Pengiriman` | Subsidi ongkir dari Shopee (Rp) | 10000 |
| 16 | `Total Pembayaran` | Total uang yang diterima penjual (Rp) | 40996 |
| 17 | `Perkiraan Ongkos Kirim` | Estimasi biaya kirim aktual (Rp) | 10000 |
| 18 | `Waktu Pesanan Dibuat` | Kapan pesanan dibuat | 2024-04-01 07:09 |

### Kolom Tambahan (dibuat oleh kode kita):

| Nama Kolom | Arti | Dibuat Dari |
|---|---|---|
| `_source_file` | Dari file Excel mana data ini berasal | Otomatis saat load |
| `Tahun` | Tahun pesanan | Diambil dari Waktu Pesanan Dibuat |
| `Bulan` | Bulan pesanan (angka 1-12) | Diambil dari Waktu Pesanan Dibuat |
| `Nama_Bulan` | Bulan dalam format "2024-04" | Diambil dari Waktu Pesanan Dibuat |
| `Hari_Minggu` | Hari dalam seminggu | Diambil dari Waktu Pesanan Dibuat |
| `Jam` | Jam pesanan dibuat (0-23) | Diambil dari Waktu Pesanan Dibuat |

---

## 6. KENAPA DATA TIDAK LENGKAP?

Ini pertanyaan sangat bagus! Mari saya jelaskan.

### Data ini berasal dari MANA?

Data ini adalah **export laporan penjual Shopee** yang kemudian diupload ke Kaggle.
Fitur export ini tersedia di Seller Center Shopee.

### Kenapa tidak ada nama produk, harga satuan, nama pembeli, dll?

Karena format export Shopee memang **hanya merekam ringkasan PER PESANAN** (bukan
per produk). Ini disengaja oleh Shopee dengan beberapa alasan:

#### 1. PRIVASI PEMBELI
```
Shopee melindungi data pribadi pembeli. Nama lengkap, nomor HP,
dan alamat detail TIDAK boleh di-export untuk alasan keamanan.
Hanya kota/provinsi yang boleh terlihat.
```

#### 2. FORMAT EXPORT SHOPEE
```
Shopee menyediakan dua jenis laporan:
- Laporan PESANAN  → inilah yang kita punya (per order)
- Laporan PRODUK   → detail per item (tapi tidak public di Kaggle)

Yang di-export ke CSV/Excel adalah laporan pesanan,
bukan laporan produk yang lebih detail.
```

#### 3. AGREGASI PER ORDER
```
Satu pesanan bisa berisi BANYAK produk berbeda.
Misalnya seseorang pesan: 2 Celengan + 1 Mangkok + 3 Toples
→ Di data ini tercatat sebagai 1 baris dengan:
  total_qty = 6
  product_categories = "Celengan, Aksesoris Mandi, Toples/Sealware"
  num_product_categories = 3
```

### Apa yang TIDAK ADA di data ini:
```
❌ Nama produk spesifik (misal: "Celengan Babi Lucu 500ml")
❌ Harga per item (hanya total pembayaran per order)
❌ Nama pembeli
❌ Nomor HP pembeli
❌ Alamat lengkap (hanya kota/provinsi)
❌ Foto produk
❌ Rating/ulasan
❌ Stok produk
❌ Biaya produksi / keuntungan bersih
```

### Apa yang ADA di data ini:
```
✅ ID pesanan unik
✅ Jumlah total item per pesanan
✅ Berat total (estimasi jenis produk)
✅ Kategori produk (umum)
✅ Status pesanan (selesai/batal)
✅ Metode pembayaran
✅ Lokasi pembeli (kota/provinsi)
✅ Total nilai transaksi
✅ Informasi biaya kirim
✅ Waktu pesanan dibuat (jam, hari, bulan, tahun)
```

### Apakah datanya berguna meski "tidak lengkap"?

YA! Bahkan dengan data terbatas ini kita bisa menjawab pertanyaan penting:

```
Pertanyaan Bisnis          Data yang Digunakan
──────────────────────────────────────────────────────────
"Bulan apa penjualan       Nama_Bulan + Total Pembayaran
 paling tinggi?"

"Daerah mana pembeli       Provinsi + Kota
 paling banyak?"

"Cara bayar apa yg         Metode Pembayaran
 paling populer?"

"Produk kategori apa       product_categories
 paling laris?"

"Jam berapa paling         Jam + jumlah transaksi
 banyak pesanan masuk?"

"Berapa % pesanan batal?"  Status Pesanan
```

---

## 7. ALUR KERJA KODE

### Bagaimana kode saling berhubungan? Mari kita telusuri!

#### SAAT kamu jalankan `python main_analysis.py`:

```
main_analysis.py mulai berjalan
│
├─ Line 1-15: Import library (pandas, numpy, matplotlib, dll)
│             └─ "Library" = alat bantu yang sudah dibuat orang lain
│
├─ Line 16: from src.utils import load_all_excel, ...
│             └─ "Ambil" fungsi dari utils.py untuk dipakai di sini
│
├─ STEP 1: load_all_excel('temp_data/Clean_Dataset/CLEAN')
│   │       └─ Fungsi ini ada di src/utils.py
│   │          Dia akan:
│   │          1. Cari semua file .xlsx di folder itu
│   │          2. Baca satu per satu (24 file)
│   │          3. Gabungkan jadi satu tabel besar
│   │          4. Return DataFrame (tabel) 20.848 baris
│   │
│   └─ Simpan ke: data/processed/all_months_clean.csv
│
├─ STEP 2: Data Cleaning
│   │       Proses langsung di main_analysis.py:
│   │       - Hapus duplikat berdasarkan order_id
│   │       - Konversi kolom tanggal ke format datetime
│   │       - Konversi kolom harga ke tipe angka (int/float)
│   │       - Perbaiki teks Status Pesanan yang tidak konsisten
│   │       - Tambah kolom: Tahun, Bulan, Nama_Bulan, Hari, Jam
│   │
│   └─ Simpan ke: data/processed/all_months_cleaned.csv
│
├─ STEP 3: Statistika (memanggil summarize_numeric() dari utils.py)
│           Menghitung untuk setiap kolom angka:
│           - Count (jumlah data)
│           - Mean (rata-rata)
│           - Median (nilai tengah)
│           - Modus (nilai paling sering muncul)
│           - Std Dev (standar deviasi = seberapa menyebar data)
│           - Q1 (25% data di bawah nilai ini)
│           - Q3 (75% data di bawah nilai ini)
│           - Min, Max
│           - Skewness (condong ke mana distribusinya)
│           - Kurtosis (seberapa lancip/datar puncak distribusi)
│
└─ STEP 4: Visualisasi (membuat 9 grafik)
            Setiap grafik:
            1. Ambil data dari DataFrame
            2. Hitung aggregasi (groupby/value_counts)
            3. Buat gambar dengan matplotlib
            4. Simpan ke reports/figures/nama_file.png
```

---

### Analogi Mudah: Bayangkan seperti Dapur Restoran

```
┌─────────────────────────────────────────────────────────┐
│  BAHAN BAKU          = File Excel 24 bulan             │
│  GUDANG BAHAN        = temp_data/Clean_Dataset/CLEAN/  │
│  RESEP               = src/utils.py                    │
│  DAPUR (proses masak)= main_analysis.py / notebooks/   │
│  KULKAS (simpan)     = data/processed/                 │
│  HASIL MASAKAN       = reports/figures/ (grafik .png)  │
│  MENU (dokumentasi)  = README.md                       │
└─────────────────────────────────────────────────────────┘
```

---

## 8. FAQ (Pertanyaan yang Sering Ditanya)

### ❓ "Kenapa ada 2 versi CSV?"

```
all_months_clean.csv    → Data MENTAH yang baru digabungkan dari Excel
                          Belum diproses apa-apa
all_months_cleaned.csv  → Data yang sudah DIBERSIHKAN dan ditambah kolom baru
                          Inilah yang dipakai untuk analisis
```

### ❓ "Apa perbedaan notebook dan script Python biasa?"

```
Script (.py)         Notebook (.ipynb)
────────────────     ────────────────────────────────
Dijalankan sekaligus Bisa dijalankan per blok (cell)
Tidak ada penjelasan Ada teks penjelasan di antara kode
Output di terminal   Output langsung di bawah kode
Cocok untuk produksi Cocok untuk belajar & eksplorasi
```

### ❓ "Apa itu DataFrame?"

```
DataFrame = Tabel Data dalam Python (seperti sheet Excel tapi di memori komputer)

Contoh DataFrame:
  order_id    total_qty  Provinsi      Total Pembayaran
  ORD_000001  2          JAWA BARAT    40996
  ORD_000002  1          BANTEN        18280
  ORD_000003  5          DKI JAKARTA   92800

Kita bisa filter, hitung, dan visualisasi DataFrame ini.
```

### ❓ "Apa itu fungsi/function?"

```
Fungsi = Sekumpulan kode yang bisa dipanggil berkali-kali dengan nama pendek

Misalnya di utils.py ada fungsi load_all_excel()
Tanpa fungsi, kita harus tulis ulang 30 baris kode setiap mau baca file Excel.
Dengan fungsi, cukup tulis: df = load_all_excel('folder_excel')
```

### ❓ "Error: ModuleNotFoundError"

```
Artinya: Library Python belum terinstall.
Solusi : pip install [nama_library]
Contoh : pip install pandas
```

### ❓ "Kenapa ada kolom yang isinya 0 semua?"

```
Kolom seperti "Alasan Pembatalan" akan 0/kosong untuk pesanan yang SELESAI.
Kolom "total_returned_qty" akan 0 untuk pesanan yang tidak ada returnya.
Ini normal — tidak semua kolom relevan untuk setiap baris data.
```

---

## 🎯 RINGKASAN CARA TERCEPAT MULAI

```
1. Buka PowerShell
2. cd "C:\Users\Riski\OneDrive\Desktop\Kuliah\DTS\UTS\UTS-Data-Science"
3. pip install -r requirements.txt   (sekali saja)
4. $env:PYTHONIOENCODING='utf-8'
5. python main_analysis.py
6. Lihat hasil grafik di folder: reports/figures/
```

Atau untuk belajar lebih dalam:
```
1. Buka PowerShell
2. cd "C:\Users\Riski\OneDrive\Desktop\Kuliah\DTS\UTS\UTS-Data-Science"
3. jupyter notebook
4. Buka browser, jalankan notebook 01 → 02 → 03 → 04
```

---

*File ini dibuat sebagai panduan belajar Data Science untuk pemula.*
*Semangat belajar! 🚀*
