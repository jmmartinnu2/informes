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

# Definir los tabs según el jugador y la existencia de partidos adicionales


# Definir los tabs según el jugador y la existencia de partidos adicionales
# Construir etiquetas de tabs para Ismael Ruesca Godino
if jugador["nombre"] == "Ismael Ruesca Godino":
    tabs_labels = ["📊 Granada CF vs Atl. Marbella Paraíso"]
    if jugador.get("partido2"): tabs_labels.append("📝 Atl. Marbella Paraíso vs Real Betis")
    if jugador.get("partido3"): tabs_labels.append("⚽ La Cañada vs Atl. Marbella Paraíso")
    if jugador.get("partido4"): tabs_labels.append("⚽ CD Tiropichón vs Marbella Atl. Paraíso")
    tabs_labels.append("🎥 Videos")
    tabs = st.tabs(tabs_labels)
    tab_informe = tabs[0]
    idx = 1
    tab_detallado = tabs[idx] if jugador.get("partido2") else None
    if jugador.get("partido2"): idx += 1
    tab_partido3 = tabs[idx] if jugador.get("partido3") else None
    if jugador.get("partido3"): idx += 1
    tab_partido4 = tabs[idx] if jugador.get("partido4") else None
    tab_videos = tabs[-1]
else:
    # Otros jugadores
    tabs_labels = ["📊 Informe"]
    if jugador.get("partido2"): tabs_labels.append("⚽ Partido 2")
    if jugador.get("partido3"): tabs_labels.append("⚽ Partido 3")
    tabs_labels.append("🎥 Videos")
    tabs = st.tabs(tabs_labels)
    tab_informe = tabs[0]
    tab_partido2 = tabs[1] if jugador.get("partido2") else None
    tab_partido3 = tabs[2] if jugador.get("partido3") else None
    tab_videos = tabs[-1]

# ------------------------------
# TAB: Informe del Jugador + Posición en el Campo
# ------------------------------
with tab_informe:
    header_left, header_right = st.columns([3, 1])
    with header_left:
        st.title(f"📊 Informe de {jugador['nombre']}")
        st.subheader(f"{jugador['equipo']} - {jugador['categoria']}")
        st.markdown("**Valoración:** ⭐⭐⭐")
    with header_right:
        logotipos = jugador.get("logotipos", {})
        logo_granada = logotipos.get("Granadacf") or logotipos.get("granada_cf")
        logo_atletico = logotipos.get("atletico_marbella_paraiso")
        if logo_granada:
            st.image(logo_granada, width=120)
        if logo_atletico:
            st.image(logo_atletico, width=120)
    st.markdown("---")
    
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
            st.markdown(f"- **Sistema de Juego:** {actuacion.get('sistema_juego', 'No especificado')}")
            st.markdown(f"- **Rol:** {actuacion.get('rol', 'No especificado')}")
            st.markdown(f"- **Rendimiento:** {actuacion.get('desempeno', 'No especificado')}")
            st.markdown(f"- **Participación:** {actuacion.get('participacion', 'No especificado')}")
            st.markdown(f"- **Liderazgo:** {actuacion.get('liderazgo', 'No especificado')}")
        
        with st.expander("🎯 Posicionamiento Táctico"):
            tactico = jugador["informe"]["posicionamiento_tactico"]
            st.markdown(f"- **Formación:** {tactico.get('formacion', 'No especificado')}")
            st.markdown(f"- **Rol:** {tactico.get('rol', 'No especificado')}")
        
        with st.expander("🎯 Aspectos Técnicos"):
            tecnica = jugador["informe"]["aspectos_tecnicos"]
            st.markdown(f"- **Manejo de balón:** {tecnica.get('manejo_balon', 'No especificado')}")
            st.markdown(f"- **Puntos a mejorar:** {tecnica.get('puntos_mejorar', 'No especificado')}")
        
        with st.expander("🎯 Duelos y Recuperación"):
            duelos = jugador["informe"]["duelo_recuperacion"]
            st.markdown(f"- **Intervención y cortes:** {duelos.get('intervencion_cortes', 'No especificado')}")
            st.markdown(f"- **Observación:** {duelos.get('observacion', 'No especificado')}")
        
        with st.expander("🎯 Rendimiento Físico"):
            fisico = jugador["informe"]["desempeno_fisico"]
            st.markdown(f"- **Resistencia:** {fisico.get('resistencia', 'No especificado')}")
            st.markdown(f"- **Velocidad:** {fisico.get('velocidad', 'No especificado')}")
        
        with st.expander("🎯 Orden Táctico"):
            orden = jugador["informe"].get("orden_tactico", {})
            st.markdown(f"- **Táctico:** {orden.get('tactico', 'No especificado')}")
            st.markdown(f"- **Concentración:** {orden.get('concentracion', 'No especificado')}")
    with col2:
        st.markdown("### ⚽ Posición en el Campo")
        fig, ax = plt.subplots(figsize=(8, 7))
        pitch = Pitch(pitch_type="statsbomb", pitch_color="grass", line_color="white")
        pitch.draw(ax=ax)
        ax.scatter(pos_x, pos_y, color="black", s=600, label=jugador["nombre"])
        ax.text(pos_x, pos_y + 3, jugador["nombre"], fontsize=12, ha="center", color="white")
        st.pyplot(fig)

# ------------------------------
# TAB: Informe Detallado para Ismael Ruesca Godino (Partido2)
# ------------------------------
if jugador["nombre"] == "Ismael Ruesca Godino" and jugador.get("partido2"):
    with tab_detallado:
        p2_info = jugador["partido2"]["informe_detallado"]
        header_col1, header_col2 = st.columns([3, 1])
        with header_col1:
            st.title(p2_info.get("titulo", "Título no disponible"))
            st.subheader(p2_info.get("partido", "Partido no disponible"))
            st.markdown("**Valoración:** ⭐⭐⭐⭐")
            st.markdown(f"**Resultado del Partido:** {p2_info.get('resultado_partido', 'No especificado')}")
        with header_col2:
            logotipos = jugador.get("logotipos", {})
            logo_atletico = logotipos.get("atletico_marbella_paraiso")
            logo_betis = logotipos.get("Betis")
            if logo_atletico:
                st.image(logo_atletico, width=120)
            if logo_betis:
                st.image(logo_betis, width=120)
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            with st.expander("🎯 Contexto Táctico y Posicionamiento"):
                contexto = p2_info.get("contexto_tactico_y_posicionamiento", {})
                st.markdown(f"**Sistema de Juego:** {contexto.get('sistema_de_juego', 'No especificado')}")
                st.markdown(f"**Cambio de Rol:** {contexto.get('cambio_de_rol', 'No especificado')}")
                
            with st.expander("🎯 Aspectos Técnicos y Detalles Individuales"):
                aspectos = p2_info.get("aspectos_tecnicos_y_detalles_individuales", {})
                st.markdown(f"**Inicios con Intensidad:** {aspectos.get('inicios_con_intensidad', 'No especificado')}")
                st.markdown(f"**Velocidad y Carrera:** {aspectos.get('velocidad_y_carrera', 'No especificado')}")
                st.markdown(f"**Organización y Posicionamiento:** {aspectos.get('organizacion_y_posicionamiento', 'No especificado')}")
                
            with st.expander("🎯 Contribución Ofensiva y Áreas de Mejora"):
                contribucion = p2_info.get("contribucion_ofensiva_y_areas_de_mejora", {})
                st.markdown(f"**Aporte Ofensivo Limitado:** {contribucion.get('aporte_ofensivo_limitado', 'No especificado')}")
                st.markdown(f"**Duelo Aéreo y Lectura de Juego:** {contribucion.get('duelo_aereo_y_lectura_de_juego', 'No especificado')}")
                st.markdown(f"**Liderazgo e Intensidad:** {contribucion.get('liderazgo_e_intensidad', 'No especificado')}")
                
            with st.expander("🎯 Desarrollo del Partido y Contribución al Equilibrio"):
                desarrollo = p2_info.get("desarrollo_del_partido_y_contribucion", {})
                st.markdown(f"**Evolución en el Segundo Tiempo:** {desarrollo.get('evolucion_segundo_tiempo', 'No especificado')}")
                st.markdown(f"**Sustitución y Gestión del Ritmo:** {desarrollo.get('sustitucion_y_gestion_ritmo', 'No especificado')}")
                
            with st.expander("🎯 Conclusiones y Recomendaciones"):
                conclusiones = p2_info.get("conclusiones_y_recomendaciones", {})
                fortalezas = "\n".join([f"- {item}" for item in conclusiones.get("fortalezas", [])])
                areas = "\n".join([f"- {item}" for item in conclusiones.get("areas_de_mejora", [])])
                st.markdown(f"**Fortalezas:**\n{fortalezas}")
                st.markdown(f"**Áreas de Mejora:**\n{areas}")
                st.markdown(f"**Resumen:** {conclusiones.get('resumen', 'No especificado')}")
                

        with col2:
            st.markdown("### ⚽ Posiciones en el campo de Ismael")
            fig_pitch, ax_pitch = plt.subplots(figsize=(10, 9))
            pitch2 = Pitch(pitch_type="statsbomb", pitch_color="grass", line_color="white")
            pitch2.draw(ax=ax_pitch)
            ax_pitch.scatter(20, 40, color="black", s=600, label="Defensa Central")
            ax_pitch.scatter(40, 40, color="blue", s=600, label="Mediocentro Defensivo")
            ax_pitch.legend(loc="upper right", fontsize=12)
            st.pyplot(fig_pitch)

# ------------------------------
# TAB: Informe Detallado para Ismael Ruesca Godino (Partido3)
# ------------------------------
if jugador["nombre"] == "Ismael Ruesca Godino" and jugador.get("partido3"):
    with tab_partido3:
        p3 = jugador["partido3"]
        st.title("⚽ Informe - La Cañada vs Atl. Marbella Paraíso")
        resultado3 = p3.get("resultado", {})
        resultado_texto3 = " - ".join([f"{k.replace('_', ' ')} {v}" for k, v in resultado3.items()])
        st.markdown(f"**Resultado:** {resultado_texto3}")
        st.markdown("### 📌 Análisis del Rendimiento")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            informe3 = p3.get("informe", {})
            st.markdown(f"📝 **Comentario:** {informe3.get('comentario', 'No especificado')}")
            
            with st.expander("🎯 Actuación en el Partido"):
                act3 = informe3.get("actuacion", {})
                st.markdown(f"- **Sistema de Juego:** {act3.get('sistema_juego', 'No especificado')}")
                st.markdown(f"- **Rol:** {act3.get('rol', 'No especificado')}")
                st.markdown(f"- **Rendimiento:** {act3.get('desempeno', 'No especificado')}")
                st.markdown(f"- **Participación:** {act3.get('participacion', 'No especificado')}")
                st.markdown(f"- **Liderazgo:** {act3.get('liderazgo', 'No especificado')}")
            
            with st.expander("🎯 Posicionamiento Táctico"):
                pos3 = informe3.get("posicionamiento_tactico", {})
                st.markdown(f"- **Formación:** {pos3.get('formacion', 'No especificado')}")
                st.markdown(f"- **Rol:** {pos3.get('rol', 'No especificado')}")
                st.markdown(f"- **Observación:** {pos3.get('observacion', 'Sin observaciones')}")
            
            with st.expander("🎯 Aspectos Técnicos"):
                tec3 = informe3.get("aspectos_tecnicos", {})
                st.markdown(f"- **Manejo de balón:** {tec3.get('manejo_balon', 'No especificado')}")
                st.markdown(f"- **Puntos a mejorar:** {tec3.get('puntos_mejorar', 'No especificado')}")
            
            with st.expander("🎯 Duelos y Recuperación"):
                duel3 = informe3.get("duelo_recuperacion", {})
                st.markdown(f"- **Intervención y cortes:** {duel3.get('intervencion_cortes', 'No especificado')}")
                st.markdown(f"- **Observación:** {duel3.get('observacion', 'No especificado')}")
            
            with st.expander("🎯 Rendimiento Físico"):
                fisico3 = informe3.get("desempeno_fisico", {})
                st.markdown(f"- **Resistencia:** {fisico3.get('resistencia', 'No especificado')}")
                st.markdown(f"- **Velocidad:** {fisico3.get('velocidad', 'No especificado')}")
            
            with st.expander("🎯 Orden Táctico"):
                orden3 = informe3.get("orden_tactico", {})
                st.markdown(f"- **Táctico:** {orden3.get('tactico', 'No especificado')}")
                st.markdown(f"- **Concentración:** {orden3.get('concentracion', 'No especificado')}")
            

        with col2:
            st.markdown("### ⚽ Posición en el Campo - Partido 3")
            fig3, ax3 = plt.subplots(figsize=(6, 4))
            pitch3 = Pitch(pitch_type="statsbomb", pitch_color="grass", line_color="white")
            pitch3.draw(ax=ax3)
            ax3.scatter(40, 40, color="black", s=300, label="Defensa Central")
            ax3.scatter(20, 40, color="blue", s=300, label="Mediocentro Defensivo")
            ax3.legend(loc="upper left", fontsize="small")
            st.pyplot(fig3)

# ------------------------------
# TAB: Informe Detallado para otros jugadores (si no es Ismael Ruesca Godino)
# ------------------------------
if jugador.get("partido2") and jugador["nombre"] != "Ismael Ruesca Godino":
    with tab_partido2:
        partido2 = jugador["partido2"]
        st.title(f"⚽ Informe - {partido2.get('fecha', 'Fecha no especificada')}")
        st.markdown(f"### Rival: {partido2.get('rival', 'Desconocido')}")
        st.markdown("**Valoración:** ⭐⭐⭐")
        resultado2 = partido2.get("resultado", {})
        if resultado2:
            resultado_texto2 = " - ".join([f"{k.replace('_', ' ')} {v}" for k, v in resultado2.items()])
            st.markdown(f"**Resultado:** {resultado_texto2}")
        st.markdown("### 📌 Análisis del Rendimiento - Partido 2")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            informe2 = partido2.get("informe", {})
            if informe2:
                st.markdown(f"📝 **Comentario:** {informe2.get('comentario', 'No especificado')}")
                with st.expander("🎯 Actuación en el Partido"):
                    actuacion2 = informe2.get("actuacion", {})
                    st.markdown(f"- **Sistema de Juego:** {actuacion2.get('sistema_juego', 'No especificado')}")
                    st.markdown(f"- **Rol:** {actuacion2.get('rol', 'No especificado')}")
                    st.markdown(f"- **Rendimiento:** {actuacion2.get('desempeno', 'No especificado')}")
                    st.markdown(f"- **Participación:** {actuacion2.get('participacion', 'No especificado')}")
                    st.markdown(f"- **Liderazgo:** {actuacion2.get('liderazgo', 'No especificado')}")
                with st.expander("🎯 Posicionamiento Táctico"):
                    pos_tactico2 = informe2.get("posicionamiento_tactico", {})
                    st.markdown(f"- **Formación:** {pos_tactico2.get('formacion', 'No especificado')}")
                    st.markdown(f"- **Rol:** {pos_tactico2.get('rol', 'No especificado')}")
                with st.expander("🎯 Aspectos Técnicos"):
                    tecnicos2 = informe2.get("aspectos_tecnicos", {})
                    st.markdown(f"- **Manejo de balón:** {tecnicos2.get('manejo_balon', 'No especificado')}")
                    st.markdown(f"- **Puntos a mejorar:** {tecnicos2.get('puntos_mejorar', 'No especificado')}")
                with st.expander("🎯 Duelos y Recuperación"):
                    duelos2 = informe2.get("duelo_recuperacion", {})
                    st.markdown(f"- **Intervención y cortes:** {duelos2.get('intervencion_cortes', 'No especificado')}")
                    st.markdown(f"- **Observación:** {duelos2.get('observacion', 'No especificado')}")
                with st.expander("🎯 Rendimiento Físico"):
                    fisico2 = informe2.get("desempeno_fisico", {})
                    st.markdown(f"- **Resistencia:** {fisico2.get('resistencia', 'No especificado')}")
                    st.markdown(f"- **Velocidad:** {fisico2.get('velocidad', 'No especificado')}")
                with st.expander("🎯 Orden Táctico"):
                    orden2 = informe2.get("orden_tactico", {})
                    st.markdown(f"- **Táctico:** {orden2.get('tactico', 'No especificado')}")
                    st.markdown(f"- **Concentración:** {orden2.get('concentracion', 'No especificado')}")
            else:
                st.write("⚠️ No hay información detallada del partido 2.")
        with col2:
            st.markdown("### ⚽ Posición en el Campo - Partido 2")
            fig2, ax2 = plt.subplots(figsize=(4, 3))
            pitch2 = Pitch(pitch_type="statsbomb", pitch_color="grass", line_color="white")
            pitch2.draw(ax=ax2)
            pos_extremo_izquierdo = (85, 10)
            pos_extremo_derecho = (85, 70)
            ax2.scatter(*pos_extremo_izquierdo, color="black", s=200, label="Extremo Izquierdo")
            ax2.scatter(*pos_extremo_derecho, color="blue", s=200, label="Extremo Derecho")
            ax2.legend(loc="upper left", fontsize="small")
            st.pyplot(fig2)

# ------------------------------
# TAB: Informe Detallado para otros jugadores (Partido3, si existe y no es Ismael)
# ------------------------------
if jugador.get("partido3") and jugador["nombre"] != "Ismael Ruesca Godino":
    with tab_partido3:
        p3 = jugador["partido3"]
        st.title("⚽ Informe - Marbella CF vs Estepona")
        resultado3 = p3.get("resultado", {})
        resultado_texto3 = " - ".join([f"{k.replace('_', ' ')} {v}" for k, v in resultado3.items()])
        st.markdown(f"**Resultado:** {resultado_texto3}")
        st.markdown("**Valoración:** ⭐⭐⭐⭐")
        st.markdown("### 📌 Análisis del Rendimiento")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            informe3 = p3.get("informe", {})
            st.markdown(f"📝 **Comentario:** {informe3.get('comentario', 'No especificado')}")
            
            with st.expander("🎯 Actuación en el Partido"):
                act3 = informe3.get("actuacion", {})
                st.markdown(f"- **Sistema de Juego:** {act3.get('sistema_juego', 'No especificado')}")
                st.markdown(f"- **Rol:** {act3.get('rol', 'No especificado')}")
                st.markdown(f"- **Rendimiento:** {act3.get('desempeno', 'No especificado')}")
                st.markdown(f"- **Participación:** {act3.get('participacion', 'No especificado')}")
                st.markdown(f"- **Liderazgo:** {act3.get('liderazgo', 'No especificado')}")
            
            with st.expander("🎯 Posicionamiento Táctico"):
                pos3 = informe3.get("posicionamiento_tactico", {})
                st.markdown(f"- **Formación:** {pos3.get('formacion', 'No especificado')}")
                st.markdown(f"- **Rol:** {pos3.get('rol', 'No especificado')}")
            
            with st.expander("🎯 Aspectos Técnicos"):
                tec3 = informe3.get("aspectos_tecnicos", {})
                st.markdown(f"- **Manejo de balón:** {tec3.get('manejo_balon', 'No especificado')}")
                st.markdown(f"- **Puntos a mejorar:** {tec3.get('puntos_mejorar', 'No especificado')}")
            
            with st.expander("🎯 Duelos y Recuperación"):
                duel3 = informe3.get("duelo_recuperacion", {})
                st.markdown(f"- **Observación:** {duel3.get('observacion', 'No especificado')}")
            
            with st.expander("🎯 Detalles Adicionales"):
                det3 = informe3.get("detalles_adicionales", {})
                st.markdown(f"- **Entrada y Sustitución:** {det3.get('entrada_sustitucion', 'No especificado')}")
                st.markdown(f"- **Acciones Destacadas:** {det3.get('acciones_destacadas', 'No especificado')}")
            
        with col2:
            st.markdown("### ⚽ Posición en el Campo - Partido 3")
            fig3, ax3 = plt.subplots(figsize=(4, 3))
            pitch3 = Pitch(pitch_type="statsbomb", pitch_color="grass", line_color="white")
            pitch3.draw(ax=ax3)
            pos_extremo_derecho = (85, 70)
            ax3.scatter(*pos_extremo_derecho, color="blue", s=200, label="Extremo Derecho")
            ax3.legend(loc="upper left", fontsize="small")
            st.pyplot(fig3)

# ------------------------------
# TAB: Informe Detallado para Ismael (Partido4)
# ------------------------------
if jugador.get('partido4'):
    with tab_partido4:
        p4 = jugador['partido4']
        st.title(f"⚽ Informe - {p4['rival']}")
        st.markdown("**Resultado:** " + " - ".join([f"{k.replace('_',' ')} {v}" for k,v in p4['resultado'].items()]))
        st.markdown(f"📝 **Comentario:** {p4['informe']['comentario']}")
        st.markdown("### 📌 Análisis del Rendimiento")
        col1,col2 = st.columns([2,1])
        with col1:
            inf4 = p4['informe']
            st.markdown(f"📝 **Comentario:** {inf4.get('comentario','No especificado')}")
            with st.expander("🎯 Actuación en el Partido"):
                for k,v in inf4['actuacion'].items(): st.markdown(f"- **{k}:** {v}")
            with st.expander("🎯 Posicionamiento Táctico"):
                pt4 = inf4['posicionamiento_tactico']
                st.markdown(f"- **Formación:** {pt4.get('formacion')}")
                st.markdown(f"- **Rol:** {pt4.get('rol')}")
            with st.expander("🎯 Aspectos Técnicos"):
                at4 = inf4['aspectos_tecnicos']
                st.markdown(f"- **Manejo de balón:** {at4.get('manejo_balon')}")
                st.markdown(f"- **Puntos a mejorar:** {at4.get('puntos_mejorar')}")
            with st.expander("🎯 Duelos y Recuperación"):
                dr4 = inf4['duelo_recuperacion']
                st.markdown(f"- **Intervención y cortes:** {dr4.get('intervencion_cortes')}")
                st.markdown(f"- **Observación:** {dr4.get('observacion')}")
            with st.expander("🎯 Rendimiento Físico"):
                rf4 = inf4['desempeno_fisico']
                st.markdown(f"- **Resistencia:** {rf4.get('resistencia')}")
                st.markdown(f"- **Velocidad:** {rf4.get('velocidad')}")
            with st.expander("🎯 Orden Táctico"):
                od4 = inf4['orden_tactico']
                st.markdown(f"- **Táctico:** {od4.get('tactico')}")
                st.markdown(f"- **Concentración:** {od4.get('concentracion')}")
        with col2:
            st.markdown("### ⚽ Posición en el Campo - Partido 3")
            fig3, ax3 = plt.subplots(figsize=(6, 4))
            pitch3 = Pitch(pitch_type="statsbomb", pitch_color="grass", line_color="white")
            pitch3.draw(ax=ax3)
            ax3.scatter(20, 40, color="black", s=300, label="Defensa Central")
            ax3.legend(loc="upper left", fontsize="small")
            st.pyplot(fig3)

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
