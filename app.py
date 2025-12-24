import streamlit as st
import pandas as pd
import random
import time
import base64
from PIL import Image
import io

# Configuration de la page
st.set_page_config(page_title="Giveaway Master", page_icon="🏆", layout="wide")

# Style CSS personnalisé pour l'esthétique et la zone de capture
st.markdown("""
    <style>
    .main {
        background-color: #f8fafc;
    }
    .stButton>button {
        width: 100%;
        border-radius: 50px;
        height: 3em;
        background-color: #4f46e5;
        color: white;
        font-weight: bold;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #4338ca;
        transform: scale(1.02);
    }
    .capture-zone {
        background-color: white;
        border-radius: 2rem;
        padding: 40px;
        box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1);
        border: 4px solid white;
        text-align: center;
        min-height: 400px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .winner-text {
        color: #4338ca;
        font-size: 4rem;
        font-weight: 900;
        margin: 20px 0;
        text-transform: uppercase;
    }
    .lot-card {
        display: flex;
        align-items: center;
        gap: 20px;
        background: #ffffff;
        padding: 20px;
        border-radius: 1.5rem;
        border: 1px solid #e2e8f0;
        max-width: 400px;
        margin: 0 auto;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Initialisation du State ---
if 'participants' not in st.session_state:
    st.session_state.participants = []
if 'winner' not in st.session_state:
    st.session_state.winner = None
if 'started' not in st.session_state:
    st.session_state.started = False

# --- Header ---
st.markdown("<h1 style='text-align: center; color: #4f46e5; font-weight: 900;'>🏆 GIVEAWAY MASTER</h1>", unsafe_allow_html=True)

# --- Layout ---
col_config, col_canvas = st.columns([1, 2], gap="large")

with col_config:
    st.subheader("1. Configuration du lot")
    lot_name = st.text_input("Nom du cadeau", value="Bon d'achat de 100€")
    uploaded_image = st.file_uploader("Uploader le visuel", type=["png", "jpg", "jpeg"])
    
    if uploaded_image:
        st.image(uploaded_image, width=150)

    st.divider()
    
    st.subheader("2. Participants")
    source = st.radio("Source", ["Manuel", "Fichier CSV/TXT", "Instagram (Simulé)"], horizontal=True)
    
    if source == "Manuel":
        text_area = st.text_area("Un nom par ligne", height=150)
        if st.button("Valider la liste"):
            st.session_state.participants = [n.strip() for n in text_area.split('\n') if n.strip()]
            
    elif source == "Fichier CSV/TXT":
        file = st.file_uploader("Choisir un fichier", type=["csv", "txt"])
        if file:
            content = file.read().decode("utf-8")
            st.session_state.participants = [n.strip() for n in content.split('\n') if n.strip()]

    else:
        insta_url = st.text_input("Lien du post Instagram")
        if st.button("Simuler l'import"):
            st.session_state.participants = ["@marie_l", "@jean_dupont", "@lucas_v", "@sophie.q", "@pierre_run"]

    if st.session_state.participants:
        st.success(f"✅ {len(st.session_state.participants)} participants chargés")
        if st.button("Réinitialiser"):
            st.session_state.participants = []
            st.session_state.winner = None
            st.rerun()

with col_canvas:
    # Conteneur principal pour la capture d'écran
    canvas = st.container()
    
    with canvas:
        st.markdown('<div class="capture-zone">', unsafe_allow_html=True)
        
        # Titre discret du concours en haut de la zone
        st.markdown(f"<p style='color: #94a3b8; font-weight: 800; font-style: italic; font-size: 0.8rem;'>CONCOURS : {lot_name.upper()}</p>", unsafe_allow_html=True)
        
        display_area = st.empty()
        
        if not st.session_state.winner:
            # État initial
            with display_area.container():
                st.markdown("<br>", unsafe_allow_html=True)
                if uploaded_image:
                    st.image(uploaded_image, width=200)
                else:
                    st.markdown("<h1>🎁</h1>", unsafe_allow_html=True)
                
                st.markdown("<p style='color: #cbd5e1; font-weight: bold;'>PRÊT POUR LE TIRAGE</p>", unsafe_allow_html=True)
                
                if len(st.session_state.participants) >= 2:
                    if st.button("🎯 LANCER LE TIRAGE"):
                        # Animation de tirage
                        for i in range(25):
                            temp_name = random.choice(st.session_state.participants)
                            display_area.markdown(f"<h2 style='color: #4f46e5; font-size: 3rem; font-weight: 900;'>{temp_name}</h2>", unsafe_allow_html=True)
                            time.sleep(0.1)
                        
                        st.session_state.winner = random.choice(st.session_state.participants)
                        st.rerun()
                else:
                    st.info("Ajoutez au moins 2 participants à gauche.")

        else:
            # Affichage du Gagnant (Résultat Final)
            with display_area.container():
                st.markdown("<h3>🎊 FÉLICITATIONS 🎊</h3>", unsafe_allow_html=True)
                st.markdown(f"<div class='winner-text'>{st.session_state.winner}</div>", unsafe_allow_html=True)
                
                # Carte du lot
                st.markdown("<p style='color: #94a3b8; font-size: 0.7rem; font-weight: 900;'>A REMPORTÉ</p>", unsafe_allow_html=True)
                
                # Construction d'un layout HTML pour le lot
                img_html = ""
                if uploaded_image:
                    # Conversion de l'image pour affichage HTML
                    img_data = uploaded_image.getvalue()
                    b64_img = base64.b64encode(img_data).decode()
                    img_html = f'<img src="data:image/png;base64,{b64_img}" style="width: 80px; height: 80px; border-radius: 10px; object-fit: cover;">'
                
                st.markdown(f"""
                    <div class="lot-card">
                        {img_html}
                        <div style="text-align: left;">
                            <p style="margin: 0; font-weight: 900; font-size: 1.2rem; color: #1e293b;">{lot_name}</p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button("🔄 REFAIRE UN TIRAGE"):
                    st.session_state.winner = None
                    st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

# Footer info
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.8rem; margin-top: 20px;'>Cadrez votre enregistreur d'écran sur la zone blanche centrale pour un rendu optimal.</p>", unsafe_allow_html=True)
