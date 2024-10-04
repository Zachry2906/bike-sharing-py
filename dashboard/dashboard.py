import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Read the datasets
day_df = pd.read_csv("data/day.csv")
hour_df = pd.read_csv("data/hour.csv")

# Convert date columns
day_df["dteday"] = pd.to_datetime(day_df["dteday"])
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])

# Create merged dataframe
merged_df = pd.merge(
    left=hour_df,
    right=day_df,
    how="left",
    left_on="dteday",  
    right_on="dteday" 
)

# Set page config
st.set_page_config(page_title="Analisis Penyewaan Sepeda", layout="wide")


# Sidebar
st.sidebar.title("Menu Navigasi")
page = st.sidebar.selectbox(
    "Pilih Halaman",
    ["Beranda", "Tampilan Dataset", "Pertanyaan 1", "Pertanyaan 2", "Pertanyaan 3", "Kesimpulan"]
)

# Home page
if page == "Beranda":
    st.title("🚲 Dashboard Analisis Penyewaan Sepeda")
    # Halaman Beranda
    
    # Tampilan metrik yang lebih menarik
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.metric(
            "Total Penyewaan",
            f"{day_df['cnt'].sum():,}",
            delta="Semua Waktu"
        )
    with col2:
        st.metric(
            "Rata-rata Harian",
            f"{int(day_df['cnt'].mean()):,}",
            delta="Per Hari"
        )
    with col3:
        st.metric(
            "Penyewaan Tertinggi",
            f"{day_df['cnt'].max():,}",
            delta="Maksimum"
        )

    st.markdown("---")
    st.markdown("""
    ## Selamat Datang di Dashboard Analisis Penyewaan Sepeda!
    
    Dashboard ini menampilkan analisis mendalam tentang pola penyewaan sepeda. Dataset ini berisi informasi tentang penyewaan sepeda per jam dan harian, termasuk faktor-faktor seperti:
    
    - Kondisi cuaca
    - Waktu dalam sehari
    - Hari dalam seminggu
    - Hari libur
    - Variasi musiman
    
    ### Tujuan Analisis
    - Memahami bagaimana cuaca mempengaruhi pola penyewaan
    - Mengidentifikasi jam-jam puncak penyewaan
    - Menganalisis dampak hari libur terhadap penyewaan
    - Menemukan tren musiman dalam penyewaan sepeda
    
    ### Ringkasan Dataset
    Berikut adalah ringkasan statistik dari dataset yang digabungkan:
    """)
    
    st.dataframe(merged_df.describe())

# Dataset Overview page
elif page == "Tampilan Dataset":
    st.title("Tampilan Dataset")
    
    st.header("Dataset Harian")
    st.dataframe(day_df.head())
    st.markdown("---")
    
    st.header("Dataset Per Jam")
    st.dataframe(hour_df.head())
    st.markdown("---")
    
    st.header("Dataset Gabungan")
    st.dataframe(merged_df.head())

# Question 1 page
elif page == "Pertanyaan 1":
    st.title("Bagaimana suhu mempengaruhi penyewaan sepeda di musim yang berbeda?")
    
    season_temp = day_df.groupby(["season", "temp"])["cnt"].mean().reset_index()
    
    plt.figure(figsize=(12, 8))
    sns.lineplot(data=season_temp, x="temp", y="cnt", hue="season", palette="mako")
    plt.title("Rata-rata Penyewaan Sepeda Berdasarkan Suhu di Berbagai Musim", fontsize=14)
    plt.xlabel("Suhu (temp)", fontsize=12)
    plt.ylabel("Rata-rata Penyewaan Sepeda (cnt)", fontsize=12)
    st.pyplot(plt)
    plt.clf()
    
    st.markdown("""
    Dari hasil di atas, dapat disimpulkan bahwa pola penyewaan sepeda berubah-ubah sesuai dengan musim dan suhu:
    Season akan membagi data ke dalam 4 musim yang berbeda:
    1. Musim semi
    2. Musim panas
    3. Musim gugur
    4. Musim dingin

    - **Musim panas**: Penyewaan sepeda mengalami peningkatan seiring dengan suhu yang lebih tinggi, mencapai puncaknya pada suhu optimal. Namun, jika suhu terlalu panas, penyewaan mulai menurun.

    - **Musim dingin**: Penyewaan sepeda cenderung lebih rendah karena suhu dingin. Namun, jika suhu sedikit menghangat, akan ada sedikit peningkatan dalam penyewaan, walaupun tetap lebih rendah dibandingkan musim lainnya.

    - **Musim semi dan musim gugur**: Kedua musim ini menunjukkan hal yang mirip dengan musim panas, namun dengan tingkat penyewaan yang lebih rendah. Peningkatan penyewaan masih terjadi seiring dengan suhu yang hangat, meskipun tidak sekuat di musim panas.

    Secara keseluruhan, penyewaan sepeda dipengaruhi oleh suhu, dengan variasi tergantung musim. Musim panas cenderung paling optimal untuk penyewaan, sementara musim dingin memiliki permintaan yang paling rendah.
    """)

# Question 2 page
elif page == "Pertanyaan 2":
    st.title("Kapan waktu puncak penyewaan sepeda setiap harinya?")
    
    hourly_data = merged_df.groupby("hr")["cnt_x"].mean().reset_index()
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=hourly_data, x="hr", y="cnt_x", palette="mako")
    plt.title("Rata-rata Penyewaan Sepeda Berdasarkan Jam dalam Sehari", fontsize=14)
    plt.xlabel("Jam (hr)", fontsize=12)
    plt.ylabel("Rata-rata Penyewaan Sepeda (cnt_x)", fontsize=12)
    plt.xticks(ticks=range(0, 24))
    st.pyplot(plt)
    plt.clf()
    
    st.markdown("""
    Dari pernyataan di atas, dapat disimpulkan bahwa pola penyewaan sepeda juga dipengaruhi oleh waktu dalam sehari:

    - Pagi hari (terutama jam 8): Ada lonjakan signifikan pada penyewaan sepeda di jam pagi, terutama sekitar jam 8. Ini disebabkan oleh orang-orang yang menggunakan sepeda untuk berangkat kerja atau sekolah, sehingga menciptakan tingginya rental sepeda

    - Sore hari (antara jam 5 hingga 7): Lonjakan lain terjadi pada sore hari, antara jam 5 hingga 7, yang berhubungan dengan waktu pulang kerja atau sekolah. Ini menunjukkan bahwa sepeda juga menjadi moda transportasi untuk pulang kerja maupun pulang sekolah

    - Tengah malam hingga dini hari: Penyewaan sepeda cenderung rendah selama periode ini, yaitu dari tengah malam hingga dini hari. Hal ini disebabkan oleh minimnya aktivitas pada waktu tersebut, di mana orang-orang cenderung beristirahat dan tidak beraktivitas di luar rumah.

    Secara keseluruhan, pola penyewaan sepeda mengikuti rutinitas harian, dengan dua puncak utama di pagi dan sore hari, serta penurunan signifikan pada malam hingga dini hari. penyewaan, sementara musim dingin memiliki permintaan yang paling rendah.
    """)

# Question 3 page
elif page == "Pertanyaan 3":
    st.title("Apakah libur nasional (holiday) meningkatkan atau menurunkan penyewaan sepeda?")
    
    holiday_rentals = day_df.groupby("holiday")["cnt"].mean().reset_index()
    holiday_rentals["holiday"] = holiday_rentals["holiday"].map({0: "Bukan Libur", 1: "Libur Nasional"})
    
    plt.figure(figsize=(8, 6))
    sns.barplot(x="holiday", y="cnt", data=holiday_rentals, palette="viridis")
    plt.title("Rata-rata Penyewaan Sepeda pada Hari Libur vs Hari Biasa", fontsize=14)
    plt.xlabel("Status Hari", fontsize=12)
    plt.ylabel("Rata-rata Penyewaan Sepeda (cnt)", fontsize=12)
    st.pyplot(plt)
    plt.clf()
    
    st.markdown("""
    Konklusi:
    Berdasarkan apa yang menjadi hasil diatas ternyata hari libur nasional atau holiday justru menurunkan jumlah angka penyewaan sepeda diakrenakan kemungkinan banyak orang lebih memilih untuk tetap istirahat selama waktu libur daripada berkegiatan diluar rumah
    """)

elif page == "Kesimpulan":
    st.title("Kesimpulan Analisis Penyewaan Sepeda")
    
    st.markdown("""
    ### 1. Bagaimana suhu mempengaruhi penyewaan sepeda di musim yang berbeda?
    
    Dari hasil di atas, dapat disimpulkan bahwa pola penyewaan sepeda berubah-ubah sesuai dengan musim dan suhu:

    - **Musim panas**: Penyewaan sepeda mengalami peningkatan seiring dengan suhu yang lebih tinggi, mencapai puncaknya pada suhu optimal. Namun, jika suhu terlalu panas, penyewaan mulai menurun

    - **Musim dingin**: Penyewaan sepeda cenderung lebih rendah karena suhu dingin. Namun, jika suhu sedikit menghangat, akan ada sedikit peningkatan dalam penyewaan, walaupun tetap lebih rendah dibandingkan musim lainnya

    - **Musim semi dan musim gugur**: Kedua musim ini menunjukkan hal yang mirip dengan musim panas, namun dengan tingkat penyewaan yang lebih rendah. Peningkatan penyewaan masih terjadi seiring dengan suhu yang hangat, meskipun tidak sekuat di musim panas

    Secara keseluruhan, penyewaan sepeda dipengaruhi oleh suhu, dengan variasi tergantung musim. Musim panas cenderung paling optimal untuk penyewaan, sementara musim dingin memiliki permintaan yang paling rendah.
    
    ---
    
    ### 2. Kapan waktu puncak penyewaan sepeda setiap harinya?
    
    Dari pernyataan di atas, dapat disimpulkan bahwa pola penyewaan sepeda juga dipengaruhi oleh waktu dalam sehari:

    - **Pagi hari (terutama jam 8)**: Ada lonjakan signifikan pada penyewaan sepeda di jam pagi, terutama sekitar jam 8. Ini disebabkan oleh orang-orang yang menggunakan sepeda untuk berangkat kerja atau sekolah, sehingga menciptakan tingginya rental sepeda

    - **Sore hari (antara jam 5 hingga 7)**: Lonjakan lain terjadi pada sore hari, antara jam 5 hingga 7, yang berhubungan dengan waktu pulang kerja atau sekolah. Ini menunjukkan bahwa sepeda juga menjadi moda transportasi untuk pulang kerja maupun pulang sekolah

    - **Tengah malam hingga dini hari**: Penyewaan sepeda cenderung rendah selama periode ini, yaitu dari tengah malam hingga dini hari. Hal ini disebabkan oleh minimnya aktivitas pada waktu tersebut, di mana orang-orang cenderung beristirahat dan tidak beraktivitas di luar rumah.

    Secara keseluruhan, pola penyewaan sepeda mengikuti rutinitas harian, dengan dua puncak utama di pagi dan sore hari, serta penurunan signifikan pada malam hingga dini hari.
    
    ---
    
    ### 3. Apakah libur nasional (holiday) meningkatkan atau menurunkan penyewaan sepeda?

    Berdasarkan apa yang menjadi hasil diatas ternyata hari libur nasional atau holiday justru menurunkan jumlah angka penyewaan sepeda diakrenakan kemungkinan banyak orang lebih memilih untuk tetap istirahat selama waktu libur daripada berkegiatan diluar rumah.
    """)
