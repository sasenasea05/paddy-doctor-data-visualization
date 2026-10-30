import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------------
# 1. KONFIGURASI HALAMAN
# ---------------------------------------------------------
st.set_page_config(
    page_title="Dashboard Analisis Penyakit Tanaman Padi",
    page_icon="🌾",
    layout="wide"
)

# ---------------------------------------------------------
# 2. LOAD DATASET
# ---------------------------------------------------------
@st.cache_data
def load_data():
    # Membaca dataset dari folder data/
    df = pd.read_csv("data/dataset.csv")
    return df

try:
    df = load_data()
except Exception as e:
    st.error("⚠️ File 'dataset.csv' tidak ditemukan di folder 'data/'. Pastikan file sudah dipindahkan dan namanya diubah menjadi 'dataset.csv'.")
    st.stop()

# ---------------------------------------------------------
# 3. SIDEBAR - FILTER INTERAKTIF (Komponen #3 UTS)
# ---------------------------------------------------------
st.sidebar.header("🔍 Filter Data Interaktif")

# Filter 1: Pilih Varietas Padi
all_varieties = sorted(df["variety"].dropna().unique().tolist())
selected_variety = st.sidebar.multiselect(
    "Pilih Varietas Tanaman:",
    options=all_varieties,
    default=all_varieties
)

# Filter 2: Pilih Jenis Penyakit (Label)
all_labels = sorted(df["label"].dropna().unique().tolist())
selected_label = st.sidebar.multiselect(
    "Pilih Kondisi / Penyakit:",
    options=all_labels,
    default=all_labels
)

# Penerapan Filter pada Dataframe
filtered_df = df[
    (df["variety"].isin(selected_variety)) & 
    (df["label"].isin(selected_label))
]

# ---------------------------------------------------------
# 4. HEADER DASHBOARD & DESAIN UI/UX
# ---------------------------------------------------------
st.title("🌾 Dashboard Analisis Kesehatan Tanaman Padi - Sabrina Septiananda 241051026")
st.markdown("Dashboard interaktif untuk memantau varietas tanaman padi, distribusi umur, dan tingkat infeksi penyakit tanaman.")
st.markdown("---")

# ---------------------------------------------------------
# 5. KPI CARDS (Komponen #1 UTS)
# ---------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

total_samples = len(filtered_df)
avg_age = filtered_df["age"].mean() if total_samples > 0 else 0
total_diseases = filtered_df["label"].nunique() if total_samples > 0 else 0
total_varieties = filtered_df["variety"].nunique() if total_samples > 0 else 0

col1.metric("Total Sampel Tanaman", f"{total_samples:,}")
col2.metric("Rata-rata Umur Tanaman", f"{avg_age:.1f} Hari")
col3.metric("Jumlah Jenis Penyakit", f"{total_diseases} Jenis")
col4.metric("Varietas Padi Terdaftar", f"{total_varieties} Varietas")

st.markdown("---")

# ---------------------------------------------------------
# 6. VARIASI CHARTS (Komponen #2 UTS - Minimal 4 Grafik)
# ---------------------------------------------------------
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.subheader("1. Frekuensi Jenis Penyakit (Bar Chart)")
    if total_samples > 0:
        label_counts = filtered_df["label"].value_counts().reset_index()
        label_counts.columns = ["Jenis Penyakit", "Jumlah Sampel"]
        fig_bar = px.bar(
            label_counts, 
            x="Jumlah Sampel", 
            y="Jenis Penyakit", 
            orientation="h",
            color="Jenis Penyakit",
            title="Jumlah Kasus berdasarkan Jenis Penyakit"
        )
        fig_bar.update_layout(showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)

with row1_col2:
    st.subheader("2. Proporsi Varietas Padi (Donut Chart)")
    if total_samples > 0:
        variety_counts = filtered_df["variety"].value_counts().reset_index()
        variety_counts.columns = ["Varietas", "Jumlah Sampel"]
        fig_pie = px.pie(
            variety_counts, 
            names="Varietas", 
            values="Jumlah Sampel", 
            hole=0.4,
            title="Persentase Sampel per Varietas Tanaman"
        )
        st.plotly_chart(fig_pie, use_container_width=True)

row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.subheader("3. Distribusi Umur Tanaman per Penyakit (Box Plot)")
    if total_samples > 0:
        fig_box = px.box(
            filtered_df, 
            x="label", 
            y="age", 
            color="label",
            title="Rentang Umur Tanaman (Hari) berdasarkan Jenis Penyakit"
        )
        fig_box.update_layout(showlegend=False, xaxis_tickangle=-45)
        st.plotly_chart(fig_box, use_container_width=True)

with row2_col2:
    st.subheader("4. Sebaran Umur vs Varietas Tanaman (Scatter Plot)")
    if total_samples > 0:
        fig_scatter = px.strip(
            filtered_df, 
            x="variety", 
            y="age", 
            color="label",
            title="Sebaran Umur Tanaman berdasarkan Varietas Padi"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("---")

# ---------------------------------------------------------
# 7. ANALISIS & STORYTELLING (Komponen #5 UTS)
# ---------------------------------------------------------
st.subheader("💡 Wawasan Utama (Key Insights)")
st.info("""
- **Kondisi Tanaman**: Dataset mencakup **10.407 sampel** dengan gabungan varietas lokal dan jenis penyakit daun padi.
- **Kerentanan Usia**: Penyakit tertentu cenderung menyerang pada rentang umur tanaman tertentu (misalnya pada fase vegetatif akhir / generatif).
- **Dominasi Varietas**: Varietas tertentu memiliki ketahanan yang berbeda terhadap jenis infeksi bakteri/jamur pada daun padi.
""")