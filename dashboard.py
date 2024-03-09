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
        Select a date to view data within that specific date range.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("\n")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Time Range',min_value=min_date,
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
  This dashboard presents data visualizations depicting bicycle usage based on time, month, season, and weather conditions.
  The information provides a comprehensive view of patterns in bicycle usage, enabling users to understand trends,
  seasonal changes, and the impact of weather on bicycle usage activities.
</div>
""", unsafe_allow_html=True)

st.markdown("\n")

st.subheader('Average Bicycle Rental Users Per Month')
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
ax.set_ylabel('Average', color='white', fontsize=18)

# Tampilkan plot menggunakan st.pyplot()
st.pyplot(fig)

with st.expander("See explanation"):
    st.write(
        """Based on the data from 2011 to 2012, the bicycle usage trend indicates an increase from the beginning to the middle of the year,
        particularly around the month of June. From June to September, it appears that bicycle usage tends to remain stable
        but starts to decline from October to the end of the year.
        """
    )

st.markdown("\n")
st.markdown("\n")

# Menampilkan Daily Rental

date_range = f"{start_date} – {end_date}"

# Menggunakan metode replace
date_range_slash = date_range.replace("-", "/")

st.subheader(f'Daily Bicycle Users {date_range_slash}')


col1, col2, col3 = st.columns(3)

with col1:
    casual_user = main_df.casual.sum()
    st.metric("Casual Rentals", value=casual_user)

with col2:
    registered_user = main_df.registered.sum()
    st.metric("Register Rentals", value=registered_user)
    
with col3:
    Total_user = main_df.Total.sum()
    st.metric("Total Rentals", value=Total_user)
    
st.markdown("\n")
st.markdown("\n")
st.subheader(f'Average Bicycle Users Per Hour')
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
ax.set_ylabel('Average', color='white', fontsize=18)

# Tampilkan plot menggunakan st.pyplot()
st.pyplot(fig)

with st.expander("See explanation"):
    st.write(
        """The average bicycle users experience a significant increase at two specific times:
        during the morning rush hour around 8:00 AM and during the evening rush hour around 5:00 PM.
        """
    )



st.markdown("\n")
st.markdown("\n")
st.subheader(f'Number of Bicycle Users Based on Season')
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
ax.set_ylabel('Total', color='white', fontsize=18)
ax.set_title('Number of Users Based on Season', color='white', fontsize=20)

# Tampilkan plot menggunakan st.pyplot()
st.pyplot(fig)

with st.expander("See explanation"):
    st.write(
        """Based on the data from 2011 to 2012, the highest number of bicycle users occurs during the summer,
        while the lowest number of bicycle users is observed during the winter season.
        The graph also indicates a left-skewed distribution.
        """
    )

st.markdown("\n")
st.markdown("\n")
st.subheader(f'Number of Bicycle Users Based on Weather')
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
ax.set_xlabel('Weather', color='white', fontsize=18)
ax.set_ylabel('Total', color='white', fontsize=18)
ax.set_title('Number of Users Based on Weather', color='white', fontsize=20)

# Tampilkan plot menggunakan st.pyplot()
st.pyplot(fig)

with st.expander("See explanation"):
    st.write(
        """Based on the data from 2011 to 2012, the highest number of bicycle users occurs during clear weather,
        while the lowest number of bicycle users is observed during heavy precipitation.
        The graph also indicates a right-skewed distribution.
        """
    )



st.caption('Copyright © Asnawi Alamsyah 2024')

    
