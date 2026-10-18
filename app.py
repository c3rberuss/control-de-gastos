# ============================================================
#  SISTEMA DE CONTROL DE GASTOS
#  Hecho con Python + Streamlit
#
#  Para ejecutarlo, escribe en la terminal:
#      streamlit run app.py
# ============================================================

# --- 1. IMPORTAR LIBRERÍAS ---------------------------------
# Las librerías son "herramientas" que otras personas ya programaron.
import os                       # Para revisar si un archivo existe
from datetime import date       # Para trabajar con fechas

import pandas as pd             # Para manejar tablas de datos
import plotly.express as px     # Para hacer gráficas bonitas
import streamlit as st          # Para crear la página web


# --- 2. CONFIGURACIÓN GENERAL ------------------------------
ARCHIVO = "gastos.csv"          # Archivo donde se guardan los gastos

# Lista de categorías que el usuario puede elegir
CATEGORIAS = [
    "Comida",
    "Transporte",
    "Estudios",
    "Entretenimiento",
    "Salud",
    "Ropa",
    "Otros",
]

# Título y diseño de la página
st.set_page_config(page_title="Control de Gastos", page_icon="💰", layout="wide")


# --- 3. FUNCIONES PARA LEER Y GUARDAR DATOS ----------------
def cargar_gastos():
    """Lee el archivo CSV. Si no existe, devuelve una tabla vacía."""
    if os.path.exists(ARCHIVO):
        datos = pd.read_csv(ARCHIVO)
        # Convertimos la columna "fecha" de texto a fecha real
        datos["fecha"] = pd.to_datetime(datos["fecha"])
        return datos
    # Si el archivo no existe todavía, creamos una tabla vacía
    return pd.DataFrame(columns=["fecha", "monto", "categoria", "descripcion"])


def guardar_gasto(fecha, monto, categoria, descripcion):
    """Agrega un gasto nuevo al final del archivo CSV."""
    nuevo = pd.DataFrame([{
        "fecha": fecha,
        "monto": monto,
        "categoria": categoria,
        "descripcion": descripcion,
    }])
    # Si el archivo ya existe, agregamos sin repetir los encabezados
    existe = os.path.exists(ARCHIVO)
    nuevo.to_csv(ARCHIVO, mode="a", header=not existe, index=False)


def borrar_gasto(numero_fila):
    """Borra un gasto usando su número de fila dentro del CSV."""
    datos = pd.read_csv(ARCHIVO)
    datos = datos.drop(index=numero_fila)       # Quitamos esa fila
    datos.to_csv(ARCHIVO, index=False)          # Guardamos el archivo de nuevo


# --- 4. ENCABEZADO DE LA PÁGINA ----------------------------
st.title("💰 Sistema de Control de Gastos")
st.write("Registra tus gastos y descubre en qué se va tu dinero.")

# Si en la vuelta anterior se borró un gasto, mostramos el aviso.
# (st.session_state es la "memoria" de la página entre recargas)
if "mensaje" in st.session_state:
    st.success(st.session_state.pop("mensaje"))


# --- 5. BARRA LATERAL: PRESUPUESTO Y FORMULARIO ------------
with st.sidebar:
    st.header("⚙️ Presupuesto")
    # El usuario elige cuánto quiere gastar como máximo al mes
    presupuesto = st.number_input(
        "Presupuesto mensual ($)", min_value=0.0, value=300.0, step=10.0
    )

    st.header("➕ Registrar gasto")
    # Un "form" agrupa los campos y solo se envía al presionar el botón
    with st.form("nuevo_gasto", clear_on_submit=True):
        fecha = st.date_input("Fecha", value=date.today())
        monto = st.number_input("Monto ($)", min_value=0.0, step=0.25)
        categoria = st.selectbox("Categoría", CATEGORIAS)
        descripcion = st.text_input("Descripción (opcional)")
        enviado = st.form_submit_button("Guardar gasto")

    # Qué pasa cuando presionan "Guardar gasto"
    if enviado:
        if monto <= 0:
            st.error("El monto debe ser mayor que cero.")
        else:
            guardar_gasto(fecha, monto, categoria, descripcion)
            st.success("¡Gasto guardado! ✅")


# --- 6. CARGAR LOS DATOS -----------------------------------
gastos = cargar_gastos()

# Si todavía no hay gastos, mostramos un mensaje y detenemos aquí
if gastos.empty:
    st.info("Aún no hay gastos registrados. Usa el formulario de la izquierda. 👈")
    st.stop()

# Creamos una columna "mes" (por ejemplo "2026-10") para poder agrupar
gastos["mes"] = gastos["fecha"].dt.strftime("%Y-%m")


# --- 7. FILTRO POR MES -------------------------------------
meses = sorted(gastos["mes"].unique(), reverse=True)   # Más reciente primero
mes_elegido = st.selectbox("📅 Ver mes:", meses)

# Nos quedamos solo con los gastos del mes elegido
gastos_mes = gastos[gastos["mes"] == mes_elegido]


# --- 8. RESUMEN EN NÚMEROS ---------------------------------
total_mes = gastos_mes["monto"].sum()
restante = presupuesto - total_mes

# Mostramos tres "tarjetas" con números importantes
col1, col2, col3 = st.columns(3)
col1.metric("Total gastado", f"${total_mes:,.2f}")
col2.metric("Presupuesto", f"${presupuesto:,.2f}")
col3.metric("Disponible", f"${restante:,.2f}")

# Barra de progreso: qué porcentaje del presupuesto ya se usó
if presupuesto > 0:
    porcentaje = total_mes / presupuesto
    st.progress(min(porcentaje, 1.0), text=f"Has usado el {porcentaje:.0%} de tu presupuesto")

    # Alertas según cuánto se ha gastado
    if porcentaje >= 1:
        st.error("🚨 ¡Te pasaste del presupuesto este mes!")
    elif porcentaje >= 0.8:
        st.warning("⚠️ Cuidado: ya usaste más del 80% de tu presupuesto.")


# --- 9. GRÁFICAS -------------------------------------------
izquierda, derecha = st.columns(2)

with izquierda:
    st.subheader("¿En qué gasto más?")
    # Sumamos los montos por categoría
    por_categoria = gastos_mes.groupby("categoria", as_index=False)["monto"].sum()
    grafica_pastel = px.pie(por_categoria, names="categoria", values="monto", hole=0.4)
    st.plotly_chart(grafica_pastel, width="stretch")

with derecha:
    st.subheader("Gasto total por mes")
    # Sumamos los montos de cada mes (de todos los meses)
    por_mes = gastos.groupby("mes", as_index=False)["monto"].sum()
    grafica_barras = px.bar(por_mes, x="mes", y="monto", text_auto=".2f")
    # Línea roja que marca el presupuesto
    grafica_barras.add_hline(y=presupuesto, line_dash="dash", line_color="red",
                             annotation_text="Presupuesto")
    st.plotly_chart(grafica_barras, width="stretch")


# --- 10. TABLA CON EL HISTORIAL ----------------------------
st.subheader("📋 Historial del mes")
tabla = gastos_mes.sort_values("fecha", ascending=False).copy()
tabla["fecha"] = tabla["fecha"].dt.strftime("%d/%m/%Y")   # Fecha en formato local
st.dataframe(
    tabla[["fecha", "categoria", "descripcion", "monto"]],
    width="stretch",
    hide_index=True,
)


# --- 11. BORRAR UN GASTO -----------------------------------
st.subheader("🗑️ Borrar un gasto")


def describir(numero_fila):
    """Convierte un gasto en un texto legible para la lista."""
    g = gastos.loc[numero_fila]
    descripcion = g["descripcion"] if pd.notna(g["descripcion"]) else "sin descripción"
    return f'{g["fecha"]:%d/%m/%Y} | {g["categoria"]} | {descripcion} | ${g["monto"]:.2f}'


# clear_on_submit=True limpia el formulario después de usarlo
with st.form("borrar_gasto", clear_on_submit=True):
    # Cada opción es el número de fila del gasto; format_func lo muestra bonito
    fila = st.selectbox(
        "Elige el gasto que quieres borrar",
        options=gastos_mes.sort_values("fecha", ascending=False).index,
        format_func=describir,
    )
    # Casilla de confirmación para evitar borrar por accidente
    confirmar = st.checkbox("Sí, estoy seguro de borrar este gasto")
    borrar = st.form_submit_button("Borrar gasto", type="primary")

if borrar:
    if not confirmar:
        st.warning("Marca la casilla de confirmación para poder borrar.")
    else:
        borrar_gasto(fila)
        st.session_state["mensaje"] = "Gasto borrado correctamente 🗑️"
        st.rerun()   # Recarga la página para que todo se actualice
