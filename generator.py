
import requests, os, io, random
from PIL import Image, ImageDraw, ImageFont

TEXT_MODEL = "gpt2"
IMAGE_MODEL = "stabilityai/stable-diffusion-2"

def hf_inference(model, token, payload, timeout=60):
    url = f"https://api-inference.huggingface.co/models/{model}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(url, headers=headers, json=payload, timeout=timeout)
    if response.status_code == 200:
        return response.content, None
    else:
        try:
            return None, response.json()
        except:
            return None, {"error": "Unknown error"}

def generate_text_online(token, business, tone, keywords, length):
    prompt = f"Genera una breve descripción para redes sociales para un negocio tipo: {business}. Tono: {tone}. Palabras clave: {keywords}. Longitud: {length} frases."
    payload = {"inputs": prompt, "options": {"wait_for_model": True}}
    content, err = hf_inference(TEXT_MODEL, token, payload)
    if content:
        try:
            text = content.decode("utf-8")
            return text.strip()
        except:
            return "Texto generado (no decodificable)."
    else:
        return f"Error generando texto: {err}"

def generate_image_online(token, business, tone, keywords):
    prompt = f"Imagen para {business} en estilo {tone}. Incluye elementos relacionados con: {keywords}"
    payload = {"inputs": prompt, "options": {"wait_for_model": True}}
    content, err = hf_inference(IMAGE_MODEL, token, payload, timeout=120)
    if content:
        return content
    else:
        return None

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
TEMPLATES = {
    "Tienda": [
        "Compra hoy: productos seleccionados con descuento. {keywords}",
        "Descubre lo mejor en nuestra tienda: calidad y servicio. {keywords}"
    ],
    "Restaurante": [
        "Prueba nuestro menú especial hoy. {keywords}",
        "Sabores auténticos que te enamoran. {keywords}"
    ],
    "Marca personal": [
        "Construyendo mi marca con pasión y constancia. {keywords}",
        "Detrás de cada proyecto, una historia auténtica. {keywords}"
    ],
    "Servicios": [
        "Servicios profesionales con resultados garantizados. {keywords}",
        "Tu solución confiable en {keywords}."
    ],
    "Educación": [
        "Aprende con nosotros: cursos prácticos y aplicables. {keywords}",
        "Formación que impulsa tu carrera. {keywords}"
    ],
    "Salud": [
        "Cuidamos lo más importante: tu salud y bienestar. {keywords}",
        "Compromiso con tu bienestar día a día. {keywords}"
    ],
    "Otro": [
        "Descubre lo que tenemos para ti. {keywords}",
        "Lo que buscas, lo encuentras aquí. {keywords}"
    ]
}

def generate_text_offline(business, tone, keywords, length):
    templates = TEMPLATES.get(business, TEMPLATES["Otro"])
    result = []
    for i in range(length):
        template = random.choice(templates)
        result.append(template.format(keywords=keywords or ""))
    return " ".join(result)

def generate_image_offline(business, tone):
    files = [f for f in os.listdir(ASSETS_DIR) if f.lower().endswith((".png",".jpg",".jpeg"))]
    if not files:
        img = Image.new("RGB", (800,500), color=(230,230,230))
        d = ImageDraw.Draw(img)
        d.text((50,200), f"Imagen demo - {business}", fill=(80,80,80))
        return img
    choice = random.choice(files[:6])
    img_path = os.path.join(ASSETS_DIR, choice)
    img = Image.open(img_path)
    return img
