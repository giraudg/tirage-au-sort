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
        box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1);
    }
    /* Zone de capture optimisée */
    .capture-zone {
        background-color: white;
        border-radius: 2.5rem;
        padding: 60px 40px;
        box-shadow: 0 25px 50px -12px rgb(0 0 0 / 0.15);
        border: 1px solid #e2e8f0;
        text-align: center;
        min-height: 550px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        position: relative;
    }
    .winner-label {
        color: #94a3b8;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.2em;
        font-size: 0.75rem;
        margin-bottom: 10px;
    }
    .winner-text {
        color: #1e1b4b;
        font-size: 5rem;
        font-weight: 900;
        margin: 10px 0 30px 0;
        text-transform: uppercase;
        letter-spacing: -0.02em;
        line-height: 1;
    }
    /* Carte du lot améliorée */
    .lot-card-container {
        display: flex;
        justify-content: center;
        width: 100%;
        margin-top: 20px;
    }
    .lot-card {
        display: flex;
        align-items: center;
        gap: 20px;
        background: #f8fafc;
        padding: 15px 25px;
        border-radius: 1.25rem;
        border: 2px solid #f1f5f9;
        max-width: 450px;
        width: fit-content;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05);
    }
    .lot-image-preview {
        width: 80px;
        height: 80px;
        border-radius: 12px;
        object-fit: cover;
        border: 3px solid white;
        box-shadow: 0 2px 4px rgb(0 0 0 / 0.1);
    }
    .lot-info-text {
        text-align: left;
    }
    .lot-info-label {
        font-size: 0.65rem;
        font-weight: 900;
        color: #64748b;
        text-transform: uppercase;
        margin: 0;
    }
    .lot-info-name {
        font-size: 1.25rem;
        font-weight: 800;
        color: #334155;
        margin: 0;
        line-height: 1.2;
    }
    /* Style pour le texte d'attente */
    .waiting-text {
        font-size: 1rem;
        font-weight: 700;
        color: #cbd5e1;
        letter-spacing: 0.1em;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Initialisation du State ---
if 'participants' not in st.session_state:
    st.session_state.participants = []
if 'winner' not in st.session_state:
    st.session_state.winner = None

# --- Header ---
st.markdown("<div style='padding: 20px 0;'><h1 style='text-align: center; color: #4f46e5; font-weight: 900; margin-bottom: 0;'>🏆 GIVEAWAY MASTER</h1></div>", unsafe_allow_html=True)

# --- Layout ---
col_config, col_canvas = st.columns([1, 1.8], gap="large")

with col_config:
    st.markdown("### 🛠️ Configuration")
    with st.container(border=True):
        lot_name = st.text_input("Nom du cadeau", value="Bon d'achat de 100€")
        uploaded_image = st.file_uploader("Image du lot", type=["png", "jpg", "jpeg"])
        
        if uploaded_image:
            st.image(uploaded_image, width=100)

    st.markdown("### 👥 Participants")
    with st.container(border=True):
        source = st.radio("Source d'import", ["Manuel", "Fichier", "Instagram"], horizontal=True)
        
        if source == "Manuel":
            text_area = st.text_area("Saisissez les noms (un par ligne)", height=150)
            if st.button("Valider la liste"):
                st.session_state.participants = [n.strip() for n in text_area.split('\n') if n.strip()]
                
        elif source == "Fichier":
            file = st.file_uploader("Fichier CSV ou TXT", type=["csv", "txt"])
            if file:
                content = file.read().decode("utf-8")
                st.session_state.participants = [n.strip() for n in content.split('\n') if n.strip()]

        else:
            insta_url = st.text_input("Lien Instagram")
            if st.button("Importer les commentaires"):
                st.session_state.participants = ["@user_alpha", "@insta_fan", "@contest_lover", "@lucky_star", "@winner_today"]

        if st.session_state.participants:
            st.success(f"✅ {len(st.session_state.participants)} participants chargés")
            if st.button("Réinitialiser tout", type="secondary"):
                st.session_state.participants = []
                st.session_state.winner = None
                st.rerun()

with col_canvas:
    # Conteneur principal pour la capture d'écran
    st.markdown('<div class="capture-zone">', unsafe_allow_html=True)
    
    # Titre discret du concours
    st.markdown(f"""
        <div style='position: absolute; top: 30px; width: 100%; text-align: center;'>
            <span style='background: #f1f5f9; padding: 5px 15px; border-radius: 20px; color: #64748b; font-weight: 800; font-size: 0.7rem; letter-spacing: 0.1em;'>
                CONCOURS : {lot_name.upper()}
            </span>
        </div>
    """, unsafe_allow_html=True)
    
    display_area = st.empty()
    
    if not st.session_state.winner:
        with display_area.container():
            # Espace flex pour centrer verticalement
            st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
            
            if uploaded_image:
                # Preview circulaire/arrondie du lot au centre pendant l'attente
                img_data = uploaded_image.getvalue()
                b64_img = base64.b64encode(img_data).decode()
                st.markdown(f"""
                    <div style='display: flex; justify-content: center; margin-bottom: 20px;'>
                        <img src="data:image/png;base64,{b64_img}" style="width: 140px; height: 140px; border-radius: 30px; object-fit: cover; border: 5px solid #f8fafc; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);">
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("<h1 style='font-size: 4rem; margin-bottom: 20px;'>🎁</h1>", unsafe_allow_html=True)
            
            st.markdown("<p class='waiting-text'>PRÊT POUR LE TIRAGE</p>", unsafe_allow_html=True)
            
            # Bouton de lancement
            st.markdown("<div style='width: 300px; margin: 30px auto;'>", unsafe_allow_html=True)
            if len(st.session_state.participants) >= 2:
                if st.button("🎯 LANCER LE TIRAGE"):
                    # Animation
                    for i in range(20):
                        temp_name = random.choice(st.session_state.participants)
                        display_area.markdown(f"""
                            <div style='height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center;'>
                                <div style='height: 140px;'></div>
                                <h2 style='color: #4f46e5; font-size: 4rem; font-weight: 900; text-transform: uppercase;'>{temp_name}</h2>
                                <div style='height: 100px;'></div>
                            </div>
                        """, unsafe_allow_html=True)
                        time.sleep(0.08)
                    
                    st.session_state.winner = random.choice(st.session_state.participants)
                    st.rerun()
            else:
                st.warning("Ajoutez au moins 2 participants.")
            st.markdown("</div>", unsafe_allow_html=True)

    else:
        # Affichage du Résultat Final
        with display_area.container():
            st.markdown("<p class='winner-label'>Le gagnant est</p>", unsafe_allow_html=True)
            st.markdown(f"<div class='winner-text'>{st.session_state.winner}</div>", unsafe_allow_html=True)
            
            # Carte du lot stylisée
            img_html = ""
            if uploaded_image:
                img_data = uploaded_image.getvalue()
                b64_img = base64.b64encode(img_data).decode()
                img_html = f'<img src="data:image/png;base64,{b64_img}" class="lot-image-preview">'
            
            st.markdown(f"""
                <div class="lot-card-container">
                    <div class="lot-card">
                        {img_html}
                        <div class="lot-info-text">
                            <p class="lot-info-label">Prix remporté</p>
                            <p class="lot-info-name">{lot_name}</p>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Bouton pour recommencer discret sous la zone
            st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
            if st.button("🔄 NOUVEAU TIRAGE", type="secondary"):
                st.session_state.winner = None
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# Footer info
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.75rem; margin-top: 30px; font-weight: 600;'>ASTUCE : Cadrez votre logiciel de capture sur le rectangle blanc central.</p>", unsafe_allow_html=True)
