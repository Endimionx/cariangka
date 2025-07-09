# modules/sidebar_config.py

import streamlit as st
from lokasi_list import lokasi_list

def configure_sidebar():
    st.header("⚙️ Pengaturan")
    selected_lokasi = st.selectbox("🌍 Pilih Pasaran", lokasi_list)
    selected_hari = st.selectbox("📅 Pilih Hari", ["harian", "kemarin", "2hari", "3hari", "4hari", "5hari"])
    use_auto = st.checkbox("🔍 Cari Putaran Terbaik Otomatis")
    max_auto_putaran = st.number_input("🔢 Maks Putaran Otomatis", min_value=50, max_value=1000, value=300, step=50) if use_auto else None
    putaran = st.slider("🔁 Jumlah Putaran", 1, 1000, 100) if not use_auto else None
    jumlah_uji = st.number_input("📊 Data Uji Akurasi", min_value=1, max_value=200, value=10)
    metode = st.selectbox("🧠 Metode Prediksi", ["Markov", "Markov Order-2", "Markov Gabungan", "LSTM AI", "Ensemble AI + Markov"])

    min_conf, power, temperature, voting_mode, model_type = 0.005, 1.5, 0.5, "product", "lstm"
    use_transformer = False

    if metode in ["LSTM AI", "Ensemble AI + Markov"]:
        min_conf = st.slider("🔎 Minimum Confidence", 0.0001, 0.01, 0.0005, step=0.0001, format="%.4f")
        power = st.slider("📈 Confidence Power", 0.5, 3.0, 1.5, step=0.1)
        temperature = st.slider("🌡️ Temperature Scaling", 0.1, 2.0, 0.5, step=0.1)
        voting_mode = st.selectbox("⚖️ Kombinasi Mode", ["product", "average"])
        use_transformer = st.checkbox("🧠 Gunakan Transformer")
        model_type = "transformer" if use_transformer else "lstm"

    return {
        "selected_lokasi": selected_lokasi,
        "selected_hari": selected_hari,
        "use_auto": use_auto,
        "max_auto_putaran": max_auto_putaran,
        "putaran": putaran,
        "jumlah_uji": jumlah_uji,
        "metode": metode,
        "min_conf": min_conf,
        "power": power,
        "temperature": temperature,
        "voting_mode": voting_mode,
        "model_type": model_type
  }
