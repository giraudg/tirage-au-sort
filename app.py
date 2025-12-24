import streamlit as st
import pandas as pd
import random
import time
import base64
from PIL import Image
import io

# Configuration de la page
st.set_page_config(page_title="Giveaway Master", page_icon="🏆", layout="wide")

# Style CSS personnalisé
st.markdown("""
    <style>
    .main {
        background-color: #f1f5f9;
    }
    /* Boutons personnalisés */
    .stButton>button {
        width: 100%;
        border-radius: 50px;
        height: 3.5em;
        background-color: #4f46e5;
        color: white;
        font-weight: bold;
        border: none;
        transition: all 0.3s;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    }
    .stButton>button:hover {
        background-color: #4338ca;
        transform: translateY(-2px);
    }
    
    /* Zone de capture fixe */
    .capture-container {
        background-color: white;
        border-radius: 2.5rem;
        padding: 40px;
        box-shadow: 0 25px 50px -12px rgb(0 0 0 / 0.15);
        border: 1px solid #e2e8f0;
        min-height: 550px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
    }
    
    .winner-label {
        color: #94a3b8;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.2em;
        font-size: 0.8rem;
        margin-bottom: 5px;
    }
    
    .winner-name {
        color: #1e1b4b;
        font-size: 5rem;
        font-weight: 900;
        text-transform: uppercase;
        margin: 10px 0;
        line-height: 1;
    }

    .lot-card {
        display: flex;
        align-items: center;
        gap: 20px;
        background: #f8fafc;
        padding: 15px 25px;
        border-radius: 1.25rem;
        border: 2px solid #f1f5f9;
        margin-top: 30px;
    }
    
    .lot-img {
        width: 80px;
        height: 80px;
        border-radius: 12px;
        object-fit: cover;
        box-shadow: 0 2px 4px rgb(0 0 0 / 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- Initialisation du State ---
if 'participants' not in st.session_state:
    st.session_state.participants = []
if 'winner' not in st.session_state:
    st.session_state.winner = None

# --- Header ---
st.markdown("<div style='padding: 20px 0;'><h1 style='text-align: center; color: #4f46e5; font-weight: 900;'>🏆 GIVEAWAY MASTER</h1></div>", unsafe_allow_html=True)

# --- Layout ---
col_config, col_canvas = st.columns([1, 1.8], gap="large")

with col_config:
    st.markdown("### 🛠️ Configuration")
    with st.container(border=True):
        lot_name = st.text_input("Nom du cadeau", value="Bon d'achat de 100€")
        uploaded_image = st.file_uploader("Image du lot", type=["png", "jpg", "jpeg"])
    
    st.markdown("### 👥 Participants")
    with st.container(border=True):
        source = st.radio("Source d'import", ["Manuel", "Fichier", "Instagram"], horizontal=True)
        
        if source == "Manuel":
            text_area = st.text_area("Saisissez les noms", height=100)
            if st.button("Valider"):
                st.session_state.participants = [n.strip() for n in text_area.split('\n') if n.strip()]
        elif source == "Fichier":
            file = st.file_uploader("CSV/TXT", type=["csv", "txt"])
            if file:
                st.session_state.participants = [n.strip() for n in file.read().decode().split('\n') if n.strip()]
        else:
            if st.button("Simuler Instagram"):
                st.session_state.participants = ["@user1", "@user2", "@user3", "@user4", "@user5"]

        if st.session_state.participants:
            st.success(f"{len(st.session_state.participants)} participants")
            if st.button("Reset", type="secondary"):
                st.session_state.participants = []
                st.session_state.winner = None
                st.rerun()

with col_canvas:
    # On définit l'image en base64 une seule fois pour tout le script
    b64_img = ""
    if uploaded_image:
        b64_img = base64.b64encode(uploaded_image.getvalue()).decode()

    # Conteneur vide pour la zone de capture
    capture_placeholder = st.empty()

    if not st.session_state.winner:
        with capture_placeholder.container():
            st.markdown('<div class="capture-container">', unsafe_allow_html=True)
            st.markdown(f"<div style='margin-bottom: 20px;'><span style='background:#f1f5f9; padding:5px 15px; border-radius:20px; font-size:0.7rem; font-weight:800; color:#64748b;'>CONCOURS : {lot_name.upper()}</span></div>", unsafe_allow_html=True)
            
            if b64_img:
                st.markdown(f'<img src="data:image/png;base64,{b64_img}" style="width:140px; height:140px; border-radius:30px; object-fit:cover; margin-bottom:20px; border:5px solid #f8fafc; box-shadow:0 10px 15px rgba(0,0,0,0.1);">', unsafe_allow_html=True)
            else:
                st.markdown("<h1 style='font-size:4rem;'>🎁</h1>", unsafe_allow_html=True)
            
            st.markdown("<p style='color:#cbd5e1; font-weight:800; letter-spacing:0.1em;'>PRÊT POUR LE TIRAGE</p>", unsafe_allow_html=True)
            
            if len(st.session_state.participants) >= 2:
                if st.button("🎯 LANCER LE TIRAGE"):
                    # Animation manuelle
                    for _ in range(20):
                        temp_name = random.choice(st.session_state.participants)
                        # On réécrit tout le HTML pour l'animation pour garder le style
                        capture_placeholder.markdown(f"""
                            <div class="capture-container">
                                <div style='height:140px;'></div>
                                <h2 style='color:#4f46e5; font-size:4rem; font-weight:900;'>{temp_name}</h2>
                                <div style='height:100px;'></div>
                            </div>
                        """, unsafe_allow_html=True)
                        time.sleep(0.08)
                    
                    st.session_state.winner = random.choice(st.session_state.participants)
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Résultat Final
        with capture_placeholder.container():
            img_tag = f'<img src="data:image/png;base64,{b64_img}" class="lot-img">' if b64_img else ""
            
            st.markdown(f"""
                <div class="capture-container">
                    <div style='margin-bottom: 20px;'><span style='background:#f1f5f9; padding:5px 15px; border-radius:20px; font-size:0.7rem; font-weight:800; color:#64748b;'>CONCOURS : {lot_name.upper()}</span></div>
                    <p class="winner-label">Le gagnant est</p>
                    <div class="winner-name">{st.session_state.winner}</div>
                    
                    <div class="lot-card">
                        {img_tag}
                        <div style="text-align:left;">
                            <p style="font-size:0.6rem; font-weight:900; color:#64748b; text-transform:uppercase; margin:0;">Prix remporté</p>
                            <p style="font-size:1.2rem; font-weight:800; color:#334155; margin:0;">{lot_name}</p>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("🔄 NOUVEAU TIRAGE", type="secondary"):
                st.session_state.winner = None
                st.rerun()

st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.75rem; margin-top: 30px;'>ASTUCE : Cadrez votre capture sur le rectangle blanc.</p>", unsafe_allow_html=True)
