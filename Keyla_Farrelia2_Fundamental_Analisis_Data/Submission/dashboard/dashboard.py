import os
import streamlit as st
import pandas as pd
import plotly.express as px

# Konfigurasi halaman
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide"
)

# Mengambil lokasi folder tempat dashboard.py berada
current_dir = os.path.dirname(os.path.abspath(__file__))

# Membaca dataset secara aman untuk Streamlit Cloud & lokal
day_df = pd.read_csv(os.path.join(current_dir, "day.csv"))
hour_df = pd.read_csv(os.path.join(current_dir, "hour.csv"))

# Mengubah kolom tanggal menjadi datetime
day_df["dteday"] = pd.to_datetime(day_df["dteday"])
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])

# ==========================================
# FILTER INTERAKTIF
# ==========================================

st.sidebar.header("Filter Dashboard")

# Filter tahun
selected_year = st.sidebar.selectbox(
    "Pilih Tahun",
    ["Semua", 2011, 2012]
)

# Filter bulan
month_names = {
    1: "January", 2: "February", 3: "March",
    4: "April", 5: "May", 6: "June",
    7: "July", 8: "August", 9: "September",
    10: "October", 11: "November", 12: "December"
}

selected_month = st.sidebar.selectbox(
    "Pilih Bulan",
    ["Semua"] + list(month_names.keys()),
    format_func=lambda x: "Semua Bulan" if x == "Semua" else month_names[x]
)

# Filter jenis hari
selected_day_type = st.sidebar.selectbox(
    "Pilih Jenis Hari",
    ["Semua", "Working Day", "Non-Working Day"]
)

# Membuat salinan dataset
filtered_day_df = day_df.copy()
filtered_hour_df = hour_df.copy()

# Menerapkan filter tahun
if selected_year != "Semua":
    year_value = 0 if selected_year == 2011 else 1
    filtered_day_df = filtered_day_df[filtered_day_df["yr"] == year_value]
    filtered_hour_df = filtered_hour_df[filtered_hour_df["yr"] == year_value]

# Menerapkan filter bulan
if selected_month != "Semua":
    filtered_day_df = filtered_day_df[filtered_day_df["mnth"] == selected_month]
    filtered_hour_df = filtered_hour_df[filtered_hour_df["mnth"] == selected_month]

# Menerapkan filter jenis hari
if selected_day_type == "Working Day":
    filtered_day_df = filtered_day_df[filtered_day_df["workingday"] == 1]
    filtered_hour_df = filtered_hour_df[filtered_hour_df["workingday"] == 1]
elif selected_day_type == "Non-Working Day":
    filtered_day_df = filtered_day_df[filtered_day_df["workingday"] == 0]
    filtered_hour_df = filtered_hour_df[filtered_hour_df["workingday"] == 0]


# Judul dashboard
st.title("🚲 Bike Sharing Dashboard")
st.subheader("Analisis Penyewaan Sepeda Tahun 2011–2012")

st.markdown("""
Dashboard ini menyajikan informasi mengenai pola penyewaan sepeda
berdasarkan bulan, musim, jam, dan jenis hari.
""")

# Informasi dataset
col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="Total Data Harian",
        value=f"{len(filtered_day_df):,}"
    )

with col2:
    st.metric(
        label="Total Data Per Jam",
        value=f"{len(filtered_hour_df):,}"
    )

# Menampilkan data
st.subheader("Preview Dataset Harian")
st.dataframe(filtered_day_df.head())

st.subheader("Preview Dataset Per Jam")
st.dataframe(filtered_hour_df.head())


# ==========================================
# VISUALISASI 1: PENYEWAAN BERDASARKAN BULAN
# ==========================================

st.header("Pola Penyewaan Berdasarkan Bulan")

monthly_rentals = filtered_day_df.groupby("mnth").agg(
    avg_rentals=("cnt", "mean")
).reset_index()

monthly_rentals["month_name"] = monthly_rentals["mnth"].map(month_names)

fig_month = px.line(
    monthly_rentals,
    x="month_name",
    y="avg_rentals",
    markers=True,
    title="Average Daily Bike Rentals by Month"
)

fig_month.update_layout(
    xaxis_title="Month",
    yaxis_title="Average Daily Rentals"
)

st.plotly_chart(fig_month, use_container_width=True)


# ==========================================
# VISUALISASI 2: PENYEWAAN BERDASARKAN MUSIM
# ==========================================

st.header("Pola Penyewaan Berdasarkan Musim")

season_rentals = filtered_day_df.groupby("season").agg(
    avg_rentals=("cnt", "mean")
).reset_index()

season_names = {
    1: "Spring",
    2: "Summer",
    3: "Fall",
    4: "Winter"
}

season_rentals["season_name"] = season_rentals["season"].map(season_names)

fig_season = px.bar(
    season_rentals,
    x="season_name",
    y="avg_rentals",
    title="Average Daily Bike Rentals by Season",
    text_auto=".0f"
)

fig_season.update_layout(
    xaxis_title="Season",
    yaxis_title="Average Daily Rentals"
)

st.plotly_chart(fig_season, use_container_width=True)


# ==========================================
# VISUALISASI 3: PENYEWAAN BERDASARKAN JAM
# ==========================================

st.header("Pola Penyewaan Berdasarkan Jam")

hourly_rentals = filtered_hour_df.groupby(
    ["workingday", "hr"]
).agg(
    avg_rentals=("cnt", "mean")
).reset_index()

hourly_rentals["day_type"] = hourly_rentals["workingday"].map({
    1: "Working Day",
    0: "Non-Working Day"
})

fig_hour = px.line(
    hourly_rentals,
    x="hr",
    y="avg_rentals",
    color="day_type",
    markers=True,
    title="Average Bike Rentals by Hour and Day Type"
)

fig_hour.update_layout(
    xaxis_title="Hour",
    yaxis_title="Average Rentals",
    xaxis=dict(dtick=1),
    legend_title="Day Type"
)

st.plotly_chart(fig_hour, use_container_width=True)


# ==========================================
# VISUALISASI 4: TIPE PENGGUNA
# ==========================================

st.header("Perbandingan Tipe Pengguna")

user_rentals = filtered_hour_df.groupby(
    ["workingday", "hr"]
).agg(
    casual=("casual", "mean"),
    registered=("registered", "mean")
).reset_index()

user_rentals["day_type"] = user_rentals["workingday"].map({
    1: "Working Day",
    0: "Non-Working Day"
})

user_long = user_rentals.melt(
    id_vars=["hr", "day_type"],
    value_vars=["casual", "registered"],
    var_name="user_type",
    value_name="average_users"
)

user_long["user_type"] = user_long["user_type"].map({
    "casual": "Casual Users",
    "registered": "Registered Users"
})

fig_users = px.line(
    user_long,
    x="hr",
    y="average_users",
    color="user_type",
    line_dash="day_type",
    markers=True,
    title="Casual and Registered Users by Hour"
)

fig_users.update_layout(
    xaxis_title="Hour",
    yaxis_title="Average Number of Users",
    xaxis=dict(dtick=1)
)

st.plotly_chart(fig_users, use_container_width=True)
