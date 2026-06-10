"""
=============================================================================
GENERADOR DE DATOS DE EJEMPLO
=============================================================================
Genera un CSV con datos ficticios de clientes de telecomunicaciones.
Se usa como input para las simulaciones del pipeline de datos.

Ejecutar: python generar_datos.py
Genera:   data/clientes_demo.csv
=============================================================================
"""

import csv
import random
from datetime import datetime, timedelta

random.seed(42)  # Semilla fija para resultados reproducibles

PLANES = ["Básico", "Standard", "Premium"]
NOMBRES = [
    "Juan García", "María López", "Carlos Martínez", "Ana Rodríguez",
    "Pedro Sánchez", "Laura Fernández", "Miguel Torres", "Sofía Ramírez",
    "Diego Flores", "Valentina Herrera", "Lucas Morales", "Camila Jiménez"
]

def generar_clientes(cantidad: int = 100) -> list:
    """Genera una lista de clientes con datos ficticios."""
    clientes = []
    fecha_base = datetime(2022, 1, 1)

    for i in range(1, cantidad + 1):
        meses_activo = random.randint(1, 48)
        fecha_alta = fecha_base + timedelta(days=random.randint(0, 730))

        # Probabilidad de churn más alta para clientes nuevos y plan básico
        plan = random.choice(PLANES)
        base_churn = {"Básico": 0.6, "Standard": 0.3, "Premium": 0.15}[plan]
        if meses_activo < 6:
            base_churn += 0.2
        prob_churn = round(min(base_churn + random.uniform(-0.1, 0.2), 1.0), 2)

        segmento = (
            "Alto" if prob_churn > 0.7
            else "Medio" if prob_churn > 0.4
            else "Bajo"
        )

        clientes.append({
            "cliente_id": 1000 + i,
            "nombre": random.choice(NOMBRES),
            "plan": plan,
            "meses_activo": meses_activo,
            "fecha_alta": fecha_alta.strftime("%Y-%m-%d"),
            "prob_churn": prob_churn,
            "segmento_riesgo": segmento,
            "llamadas_soporte": random.randint(0, 10),
            "consumo_gb_mes": round(random.uniform(1, 50), 1),
        })

    return clientes


def guardar_csv(clientes: list, ruta: str):
    """Guarda la lista de clientes en un archivo CSV."""
    if not clientes:
        return

    with open(ruta, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=clientes[0].keys())
        writer.writeheader()
        writer.writerows(clientes)

    print(f"✅ Archivo generado: {ruta} ({len(clientes)} clientes)")


def mostrar_resumen(clientes: list):
    """Muestra estadísticas básicas del dataset generado."""
    total = len(clientes)
    alto = sum(1 for c in clientes if c["segmento_riesgo"] == "Alto")
    medio = sum(1 for c in clientes if c["segmento_riesgo"] == "Medio")
    bajo = sum(1 for c in clientes if c["segmento_riesgo"] == "Bajo")
    churn_prom = sum(c["prob_churn"] for c in clientes) / total

    print("\n📊 Resumen del dataset generado:")
    print(f"   Total de clientes:   {total}")
    print(f"   Riesgo Alto:         {alto} ({100*alto//total}%)")
    print(f"   Riesgo Medio:        {medio} ({100*medio//total}%)")
    print(f"   Riesgo Bajo:         {bajo} ({100*bajo//total}%)")
    print(f"   Churn promedio:      {churn_prom:.2f}")
    print(f"\n   Primeras 3 filas:")
    for cliente in clientes[:3]:
        print(f"   {cliente}")


if __name__ == "__main__":
    import os
    os.makedirs("data", exist_ok=True)

    print("Generando datos de ejemplo para el pipeline...")
    clientes = generar_clientes(cantidad=200)
    guardar_csv(clientes, "data/clientes_demo.csv")
    mostrar_resumen(clientes)
    print("\n✅ Listo. Usá este archivo como input para las simulaciones.")
