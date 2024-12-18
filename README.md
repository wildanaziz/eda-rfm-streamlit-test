# Streamlit Dashboard for EDA and RFM Analysis

## Overview
Proyek ini adalah dasbor Streamlit untuk memvisualisasikan hasil Analisis Data Eksploratif (EDA) dan Analisis RFM (Recency, Frequency, and Monetary). Aplikasi ini memungkinkan pengguna untuk memuat data pelanggan, menganalisis pola, dan memahami segmentasi pelanggan.

## Prasyarat
Sebelum menjalankan aplikasi, pastikan Anda telah menginstal yang berikut:
- Python (versi 3.8 atau yang lebih baru)
- Anaconda (opsional) untuk mengelola lingkungan

## Setup Environment - Anaconda
```bash
conda create --name eda-rfm python=3.12
conda activate eda-rfm
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal
```bash
# Buat direktori projek
mkdir EDA_RFM_WILDAN
cd EDA_RFM_WILDAN

# Gunakan pipenv untuk manajemen environment
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Install library yang dibutuhkan
Buat file `requirements.txt` di direktori proyek dengan konten berikut:
```txt
pandas
numpy
seaborn
matplotlib
streamlit
```
Install library menggunakan:
```bash
pip install -r requirements.txt
```

## Menjalankan Aplikasi Streamlit
Untuk menjalankan aplikasi, gunakan perintah berikut di terminal Anda:
```bash
streamlit run app.py
```

## Struktur File
Pastikan proyek Anda memiliki struktur berikut:
```
EDA_RFM_WILDAN/
|-- app.py
|-- main.ipynb
|-- requirements.txt
|-- rfm_dataset/
    |-- olist_orders_dataset.csv
    |-- olist_order_payments_dataset.csv
```

## Petunjuk
1. Klon atau unduh repositori ini.
2. Tempatkan kumpulan data yang diperlukan (`olist_orders_dataset.csv` dan `olist_order_payments_dataset.csv`) di dalam folder `rfm_dataset`.
3. Ikuti langkah-langkah untuk menyiapkan lingkungan dan menginstal dependensi.
4. Jalankan aplikasi dengan perintah `streamlit run`.
5. Buka URL yang diberikan di browser Anda untuk berinteraksi dengan dasbor.

## Penggunaan
- Muat kumpulan data dari direktori `rfm_dataset`.
- Lihat visualisasi EDA, termasuk tren, peta panas, dan distribusi.
- Jelajahi segmentasi RFM untuk mengidentifikasi kategori pelanggan.

## Troubleshooting
Jika Anda mengalami masalah:
- Verifikasi bahwa semua dependensi telah diinstal dengan benar.
- Pastikan file kumpulan data berada di direktori yang benar.
- Periksa versi Python dan pengaturan lingkungan.

