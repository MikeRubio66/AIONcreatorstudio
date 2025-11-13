
import streamlit as st
from generator import generate_text_online, generate_image_online, generate_text_offline, generate_image_offline
from PIL import Image
import io, os, random

st.set_page_config(page_title="AION Creator Studio", layout="centered")
st.markdown("<h1 style='text-align:center'>AION Creator Studio</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:gray;margin-top:-10px;'>Generador rápido de imagen + texto para redes sociales (demo)</p>", unsafe_allow_html=True)

mode = st.sidebar.selectbox("Modo", ["Online (Hugging Face)", "Offline (Demo)"])
st.sidebar.markdown("---")
st.sidebar.markdown("AION Digital Agency · IA aplicada a contenidos")

with st.form("form_inputs"):
    business = st.selectbox("Tipo de negocio", ["Tienda", "Restaurante", "Marca personal", "Servicios", "Educación", "Salud", "Otro"])
    tone = st.selectbox("Tono", ["Informal", "Moderno", "Emocional", "Profesional", "Minimalista"])
    keywords = st.text_input("Palabras clave (separadas por comas)", "")
    length = st.slider("Longitud del texto (frases)", 1, 4, 2)
    submitted = st.form_submit_button("Generar")

if submitted:
    if mode.startswith("Online"):
        hf_token = st.sidebar.text_input("Hugging Face API Key", type="password")
        if not hf_token:
            st.error("Necesitas proporcionar tu Hugging Face API Key en la barra lateral para el modo Online.")
        else:
            with st.spinner("Generando texto..."):
                text = generate_text_online(hf_token, business, tone, keywords, length)
            st.success("Texto generado")
            st.markdown("**Descripción sugerida:**")
            st.write(text)
            with st.spinner("Generando imagen..."):
                img_bytes = generate_image_online(hf_token, business, tone, keywords)
            if img_bytes:
                image = Image.open(io.BytesIO(img_bytes))
                st.image(image, caption="Imagen sugerida", use_column_width=True)
                buf = io.BytesIO()
                image.save(buf, format="PNG")
                st.download_button("Descargar imagen (PNG)", data=buf.getvalue(), file_name="aion_image.png", mime="image/png")
            else:
                st.warning("No se pudo generar la imagen (comprueba la clave o el modelo de HF).")
    else:
        # Offline demo
        text = generate_text_offline(business, tone, keywords, length)
        st.markdown("**Descripción sugerida (modo demo):**")
        st.write(text)
        img = generate_image_offline(business, tone)
        st.image(img, caption="Imagen demo", use_column_width=True)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        st.download_button("Descargar imagen (PNG)", data=buf.getvalue(), file_name="aion_demo_image.png", mime="image/png")

st.markdown("<div style='position:fixed;bottom:8px;width:100%;text-align:center;color:#999;font-size:12px;'>AION Digital Agency · IA aplicada · Miguel Álvarez</div>", unsafe_allow_html=True)
