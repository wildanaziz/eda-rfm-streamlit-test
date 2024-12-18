# Dashboard untuk Hasil EDA dan RFM Analysis
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import timedelta

# Konfigurasi halaman
st.set_page_config(page_title="Dashboard RFM Analysis", layout="wide")

# Fungsi untuk memuat data
@st.cache_data
def load_data():
    order_pelanggan = pd.read_csv("rfm_dataset/olist_orders_dataset.csv")
    payment_pelanggan = pd.read_csv("rfm_dataset/olist_order_payments_dataset.csv")
    return order_pelanggan, payment_pelanggan

# Memuat data
order_pelanggan, payment_pelanggan = load_data()

# Membersihkan data
order_pelanggan_clean = order_pelanggan.dropna(subset=['order_approved_at', 'order_delivered_carrier_date', 'order_delivered_customer_date'])

order_pelanggan_clean[['order_purchase_timestamp',
                       'order_approved_at',
                       'order_delivered_carrier_date',
                       'order_delivered_customer_date',
                       'order_estimated_delivery_date']] = order_pelanggan_clean[
    ['order_purchase_timestamp', 'order_approved_at', 'order_delivered_carrier_date',
     'order_delivered_customer_date', 'order_estimated_delivery_date']] \
    .apply(lambda x: pd.to_datetime(x, errors='coerce'))

order_terakhir = order_pelanggan_clean['order_delivered_carrier_date'].max() + timedelta(days=1)
df_group = order_pelanggan_clean.merge(payment_pelanggan, how='inner', on=['order_id'])

# Membuat RFM table
rfm_merge = df_group.groupby('customer_id').agg(
    r=('order_delivered_carrier_date', lambda x: (order_terakhir - x.max()).days),
    f=('payment_sequential', 'count'),
    m=('payment_value', 'sum')
).reset_index()

# Membuat kolom rfm-score
quantiles = {
    'r': rfm_merge['r'].quantile([.33, .66]).values,
    'f': np.array([1, 2]),
    'm': rfm_merge['m'].quantile([.33, .66]).values
}

def rfm_segment(x, col):
    if col in ['f', 'm']:
        if x <= quantiles[col][0]:
            return 1
        elif x <= quantiles[col][1]:
            return 2
        else:
            return 3
    elif col == 'r':
        if x <= quantiles[col][0]:
            return 3
        elif x <= quantiles[col][1]:
            return 2
        else:
            return 1

for col in ['r', 'f', 'm']:
    rfm_merge[f'{col}-segment'] = rfm_merge[col].apply(lambda x: rfm_segment(x, col))

rfm_merge['rfm-score'] = rfm_merge['r-segment'].astype(str) + \
                         rfm_merge['f-segment'].astype(str) + \
                         rfm_merge['m-segment'].astype(str)

# Menentukan tipe pelanggan berdasarkan rfm-score
def segmentasi(x):
    if x in ['333', '323']:
        return 'TERBAIK'
    elif x in ['223', '233']:
        return 'PELANGGAN PENGELUARAN TERBESAR'
    elif x in ['111', '112', '113']:
        return 'HILANG'
    elif x in ['321', '322', '331', '332']:
        return 'PELANGGAN SETIA'
    elif x in ['311', '312', '313']:
        return 'PELANGGAN BARU'
    elif x in ['231', '232']:
        return 'DULU SERING BELANJA'
    elif x in ['131', '132', '133']:
        return 'DULU SETIA'
    elif x in ['211', '212', '213']:
        return 'PELANGGAN BARU SATU KALI BELANJA'
    elif x in ['221', '222']:
        return 'NORMAL'
    elif x in ['121', '122', '123']:
        return 'SEGERA HILANG'

rfm_merge['customer_type'] = rfm_merge['rfm-score'].apply(segmentasi)

# Distribusi pelanggan
dist_rfm = rfm_merge.groupby(['customer_type'], as_index=False).agg({'customer_id': 'count'})
dist_rfm['persentase_pengguna'] = dist_rfm['customer_id'] * 100 / dist_rfm['customer_id'].sum()
    

# Halaman EDA
st.title("Dashboard EDA dan RFM Analysis")
st.markdown("""Pada projek ini akan menggunakan RFM Analysis pada dataset *Brazilian E-Commerce Public Dataset by Olist*
Dimana RFM Analysis terdiri atas 3 parameter utama yakni
- Recency (R): Seberapa baru pelanggan melakukan transaksi terakhir.
- Frequency (F): Seberapa sering pelanggan melakukan pembelian.
- Monetary (M): Total uang yang dihabiskan oleh pelanggan.

Akhir dari projek ini ditujukan untuk menganalisis serta mengelompokkan pelanggan ke dalam segmen berdasarkan perilaku mereka, dan dengan analisis ini diharapkan membantu dalam strategi pemasaran.""")

st.sidebar.title("Menu")
menu = st.sidebar.selectbox("Pilih Analisis", ["EDA", "RFM Analysis"])

if menu == "EDA":
    st.header("Exploratory Data Analysis (EDA)")

    # Korelasi Heatmap
    st.subheader("Korelasi Heatmap")
    st.markdown("Dapat dilihat dari heatmap korelasi bahwa nilai korelasi antar variabel r, f, dan m sangat rendah. Hal ini juga sejalan dengan prinsip dari RFM dimana RFM didesain untuk menangkap dimensi berbeda dari perilaku pelanggan. Oleh karena itu, korelasi rendah diharapkan.")

    st.write("")
    corr = rfm_merge[['r', 'f', 'm']].corr()
    plt.figure(figsize=(6, 4))
    sns.heatmap(corr, annot=True, cmap='coolwarm')
    st.pyplot(plt)

    # Tren Pembelian per Bulan
    st.subheader("Tren Pembelian per Bulan")
    st.markdown("Dapat dilihat dari dari trend pembelian perbulan selalu mengalami peningkatan")
    order_pelanggan_clean['month'] = order_pelanggan_clean['order_purchase_timestamp'].dt.to_period('M')
    monthly_trend = order_pelanggan_clean.groupby('month').size()
    plt.figure(figsize=(10, 5))
    monthly_trend.plot(kind='line')
    plt.title('Tren Jumlah Pesanan per Bulan')
    plt.xlabel('Bulan')
    plt.ylabel('Jumlah Pesanan')
    plt.grid(True)
    st.pyplot(plt)

    # Retensi Pelanggan
    st.subheader("Retensi Pelanggan per Tahun")
    st.markdown("Dapat dilihat dari dari resistensi pelanggan unik pertahun selalu meningkat")
    order_pelanggan_clean['year'] = order_pelanggan_clean['order_purchase_timestamp'].dt.year
    customer_retention = order_pelanggan_clean.groupby('year')['customer_id'].nunique()
    plt.figure(figsize=(8, 4))
    customer_retention.plot(kind='bar', color='orange')
    plt.title('Retensi Pelanggan per Tahun')
    plt.xlabel('Tahun')
    plt.ylabel('Jumlah Pelanggan Unik')
    plt.grid(axis='y')
    st.pyplot(plt)

elif menu == "RFM Analysis":
    st.header("RFM Analysis")

    st.subheader("Tabel RFM")
    st.write(rfm_merge.head())

    # Distribusi R, F, dan M
    st.subheader("Distribusi Recency")
    plt.figure(figsize=(8, 4))
    sns.histplot(rfm_merge['r'], bins=30, kde=False)
    plt.title('Distribusi Recency (R)')
    st.pyplot(plt)

    st.subheader("Distribusi Monetary")
    plt.figure(figsize=(8, 4))
    sns.histplot(rfm_merge['m'], bins=30, kde=False)
    plt.title('Distribusi Monetary (M)')
    st.pyplot(plt)

    # Segmentasi Pelanggan
    st.subheader("Distribusi Pelanggan Berdasarkan Tipe")
    
    dist_rfm = rfm_merge.reset_index().groupby(['customer_type'], as_index=False).agg({'customer_id': 'count'}).rename(columns={'customer_id': 'jumlah'})
    st.dataframe(dist_rfm)

    # Visualisasi Tipe Pelanggan
    st.bar_chart(dist_rfm.set_index('customer_type')['jumlah'])
    st.markdown("""
### Analisis Distribusi Pelanggan

Dapat dilihat dari output distribusi tersebut bahwa:
1. **Churned (32.78%)**  
   Sekitar **1/3 dari pengguna** sudah keluar (*churned*).  
   Ini menunjukkan adanya **masalah retensi pelanggan**, di mana bisnis kehilangan pelanggan secara signifikan dan belum berhasil mempertahankannya.

2. **Newest dan Recent One-Timers (32.47% + 31.77%)**  
   Sekitar **2/3 dari pengguna** adalah pendatang baru atau hanya melakukan **satu kali transaksi**.  
   Ini berarti ada banyak **traffic** tetapi **konversi** menjadi pelanggan loyal masih sangat rendah.  

   **Strategi Re-Engagement:**  
   - Fokus pada **program onboarding** pelanggan baru.  
   - Berikan **penawaran khusus** atau **diskon transaksi kedua** untuk mendorong pembelian berikutnya.  
   - Gunakan **kampanye email** atau **program referral** agar mereka tertarik kembali bertransaksi.  

3. **Loyal, Normal, dan Returning Customers (~3% total)**  
   Hanya sebagian kecil pengguna (**~3%**) yang **setia** atau **aktif kembali** melakukan transaksi.  
   Ini menunjukkan adanya **kesulitan dalam mempertahankan pelanggan** untuk melakukan pembelian berulang.  

   **Strategi Menanggulangi:**  
   - Implementasikan **program loyalitas pelanggan** seperti sistem poin atau reward.  
   - Tawarkan **insentif eksklusif** untuk pelanggan setia, seperti diskon spesial atau akses prioritas.  
   - Bangun hubungan jangka panjang dengan meningkatkan **customer experience** melalui pelayanan yang lebih baik.  
""")
