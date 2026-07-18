import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="IoT DDoS Detection", page_icon="🛡️", layout="wide")

# --- MEMUAT MODEL TERBAIK ---
# path ke file model
model_path = os.path.join(os.path.dirname(__file__), '../models/best_lgb_model.pkl')

@st.cache_resource
def load_model():
    return joblib.load(model_path)

try:
    model = load_model()
    model_loaded = True
except Exception as e:
    model_loaded = False
    st.error(f"Error memuat model: {e}. Pastikan file best_lgb_model.pkl sudah ada di folder 'models'.")

# --- JUDUL & DESKRIPSI UTAMA ---
st.title("🛡️ Sistem Deteksi Intrusi DDoS pada Jaringan IoT")
st.markdown("""
Aplikasi web ini menggunakan model **LightGBM** yang telah dioptimasi untuk mendeteksi apakah trafik jaringan yang mengalir di perangkat *Smart Home* Anda adalah trafik **Normal** atau serangan **DDoS**.
""")
st.divider()

if model_loaded:
    # nama2 kolom
    feature_names = model.feature_name_
    
    st.sidebar.header("📡 Input Data Trafik Jaringan")
    st.sidebar.write("Masukkan nilai metrik jaringan di bawah ini:")
    
    # --- MEMBUAT FORM INPUT DINAMIS ---
    # input_data akan menampung nilai input dari user
    input_data = {}
    for feature in feature_names:
        # Memberikan nilai default acak/0 untuk simulasi
        input_data[feature] = st.sidebar.number_input(f"{feature}", value=0.0)
    
    # --- TOMBOL PREDIKSI ---
    if st.sidebar.button("🔍 Deteksi Ancaman", type="primary"):
        # ubah input_data menjadi DataFrame untuk prediksi
        input_df = pd.DataFrame([input_data])
        
        with st.spinner("Menganalisis trafik jaringan..."):
            # prediksi menggunakan model
            prediction = model.predict(input_df)[0]
            probability = model.predict_proba(input_df)[0]
            
        # --- MENAMPILKAN HASIL ---
        st.subheader("Berdasarkan hasil analisis metrik jaringan:")
        
        if prediction == 1: # 1 adalah DDoS
            st.error("🚨 **PERINGATAN: TERDETEKSI SERANGAN DDoS!** 🚨")
            st.write(f"Tingkat Keyakinan Model: **{probability[1] * 100:.2f}%**")
            st.info("Sistem IoT Anda mungkin sedang dikompromikan. Segera blokir IP sumber atau putuskan koneksi perangkat dari gateway.")
        else: # 0 adalah Normal (BENIGN)
            st.success("✅ **TRAFIK NORMAL (AMAN)**")
            st.write(f"Tingkat Keyakinan Model: **{probability[0] * 100:.2f}%**")
            st.write("Tidak ada anomali DDoS yang terdeteksi pada aliran data ini.")

# --- DOKUMENTASI TAMBAHAN ---
st.divider()
st.markdown("""
### 📊 Metodologi
Aplikasi ini merupakan hasil implementasi *Capstone Project* dengan alur:
1. **Algoritma Utama**: LightGBM (Gradient Boosting)
2. **Optimasi**: Optuna (Hyperparameter Tuning)
3. **Dataset**: CIC-IDS-2017 (Trafik DDoS & Benign)
""")