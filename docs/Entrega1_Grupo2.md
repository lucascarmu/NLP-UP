TRABAJO PRÁCTICO

Procesamiento de Lenguaje Natural

Trabajo Integrador Grupal – Primera parte

Grupo 2

Legajo  Apellido y Nombre
0136221 - Carmusciano Lucas - lucascarmusciano@gmail.com
0142480 - Minnaar Santiago - santyminnaard@gmail.com
0133718 - Cocco Magdalena - maguicocco@gmail.com
0147233 - Medina Jimena- medina.jime@gmail.com

e-mail

Carrera: Ingeniería/Licenciatura en Inteligencia Artificial

Turno: Modalidad Online (Asincrónico)

Docente: Victor Ezequiel Muñoz

Fecha de entrega: 31/03/26 20:00 (UTC-3)

1

Facultad de Ingeniería

Índice

Etapa Número 1

Planteamiento del problema: descripción breve

Métodos a utilizar: técnicas de NLP a aplicar

Dataset: Descripción y origen

Resultados: Resultados esperados y cómo se van a presentar

3

3

3

4

4

1

Facultad de Ingeniería

Etapa Número 1

Planteamiento del problema: descripción breve

En la actualidad, la búsqueda de películas suele basarse en coincidencias exactas de título,
género o actores, lo que limita la capacidad del usuario para encontrar contenidos cuando solo
recuerda fragmentos, descripciones vagas o características parciales de una película.

El problema que se propone abordar es el desarrollo de un sistema de búsqueda semántica de
películas, capaz de interpretar descripciones libres ingresadas por el usuario (por ejemplo: “una
película donde el protagonista pierde la memoria y hay viajes en el tiempo”) y recuperar
aquellas películas cuya información textual sea semánticamente similar a dicha descripción.

El enfoque adoptado se basa en técnicas de Procesamiento de Lenguaje Natural (NLP),
utilizando representaciones vectoriales del texto (embeddings multilingües) para comparar la
similitud semántica entre la consulta del usuario y la información asociada a cada película.

Métodos a utilizar: técnicas de NLP a aplicar

Para resolver el problema se aplicarán las siguientes técnicas y herramientas de NLP:

Preprocesamiento de texto:

●  Normalización (minúsculas, eliminación de caracteres especiales)
●  Tokenización
●  Eliminación de stopwords (opcional según modelo)

Representación semántica:

●  Generación de embeddings a partir de textos descriptivos de películas (sinopsis,

géneros, actores, keywords)

●  Uso de modelos preentrenados (por ejemplo: Sentence Transformers o similares)

Cálculo de similitud:

●  Similitud del coseno entre el embedding de la consulta y los embeddings de las

películas

Recuperación de información:

●  Ranking de películas según similitud
●  Devolución de los resultados más relevantes (Top-N)

1

Facultad de Ingeniería

Herramientas y entorno:

●  Python
●  Librerías: pandas, numpy, scikit-learn, sentence-transformers
●  Entorno de desarrollo: Google Colab o Jupyter Notebook

Dataset: Descripción y origen

El dataset será construido a partir de la API de películas The Movie Database (TMDB).

Se utilizarán los siguientes campos para cada película:

●  Título
●  Sinopsis (overview)
●  Géneros
●  Actores principales
●  Palabras clave (keywords)
●  Año de lanzamiento

La API permite obtener información actualizada y estructurada sobre películas, lo que facilita la
construcción dinámica del dataset.

Adicionalmente, se podrá complementar con datasets públicos como MovieLens para
enriquecer el análisis si fuera necesario.

Resultados: Resultados esperados y cómo se van a presentar

Se espera desarrollar un sistema funcional capaz de:

●  Recibir descripciones textuales libres del usuario
●
Interpretar el significado semántico de la consulta
●  Recuperar un conjunto de películas relevantes ordenadas por similitud

Los resultados se presentarán en forma de:

●  Lista de películas recomendadas (Top-5 o Top-10)
●  Puntaje de similitud asociado a cada resultado

Como métrica de evaluación preliminar se utilizará:

●  Evaluación cualitativa, verificando si las películas recuperadas son coherentes con la

consulta

1

●  Posible uso de métricas de recuperación como precisión en Top-N (si se dispone de

casos de prueba)

Facultad de Ingeniería


