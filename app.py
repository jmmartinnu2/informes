import streamlit as st
import json
import matplotlib.pyplot as plt
from mplsoccer import Pitch

# Configurar la página para ocupar todo el ancho
st.set_page_config(page_title="Informe de Jugadores", layout="wide")

# Cargar el JSON desde el fichero en la raíz del proyecto
try:
    with open("informe_jugadores.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        if "informe_jugadores" not in data or not data["informe_jugadores"]:
            st.error("⚠️ No se encontraron jugadores en el JSON.")
            st.stop()
except Exception as e:
    st.error(f"⚠️ Error al cargar el JSON: {e}")
    st.stop()

# Extraer nombres de los jugadores para el sidebar
jugadores = [jugador["nombre"] for jugador in data["informe_jugadores"]]

# Sidebar para seleccionar el jugador
st.sidebar.title("🎯 Selecciona un Jugador")
jugador_seleccionado = st.sidebar.selectbox("Elige un jugador:", jugadores)

# Buscar los datos del jugador seleccionado
jugador = next(j for j in data["informe_jugadores"] if j["nombre"] == jugador_seleccionado)

# Obtener posición en el campo
pos_x, pos_y = jugador["posicion_campo"]["x"], jugador["posicion_campo"]["y"]

# Verificar si el jugador tiene información de partido2
if "partido2" in jugador:
    tabs = st.tabs(["📊 Informe", "⚽ Partido 2", "🎥 Videos"])
    tab_informe, tab_partido2, tab_videos = tabs
else:
    tabs = st.tabs(["📊 Informe", "🎥 Videos"])
    tab_informe, tab_videos = tabs

# 📊 TAB: Informe del Jugador + Posición en el Campo
with tab_informe:
    st.title(f"📊 Informe de {jugador['nombre']}")
    st.subheader(f"{jugador['equipo']} - {jugador['categoria']}")
    st.markdown(f"⭐ **Valoración:** {jugador['valoracion']} / 5")

    # Crear columnas: info a la izquierda, campo a la derecha
    col1, col2 = st.columns([2, 1])

    with col1:
        # Mostrar información del partido
        st.markdown(f"### 🏆 Partido contra {jugador['partido']['rival']}")
        resultado = jugador["partido"]["resultado"]
        resultado_texto = " - ".join([f"{k.replace('_', ' ')} {v}" for k, v in resultado.items()])
        st.markdown(f"**Resultado:** {resultado_texto}")

        # Mostrar el informe completo
        st.markdown("### 📌 Análisis del Rendimiento")
        st.markdown(f"📝 **Comentario:** {jugador['informe']['comentario']}")

        with st.expander("🎯 Actuación en el Partido"):
            actuacion = jugador["informe"]["actuacion"]
            st.markdown(f"- **Sistema de Juego:** {actuacion['sistema_juego']}")
            st.markdown(f"- **Rol:** {actuacion['rol']}")
            st.markdown(f"- **Rendimiento:** {actuacion['desempeno']}")
            st.markdown(f"- **Participación:** {actuacion['participacion']}")
            st.markdown(f"- **Liderazgo:** {actuacion['liderazgo']}")

        with st.expander("🎯 Posicionamiento Táctico"):
            tactico = jugador["informe"]["posicionamiento_tactico"]
            st.markdown(f"- **Formación:** {tactico['formacion']}")
            st.markdown(f"- **Rol:** {tactico['rol']}")

        with st.expander("🎯 Aspectos Técnicos"):
            tecnica = jugador["informe"]["aspectos_tecnicos"]
            st.markdown(f"- **Manejo de balón:** {tecnica['manejo_balon']}")
            st.markdown(f"- **Puntos a mejorar:** {tecnica['puntos_mejorar']}")

        with st.expander("🎯 Duelos y Recuperación"):
            duelos = jugador["informe"]["duelo_recuperacion"]
            st.markdown(f"- **Intervención y cortes:** {duelos['intervencion_cortes']}")
            st.markdown(f"- **Observación:** {duelos['observacion']}")

        with st.expander("🎯 Rendimiento Físico"):
            fisico = jugador["informe"]["desempeno_fisico"]
            st.markdown(f"- **Resistencia:** {fisico['resistencia']}")
            st.markdown(f"- **Velocidad:** {fisico['velocidad']}")

        with st.expander("🎯 Orden Táctico"):  
            if "orden_tactico" in jugador["informe"]:
                tactico = jugador["informe"]["orden_tactico"]
                st.markdown(f"- **Táctico:** {tactico['tactico']}")
                st.markdown(f"- **Concentración:** {tactico['concentracion']}")
            else:
                st.markdown("⚠️ No hay información sobre el orden táctico.")

    # 📌 Columna derecha: Posición en el Campo
    with col2:
        st.markdown("### ⚽ Posición en el Campo")
        fig, ax = plt.subplots(figsize=(8, 7))
        pitch = Pitch(pitch_type='statsbomb', pitch_color='grass', line_color='white')
        pitch.draw(ax=ax)

        # Añadir la posición del jugador en el campo
        ax.scatter(pos_x, pos_y, color="black", s=600, label=jugador["nombre"])
        ax.text(pos_x, pos_y + 3, jugador["nombre"], fontsize=12, ha="center", color="white")

        # Mostrar el gráfico en Streamlit
        st.pyplot(fig)

# ⚽ TAB: Partido 2 (solo se muestra si existe la información en el JSON)
if "partido2" in jugador:
    with tab_partido2:
        partido2 = jugador["partido2"]
        st.title(f"⚽ Informe - {partido2.get('fecha', '')}")
        st.markdown(f"### Rival: {partido2.get('rival', 'Desconocido')}")
        resultado2 = partido2.get("resultado", {})
        if resultado2:
            resultado_texto2 = " - ".join([f"{k.replace('_', ' ')} {v}" for k, v in resultado2.items()])
            st.markdown(f"**Resultado:** {resultado_texto2}")
        st.markdown("### 📌 Análisis del Rendimiento - Partido 2")
        informe2 = partido2.get("informe", {})
        if informe2:
            st.markdown(f"📝 **Comentario:** {informe2.get('comentario', '')}")
            with st.expander("🎯 Actuación en el Partido"):
                actuacion2 = informe2.get("actuacion", {})
                st.markdown(f"- **Sistema de Juego:** {actuacion2.get('sistema_juego', '')}")
                st.markdown(f"- **Rol:** {actuacion2.get('rol', '')}")
                st.markdown(f"- **Rendimiento:** {actuacion2.get('desempeno', '')}")
                st.markdown(f"- **Participación:** {actuacion2.get('participacion', '')}")
                st.markdown(f"- **Liderazgo:** {actuacion2.get('liderazgo', '')}")
            with st.expander("🎯 Posicionamiento Táctico"):
                pos_tactico2 = informe2.get("posicionamiento_tactico", {})
                st.markdown(f"- **Formación:** {pos_tactico2.get('formacion', '')}")
                st.markdown(f"- **Rol:** {pos_tactico2.get('rol', '')}")
            with st.expander("🎯 Aspectos Técnicos"):
                tecnicos2 = informe2.get("aspectos_tecnicos", {})
                st.markdown(f"- **Manejo de balón:** {tecnicos2.get('manejo_balon', '')}")
                st.markdown(f"- **Puntos a mejorar:** {tecnicos2.get('puntos_mejorar', '')}")
            with st.expander("🎯 Duelos y Recuperación"):
                duelos2 = informe2.get("duelo_recuperacion", {})
                st.markdown(f"- **Intervención y cortes:** {duelos2.get('intervencion_cortes', '')}")
                st.markdown(f"- **Observación:** {duelos2.get('observacion', '')}")
            with st.expander("🎯 Rendimiento Físico"):
                fisico2 = informe2.get("desempeno_fisico", {})
                st.markdown(f"- **Resistencia:** {fisico2.get('resistencia', '')}")
                st.markdown(f"- **Velocidad:** {fisico2.get('velocidad', '')}")
            with st.expander("🎯 Orden Táctico"):
                orden2 = informe2.get("orden_tactico", {})
                st.markdown(f"- **Táctico:** {orden2.get('tactico', '')}")
                st.markdown(f"- **Concentración:** {orden2.get('concentracion', '')}")
        else:
            st.write("⚠️ No hay información detallada del partido 2.")

# 🎥 TAB: Videos
with (tab_videos if "partido2" in jugador else tab_videos):
    st.title("🎥 Videos del Jugador")
    if "video" in jugador:
        if isinstance(jugador["video"], list):
            for video_url in jugador["video"]:
                st.video(video_url)
        else:
            st.video(jugador["video"])
    else:
        st.write("🎬 No hay videos disponibles para este jugador.")
