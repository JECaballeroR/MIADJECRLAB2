import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Fase 4 Lab 2 JECR", layout="wide")

#### FUNCIONES ###
@st.cache()
def plot_heatmap(df: pd.DataFrame, x: str, y: str):
    data_heatmap = (
        df.reset_index()[[x, y, "index"]]
        .groupby([x, y])
        .count()
        .reset_index()
        .pivot(x, y, "index")
        .fillna(0)
    )
    fig = px.imshow(
        data_heatmap,
        color_continuous_scale="Blues",
        aspect="auto",
        title=f"Heatmap {x} vs {y}",
    )
    fig.update_traces(
        hovertemplate="<b><i>"
        + y
        + "</i></b>: %{x} <br><b><i>"
        + x
        + "</i></b>: %{y} <br><b><i>Conteo interacción variables</i></b>: %{z}<extra></extra>"
    )
    return fig


@st.cache()
def cargar_datos():
    data20201 = pd.read_csv("Resultados__nicos_Saber_11_plain_20201.csv")
    data20211 = pd.read_csv("Resultados__nicos_Saber_11_plain_20211.csv")
    # Se concatenan los dos periodos de los datos
    data = pd.concat([data20201, data20211])

    data["PUNT_GLOBAL_CAT"] = data["PUNT_GLOBAL"].apply(
        lambda x: "BAJO (<=294)" if x <= 294 else "ALTO (>294)"
    )
    # Se presentan los datos seleccionados
    return data


data = cargar_datos()

st.sidebar.markdown("# Dashboard de exploración")

st.sidebar.image("logo.jpg", use_column_width=True)
st.sidebar.markdown(
    "## Fase 4 Entrega Laboratorio 2 de Jorge Esteban Caballero Rodríguez"
)

st.sidebar.markdown(
    "### Datos ICFES periodos 20201 y 20211, obtenidos de "
    "[https://www.datos.gov.co/Educaci-n/Resultados-nicos-Saber-11/kgxf-xxbe/data](https://www.datos.gov.co/Educaci-n/Resultados-nicos-Saber-11/kgxf-xxbe/data)"
)
st.sidebar.markdown(
    """A su derecha, tendrá una serie de gráficos con sus controladores
en la parte superior de los mismos.

Se han elegido 3 gráficos para explorar los datos:

- Un scatterplot, para comparar los puntajes entre si.
- Un countplot, para ver la distribución de los niveles de las variables categóricas.
    - Este gráfico además, separa cada nivel según su nivel de desempeño. 
- Un heatmap, para comparar las variables del modelo con la clasificación hecha del puntaje.
    - Este 

Dados los resultados obtenidos en la exploración y modelado, un puntaje se considera bajo si es menor o igual 
a 294 (de 500)


En cambio, los puntajes altos serán los superiores a 294"""
)

col1, col2 = st.columns(2)
col1.markdown(
    """## Scatterplot:
Comparación entre las variables asociadas al puntaje"""
)
col2.markdown(
    """## Countplot:
Comparación entre los conteos de las diferentes variables categóricas y el nivel de puntaje obtenido.

 
 **El nivel de puntaje es "BAJO" para puntajes de 294 o menos, ya alto para puntajes mayores a 294**"""
)
variables_numericas = [
    "PUNT_INGLES",
    "PUNT_MATEMATICAS",
    "PUNT_SOCIALES_CIUDADANAS",
    "PUNT_C_NATURALES",
    "PUNT_LECTURA_CRITICA",
    "PUNT_GLOBAL",
]
scatterx = col1.selectbox(
    label="Elija una de las variables numéricas para el eje X del Scatterplot",
    options=variables_numericas,
)
opciones_scatter2 = variables_numericas.copy()
opciones_scatter2.pop(variables_numericas.index(scatterx))
scattery = col1.selectbox(
    label="Elija una de las variables numéricas para el eje Y del Scatterplot",
    options=opciones_scatter2,
)


fig = px.scatter(
    data,
    x=scatterx,
    y=scattery,
)
fig.update_traces(
    marker=dict(size=7, line=dict(width=2, color="DarkSlateGrey")),
    selector=dict(mode="markers"),
    opacity=0.69,
)
col1.plotly_chart(fig, use_container_width=True)


histx = col2.selectbox(
    label="Elije la variable categórica para observar su conteo y distribución entre puntajes ALTO y BAJO",
    options=[
        "COLE_BILINGUE",
        "COLE_AREA_UBICACION",
        "COLE_CALENDARIO",
        "COLE_CARACTER",
        "COLE_GENERO",
        "COLE_JORNADA",
        "COLE_NATURALEZA",
        "COLE_DEPTO_UBICACION",
        "ESTU_GENERO",
        "FAMI_CUARTOSHOGAR",
        "FAMI_EDUCACIONMADRE",
        "FAMI_EDUCACIONPADRE",
        "FAMI_ESTRATOVIVIENDA",
        "FAMI_PERSONASHOGAR",
        "FAMI_TIENEAUTOMOVIL",
        "FAMI_TIENECOMPUTADOR",
        "FAMI_TIENEINTERNET",
        "FAMI_TIENELAVADORA",
    ],
)


def plot_histogram(data, x):
    df = data.copy()
    df = df.sort_values(by=x, ascending=False)

    fig = px.histogram(df, x=x, color="PUNT_GLOBAL_CAT")
    return fig


fig2 = plot_histogram(data, histx)
col2.plotly_chart(fig2, use_container_width=True)

st.markdown(
    """## Heatmap de PUNT_GLOBAL_CAT (clasificación del puntaje global) vs Otras variables categóricas. 

Las variables categóricas habilitadas son aquellas que llegaron al modelo final.

"""
)
heatmap_opcion = st.selectbox(
    label="Elige la opción de la variable a comparar con la clasificación del puntaje global",
    options=[
        "COLE_BILINGUE",
        "COLE_CALENDARIO",
        "COLE_JORNADA",
        "FAMI_EDUCACIONPADRE",
        "FAMI_TIENEAUTOMOVIL",
    ],
)

st.plotly_chart(
    plot_heatmap(data, "PUNT_GLOBAL_CAT", heatmap_opcion), use_container_width=True
)
