import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

pwd = os.getcwd()
# Membuatkan function untuk manipulasi dataframe

def byhour(df):
    hourly_rental = df.groupby(by='hr')['Total'].mean()
    return hourly_rental

def bymonth(df):
    monthly_rental = df.groupby(by='mnth')['Total'].mean()
    return monthly_rental

# import dataframe
daily_df = pd.read_csv('daily_modified_df.csv')
hourly_df = pd.read_csv('hourly_modified_df.csv')
season_df = pd.read_csv('melt_season_df.csv')
weather_df = pd.read_csv('melt_weathersit_df.csv')

daily_df['dteday'] = pd.to_datetime(daily_df['dteday'])
hourly_df['dteday'] = pd.to_datetime(hourly_df['dteday'])


# Filter data
min_date = hourly_df["dteday"].min()
max_date = hourly_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image('https://raw.githubusercontent.com/awiawii/streamlit-visualization/main/logo-bike.png', width=100)
    st.header('Bike Sharing')
    st.markdown("\n")
    
    
    st.markdown("""
    <div style="text-align: justify">
        Pilih tanggal untuk melihat data pada rentang tanggal tersebut.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("\n")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
main_df = hourly_df[(hourly_df["dteday"] >= str(start_date)) & 
                (hourly_df["dteday"] <= str(end_date))]

# Menyiapkan dataframe yang dikelompokkan
byhour_df = byhour(main_df)
bymonth_df = bymonth(hourly_df)

st.header('Bike Sharing Dashboard')
st.markdown("""
<div style="text-align: justify">
  Dashboard ini menyajikan visualisasi data yang menggambarkan penggunaan sepeda berdasarkan waktu, bulan, musim, dan kondisi cuaca. Informasi tersebut memberikan pandangan komprehensif terhadap pola-pola penggunaan sepeda, memungkinkan pengguna untuk memahami tren, perubahan musiman, dan dampak cuaca terhadap aktivitas penggunaan sepeda.
</div>
""", unsafe_allow_html=True)

st.markdown("\n")

st.subheader('Rata-rata Pengguna Rental Sepeda Setiap Bulan')
# Plotting Rata-rata Pengguna Sepeda Bulanan

fig, ax = plt.subplots(figsize=(16, 8))
ax.bar(bymonth_df.index, bymonth_df.values, color='#00E8FF')
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

# Mengubah latar belakang grafik menjadi hitam
fig.patch.set_facecolor('#0E1117')
ax.set_facecolor('#262730')

# Mengubah warna label dan ticks jika diperlukan
ax.xaxis.label.set_color('white')
ax.yaxis.label.set_color('white')
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')

# Menambahkan label x, label y, dan judul
ax.set_xlabel('Month', color='white', fontsize=18)
ax.set_ylabel('Rata-rata', color='white', fontsize=18)

# Tampilkan plot menggunakan st.pyplot()
st.pyplot(fig)

with st.expander("See explanation"):
    st.write(
        """Berdasarkan data tahun 2011 sampai tahun 2012, Tren pengguna sepeda menunjukkan peningkatan
        sejak awal tahun hingga pertengahan tahun,
        khususnya sekitar bulan Juni. Dari bulan Juni hingga September, terlihat bahwa penggunaan
        sepeda cenderung tetap stabil, namun mulai mengalami penurunan pada bulan Oktober hingga akhir tahun.
        """
    )

st.markdown("\n")
st.markdown("\n")

# Menampilkan Daily Rental

date_range = f"{start_date} – {end_date}"

# Menggunakan metode replace
date_range_slash = date_range.replace("-", "/")

st.subheader(f'Pengguna Sepeda Harian {date_range_slash}')


col1, col2, col3 = st.columns(3)

with col1:
    casual_user = main_df.casual.sum()
    st.metric("Casual Rental", value=casual_user)

with col2:
    registered_user = main_df.registered.sum()
    st.metric("Register Rental", value=registered_user)
    
with col3:
    Total_user = main_df.Total.sum()
    st.metric("Total Rental", value=Total_user)
    
st.markdown("\n")
st.markdown("\n")
st.subheader(f'Rata-Rata Pengguna Sepeda Setiap Jam')
# Plotting rata-rata pengguna setiap jamnya
    
fig, ax = plt.subplots(figsize=(16, 8))
ax.bar(byhour_df.index, byhour_df.values, color='#00E8FF')
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

# Mengubah latar belakang grafik menjadi hitam
fig.patch.set_facecolor('#0E1117')
ax.set_facecolor('#262730')

# Mengubah warna label dan ticks jika diperlukan
ax.xaxis.label.set_color('white')
ax.yaxis.label.set_color('white')
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')

# Menambahkan label x, label y, dan judul
ax.set_xlabel('Hour', color='white', fontsize=18)
ax.set_ylabel('Rata-rata', color='white', fontsize=18)

# Tampilkan plot menggunakan st.pyplot()
st.pyplot(fig)

with st.expander("See explanation"):
    st.write(
        """Rata-rata pengguna sepeda mengalami peningkatan yang mencolok pada dua waktu tertentu,
        yaitu pada saat jam berangkat kerja sekitar pukul 08.00 pagi, dan pada saat jam pulang kerja sekitar pukul 17.00.
        """
    )



st.markdown("\n")
st.markdown("\n")
st.subheader(f'Jumlah Pengguna Sepeda Berdasarkan Musim')
#Plotting pengguna berdasarkan musim

fig, ax = plt.subplots(figsize=(16, 8))
ax.bar(main_df['season'], main_df['Total'], color='#00E8FF')
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

# Mengubah latar belakang grafik menjadi hitam
fig.patch.set_facecolor('#0E1117')
ax.set_facecolor('#262730')

# Mengubah warna label dan ticks jika diperlukan
ax.xaxis.label.set_color('white')
ax.yaxis.label.set_color('white')
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')

# Menambahkan label x, label y, dan judul
ax.set_xlabel('Season', color='white', fontsize=18)
ax.set_ylabel('Jumlah', color='white', fontsize=18)
ax.set_title('Jumlah Pengguna Berdasarkan Musim', color='white', fontsize=20)

# Tampilkan plot menggunakan st.pyplot()
st.pyplot(fig)

with st.expander("See explanation"):
    st.write(
        """Berdasarkan data tahun 2011 sampai tahun 2012, jumlah tertinggi pengguna sepeda terjadi pada *summer*
        dan jumlah terendah pengguna sepeda terjadi pada musim *winter*. Dari grafik juga terlihat menunjukkan *left-skewed distribution*.
        """
    )

st.markdown("\n")
st.markdown("\n")
st.subheader(f'Jumlah Pengguna Sepeda Berdasarkan Cuaca')
#Plotting pengguna berdasarkan cuaca

fig, ax = plt.subplots(figsize=(16, 8))
ax.bar(main_df['weathersit'], main_df['Total'], color='#00E8FF')
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

# Mengubah latar belakang grafik menjadi hitam
fig.patch.set_facecolor('#0E1117')
ax.set_facecolor('#262730')

# Mengubah warna label dan ticks jika diperlukan
ax.xaxis.label.set_color('white')
ax.yaxis.label.set_color('white')
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')

# Menambahkan label x, label y, dan judul
ax.set_xlabel('Cuaca', color='white', fontsize=18)
ax.set_ylabel('Jumlah', color='white', fontsize=18)
ax.set_title('Jumlah Pengguna Berdasarkan Cuaca', color='white', fontsize=20)

# Tampilkan plot menggunakan st.pyplot()
st.pyplot(fig)

with st.expander("See explanation"):
    st.write(
        """Berdasarkan data tahun 2011 sampai tahun 2012, jumlah tertinggi pengguna sepeda terjadi pada saat cuaca cerah/*clear*
        dan jumlah terendah pengguna sepeda terjadi pada saat cuaca hujan lebat/*heavy precipitation*. Dari grafik juga terlihat menunjukkan *right-skewed distribution*.
        """
    )



st.caption('Copyright © Asnawi Alamsyah 2024')

    
