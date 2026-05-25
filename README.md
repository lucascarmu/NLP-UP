# Buscador Semántico de Películas

Trabajo Integrador de **Procesamiento de Lenguaje Natural** (Grupo 2).

Sistema de búsqueda de películas que interpreta descripciones libres en lenguaje natural
(por ejemplo: *"film about genius, science and war"*) y recupera las películas
semánticamente más similares. Compara dos enfoques de recuperación de información:

- **Léxico (TF-IDF):** coincidencias de palabras ponderadas + similitud coseno.
- **Semántico (embeddings):** vectores densos con Sentence-BERT (`all-MiniLM-L6-v2`) + similitud coseno.

El proyecto incluye un frontend web en **Streamlit** para probar el buscador de forma
interactiva y comparar ambos enfoques lado a lado.

> El objetivo es demostrar conceptos de NLP, no construir un sistema de producción.

## Estructura del proyecto

```
.
├── app.py                  # Frontend Streamlit (punto de entrada)
├── requirements.txt        # Dependencias
├── src/
│   └── search_engine.py    # Lógica NLP: carga, TF-IDF, embeddings y búsqueda
├── data/
│   └── movies_expanded_1000.csv   # "Base de datos" simulada (1000 películas de TMDB)
├── Notebook/
│   └── Notebook_1.ipynb    # Notebook con la experimentación y evaluación
└── docs/
    ├── Consigna.md
    ├── Entrega1_Grupo2.md
    └── Informe_Grupo2.docx # Informe final
```

## Requisitos

- Python 3.10 o superior
- Conexión a internet la primera vez (descarga el modelo `all-MiniLM-L6-v2`, ~90 MB)

## Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/lucascarmu/NLP-UP.git
cd NLP-UP

# 2. Crear y activar un entorno virtual
python -m venv .venv
source .venv/bin/activate        # En Windows: .venv\Scripts\activate

# 3. Instalar las dependencias
pip install -r requirements.txt
```

## Cómo levantar el servicio localmente

```bash
streamlit run app.py
```

Streamlit abrirá automáticamente el navegador en `http://localhost:8501`.
La primera ejecución tarda unos segundos: descarga el modelo y genera los embeddings
de las 1000 películas (luego quedan cacheados en memoria mientras el servidor sigue activo).

## Cómo probarlo

1. Escribí una descripción en el cuadro de búsqueda, o elegí una **consulta de ejemplo**
   en la barra lateral.
2. En la barra lateral podés:
   - Elegir el método: **Semántico**, **Léxico** o **Comparar ambos** (lado a lado).
   - Ajustar la cantidad de resultados (Top-K).
3. Cada resultado muestra el puntaje de **similitud coseno**, géneros, sinopsis, reparto y dirección.

Consultas sugeridas para apreciar la diferencia entre ambos enfoques:

- `thief who infiltrates dreams`
- `film about genius, science and war`
- `animated movie with dinosaurs and friendship`

> El modelo está optimizado para inglés, por lo que las consultas en inglés rinden mejor.

## Notebook de experimentación

El notebook `Notebook/Notebook_1.ipynb` contiene el pipeline completo: carga y validación
del dataset, construcción de la representación textual, ambos enfoques y la **evaluación
cuantitativa** con las métricas Hit Rate@K y MRR.

Puede ejecutarse localmente con Jupyter:

```bash
pip install jupyter
jupyter notebook Notebook/Notebook_1.ipynb
```

o subirse a Google Colab (en ese caso, subir el CSV al entorno y ajustar la ruta).

## Resultados de la evaluación

Evaluación sobre 56 consultas con película esperada (*ground truth*), con K = 5:

| Modelo | Hit Rate@5 | MRR |
|---|---|---|
| TF-IDF (léxico) | 87.50% | 0.8214 |
| Embeddings (semántico) | **94.64%** | **0.8405** |

El enfoque semántico supera al baseline léxico en ambas métricas, validando la ventaja
de las representaciones vectoriales frente a la coincidencia de palabras.

## Integrantes — Grupo 2

- Carmusciano, Lucas
- Minnaar, Santiago
- Cocco, Magdalena
- Medina, Jimena
