import pandas as pd
import requests

def fetch_data(lokasi, hari, putaran):
    url = f"https://wysiwygscan.com/api?pasaran={lokasi.lower()}&hari={hari}&putaran={putaran}&format=json&urut=asc"
    headers = {"Authorization": "Bearer 6705327a2c9a9135f2c8fbad19f09b46"}
    response = requests.get(url, headers=headers)
    data = response.json()
    return [item["result"] for item in data.get("data", []) if len(item["result"]) == 4 and item["result"].isdigit()]

def cari_putaran_terbaik(selected_lokasi, selected_hari, metode, max_auto_putaran, model_type, top6_markov, top6_markov_order2, top6_markov_hybrid, top6_model):
    best_putaran = 100
    best_acc = -1
    for p in range(50, max_auto_putaran + 1, 50):
        data_try = fetch_data(selected_lokasi, selected_hari, p)
        df_try = pd.DataFrame({"angka": data_try})
        if len(df_try) < 11: continue
        pred = (
            top6_markov(df_try)[0] if metode == "Markov" else
            top6_markov_order2(df_try) if metode == "Markov Order-2" else
            top6_markov_hybrid(df_try) if metode == "Markov Gabungan" else
            top6_model(df_try, lokasi=selected_lokasi, model_type=model_type)
        )
        if not pred: continue
        uji_df = df_try.tail(10)
        total, benar = 0, 0
        for i in range(len(uji_df)):
            actual = f"{int(uji_df.iloc[i]['angka']):04d}"
            for j in range(4):
                if int(actual[j]) in pred[j]:
                    benar += 1
                total += 1
        acc = benar / total * 100 if total else 0
        if acc > best_acc:
            best_acc = acc
            best_putaran = p
    return best_putaran, best_acc

def load_and_display_data(selected_lokasi, selected_hari, use_auto, metode, model_type, max_auto_putaran, putaran_manual):
    angka_list = []
    riwayat_input = ""
    best_putaran = putaran_manual if not use_auto else None

    if selected_lokasi and selected_hari:
        try:
            if use_auto:
                with st.spinner("🚀 Mencari putaran terbaik otomatis..."):
                    best_acc = -1
                    for p in range(50, max_auto_putaran + 1, 50):
                        data_try = fetch_data(selected_lokasi, selected_hari, p)
                        df_try = pd.DataFrame({"angka": data_try})
                        if len(df_try) < 11: continue

                        pred = (
                            st.session_state["top6_markov"](df_try)[0] if metode == "Markov" else
                            st.session_state["top6_markov_order2"](df_try) if metode == "Markov Order-2" else
                            st.session_state["top6_markov_hybrid"](df_try) if metode == "Markov Gabungan" else
                            st.session_state["top6_model"](df_try, lokasi=selected_lokasi, model_type=model_type)
                        )
                        if not pred: continue
                        uji_df = df_try.tail(10)
                        total, benar = 0, 0
                        for i in range(len(uji_df)):
                            actual = f"{int(uji_df.iloc[i]['angka']):04d}"
                            for j in range(4):
                                if int(actual[j]) in pred[j]:
                                    benar += 1
                                total += 1
                        acc = benar / total * 100 if total else 0
                        if acc > best_acc:
                            best_acc = acc
                            best_putaran = p

                if best_putaran:
                    st.success(f"✅ Putaran terbaik: {best_putaran} (akurasi {best_acc:.2f}%)")
                else:
                    best_putaran = 100
                    st.warning("⚠️ Tidak ditemukan putaran optimal, default ke 100.")

            with st.spinner(f"🔄 Mengambil data dari API (putaran {best_putaran})..."):
                angka_list = fetch_data(selected_lokasi, selected_hari, best_putaran)
                riwayat_input = "\n".join(angka_list)
                st.success(f"✅ {len(angka_list)} angka berhasil diambil.")
                with st.expander("📥 Lihat Data"):
                    st.code(riwayat_input, language="text")

        except Exception as e:
            st.error(f"❌ Gagal ambil data API: {e}")

    return angka_list


