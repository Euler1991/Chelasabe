# matching.py — Motor de recomendación de Chelasabe
#
# Estrategia:
#   1. Vectorizar al principiante y a cada avanzado usando las mismas dimensiones:
#      - Ratings de cervezas comerciales (0-5, normalizados)
#      - Preferencias ordinales (color, abv, amargor, cuerpo) codificadas como enteros
#   2. Calcular similitud coseno entre el principiante y cada avanzado
#   3. Seleccionar top-K más similares (K configurable, default 5)
#   4. Ponderar los ratings de estilos artesanales de esos K usuarios
#      por su score de similitud → ranking final de estilos

import numpy as np
from data import CERVEZAS_COMERCIALES, ESTILOS_ARTESANAL

# ── Encoders para variables ordinales ────────────────────────────────────────
COLOR_ENC   = {"Muy clara": 1, "Clara": 2, "Ámbar": 3, "Oscura": 4, "Muy oscura": 5}
ABV_ENC     = {"Bajo (<4%)": 1, "Moderado (4-6%)": 2, "Alto (6-9%)": 3, "Muy alto (9%+)": 4}
AMARGOR_ENC = {"Nada amarga": 1, "Poco amarga": 2, "Medio": 3, "Bastante amarga": 4, "Muy amarga": 5}
CUERPO_ENC  = {"Muy ligera": 1, "Ligera": 2, "Media": 3, "Robusta": 4, "Muy robusta": 5}

# IDs en orden fijo para vectorización consistente
COM_IDS = [c["id"] for c in CERVEZAS_COMERCIALES]
EST_IDS = [e["id"] for familia in ESTILOS_ARTESANAL.values() for e in familia]

# ── Notas multivaluadas ───────────────────────────────────────────────────────
from data import NOTAS_AROMA, NOTAS_SABOR

def encode_multiselect(selected: list, catalog: list) -> list:
    """One-hot encoding de notas de aroma/sabor."""
    return [1 if item in selected else 0 for item in catalog]


def build_vector(ratings_com: dict, prefs: dict) -> np.ndarray:
    """
    Construye el vector de features para comparación.
    Dimensiones:
        - 8   ratings de comerciales (0-5 → 0-1)
        - 4   preferencias ordinales (1-5 → 0-1)
        - 12  one-hot aromas
        - 13  one-hot sabores
    Total: 37 dimensiones
    """
    # Ratings comerciales (normalizar a 0-1)
    com_vec = [ratings_com.get(cid, 0) / 5.0 for cid in COM_IDS]

    # Preferencias ordinales (normalizar a 0-1)
    ord_vec = [
        (COLOR_ENC.get(prefs.get("color", "Clara"), 2) - 1) / 4.0,
        (ABV_ENC.get(prefs.get("abv", "Moderado (4-6%)"), 2) - 1) / 3.0,
        (AMARGOR_ENC.get(prefs.get("amargor", "Poco amarga"), 2) - 1) / 4.0,
        (CUERPO_ENC.get(prefs.get("cuerpo", "Ligera"), 2) - 1) / 4.0,
    ]

    # Notas one-hot
    aroma_vec = encode_multiselect(prefs.get("aroma", []), NOTAS_AROMA)
    sabor_vec = encode_multiselect(prefs.get("sabor", []), NOTAS_SABOR)

    return np.array(com_vec + ord_vec + aroma_vec + sabor_vec, dtype=float)


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Similitud coseno entre dos vectores. Devuelve 0 si alguno es cero."""
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))


def find_similar_users(
    ratings_com: dict,
    prefs: dict,
    avanzados: list[dict],
    top_k: int = 5,
) -> tuple[list[dict], list[float]]:
    """
    Devuelve los top_k usuarios avanzados más similares al principiante
    junto con sus scores de similitud.
    """
    target_vec = build_vector(ratings_com, prefs)

    scored = []
    for user in avanzados:
        user_vec = build_vector(user["ratings_com"], user["prefs"])
        sim = cosine_similarity(target_vec, user_vec)
        scored.append((user, sim))

    # Ordenar descendente por similitud
    scored.sort(key=lambda x: x[1], reverse=True)

    top = scored[:top_k]
    similar_users = [u for u, _ in top]
    scores        = [s for _, s in top]

    return similar_users, scores


def build_style_recommendation(
    similar_users: list[dict],
    scores: list[float],
) -> list[tuple[str, float]]:
    """
    Calcula un score ponderado por similitud para cada estilo artesanal,
    usando solo los ratings no-cero de los usuarios similares.
    
    Retorna lista de (estilo_id, score_normalizado) ordenada descendente.
    """
    style_scores: dict[str, float] = {eid: 0.0 for eid in EST_IDS}
    style_weights: dict[str, float] = {eid: 0.0 for eid in EST_IDS}

    for user, sim_score in zip(similar_users, scores):
        for estilo_id in EST_IDS:
            rating = user["ratings_est"].get(estilo_id, 0)
            if rating > 0:  # solo considerar estilos que el usuario conoce
                style_scores[estilo_id]  += sim_score * (rating / 5.0)
                style_weights[estilo_id] += sim_score

    # Normalizar: score ponderado promedio
    final: dict[str, float] = {}
    for eid in EST_IDS:
        if style_weights[eid] > 0:
            final[eid] = style_scores[eid] / style_weights[eid]
        else:
            final[eid] = 0.0

    # Ordenar descendente
    ranked = sorted(final.items(), key=lambda x: x[1], reverse=True)
    return ranked
