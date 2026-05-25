"""Frontend Streamlit para el Buscador Semántico de Películas.

Ejecutar con:  streamlit run app.py
"""
from pathlib import Path

import pandas as pd
import streamlit as st

from src.search_engine import MovieSearchEngine, load_movies, parse_list

DATA_PATH = Path(__file__).parent / "data" / "movies_expanded_1000.csv"

EXAMPLES = [
    "animated movie with dinosaurs and friendship",
    "film about genius, science and war",
    "thief who infiltrates dreams",
    "historical drama about royalty and power",
    "movie about dreams, memory and the mind",
]

st.set_page_config(
    page_title="Buscador Semántico de Películas",
    layout="wide",
)


@st.cache_resource(show_spinner="Cargando dataset y generando embeddings (solo la primera vez)...")
def get_engine() -> MovieSearchEngine:
    df = load_movies(DATA_PATH)
    return MovieSearchEngine(df)


def render_card(row: pd.Series, rank: int) -> None:
    with st.container(border=True):
        info, score = st.columns([5, 1])
        with info:
            year = "" if pd.isna(row["release_year"]) else f" ({int(row['release_year'])})"
            st.markdown(f"**{rank}. {row['title']}**{year}")
            genres = " · ".join(parse_list(row["genres"]))
            if genres:
                st.caption(genres)
        with score:
            st.metric("Similitud", f"{row['similarity']:.3f}")
        if row["overview"]:
            st.write(row["overview"])
        cast = ", ".join(parse_list(row["cast"])[:5])
        directors = ", ".join(parse_list(row["directors"]))
        meta = []
        if cast:
            meta.append(f"**Reparto:** {cast}")
        if directors:
            meta.append(f"**Dirección:** {directors}")
        if meta:
            st.caption("  ·  ".join(meta))


def render_results(results: pd.DataFrame) -> None:
    for i, row in results.iterrows():
        render_card(row, i + 1)


st.title("Buscador Semántico de Películas")
st.caption(
    "Encontrá películas describiéndolas en lenguaje natural. "
    "Comparativa entre recuperación léxica (TF-IDF) y semántica (embeddings)."
)

if "query" not in st.session_state:
    st.session_state.query = ""

with st.sidebar:
    st.header("Opciones")
    method = st.radio(
        "Método de búsqueda",
        ["Semántico (embeddings)", "Léxico (TF-IDF)", "Comparar ambos"],
    )
    top_k = st.slider("Cantidad de resultados", min_value=3, max_value=10, value=5)

    st.divider()
    st.subheader("Consultas de ejemplo")
    for ex in EXAMPLES:
        if st.button(ex, use_container_width=True):
            st.session_state.query = ex

    st.divider()
    st.caption(
        "Modelo: all-MiniLM-L6-v2 (optimizado para inglés). "
        "Dataset: 1000 películas de TMDB (simulado vía CSV)."
    )

engine = get_engine()

query = st.text_input(
    "Describí la película que buscás",
    key="query",
    placeholder="p. ej. film about genius, science and war",
)

if query:
    if method == "Comparar ambos":
        col_sem, col_lex = st.columns(2)
        with col_sem:
            st.subheader("Semántico (embeddings)")
            render_results(engine.search_semantic(query, top_k))
        with col_lex:
            st.subheader("Léxico (TF-IDF)")
            render_results(engine.search_tfidf(query, top_k))
    elif method.startswith("Semántico"):
        render_results(engine.search_semantic(query, top_k))
    else:
        render_results(engine.search_tfidf(query, top_k))
else:
    st.info("Ingresá una descripción o elegí una consulta de ejemplo en la barra lateral.")
