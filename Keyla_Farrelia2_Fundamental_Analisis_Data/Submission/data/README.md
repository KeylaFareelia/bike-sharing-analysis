Bike Sharing Data Analysis & Dashboard 

Proyek ini merupakan hasil analisis data eksploratif dan pembuatan dashboard interaktif menggunakan Bike Sharing Dataset (periode 2011–2012) untuk memenuhi tugas akhir kelas Belajar Analisis Data dengan Python di Dicoding.

Struktur Direktori
```text
Submission/
├── dashboard/
│   ├── dashboard.py                            # Kode utama aplikasi dashboard Streamlit
│   ├── day.csv                                 # Dataset penyewaan sepeda harian
│   ├── hour.csv                                # Dataset penyewaan sepeda per jam
│   ├── main_data.csv                           # Dataset bersih hasil tahap Data Wrangling
│   └── requirements.txt                        # Daftar pustaka Python yang digunakan
├── data/
│   └── notebook_Proyek_Analisis_Data3.ipynb    # Jupyter Notebook berisi seluruh proses analisis data
├── README.md                                   # Dokumentasi proyek
└── URL STREAMLIT.txt                           # Tautan aplikasi Streamlit Cloud

Setup Environment - Anaconda
```bash
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt

Setup Environment - Shell/Terminal   Bashmkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt

Run Streamlit App
Bash
streamlit run dashboard/dashboard.py