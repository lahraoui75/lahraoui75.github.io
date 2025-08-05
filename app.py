import streamlit as st
import pandas as pd
import os

# Charger les données utilisateurs
USERS_FILE = 'users.csv'
users_df = pd.read_csv(USERS_FILE)

# Initialiser session_state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None

# Fonction de vérification des identifiants
def authenticate(username, password):
    user = users_df[users_df['name'] == username]
    if not user.empty:
        if user.iloc[0]['password'] == password:
            return True
    return False

# Fonction de déconnexion
def logout():
    st.session_state.authenticated = False
    st.session_state.username = None
    st.experimental_rerun()

# Interface d'authentification
def login_page():
    st.title("Connexion")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        if authenticate(username, password):
            st.session_state.authenticated = True
            st.session_state.username = username
            st.success("Connexion réussie.")
            st.experimental_rerun()
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect.")

# Interface de la page d'accueil
def home_page():
    st.title("Page d'accueil")
    st.write("Bienvenue sur l'application Streamlit avec authentification !")

# Interface de l'album photo
def photo_album_page():
    st.title("Album Photo 🐱")
    image_dir = "images"
    image_files = [f for f in os.listdir(image_dir) if f.lower().endswith((".jpg", ".png", ".jpeg"))]
    for i in range(0, len(image_files), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(image_files):
                img_path = os.path.join(image_dir, image_files[i + j])
                with cols[j]:
                    st.image(img_path, use_column_width=True)

# Menu latéral et navigation
def main_app():
    st.sidebar.markdown(f"👋 Bienvenue **{st.session_state.username}**")
    page = st.sidebar.selectbox("Menu", ["Accueil", "Album Photo", "Déconnexion"])

    if page == "Accueil":
        home_page()
    elif page == "Album Photo":
        photo_album_page()
    elif page == "Déconnexion":
        logout()

# Affichage conditionnel
if not st.session_state.authenticated:
    login_page()
else:
    main_app()
