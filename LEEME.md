# 💰 Sistema de Control de Gastos (Python + Streamlit)

## Archivos del proyecto
| Archivo | Para qué sirve |
|---|---|
| `app.py` | El sistema completo (la página web). |
| `requirements.txt` | Lista de librerías que necesita el proyecto. |
| `generar_datos_ejemplo.py` | Crea 3 meses de gastos de ejemplo para la demostración. |
| `gastos.csv` | Se crea solo. Ahí se guardan los gastos (se puede abrir con Excel). |

---

## Opción A: ejecutarlo en tu computadora

1. **Instalar Python** desde https://www.python.org/downloads/
   - En Windows, marca la casilla **"Add Python to PATH"** al instalar.
2. **Poner los archivos en una carpeta**, por ejemplo `control_gastos`.
3. **Abrir una terminal en esa carpeta.**
   - Windows: abre la carpeta, escribe `cmd` en la barra de dirección y presiona Enter.
   - Mac: clic derecho en la carpeta → "Nuevo terminal en la carpeta".
4. **Instalar las librerías** (solo la primera vez):
   ```
   pip install -r requirements.txt
   ```
5. **(Opcional) Crear datos de ejemplo** para que la app no se vea vacía:
   ```
   python generar_datos_ejemplo.py
   ```
6. **Ejecutar el sistema:**
   ```
   streamlit run app.py
   ```
   Se abrirá solo en el navegador. Para detenerlo, presiona `Ctrl + C` en la terminal.

> Si `pip` o `python` no funcionan, prueben con `pip3` y `python3`, o con `py -m pip` en Windows.

---

## Opción B: publicarlo en internet (para el código QR de la feria)

1. Crear una cuenta gratis en https://github.com y subir los archivos a un repositorio nuevo
   (botón **"Add file → Upload files"**). Incluyan `gastos.csv` si quieren los datos de ejemplo.
2. Entrar a https://share.streamlit.io con esa cuenta de GitHub.
3. Presionar **"Create app"**, elegir el repositorio y el archivo `app.py`, y luego **"Deploy"**.
4. Copiar el enlace que les dan y convertirlo en código QR (por ejemplo en https://www.qrcode-monkey.com).

> ⚠️ En la versión publicada, los gastos nuevos se borran cuando la app se reinicia
> (vuelven los datos de ejemplo). Para la feria no es problema; solo tenganlo presente
> por si el jurado pregunta. Una mejora futura sería usar una base de datos.

---

## Cómo funciona (para explicarlo en la feria)

1. **Registro:** el formulario de la izquierda pide fecha, monto, categoría y descripción.
2. **Almacenamiento:** cada gasto se guarda como una fila nueva en `gastos.csv`.
3. **Procesamiento:** con *pandas* se suman los gastos por categoría y por mes.
4. **Visualización:** con *plotly* se muestran una gráfica de pastel y una de barras.
5. **Alertas:** si se usa más del 80 % del presupuesto aparece una advertencia, y si se pasa del 100 %, una alerta roja.
6. **Borrar:** al final de la página se elige un gasto, se marca la casilla de confirmación y se borra del archivo.

## Ideas para mejorarlo (si les sobra tiempo)
- Descargar el reporte del mes en Excel.
- Presupuesto distinto por categoría.
- Agregar ingresos además de gastos.

## Guion corto para la presentación
1. **Problema:** "Muchos estudiantes no saben en qué se les va el dinero."
2. **Solución:** mostrar la app y registrar un gasto en vivo.
3. **Resultado:** señalar cómo cambian la gráfica y la barra de presupuesto.
4. **Aprendizaje:** qué aprendieron de Python, datos y gráficas.
