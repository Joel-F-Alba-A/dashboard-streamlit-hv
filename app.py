# app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt

# =========================================================
# CONFIGURACIÓN GENERAL
# =========================================================

st.set_page_config(
    page_title="Retail Sales Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# PALETA DE COLORES
# =========================================================

BACKGROUND = "#F8FAFC"

PRIMARY = "#1D4ED8"
SECONDARY = "#93C5FD"

TEXT = "#0F172A"
TEXT2 = "#475569"

GRID = "#CBD5E1"

# =========================================================
# CSS PREMIUM
# =========================================================

st.markdown(
    f"""
    <style>

    /* =====================================================
       FONDO GENERAL
    ===================================================== */

    .stApp {{
        background: linear-gradient(
            180deg,
            #F8FAFC 0%,
            #EEF2FF 100%
        );
    }}

    /* =====================================================
       TEXTO GENERAL
    ===================================================== */

    html, body, p, div, span, label {{
        color: {TEXT};
    }}

    /* =====================================================
       TÍTULO PRINCIPAL
    ===================================================== */

    h1 {{
        color: {TEXT} !important;

        font-size: 64px !important;

        font-weight: 900 !important;

        letter-spacing: -1px !important;

        margin-bottom: 10px !important;
    }}

    /* =====================================================
       SUBTÍTULOS
    ===================================================== */

    h2 {{
        color: {TEXT} !important;
        font-size: 40px !important;
        font-weight: 800 !important;
    }}

    h3 {{
        color: {TEXT} !important;
        font-size: 32px !important;
        font-weight: 800 !important;
    }}

    /* =====================================================
       TEXTO
    ===================================================== */

    p {{
        font-size: 21px !important;
    }}

    /* =====================================================
       SIDEBAR
    ===================================================== */

    section[data-testid="stSidebar"] {{

        background: linear-gradient(
            180deg,
            #E0E7FF 0%,
            #DBEAFE 100%
        );

        border-right: 1px solid #CBD5E1;
    }}

    section[data-testid="stSidebar"] * {{

        font-size: 19px !important;

        color: #0F172A !important;
    }}

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {{

        font-size: 30px !important;

        font-weight: 800 !important;
    }}

    /* =====================================================
       SELECTBOX
    ===================================================== */

    div[data-baseweb="select"] {{

        background-color: white !important;

        border-radius: 14px !important;

        border: 1px solid #CBD5E1 !important;
    }}

    /* =====================================================
       MÉTRICAS
    ===================================================== */

    div[data-testid="metric-container"] {{

        background: linear-gradient(
            180deg,
            #FFFFFF 0%,
            #F8FAFC 100%
        );

        border: 1px solid #D6E0F0;

        padding: 32px;

        border-radius: 24px;

        box-shadow:
            0px 4px 14px rgba(0,0,0,0.06);

        transition: 0.2s ease-in-out;
    }}

    div[data-testid="metric-container"]:hover {{

        transform: translateY(-3px);

        box-shadow:
            0px 8px 18px rgba(0,0,0,0.08);
    }}

    div[data-testid="metric-container"] label {{

        color: {TEXT2} !important;

        font-weight: 700 !important;

        font-size: 20px !important;
    }}

    div[data-testid="metric-container"]
    [data-testid="stMetricValue"] {{

        color: {PRIMARY};

        font-size: 44px !important;

        font-weight: 900 !important;
    }}

    /* =====================================================
       TABS
    ===================================================== */

    button[data-baseweb="tab"] {{

        background-color: white !important;

        border-radius: 14px 14px 0px 0px !important;

        margin-right: 8px;

        padding: 14px 26px !important;

        font-size: 22px !important;

        font-weight: 800 !important;

        border: 1px solid #CBD5E1 !important;
    }}

    button[data-baseweb="tab"][aria-selected="true"] {{

        background-color: #DBEAFE !important;

        color: {PRIMARY} !important;
    }}

    /* =====================================================
       ESPACIADO COLUMNAS
    ===================================================== */

    [data-testid="column"] {{

        padding-left: 18px !important;

        padding-right: 18px !important;
    }}

    /* =====================================================
       GRÁFICOS
    ===================================================== */

    div[data-testid="stPlotlyChart"] {{

        background-color: white;

        padding: 10px;

        overflow: hidden;

        margin-bottom: 30px !important;

        border-radius: 20px;

        border: 1px solid #E2E8F0;

        box-shadow:
            0px 3px 10px rgba(0,0,0,0.04);
    }}

    .vega-embed {{

        background-color: white;

        padding: 24px;

        margin-bottom: 30px !important;

        border-radius: 20px;

        border: 1px solid #E2E8F0;

        box-shadow:
            0px 3px 10px rgba(0,0,0,0.04);
    }}

    /* =====================================================
       TABLA
    ===================================================== */

    .stDataFrame {{

        border-radius: 20px;

        overflow: hidden;

        border: 1px solid #CBD5E1;

        background-color: white;
    }}

    /* =====================================================
       ALERTAS
    ===================================================== */

    div[data-testid="stAlert"] {{

        font-size: 18px !important;

        border-radius: 14px;

        border: none;
    }}

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# HEADER
# =========================================================

st.title("🛒 Retail Sales Dashboard")

st.markdown(
    f"""
    <p style='font-size:22px; color:{TEXT2}; margin-top:-10px;'>
    Análisis académico del comportamiento de ventas y clientes
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

# =========================================================
# CARGA DATOS
# =========================================================

@st.cache_data
def cargar_datos():

    return pd.read_csv(
        "data/retail_sales_dataset.csv"
    )

try:

    df = cargar_datos()

except FileNotFoundError:

    st.error(
        "❌ No se encontró el archivo retail_sales_dataset.csv"
    )

    st.stop()

except Exception as e:

    st.error(
        f"❌ Error al cargar archivo: {e}"
    )

    st.stop()

# =========================================================
# VALIDACIONES
# =========================================================

columnas_requeridas = [
    "Transaction ID",
    "Date",
    "Customer ID",
    "Gender",
    "Age",
    "Product Category",
    "Quantity",
    "Price per Unit",
    "Total Amount"
]

faltantes = [
    col for col in columnas_requeridas
    if col not in df.columns
]

if faltantes:

    st.error(
        f"❌ Faltan columnas requeridas: {faltantes}"
    )

    st.stop()

df["Date"] = pd.to_datetime(df["Date"])

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("⚙️ Filtros")

categorias = st.sidebar.multiselect(
    "Categoría de producto",
    options=df["Product Category"].unique(),
    default=df["Product Category"].unique()
)

generos = st.sidebar.multiselect(
    "Género",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

# =========================================================
# VALIDACIONES FILTROS
# =========================================================

if len(categorias) == 0:

    st.warning(
        "⚠️ Debe seleccionar al menos una categoría."
    )

    st.stop()

if len(generos) == 0:

    st.warning(
        "⚠️ Debe seleccionar al menos un género."
    )

    st.stop()

# =========================================================
# FILTRADO
# =========================================================

df_filtrado = df[
    (df["Product Category"].isin(categorias)) &
    (df["Gender"].isin(generos))
]

if df_filtrado.empty:

    st.warning(
        "⚠️ No existen datos para los filtros seleccionados."
    )

    st.stop()

# =========================================================
# KPIs
# =========================================================

ventas = df_filtrado["Total Amount"].sum()

clientes = df_filtrado["Customer ID"].nunique()

productos = df_filtrado["Quantity"].sum()

ticket = df_filtrado["Total Amount"].mean()

st.subheader("📊 Indicadores Principales")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Ventas Totales",
    f"${ventas:,.0f}"
)

c2.metric(
    "Clientes Únicos",
    f"{clientes:,}"
)

c3.metric(
    "Productos Vendidos",
    f"{productos:,}"
)

c4.metric(
    "Ticket Promedio",
    f"${ticket:,.2f}"
)

st.divider()

# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3 = st.tabs([
    "📈 Tendencias",
    "📊 Comparaciones",
    "📋 Datos"
])

# =========================================================
# TAB 1
# =========================================================

with tab1:

    st.subheader(
        "📈 Evolución Temporal de Ventas"
    )

    ventas_fecha = (
        df_filtrado
        .groupby("Date")["Total Amount"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        ventas_fecha,
        x="Date",
        y="Total Amount",
        markers=True,
        title="Ventas Totales por Fecha"
    )

    fig.update_traces(
        line=dict(
            color=PRIMARY,
            width=5
        ),
        marker=dict(
            color=PRIMARY,
            size=9
        )
    )

    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",

        font=dict(
            color=TEXT,
            size=16
        ),

        title_font_size=28,

        xaxis=dict(
            title="Fecha",
            title_font=dict(size=18),
            tickfont=dict(size=15),
            showgrid=False
        ),

        yaxis=dict(
            title="Ventas Totales",
            title_font=dict(size=18),
            tickfont=dict(size=15),
            gridcolor=GRID,
            rangemode="tozero"
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    promedio_ventas = (
        ventas_fecha["Total Amount"]
        .mean()
    )

    max_ventas = (
        ventas_fecha["Total Amount"]
        .max()
    )

    fecha_max = (
        ventas_fecha
        .sort_values(
            by="Total Amount",
            ascending=False
        )
        .iloc[0]["Date"]
        .strftime("%Y-%m-%d")
    )

    st.markdown(
        f"""
        <div style="
            background-color:#DBEAFE;
            padding:20px;
            border-radius:16px;
            border-left:6px solid {PRIMARY};
            font-size:20px;
            color:{TEXT};
            line-height:1.7;
            margin-top:10px;
        ">
        <b>Interpretación:</b><br>

        Las ventas presentan un promedio de
        <b>${promedio_ventas:,.0f}</b>
        por periodo analizado.

        El punto más alto de ventas se registró el
        <b>{fecha_max}</b>,
        alcanzando aproximadamente
        <b>${max_ventas:,.0f}</b>.

        La tendencia observada permite identificar
        estabilidad comercial y comportamiento
        de crecimiento en las ventas.
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# TAB 2
# =========================================================

with tab2:

    col1, col2 = st.columns(
        2,
        gap="large"
    )

    # =====================================================
    # GRÁFICO CATEGORÍAS
    # =====================================================

    with col1:

        st.subheader("📦 Ventas por Categoría")

        categoria = (
            df_filtrado
            .groupby("Product Category")
            ["Total Amount"]
            .sum()
            .reset_index()
        )

        max_y = (
            categoria["Total Amount"]
            .max() * 1.15
        )

        chart = alt.Chart(categoria).mark_bar(
            color=PRIMARY,
            cornerRadiusTopLeft=8,
            cornerRadiusTopRight=8
        ).encode(

            x=alt.X(
                "Product Category:N",
                title="Categoría",
                sort="-y",
                axis=alt.Axis(
                    labelAngle=-45
                )
            ),

            y=alt.Y(
                "Total Amount:Q",
                title="Ventas Totales",
                scale=alt.Scale(
                    domain=[0, max_y]
                )
            )
        ).properties(
            title="Ventas Totales por Categoría",
            width=450,
            height=420
        )

        texto = chart.mark_text(
            align='center',
            baseline='bottom',
            dy=-5,
            color=TEXT,
            fontSize=14,
            fontWeight="bold"
        ).encode(

            text=alt.Text(
                "Total Amount:Q",
                format=",.0f"
            )
        )

        grafico_final = (
            chart + texto
        ).configure(
            background="white"
        ).configure_axis(
            labelColor=TEXT,
            titleColor=TEXT,
            gridColor=GRID,
            labelFontSize=14,
            titleFontSize=16
        ).configure_title(
            color=TEXT,
            fontSize=22
        )

        st.altair_chart(
            grafico_final,
            use_container_width=True
        )

        mejor_categoria = categoria.sort_values(
            by="Total Amount",
            ascending=False
        ).iloc[0]["Product Category"]

        porcentaje_categoria = (
            categoria["Total Amount"].max()
            /
            categoria["Total Amount"].sum()
        )

        st.markdown(
            f"""
            <div style="
                background-color:#DBEAFE;
                padding:20px;
                border-radius:16px;
                border-left:6px solid {PRIMARY};
                font-size:20px;
                color:{TEXT};
                line-height:1.7;
                margin-top:10px;
            ">
            <b>Interpretación:</b><br>
            La categoría con mayor volumen de ventas es
            <b>{mejor_categoria}</b>,
            representando aproximadamente
            <b>{porcentaje_categoria:.1%}</b>
            de las ventas totales.
            Esto evidencia una mayor preferencia de consumo
            hacia esta línea de productos.
            </div>
            """,
            unsafe_allow_html=True
        )

    # =====================================================
    # GRÁFICO GÉNERO
    # =====================================================

    with col2:

        st.subheader(
            "👥 Participación de Ventas por Género"
        )

        genero = (
            df_filtrado
            .groupby("Gender")
            ["Total Amount"]
            .sum()
            .reset_index()
        )

        fig2 = px.pie(
            genero,
            names="Gender",
            values="Total Amount",
            hole=0.55,
            title="Distribución de Ventas por Género"
        )

        fig2.update_traces(

            textinfo="percent+label",

            textfont_size=15,

            marker=dict(
                colors=[
                    PRIMARY,
                    SECONDARY
                ],
                line=dict(
                    color="white",
                    width=2
                )
            ),

            pull=[0.02, 0.02]
        )

        fig2.update_layout(
            autosize=True,
            paper_bgcolor="white",
            plot_bgcolor="white",

            font=dict(
                color=TEXT,
                size=15
            ),

            title_font_size=22,

            height=380,
            width=380,

            margin=dict(
                l=20,
                r=20,
                t=70,
                b=20
            ),

            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.15,
                xanchor="center",
                x=0.5,
                font=dict(size=14)
            )
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

        genero_top = genero.sort_values(
            by="Total Amount",
            ascending=False
        ).iloc[0]["Gender"]

        porcentaje_top = (
            genero["Total Amount"].max()
            /
            genero["Total Amount"].sum()
        )

        st.markdown(
            f"""
            <div style="
                background-color:#DBEAFE;
                padding:20px;
                border-radius:16px;
                border-left:6px solid {PRIMARY};
                font-size:20px;
                color:{TEXT};
                line-height:1.7;
                margin-top:10px;
            ">
            <b>Interpretación:</b><br>

            El género con mayor participación en ventas es
            <b>{genero_top}</b>,
            representando aproximadamente
            <b>{porcentaje_top:.1%}</b>
            del total de ingresos.

            Esto sugiere un comportamiento de compra
            más activo dentro de este segmento.
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================================================
# TAB 3
# =========================================================

with tab3:

    st.subheader("📋 Datos Filtrados")

    st.dataframe(
        df_filtrado.sort_values("Date"),
        use_container_width=True
    )