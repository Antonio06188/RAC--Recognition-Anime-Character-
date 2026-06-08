import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO

def decode_img(b64_str):
    img_bytes = base64.b64decode(b64_str)
    return Image.open(BytesIO(img_bytes))

API_URL = "http://localhost:8000/predict-test"
if not ("analyzed" in st.session_state):
    st.session_state["analyzed"] = False

# Upload file
st.title("Anime Character Recognition")

uploaded_file = st.file_uploader(
    "Choisir une image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    if not ("result" in st.session_state):
        st.image(uploaded_file, use_container_width=True)

        if st.button("Analyser"):
            # Run Analyze
            st.session_state["analyzed"] = True

            files = {
                "file": uploaded_file.getvalue()
            }

            response = requests.post(
                API_URL,
                files={
                    "file": (
                        uploaded_file.name,
                        uploaded_file,
                        uploaded_file.type
                    )
                }
            )

            st.session_state["result"] = response.json()
            st.rerun()

# Show the original image with box
    if "result" in st.session_state and st.session_state.get("step", 1) < 2:

        result = st.session_state["result"]

        st.subheader("Détection")

        st.image(
            decode_img(result["box_img"]),
            use_container_width=True
        )

        if st.button("Voir personnage"):
            st.session_state["step"] = 2
            st.rerun()
    
    # Show crop image used for classification        
    if st.session_state.get("step", 1) == 2:
        
        result = st.session_state["result"]

        st.subheader("Personnage détecté")

        st.image(
            decode_img(result["crop_img"]),
            use_container_width=True
        )

        if st.button("Voir référence"):
            st.session_state["step"] = 3
            st.rerun()
    
    # Result of the classification
    if st.session_state.get("step", 1) == 3:
        
        result = st.session_state["result"]

        st.subheader(result["character_name"])

        st.image(
            decode_img(result["character_ref_img"]),
            use_container_width=True
        )

        if st.button("Voir animé"):
            st.session_state["step"] = 4
            st.rerun()
    
    # Show Anime informations  
    if st.session_state.get("step", 1) == 4:
        
        result = st.session_state["result"]

        st.subheader(result["anime_name"])
        
        st.image(
            decode_img(result["anime_ref_img"]),
            use_container_width=True
        )

        if st.button("Voir opening"):
            st.session_state["step"] = 5
            st.rerun()
    
    if st.session_state.get("step", 1) == 5:
        
        result = st.session_state["result"]
        
        st.subheader(result["anime_name"])

        if "opening_index" not in st.session_state:
            st.session_state["opening_index"] = 0

        idx = st.session_state["opening_index"]

        opening = result["openings"][idx]
        
        num = opening["op_number"]
        name = opening["op_name"]
        artist = opening["op_artist"]

        st.write(f"Opening {num} : {name} de {artist}")

        st.video(opening["youtube_url"])
        
        col1, col2 = st.columns(2)

        with col1:
            if st.button("◀ Précédent"):

                st.session_state["opening_index"] = (
                    st.session_state["opening_index"] - 1
                ) % len(result["openings"])
                st.rerun()

        with col2:
            if st.button("Suivant ▶"):

                st.session_state["opening_index"] = (
                    st.session_state["opening_index"] + 1
                ) % len(result["openings"])
                st.rerun()

# Rerun button
if st.session_state["analyzed"] :              
    with st.sidebar:

        st.title("Anime Character Finder")

        if st.button("🆕 Nouvelle analyse"):

            st.session_state.clear()
            st.rerun()