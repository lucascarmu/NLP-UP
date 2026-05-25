"""Motor de búsqueda semántica de películas.

Encapsula la carga del dataset, la construcción de la representación textual
enriquecida y los dos enfoques de recuperación de información:
TF-IDF (léxico) y embeddings con Sentence-BERT (semántico).
"""
from __future__ import annotations

import ast
from pathlib import Path

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
TEXT_COLS = ["title", "overview", "genres", "keywords", "cast"]
RESULT_COLS = ["title", "release_year", "vote_average", "genres", "cast", "directors", "overview"]


def build_search_text(row: pd.Series) -> str:
    """Representación textual enriquecida usada como entrada de ambos enfoques."""
    return (
        f"Title: {row['title']}. "
        f"Genres: {row['genres']}. "
        f"Keywords: {row['keywords']}. "
        f"Cast: {row['cast']}. "
        f"Overview: {row['overview']}."
    )


def load_movies(csv_path: str | Path) -> pd.DataFrame:
    """Carga el CSV, normaliza las columnas textuales y construye `search_text`."""
    df = pd.read_csv(csv_path)
    for col in TEXT_COLS:
        df[col] = df[col].fillna("").astype(str).str.strip()
    df["search_text"] = df.apply(build_search_text, axis=1)
    return df


def parse_list(value) -> list[str]:
    """Convierte el string-repr de una lista (p.ej. "['Horror', 'Crime']") en lista real."""
    try:
        parsed = ast.literal_eval(value)
        if isinstance(parsed, list):
            return [str(x) for x in parsed]
    except (ValueError, SyntaxError):
        pass
    return [value] if value else []


class MovieSearchEngine:
    """Indexa las películas con TF-IDF y embeddings, y resuelve consultas por similitud coseno."""

    def __init__(self, df: pd.DataFrame, model_name: str = MODEL_NAME):
        self.df = df.reset_index(drop=True)
        texts = self.df["search_text"].tolist()

        # Baseline léxico: TF-IDF
        self.tfidf_vectorizer = TfidfVectorizer(
            lowercase=True, stop_words="english", max_features=5000
        )
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(texts)

        # Enfoque semántico: embeddings densos (384 dimensiones)
        self.model = SentenceTransformer(model_name)
        self.embeddings = self.model.encode(texts, convert_to_numpy=True)

    def _rank(self, scores: np.ndarray, top_k: int) -> pd.DataFrame:
        top_idx = np.argsort(scores)[::-1][:top_k]
        results = self.df.iloc[top_idx][RESULT_COLS].copy()
        results["similarity"] = scores[top_idx]
        return results.reset_index(drop=True)

    def search_tfidf(self, query: str, top_k: int = 5) -> pd.DataFrame:
        query_vec = self.tfidf_vectorizer.transform([query])
        scores = cosine_similarity(query_vec, self.tfidf_matrix)[0]
        return self._rank(scores, top_k)

    def search_semantic(self, query: str, top_k: int = 5) -> pd.DataFrame:
        query_emb = self.model.encode([query], convert_to_numpy=True)
        scores = cosine_similarity(query_emb, self.embeddings)[0]
        return self._rank(scores, top_k)
