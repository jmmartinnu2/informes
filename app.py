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

# Obtener posición en el campo (para el tab Informe)
pos_x, pos_y = jugador["posicion_campo"]["x"], jugador["posicion_campo"]["y"]

# Definir los tabs según el jugador y si existe partido2 (usando .get para mayor seguridad)
if jugador["nombre"] == "Ismael Ruesca Godino":
    if jugador.get("partido2"):
        # Se eliminó el tab "⚽ Próximo partido"
        tabs = st.tabs(["📊 Granada CF vs Atl. Marbella Paraíso", "📝 Atl. Marbella Paraíso vs Real Betis", "🎥 Videos"])
        tab_informe, tab_detallado, tab_videos = tabs
    else:
        tabs = st.tabs(["📊 Partido1", "📝 Partido2", "🎥 Videos"])
        tab_informe, tab_detallado, tab_videos = tabs
else:
    if jugador.get("partido2"):
        tabs = st.tabs(["📊 Informe", "⚽ Partido 2", "🎥 Videos"])
        tab_informe, tab_partido2, tab_videos = tabs
    else:
        tabs = st.tabs(["📊 Informe", "🎥 Videos"])
        tab_informe, tab_videos = tabs

# ------------------------------
# TAB: Informe del Jugador + Posición en el Campo
# ------------------------------
with tab_informe:
    # Cabecera con dos columnas: izquierda para la información, derecha para los logotipos
    header_left, header_right = st.columns([3, 1])
    with header_left:
        st.title(f"📊 Informe de {jugador['nombre']}")
        st.subheader(f"{jugador['equipo']} - {jugador['categoria']}")
        st.markdown(f"⭐⭐⭐⭐ **Valoración:** {jugador['valoracion']} / 5")
    with header_right:
        # Ajusta la clave según tu JSON: aquí se usa "granada_cf" en minúsculas si es la clave correcta,
        # o la que corresponda; por ejemplo, en el JSON de Ismael se usa "Granadacf"
        logo_granada = jugador["logotipos"].get("Granadacf")
        logo_atletico = jugador["logotipos"].get("atletico_marbella_paraiso")
        if logo_granada:
            st.image(logo_granada, width=120)
        if logo_atletico:
            st.image(logo_atletico, width=120)
    st.markdown("---")
    
    # Crear dos columnas: la izquierda para la información y la derecha para el pitch
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"### 🏆 Partido contra {jugador['partido']['rival']}")
        resultado = jugador["partido"]["resultado"]
        resultado_texto = " - ".join([f"{k.replace('_', ' ')} {v}" for k, v in resultado.items()])
        st.markdown(f"**Resultado:** {resultado_texto}")
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
                tactico_ord = jugador["informe"]["orden_tactico"]
                st.markdown(f"- **Táctico:** {tactico_ord['tactico']}")
                st.markdown(f"- **Concentración:** {tactico_ord['concentracion']}")
            else:
                st.markdown("⚠️ No hay información sobre el orden táctico.")
    with col2:
        st.markdown("### ⚽ Posición en el Campo")
        fig, ax = plt.subplots(figsize=(8, 7))
        pitch = Pitch(pitch_type='statsbomb', pitch_color='grass', line_color='white')
        pitch.draw(ax=ax)
        # Marcar la posición original del jugador (usada en el informe general)
        ax.scatter(pos_x, pos_y, color="black", s=600, label=jugador["nombre"])
        ax.text(pos_x, pos_y + 3, jugador["nombre"], fontsize=12, ha="center", color="white")
        st.pyplot(fig)

# ------------------------------
# TAB: Informe Detallado para Ismael Ruesca Godino (Partido2)
# ------------------------------
if jugador["nombre"] == "Ismael Ruesca Godino" and jugador.get("partido2"):
    with tab_detallado:
        p2_info = jugador["partido2"]["informe_detallado"]
        # Cabecera en dos columnas: izquierda para la información, derecha para los logotipos
        header_col1, header_col2 = st.columns([3, 1])
        with header_col1:
            st.title(p2_info["titulo"])
            st.subheader(p2_info["partido"])
            st.markdown(f"⭐⭐⭐⭐ **Valoración:** {p2_info['valoracion']}")
            st.markdown(f"**Resultado del Partido:** {p2_info['resultado_partido']}")
        with header_col2:
            st.image(jugador["logotipos"].get("atletico_marbella_paraiso"), width=120)
            st.image(jugador["logotipos"].get("Betis"), width=120)
        st.markdown("---")
        
        # Layout principal en dos columnas
        col1, col2 = st.columns(2)
        with col1:
            with st.expander("🎯 Contexto Táctico y Posicionamiento"):
                contexto = p2_info["contexto_tactico_y_posicionamiento"]
                st.markdown(f"**Sistema de Juego:** {contexto['sistema_de_juego']}")
                st.markdown(f"**Cambio de Rol:** {contexto['cambio_de_rol']}")
                
            with st.expander("🎯 Aspectos Técnicos y Detalles Individuales"):
                aspectos = p2_info["aspectos_tecnicos_y_detalles_individuales"]
                st.markdown(f"**Inicios con Intensidad:** {aspectos['inicios_con_intensidad']}")
                st.markdown(f"**Velocidad y Carrera:** {aspectos['velocidad_y_carrera']}")
                st.markdown(f"**Organización y Posicionamiento:** {aspectos['organizacion_y_posicionamiento']}")
                
            with st.expander("🎯 Contribución Ofensiva y Áreas de Mejora"):
                contribucion = p2_info["contribucion_ofensiva_y_areas_de_mejora"]
                st.markdown(f"**Aporte Ofensivo Limitado:** {contribucion['aporte_ofensivo_limitado']}")
                st.markdown(f"**Duelo Aéreo y Lectura de Juego:** {contribucion['duelo_aereo_y_lectura_de_juego']}")
                st.markdown(f"**Liderazgo e Intensidad:** {contribucion['liderazgo_e_intensidad']}")
                
            with st.expander("🎯 Desarrollo del Partido y Contribución al Equilibrio"):
                desarrollo = p2_info["desarrollo_del_partido_y_contribucion"]
                st.markdown(f"**Evolución en el Segundo Tiempo:** {desarrollo['evolucion_segundo_tiempo']}")
                st.markdown(f"**Sustitución y Gestión del Ritmo:** {desarrollo['sustitucion_y_gestion_ritmo']}")
                
            with st.expander("🎯 Conclusiones y Recomendaciones"):
                conclusiones = p2_info["conclusiones_y_recomendaciones"]
                fortalezas = "\n".join([f"- {item}" for item in conclusiones["fortalezas"]])
                areas = "\n".join([f"- {item}" for item in conclusiones["areas_de_mejora"]])
                st.markdown(f"**Fortalezas:**\n{fortalezas}")
                st.markdown(f"**Áreas de Mejora:**\n{areas}")
                st.markdown(f"**Resumen:** {conclusiones['resumen']}")
                
            with st.expander("⭐ Calificar la actuación de Ismael"):
                ismael_rating = st.slider("Califica la actuación (0 a 5 estrellas):", 0, 5, 4, key="ismael_rating")
                st.write("Calificación:", ismael_rating)
                
        with col2:
            st.markdown("### ⚽ Posición en el Campo - Partido 2")
            fig_pitch, ax_pitch = plt.subplots(figsize=(10, 9))
            pitch2 = Pitch(pitch_type='statsbomb', pitch_color='grass', line_color='white')
            pitch2.draw(ax=ax_pitch)
            # Marcar dos posiciones: ajustar las coordenadas según sea necesario
            ax_pitch.scatter(20, 40, color="black", s=600, label="Defensa Central")
            ax_pitch.scatter(40, 40, color="blue", s=600, label="Mediocentro Defensivo")
            ax_pitch.legend(loc="upper right", fontsize=12)
            st.pyplot(fig_pitch)

# ------------------------------
# TAB: Informe Detallado para otros jugadores (si no es Ismael Ruesca Godino)
# ------------------------------
if jugador.get("partido2") and jugador["nombre"] != "Ismael Ruesca Godino":
    with tab_partido2:
        partido2 = jugador["partido2"]
        st.title(f"⚽ Informe - {partido2.get('fecha', '')}")
        st.markdown(f"### Rival: {partido2.get('rival', 'Desconocido')}")
        resultado2 = partido2.get("resultado", {})
        if resultado2:
            resultado_texto2 = " - ".join([f"{k.replace('_', ' ')} {v}" for k, v in resultado2.items()])
            st.markdown(f"**Resultado:** {resultado_texto2}")
        st.markdown("### 📌 Análisis del Rendimiento - Partido 2")
        
        # Crear dos columnas: izquierda para el texto, derecha para el campo
        col1, col2 = st.columns([2, 1])
        with col1:
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
        with col2:
            st.markdown("### ⚽ Posición en el Campo - Partido 2")
            fig2, ax2 = plt.subplots(figsize=(4, 3))
            pitch2 = Pitch(pitch_type='statsbomb', pitch_color='grass', line_color='white')
            pitch2.draw(ax=ax2)
            pos_extremo_izquierdo = (85, 10)
            pos_extremo_derecho = (85, 70)
            ax2.scatter(*pos_extremo_izquierdo, color="black", s=200, label="Extremo Izquierdo")
            ax2.scatter(*pos_extremo_derecho, color="blue", s=200, label="Extremo Derecho")
            ax2.legend(loc="upper left", fontsize="small")
            st.pyplot(fig2)

# ------------------------------
# TAB: Videos
# ------------------------------
with tab_videos:
    st.title("🎥 Videos del Jugador")
    if "video" in jugador:
        if isinstance(jugador["video"], list):
            for video_url in jugador["video"]:
                st.video(video_url)
        else:
            st.video(jugador["video"])
    else:
        st.write("🎬 No hay videos disponibles para este jugador.")
