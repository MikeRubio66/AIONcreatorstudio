import streamlit as st
import requests
from PIL import Image
import base64
import io

# URL del proxy
PROXY_URL = "https://aioncreatorstudioproxy-1.onrender.com"

st.set_page_config(page_title="AION Creator Studio", layout="centered")

st.title("AION Creator Studio")
st.write("Generación de texto e imágenes para creadores de contenido y pymes.")


# FORMULARIO DE TEXTO
st.subheader("Generador de descripciones")

business = st.text_input("Tipo de negocio", "Restaurante")
tone = st.text_input("Tono", "Informal y amigable")
keywords = st.text_input("Palabras clave", "mexicana, tacos, enchiladas")
length = st.number_input("Longitud (líneas)", 2, 10, 3)

if st.button("Generar Texto"):
    payload = {
        "business": business,
        "tone": tone,
        "keywords": keywords,
        "length": length
    }

    res = requests.post(f"{PROXY_URL}/text", json=payload)

    st.write("### Resultado:")
    st.write(res.json())


# GENERADOR DE IMÁGENES
st.subheader("Generador de imágenes")

prompt_img = st.text_input("Prompt para imagen", "Mexican food illustration")

if st.button("Generar Imagen"):
    payload = {"prompt": prompt_img}

    res = requests.post(f"{PROXY_URL}/image", json=payload)
    data = res.json()

    if "image_base64" in data:
        decoded = base64.b64decode(data["image_base64"])
        img = Image.open(io.BytesIO(decoded))
        st.image(img)
    else:
        st.error(data)
