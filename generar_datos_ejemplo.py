# ============================================================
#  Genera gastos de ejemplo (3 meses) para que la app
#  no se vea vacía en la feria.
#  Ejecutar UNA vez:   python generar_datos_ejemplo.py
# ============================================================
import random
from datetime import date, timedelta

import pandas as pd

random.seed(7)  # Para que siempre salgan los mismos datos

# Cada categoría con ejemplos de descripción y rango de precios
EJEMPLOS = {
    "Comida": (["Almuerzo", "Pupusas", "Café", "Supermercado"], 2, 15),
    "Transporte": (["Bus", "Uber", "Gasolina"], 0.5, 12),
    "Estudios": (["Copias", "Cuaderno", "Libro"], 1, 25),
    "Entretenimiento": (["Cine", "Videojuego", "Salida con amigos"], 5, 30),
    "Salud": (["Farmacia", "Consulta"], 3, 40),
    "Ropa": (["Camisa", "Zapatos"], 10, 45),
    "Otros": (["Recarga celular", "Regalo"], 2, 20),
}

hoy = date.today()
filas = []
for _ in range(90):  # 90 gastos repartidos en ~3 meses
    categoria = random.choice(list(EJEMPLOS))
    descripciones, minimo, maximo = EJEMPLOS[categoria]
    filas.append({
        "fecha": hoy - timedelta(days=random.randint(0, 85)),
        "monto": round(random.uniform(minimo, maximo), 2),
        "categoria": categoria,
        "descripcion": random.choice(descripciones),
    })

pd.DataFrame(filas).sort_values("fecha").to_csv("gastos.csv", index=False)
print("Listo: se creó gastos.csv con 90 gastos de ejemplo.")
