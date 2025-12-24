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
        width: 100%;
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
        line-height: 1.1;
        word-break: break-word;
    }

    .lot-card {
        display: inline-flex;
        align-items: center;
        gap: 20px;
        background: #f8fafc;
        padding: 15px 25px;
        border-radius: 1.25rem;
        border: 2px solid #f1f5f9;
        margin-top: 30px;
        text-align: left;
    }
    
    .lot-img {
        width: 80px;
        height: 80px;
        border-radius: 12px;
        object-fit: cover;
        box-shadow: 0 2px 4px rgb(0 0 0 / 0.1);
    }

    .status-badge {
        background:#f1f5f9; 
        padding:5px 15px; 
        border-radius:20px; 
        font-size:0.7rem; 
        font-weight:800; 
        color:#64748b;
        margin-bottom: 20px;
        display: inline-block;
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
            text_area = st.text_area("Saisissez les noms (un par ligne)", height=100)
            if st.button("Valider"):
                st.session_state.participants = [n.strip() for n in text_area.split('\n') if n.strip()]
        elif source == "Fichier":
            file = st.file_uploader("CSV/TXT", type=["csv", "txt"])
            if file:
                st.session_state.participants = [n.strip() for n in file.read().decode().split('\n') if n.strip()]
        else:
            if st.button("Simuler Instagram"):
                st.session_state.participants = ["@user1", "@user2", "@user3", "@user4", "@user5", "@lucky_dev", "@stream_fan"]

        if st.session_state.participants:
            st.success(f"{len(st.session_state.participants)} participants chargés")
            if st.button("Reset", type="secondary"):
                st.session_state.participants = []
                st.session_state.winner = None
                st.rerun()

with col_canvas:
    # Préparation de l'image
    b64_img = ""
    if uploaded_image:
        b64_img = base64.b64encode(uploaded_image.getvalue()).decode()

    # Zone de capture
    capture_placeholder = st.empty()

    if not st.session_state.winner:
        with capture_placeholder.container():
            # Tout le HTML est contenu dans un seul bloc markdown pour éviter les bugs de balises
            content_html = f"""
            <div class="capture-container">
                <div class="status-badge">CONCOURS : {lot_name.upper()}</div>
                <div style="margin-bottom: 20px;">
                    {f'<img src="data:image/png;base64,{b64_img}" style="width:140px; height:140px; border-radius:30px; object-fit:cover; border:5px solid #f8fafc; box-shadow:0 10px 15px rgba(0,0,0,0.1);">' if b64_img else '<h1 style="font-size:4rem;">🎁</h1>'}
                </div>
                <p style='color:#cbd5e1; font-weight:800; letter-spacing:0.1em; margin-bottom: 30px;'>PRÊT POUR LE TIRAGE</p>
            </div>
            """
            st.markdown(content_html, unsafe_allow_html=True)
            
            # Le bouton est placé juste en dessous de la zone blanche pour ne pas polluer la capture
            if len(st.session_state.participants) >= 2:
                if st.button("🎯 LANCER LE TIRAGE AU SORT"):
                    # Animation
                    for _ in range(25):
                        temp_name = random.choice(st.session_state.participants)
                        capture_placeholder.markdown(f"""
                            <div class="capture-container">
                                <div class="status-badge">TIRAGE EN COURS...</div>
                                <div style='height:100px;'></div>
                                <div class="winner-name" style="color:#4f46e5;">{temp_name}</div>
                                <div style='height:100px;'></div>
                            </div>
                        """, unsafe_allow_html=True)
                        time.sleep(0.08)
                    
                    st.session_state.winner = random.choice(st.session_state.participants)
                    st.rerun()
            else:
                st.info("Veuillez ajouter au moins 2 participants pour commencer.")

    else:
        # Affichage du Résultat Final dans un seul bloc HTML propre
        img_tag = f'<img src="data:image/png;base64,{b64_img}" class="lot-img">' if b64_img else ""
        
        result_html = f"""
        <div class="capture-container">
            <div class="status-badge">CONCOURS : {lot_name.upper()}</div>
            <p class="winner-label">Le gagnant est</p>
            <div class="winner-name">{st.session_state.winner}</div>
            
            <div class="lot-card">
                {img_tag}
                <div>
                    <p style="font-size:0.65rem; font-weight:900; color:#64748b; text-transform:uppercase; margin:0;">Prix remporté</p>
                    <p style="font-size:1.2rem; font-weight:800; color:#334155; margin:0;">{lot_name}</p>
                </div>
            </div>
        </div>
        """
        st.markdown(result_html, unsafe_allow_html=True)
        
        # Bouton recommencer à l'extérieur de la zone blanche
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        if st.button("🔄 REFAIRE UN TIRAGE", type="secondary"):
            st.session_state.winner = None
            st.rerun()

st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.75rem; margin-top: 30px; font-weight: 600;'>ASTUCE : Cadrez votre logiciel de capture uniquement sur la zone blanche.</p>", unsafe_allow_html=True)
