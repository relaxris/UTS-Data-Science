import pandas as pd
import matplotlib.pyplot as plt
import zipfile
import os
from pathlib import Path

# =====================================
# 1. LOAD DATA
# =====================================

zip_path = "Dataset E-commerce.zip"

temp_folder = "temp_data"
os.makedirs(temp_folder, exist_ok=True)

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(temp_folder)

excel_files = []

for root, dirs, files in os.walk(temp_folder):
    for file in files:
        if file.endswith(".xlsx"):
            excel_files.append(os.path.join(root, file))

print(f"Jumlah file ditemukan: {len(excel_files)}")

df_list = []

for file in excel_files:
    try:
        df = pd.read_excel(file)
        df_list.append(df)
    except:
        print("Gagal membaca:", file)

data = pd.concat(df_list, ignore_index=True)

print("Jumlah data:", len(data))
print("Jumlah kolom:", len(data.columns))

# =====================================
# 2. DATA CLEANING
# =====================================

data.drop_duplicates(inplace=True)

data["Waktu Pesanan Dibuat"] = pd.to_datetime(
    data["Waktu Pesanan Dibuat"],
    errors="coerce"
)

data["Total Pembayaran"] = pd.to_numeric(
    data["Total Pembayaran"],
    errors="coerce"
)

data.fillna(0, inplace=True)

# =====================================
# 3. INFORMASI DATASET
# =====================================

print("\n=== INFO DATA ===")
print(data.info())

print("\n=== DESKRIPSI NUMERIK ===")
print(data.describe())

# =====================================
# 4. STATUS PESANAN
# =====================================

status = data["Status Pesanan"].value_counts()

print("\nStatus Pesanan:")
print(status)

plt.figure(figsize=(8,5))
status.plot(kind="bar")
plt.title("Distribusi Status Pesanan")
plt.ylabel("Jumlah")
plt.tight_layout()
plt.savefig("status_pesanan.png")
plt.show()

# =====================================
# 5. METODE PEMBAYARAN
# =====================================

payment = data["Metode Pembayaran"].value_counts()

print("\nMetode Pembayaran:")
print(payment)

plt.figure(figsize=(8,8))
payment.head(5).plot(
    kind="pie",
    autopct="%1.1f%%"
)
plt.ylabel("")
plt.title("5 Metode Pembayaran Teratas")
plt.tight_layout()
plt.savefig("metode_pembayaran.png")
plt.show()

# =====================================
# 6. PROVINSI TERATAS
# =====================================

province = data["Provinsi"].value_counts().head(10)

print("\nTop 10 Provinsi:")
print(province)

plt.figure(figsize=(10,5))
province.plot(kind="bar")
plt.title("Top 10 Provinsi Transaksi")
plt.ylabel("Jumlah Transaksi")
plt.tight_layout()
plt.savefig("provinsi_teratas.png")
plt.show()

# =====================================
# 7. TOTAL PENDAPATAN
# =====================================

revenue = data["Total Pembayaran"].sum()

print("\nTotal Pendapatan")
print(f"Rp {revenue:,.0f}")

# =====================================
# 8. TREN PENJUALAN BULANAN
# =====================================

data["Bulan"] = data["Waktu Pesanan Dibuat"].dt.to_period("M")

monthly_sales = (
    data.groupby("Bulan")["Total Pembayaran"]
    .sum()
)

plt.figure(figsize=(12,5))
monthly_sales.plot(marker="o")
plt.title("Tren Penjualan Bulanan")
plt.ylabel("Total Penjualan (Rp)")
plt.grid(True)
plt.tight_layout()
plt.savefig("tren_penjualan.png")
plt.show()

# =====================================
# 9. INSIGHT
# =====================================

print("\n=== HASIL ANALISIS ===")

print(f"Jumlah transaksi: {len(data):,}")
print(f"Total pendapatan: Rp {revenue:,.0f}")

print(
    f"Status terbanyak: "
    f"{status.idxmax()} ({status.max():,})"
)

print(
    f"Metode pembayaran terbanyak: "
    f"{payment.idxmax()} ({payment.max():,})"
)

print(
    f"Provinsi dengan transaksi tertinggi: "
    f"{province.idxmax()} ({province.max():,})"
)

print("\nAnalisis selesai.")