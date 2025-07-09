import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from ai_model import kombinasi_4d

def tampilkan_hasil_prediksi(result, probs):
    with st.expander("🎯 Hasil Prediksi Top 6 Digit"):
        col1, col2 = st.columns(2)
        for i, label in enumerate(["Ribuan", "Ratusan", "Puluhan", "Satuan"]):
            with (col1 if i % 2 == 0 else col2):
                st.markdown(f"**{label}:** {', '.join(map(str, result[i]))}")

    if probs:
        with st.expander("📊 Confidence Bar per Digit"):
            for i, label in enumerate(["Ribuan", "Ratusan", "Puluhan", "Satuan"]):
                st.markdown(f"**🔢 {label}**")
                digit_data = pd.DataFrame({
                    "Digit": [str(d) for d in result[i]],
                    "Confidence": probs[i]
                }).sort_values(by="Confidence", ascending=True)
                st.bar_chart(digit_data.set_index("Digit"))

def tampilkan_kombinasi_terbaik(df, selected_lokasi, model_type, min_conf, power, voting_mode):
    with st.spinner("🔢 Menghitung kombinasi 4D terbaik..."):
        top_komb = kombinasi_4d(df, lokasi=selected_lokasi, model_type=model_type,
                                top_n=10, min_conf=min_conf, power=power, mode=voting_mode)
        if top_komb:
            with st.expander("💡 Simulasi Kombinasi 4D Terbaik"):
                sim_col = st.columns(2)
                for i, (komb, score) in enumerate(top_komb):
                    with sim_col[i % 2]:
                        st.markdown(f"`{komb}` - ⚡️ Confidence: `{score:.4f}`")