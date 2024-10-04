import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Judul aplikasi
st.title('Analisis Data Pemesanan')

# Baca data
orders_df = pd.read_csv("https://raw.githubusercontent.com/dicodingacademy/dicoding_dataset/main/DicodingCollection/orders.csv")

# Konversi kolom tanggal ke format datetime
orders_df['order_date'] = pd.to_datetime(orders_df['order_date'])

# Kelompokkan data berdasarkan tanggal
daily_payments = orders_df.groupby('order_date')['payment'].sum().reset_index()

# Buat visualisasi
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(daily_payments['order_date'], daily_payments['payment'], marker='o')

# Mempercantik visualisasi
ax.set_title('Trend Total Pembayaran per Hari', fontsize=14, pad=20)
ax.set_xlabel('Tanggal Pemesanan')
ax.set_ylabel('Total Pembayaran')

# Rotasi label tanggal
plt.xticks(rotation=45)

# Tambahkan grid
ax.grid(True, linestyle='--', alpha=0.7)

# Atur layout
plt.tight_layout()

# Tampilkan di Streamlit
st.pyplot(fig)

# Tampilkan data mentah
st.subheader('Data Mentah')
st.dataframe(daily_payments)