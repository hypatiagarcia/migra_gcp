"""
=============================================================================
COMPARACIÓN DIRECTA: On-Premise vs GCP
=============================================================================
Este script ejecuta el MISMO escenario en ambos sistemas y muestra
una comparativa de resultados lado a lado.

Útil para la presentación del trabajo práctico: demuestra de forma
visual y cuantitativa por qué la migración vale la pena.
=============================================================================
"""

import time
import threading
from datetime import datetime

# Importamos las simulaciones de los módulos anteriores
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import importlib.util

def _cargar_modulo(nombre, ruta):
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo

_dir = os.path.dirname(__file__)
mod_onpremise = _cargar_modulo("mod_onpremise", os.path.join(_dir, "01_sistema_onpremise.py"))
mod_gcp = _cargar_modulo("mod_gcp", os.path.join(_dir, "02_sistema_gcp.py"))

ClusterOnPremise = mod_onpremise.ClusterOnPremise
CloudStorage = mod_gcp.CloudStorage
DataprocCluster = mod_gcp.DataprocCluster
BigQuery = mod_gcp.BigQuery


def medir_tiempo(func):
    """Decorador para medir cuánto tarda una función."""
    inicio = time.time()
    resultado = func()
    fin = time.time()
    return resultado, round(fin - inicio, 2)


def escenario_onpremise():
    """
    Escenario: dos analistas intentan trabajar en paralelo.
    Resultado esperado en on-premise: uno de los dos falla.
    """
    cluster = ClusterOnPremise()
    resultados = {"exitosos": 0, "fallidos": 0, "errores": []}

    def trabajo(nombre, ram):
        ok = cluster.ejecutar_trabajo(nombre, ram, duracion_seg=1)
        if ok:
            resultados["exitosos"] += 1
        else:
            resultados["fallidos"] += 1
            resultados["errores"].append(nombre)

    hilos = [
        threading.Thread(target=trabajo, args=("Entrenamiento Modelo A", 40)),
        threading.Thread(target=trabajo, args=("Transformación Datos B", 35)),
    ]
    for h in hilos:
        h.start()
        time.sleep(0.05)
    for h in hilos:
        h.join()

    return resultados


def escenario_gcp():
    """
    Mismo escenario en GCP.
    Resultado esperado: ambos trabajos completan exitosamente.
    """
    storage = CloudStorage()
    storage.subir_archivo("raw", "datos.parquet", {"filas": 1_000_000})

    resultados = {"exitosos": 0, "fallidos": 0, "errores": []}

    def trabajo(nombre, ram):
        cluster = DataprocCluster(nombre.replace(" ", ""), workers=4)
        cluster.conectar_storage(storage)
        cluster.crear_cluster()
        ok = cluster.ejecutar_pyspark(nombre, "raw", "processed", ram, duracion_seg=1)
        cluster.destruir_cluster()
        if ok:
            resultados["exitosos"] += 1
        else:
            resultados["fallidos"] += 1
            resultados["errores"].append(nombre)

    hilos = [
        threading.Thread(target=trabajo, args=("Entrenamiento Modelo A", 40)),
        threading.Thread(target=trabajo, args=("Transformación Datos B", 35)),
    ]
    for h in hilos:
        h.start()
    for h in hilos:
        h.join()

    return resultados


# =============================================================================
# MAIN: Ejecuta ambos escenarios y muestra la tabla comparativa
# =============================================================================

if __name__ == "__main__":
    print("\n╔══════════════════════════════════════════════════════════╗")
    print("║         COMPARACIÓN: ON-PREMISE vs GCP                  ║")
    print("╚══════════════════════════════════════════════════════════╝")

    print("\n⏳ Ejecutando escenario ON-PREMISE...")
    print("-" * 50)
    res_onpremise, tiempo_op = medir_tiempo(escenario_onpremise)

    print("\n⏳ Ejecutando escenario GCP...")
    print("-" * 50)
    res_gcp, tiempo_gcp = medir_tiempo(escenario_gcp)

    # Tabla comparativa de resultados
    print("\n")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                   RESULTADOS COMPARATIVOS                   ║")
    print("╠════════════════════════════╦═══════════════╦════════════════╣")
    print("║ Métrica                    ║  On-Premise   ║      GCP       ║")
    print("╠════════════════════════════╬═══════════════╬════════════════╣")
    print(f"║ Trabajos exitosos          ║      {res_onpremise['exitosos']}          ║       {res_gcp['exitosos']}        ║")
    print(f"║ Trabajos fallidos          ║      {res_onpremise['fallidos']}          ║       {res_gcp['fallidos']}        ║")
    print(f"║ Tiempo total (simulación)  ║   {tiempo_op}s         ║    {tiempo_gcp}s       ║")
    print(f"║ Trabajo en paralelo        ║      ❌ No     ║      ✅ Sí     ║")
    print(f"║ Auto-scaling disponible    ║      ❌ No     ║      ✅ Sí     ║")
    print(f"║ Costo cuando está inactivo ║   💰 Siempre  ║  💚 $0 (efímero)║")
    print("╚════════════════════════════╩═══════════════╩════════════════╝")

    if res_onpremise["errores"]:
        print(f"\n  ⚠️  Trabajos que fallaron en on-premise: {res_onpremise['errores']}")
        print("     El analista deberá reiniciar esos procesos mañana.\n")
