import streamlit as st
from PIL import Image
import requests
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import os

# 📌 Configuración inicial de la página
st.set_page_config(page_title="Informe de Actuación - Ismael Ruesca Godino", layout="wide")

# 📌 Estilos CSS personalizados para mejorar el diseño
st.markdown("""
    <style>
        .center-text { text-align: center; }
        .st-emotion-cache-1wivapg { justify-content: center; } /* Centrar imágenes */
        hr { border: 1px solid #ddd; margin-top: 10px; margin-bottom: 10px; }
        .stImage { display: flex; justify-content: center; }
        .title { font-size: 30px; font-weight: bold; text-align: center; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# 📌 CABECERA CON IMAGEN DEL JUGADOR Y TÍTULO
st.markdown("<h1 class='title'>📊 Informe de Actuación – Ismael Ruesca Godino</h1>", unsafe_allow_html=True)

col_img, col_title = st.columns([1, 3])
with col_img:
    if os.path.exists("data/img/granadavsmarbella.jpg"):
        jugador_img = Image.open("data/img/granadavsmarbella.jpg")
        st.image(jugador_img, width=250)

# 📌 DISTRIBUCIÓN DE LOGOS, PARTIDO Y RESULTADO
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    granada_logo_url = "https://cdn.resfu.com/img_data/equipos/4235.png?size=120x&lossy=1"
    granada_logo = Image.open(requests.get(granada_logo_url, stream=True).raw)
    st.image(granada_logo, width=120)

with col2:
    st.markdown("<h2 class='center-text'>Granada CF 🆚 Atlético Marbella Paraíso</h2>", unsafe_allow_html=True)
    st.markdown("<h3 class='center-text'>🔴 1 - 1 🔵</h3>", unsafe_allow_html=True)

with col3:
    atletico_logo_url = "https://cdn.resfu.com/img_data/escudos/medium/160991.jpg?size=120x&lossy=1"
    atletico_logo = Image.open(requests.get(atletico_logo_url, stream=True).raw)
    st.image(atletico_logo, width=120)

# 📌 SEPARADOR VISUAL
st.markdown("<hr>", unsafe_allow_html=True)

# 📌 SECCIÓN PRINCIPAL: INFORME Y POSICIONAMIENTO
col_text, col_right = st.columns([2, 1])  # Alineamos el campo de juego a la derecha

with col_text:
    st.markdown("## 📝 Informe de partido")
    st.markdown("""
### 📌 **Comentario sobre la actuación del jugador Ismael Ruesca**
En líneas generales, el conjunto visitante mostró un planteamiento táctico y físico muy trabajado, destacando en todo momento la excepcional actitud del plantel. Especialmente, el rendimiento de Ismael brilló en este choque contra un rival de gran trayectoria, el Granada CF.

Desplegado en un sistema 3-5-2, Ismael desempeñó con eficacia el rol de pivote defensivo en doble pivote, aportando el equilibrio necesario y una solidez que frustró las intenciones ofensivas del rival en el primer tiempo. Su lectura táctica se hizo evidente al mantener una línea compacta y ofrecer siempre opciones seguras en los pases cortos, evitando la pérdida de balón y permitiendo a Atlético Marbella lanzar contragolpes decisivos que se tradujeron en una ventaja temprana.

Además, realizó dos desplazamientos explosivos hacia la zona de ataque, contribuyendo significativamente a la generación de contraataques rápidos, mientras mantenía un elevado ritmo de trabajo físico, participando en el 90% del partido y siendo sustituido únicamente en los últimos 10 minutos. Su capacidad para detener el juego y conectar las jugadas fue crucial, consolidándose como un eje de contención y orden en el equipo.

Aunque es reconocido por sus compañeros como un líder en el terreno de juego, el aspecto del liderazgo es una faceta que aún puede perfeccionar. En definitiva, se trata de un jugador tácticamente inteligente y físicamente incansable, con claras cualidades defensivas y una notable capacidad para construir juego; potenciando su liderazgo, podrá alcanzar un rendimiento óptimo en partidos de alta exigencia.
    """)

    st.markdown("### 📍 Posicionamiento y Rol Táctico")
    st.markdown("""
    - **Formación y Distribución:**  
      Alineación 3-5-2 con tres centrales, dos carrileros y dos mediocampistas.  
    - **Rol de Ismael:**  
      Como pivote defensivo, mantuvo el equilibrio y controló la transición defensiva.
    """)

    st.markdown("### 🛠️ Aspectos Técnicos")
    st.markdown("""
    - **Manejo del Balón:**  
      Seguridad en la posesión, buen criterio en la toma de decisiones.  
    - **Puntos a Mejorar:**  
      Se recomienda mejorar la velocidad en la toma de decisiones.
    """)

    st.markdown("### 💪 Duelo y Recuperación")
    st.markdown("""
    - **Intervención en Cortes:**  
      Efectivo en recuperación de balón.  
    - **Observación:**  
      Se espera más presencia en duelos aéreos.
    """)

    st.markdown("### 🏃 Desempeño Físico")
    st.markdown("""
    - **Resistencia:**  
      Jugó casi todo el partido con gran despliegue.  
    - **Velocidad:**  
      Se recomienda trabajar en la rapidez para potenciar su salida al contraataque.
    """)

with col_right:
    # 📌 Mapa de Posicionamiento en el Campo
    st.markdown("### ⚽ Posicionamiento en el Campo")
    
    pitch = Pitch(pitch_color='#aabb97', line_color='white', stripe=True)
    fig, ax = plt.subplots(figsize=(6, 4))  # Tamaño más pequeño
    pitch.draw(ax=ax)

    # 📌 Posición del jugador en el campo
    player_x, player_y = 40, 40
    ax.scatter(player_x, player_y, s=600, color='black', edgecolors='black', zorder=5)
 

    st.pyplot(fig)

    

# 📌 SEPARADOR FINAL
st.markdown("<hr>", unsafe_allow_html=True)
