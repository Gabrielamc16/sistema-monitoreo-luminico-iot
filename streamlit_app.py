import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ============================
# Configuración de la página
# ============================
st.set_page_config(
    page_title="Análisis de Luminosidad IoT",
    page_icon="💡",
    layout="wide"
)

st.title("💡 Análisis de Luminosidad - Proyecto IoT")
st.markdown("**Flujo:** Sensor LDR → ESP32 → InfluxDB → Análisis en Streamlit")
st.markdown("---")

# ============================
# Cargar datos
# ============================
@st.cache_data
def cargar_datos_default():
    df = pd.read_csv("datos_luminosidad.csv")
    df['tiempo'] = pd.to_datetime(df['tiempo'])
    return df

st.sidebar.header("⚙️ Opciones")
archivo = st.sidebar.file_uploader("Cargar otro CSV (opcional)", type=['csv'])

if archivo is not None:
    df = pd.read_csv(archivo)
    df['tiempo'] = pd.to_datetime(df['tiempo'])
    st.sidebar.success("CSV personalizado cargado")
else:
    df = cargar_datos_default()
    st.sidebar.info("Usando datos por defecto")

# ============================
# Clasificación
# ============================
def clasificar_luz(valor):
    if valor < 1000: return "Oscuro"
    elif valor < 2500: return "Tenue"
    elif valor < 3500: return "Iluminado"
    else: return "Muy iluminado"

if 'categoria' not in df.columns:
    df['categoria'] = df['luminosidad'].apply(clasificar_luz)

# ============================
# Métricas
# ============================
st.subheader("📊 Métricas generales")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total lecturas", len(df))
c2.metric("Promedio", f"{df['luminosidad'].mean():.0f}")
c3.metric("Máximo", int(df['luminosidad'].max()))
c4.metric("Mínimo", int(df['luminosidad'].min()))

st.markdown("---")

# ============================
# Gráfica 1: serie temporal
# ============================
st.subheader("📈 Luminosidad en el tiempo")
fig1, ax1 = plt.subplots(figsize=(12, 4))
ax1.plot(df['tiempo'], df['luminosidad'], color='orange', linewidth=1.5)
ax1.set_xlabel("Tiempo")
ax1.set_ylabel("Nivel de luz (ADC)")
ax1.grid(True, alpha=0.3)
ax1.tick_params(axis='x', rotation=30)
st.pyplot(fig1)

# ============================
# Gráfica 2: histograma
# ============================
st.subheader("📊 Distribución de lecturas")
fig2, ax2 = plt.subplots(figsize=(10, 4))
ax2.hist(df['luminosidad'], bins=30, color='steelblue', edgecolor='black')
ax2.set_xlabel("Nivel de luz")
ax2.set_ylabel("Frecuencia")
ax2.grid(True, alpha=0.3)
st.pyplot(fig2)

# ============================
# Gráfica 3: categorías
# ============================
st.subheader("🌗 Distribución por nivel de iluminación")
col_a, col_b = st.columns([2, 1])

with col_a:
    conteo = df['categoria'].value_counts()
    orden = ['Oscuro', 'Tenue', 'Iluminado', 'Muy iluminado']
    conteo = conteo.reindex([c for c in orden if c in conteo.index])
    colores = ['#1a1a1a', '#666666', '#f5b041', '#f1c40f']
    fig3, ax3 = plt.subplots(figsize=(8, 4))
    ax3.bar(conteo.index, conteo.values, color=colores[:len(conteo)])
    ax3.set_ylabel("Cantidad de lecturas")
    ax3.grid(True, alpha=0.3, axis='y')
    st.pyplot(fig3)

with col_b:
    st.write("**Porcentajes:**")
    porc = (conteo / len(df) * 100).round(2)
    for cat, pct in porc.items():
        st.write(f"- **{cat}**: {pct} %")

# ============================
# Tabla de datos
# ============================
st.markdown("---")
st.subheader("📋 Últimas 50 lecturas")
st.dataframe(df.tail(50), use_container_width=True)

st.markdown("---")
st.caption("Proyecto IoT integrado al análisis de datos · ESP32 + InfluxDB + Grafana + Streamlit")
