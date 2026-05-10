import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
from pathlib import Path
import json

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Chelasabe 🍺",
    page_icon="🍺",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.main-title {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    color: #C8760A;
    text-align: center;
    margin-bottom: 0;
    line-height: 1.1;
}

.subtitle {
    text-align: center;
    color: #6B5B45;
    font-size: 1rem;
    margin-top: 0.3rem;
    margin-bottom: 2rem;
}

.section-header {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    color: #7B3F00;
    border-left: 4px solid #C8760A;
    padding-left: 0.75rem;
    margin-top: 1.5rem;
    margin-bottom: 0.5rem;
}

.beer-card {
    background: #FFF8F0;
    border: 1px solid #E8D5B7;
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
}

.rec-card {
    background: linear-gradient(135deg, #FFF8F0, #FFF0DC);
    border: 2px solid #C8760A;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

.rec-rank {
    font-size: 2rem;
    color: #C8760A;
}

.badge {
    display: inline-block;
    background: #C8760A;
    color: white;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
}

.stRadio > label { font-weight: 500; }

div[data-testid="stExpander"] {
    border: 1px solid #E8D5B7;
    border-radius: 8px;
}

.stProgress > div > div { background-color: #C8760A; }

footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ── Data & DB ─────────────────────────────────────────────────────────────────
from data import CERVEZAS_COMERCIALES, ESTILOS_ARTESANAL, NOTAS_AROMA, NOTAS_SABOR
from db import get_conn, init_db, save_advanced_user, get_advanced_users
from matching import find_similar_users, build_style_recommendation

init_db()

# ── Session state ─────────────────────────────────────────────────────────────
def reset_state():
    for k in list(st.session_state.keys()):
        del st.session_state[k]

if "step" not in st.session_state:
    st.session_state.step = "home"

# ══════════════════════════════════════════════════════════════════════════════
# HOME
# ══════════════════════════════════════════════════════════════════════════════
def show_home():
    st.markdown('<div class="main-title">🍺 Chelasabe</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Tu guía personal de cerveza artesanal</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### ¿Qué quieres hacer hoy?")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **🧑‍🎓 Soy nuevo en la artesanal**
        
        Encuentra tu estilo ideal basado en tus gustos actuales.
        """)
        if st.button("👶 Quiero descubrir mi estilo", use_container_width=True):
            st.session_state.step = "principiante_quiz"
            st.session_state.user_type = "principiante"
            st.rerun()

    with col2:
        st.markdown("""
        **🍺 Ya consumo artesanal regularmente**
        
        Comparte tu perfil y ayuda a orientar a otros amantes de la chela.
        """)
        if st.button("🧠 Registrar mi perfil avanzado", use_container_width=True):
            st.session_state.step = "avanzado_quiz"
            st.session_state.user_type = "avanzado"
            st.rerun()

    st.markdown("---")
    n = len(get_advanced_users())
    st.caption(f"👥 {n} catadores avanzados en la base de conocimiento")

# ══════════════════════════════════════════════════════════════════════════════
# CUESTIONARIO COMPARTIDO (Sección 1 y 2)
# ══════════════════════════════════════════════════════════════════════════════
def seccion_nombre(prefix=""):
    st.markdown('<div class="section-header">👤 ¿Cómo te llamamos?</div>', unsafe_allow_html=True)
    nombre = st.text_input("Tu nombre o apodo", key=f"{prefix}nombre", placeholder="Ej: Toño, La Güera, Don Chuy…")
    return nombre

def seccion_comerciales(prefix=""):
    st.markdown('<div class="section-header">🏪 Cervezas comerciales</div>', unsafe_allow_html=True)
    st.caption("Califica cada cerveza del 1 (no me gusta) al 5 (me encanta). Si nunca la has probado, déjala en 0.")

    ratings = {}
    for cerveza in CERVEZAS_COMERCIALES:
        with st.container():
            st.markdown(f'<div class="beer-card">', unsafe_allow_html=True)
            col1, col2 = st.columns([2, 3])
            with col1:
                st.markdown(f"**{cerveza['nombre']}**")
                st.caption(f"{cerveza['estilo']} · {cerveza['abv']}% ABV")
            with col2:
                val = st.select_slider(
                    "Calificación",
                    options=[0, 1, 2, 3, 4, 5],
                    value=0,
                    format_func=lambda x: ["No probada", "😕 1", "😐 2", "🙂 3", "😊 4", "🤩 5"][x],
                    key=f"{prefix}com_{cerveza['id']}",
                    label_visibility="collapsed"
                )
            ratings[cerveza['id']] = val
            st.markdown('</div>', unsafe_allow_html=True)
    return ratings

def seccion_preferencias_generales(prefix=""):
    st.markdown('<div class="section-header">🎨 Preferencias generales</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        color_pref = st.select_slider(
            "🎨 Color preferido",
            options=["Muy clara", "Clara", "Ámbar", "Oscura", "Muy oscura"],
            value="Clara",
            key=f"{prefix}color"
        )
        abv_pref = st.select_slider(
            "💪 Nivel de alcohol",
            options=["Bajo (<4%)", "Moderado (4-6%)", "Alto (6-9%)", "Muy alto (9%+)"],
            value="Moderado (4-6%)",
            key=f"{prefix}abv"
        )
    with col2:
        amargor_pref = st.select_slider(
            "🌿 Amargor",
            options=["Nada amarga", "Poco amarga", "Medio", "Bastante amarga", "Muy amarga"],
            value="Poco amarga",
            key=f"{prefix}amargor"
        )
        cuerpo_pref = st.select_slider(
            "💧 Cuerpo / sensación en boca",
            options=["Muy ligera", "Ligera", "Media", "Robusta", "Muy robusta"],
            value="Ligera",
            key=f"{prefix}cuerpo"
        )

    st.markdown("**Notas de aroma que me gustan** (selecciona todas las que apliquen)")
    aroma_sel = st.multiselect(
        "Aromas", NOTAS_AROMA, key=f"{prefix}aroma", label_visibility="collapsed"
    )

    st.markdown("**Notas de sabor que me gustan**")
    sabor_sel = st.multiselect(
        "Sabores", NOTAS_SABOR, key=f"{prefix}sabor", label_visibility="collapsed"
    )

    return {
        "color": color_pref,
        "abv": abv_pref,
        "amargor": amargor_pref,
        "cuerpo": cuerpo_pref,
        "aroma": aroma_sel,
        "sabor": sabor_sel,
    }

def seccion_estilos_artesanal(prefix=""):
    st.markdown('<div class="section-header">🍻 Estilos artesanales que conoces</div>', unsafe_allow_html=True)
    st.caption("Califica los estilos que hayas probado. Si no lo conoces, déjalo en 0.")

    ratings = {}
    for familia, estilos in ESTILOS_ARTESANAL.items():
        st.markdown(f"**Familia {familia}**")
        for estilo in estilos:
            col1, col2 = st.columns([2, 3])
            with col1:
                st.markdown(f"{estilo['nombre']}")
                st.caption(estilo['desc'])
            with col2:
                val = st.select_slider(
                    "Rating",
                    options=[0, 1, 2, 3, 4, 5],
                    value=0,
                    format_func=lambda x: ["No probado", "😕 1", "😐 2", "🙂 3", "😊 4", "🤩 5"][x],
                    key=f"{prefix}est_{estilo['id']}",
                    label_visibility="collapsed"
                )
            ratings[estilo['id']] = val
        st.markdown("")
    return ratings

# ══════════════════════════════════════════════════════════════════════════════
# FLUJO PRINCIPIANTE
# ══════════════════════════════════════════════════════════════════════════════
def show_principiante_quiz():
    st.markdown('<div class="main-title" style="font-size:2rem;">🍺 Chelasabe</div>', unsafe_allow_html=True)
    st.markdown("### 👶 Descubre tu perfil cervecero")
    #st.progress(0.33, text="Paso 1 de 2")

    nombre = seccion_nombre("p_")
    ratings_com = seccion_comerciales("p_")
    prefs = seccion_preferencias_generales("p_")

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Volver", use_container_width=True):
            reset_state()
            st.rerun()
    with col2:
        if st.button("🔍 Ver mi recomendación →", type="primary", use_container_width=True):
            if not nombre:
                st.error("Por favor escribe tu nombre o apodo.")
            else:
                st.session_state.saved_nombre = nombre  # key distinto al widget "p_nombre"
                st.session_state.p_ratings_com = ratings_com
                st.session_state.p_prefs = prefs
                st.session_state.step = "principiante_result"
                st.rerun()

def show_principiante_result():
    st.markdown('<div class="main-title" style="font-size:2rem;">🍺 Chelasabe</div>', unsafe_allow_html=True)
    nombre = st.session_state.saved_nombre
    st.markdown(f"### 🎯 Tu perfil cervecero, {nombre}")

    avanzados = get_advanced_users()
    if len(avanzados) == 0:
        st.warning("⚠️ Aún no hay catadores avanzados en la base. ¡Pídele a alguien con experiencia que registre su perfil primero!")
        if st.button("← Volver al inicio"):
            reset_state()
            st.rerun()
        return

    ratings_com = st.session_state.p_ratings_com
    prefs = st.session_state.p_prefs

    similar_users, scores = find_similar_users(ratings_com, prefs, avanzados)
    recomendacion = build_style_recommendation(similar_users, scores)

    st.success(f"Encontramos **{len(similar_users)} catadores similares** a ti. Aquí va tu perfil estimado:")

    st.markdown('<div class="section-header">🏆 Estilos recomendados para ti</div>', unsafe_allow_html=True)
    st.caption("Ordenados de mayor a menor afinidad estimada")

    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣"]
    for i, (estilo_id, score) in enumerate(recomendacion[:5]):
        estilo_info = get_estilo_info(estilo_id)
        if estilo_info:
            pct = int(score * 100)
            st.markdown(f"""
            <div class="rec-card">
                <span class="rec-rank">{medals[i]}</span>
                <strong style="font-size:1.1rem"> {estilo_info['nombre']}</strong>
                <span class="badge" style="float:right">Afinidad: {pct}%</span><br>
                <small style="color:#6B5B45">{estilo_info['familia']} · {estilo_info['desc']}</small>
            </div>
            """, unsafe_allow_html=True)

    with st.expander("🔍 ¿Cómo calculamos esto?"):
        st.markdown(f"""
        Comparamos tus calificaciones de cervezas comerciales y preferencias generales 
        con los **{len(avanzados)} catadores avanzados** registrados en Chelasabe.
        
        Los **{len(similar_users)} más parecidos** a ti ponderaron sus gustos en estilos artesanales, 
        y construimos tu perfil a partir de sus preferencias combinadas.
        
        *Entre más catadores avanzados haya en la base, más precisa será tu recomendación.*
        """)

    st.markdown("---")
    if st.button("🏠 Volver al inicio", use_container_width=True):
        reset_state()
        st.rerun()

def get_estilo_info(estilo_id):
    for familia, estilos in ESTILOS_ARTESANAL.items():
        for e in estilos:
            if e['id'] == estilo_id:
                return {**e, "familia": familia}
    return None

# ══════════════════════════════════════════════════════════════════════════════
# FLUJO AVANZADO
# ══════════════════════════════════════════════════════════════════════════════
def show_avanzado_quiz():
    st.markdown('<div class="main-title" style="font-size:2rem;">🍺 Chelasabe</div>', unsafe_allow_html=True)
    st.markdown("### 🧠 Registra tu perfil de catador")
    #st.progress(0.66, text="Cuestionario completo")

    nombre = seccion_nombre("a_")
    ratings_com = seccion_comerciales("a_")
    prefs = seccion_preferencias_generales("a_")
    ratings_est = seccion_estilos_artesanal("a_")

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Volver", use_container_width=True):
            reset_state()
            st.rerun()
    with col2:
        if st.button("💾 Guardar mi perfil", type="primary", use_container_width=True):
            if not nombre:
                st.error("Por favor escribe tu nombre o apodo.")
            else:
                user_id = save_advanced_user(nombre, ratings_com, prefs, ratings_est)
                st.session_state.step = "avanzado_saved"
                st.session_state.saved_nombre = nombre  # key distinto al widget "a_nombre"
                st.rerun()

def show_avanzado_saved():
    st.markdown('<div class="main-title" style="font-size:2rem;">🍺 Chelasabe</div>', unsafe_allow_html=True)
    nombre = st.session_state.saved_nombre
    st.success(f"✅ ¡Gracias, {nombre}! Tu perfil fue guardado.")
    st.markdown(f"""
    Tu experiencia ahora forma parte de la base de conocimiento de **Chelasabe**.
    
    Cada vez que un principiante use la app, tu perfil ayudará a orientarlo hacia 
    los estilos que más probablemente le van a gustar. 🍻
    """)

    n = len(get_advanced_users())
    st.info(f"👥 La base ahora tiene **{n} catador{'es' if n != 1 else ''}** avanzado{'s' if n != 1 else ''}.")

    if st.button("🏠 Volver al inicio", use_container_width=True):
        reset_state()
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# ROUTER
# ══════════════════════════════════════════════════════════════════════════════
step = st.session_state.step

if step == "home":
    show_home()
elif step == "principiante_quiz":
    show_principiante_quiz()
elif step == "principiante_result":
    show_principiante_result()
elif step == "avanzado_quiz":
    show_avanzado_quiz()
elif step == "avanzado_saved":
    show_avanzado_saved()
