import streamlit as st
from modules.sidebar_config import configure_sidebar
from modules.data_loader import load_and_display_data
from modules.model_management import handle_model_management
from modules.prediction import handle_prediction

st.set_page_config(page_title="Prediksi Togel AI", layout="wide")

st.title("🔮 Prediksi 4D - AI & Markov")

# Konfigurasi Sidebar
config = configure_sidebar()

# Ambil dan tampilkan data dari API
df, angka_list = load_and_display_data(config)

# Manajemen Model
if config["metode"] == "LSTM AI":
    handle_model_management(df, config)

# Prediksi
if st.button("🔮 Prediksi"):
    handle_prediction(df, config)