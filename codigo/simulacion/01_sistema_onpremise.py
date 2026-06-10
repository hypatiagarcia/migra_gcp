"""
=============================================================================
SIMULACIÓN: Sistema On-Premise (Situación Actual)
=============================================================================
Este script simula el comportamiento del clúster físico actual, incluyendo
los problemas identificados en el caso de estudio:

    1. Procesos que se cortan por falta de RAM/CPU
    2. Cuello de botella cuando dos analistas trabajan en paralelo
    3. Sin capacidad de escalar

NOTA: Es una simulación educativa. No requiere Hadoop ni PySpark instalado.
=============================================================================
"""

import time
import random
import threading
from datetime import datetime


# =============================================================================
# CONFIGURACIÓN DEL CLÚSTER FÍSICO
# Estos valores representan los límites reales del hardware disponible.
# =============================================================================

CLUSTER_CONFIG = {
    "ram_total_gb": 64,         # RAM total del clúster (3 nodos sumados)
    "cpu_cores_total": 24,      # Núcleos de CPU totales
    "disco_total_tb": 10,       # Almacenamiento en discos físicos
    "max_trabajos_paralelos": 1 # El hardware colapsa con más de 1 trabajo pesado
}


# =============================================================================
# CLASE: ClusterOnPremise
# Representa el estado del clúster físico y sus limitaciones.
# =============================================================================

class ClusterOnPremise:
    def __init__(self):
        self.ram_disponible = CLUSTER_CONFIG["ram_total_gb"]
        self.cpu_disponible = CLUSTER_CONFIG["cpu_cores_total"]
        self.trabajos_activos = 0
        self.lock = threading.Lock()  # Para simular concurrencia entre analistas

    def _log(self, mensaje, nivel="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        simbolos = {"INFO": "ℹ️ ", "ERROR": "❌", "OK": "✅", "WARN": "⚠️ "}
        print(f"[{timestamp}] {simbolos.get(nivel, '')} {mensaje}")

    def ejecutar_trabajo(self, nombre_trabajo, ram_requerida_gb, duracion_seg):
        """
        Intenta ejecutar un trabajo PySpark en el clúster.
        Simula los problemas reales: falta de recursos y colapso por concurrencia.
        """
        with self.lock:
            self._log(f"Analista solicita ejecutar: '{nombre_trabajo}'")
            self._log(f"Recursos requeridos: {ram_requerida_gb}GB RAM")
            self._log(f"Recursos disponibles: {self.ram_disponible}GB RAM")

            # -----------------------------------------------------------------
            # PROBLEMA 1: Sin memoria suficiente → el proceso se cancela
            # -----------------------------------------------------------------
            if ram_requerida_gb > self.ram_disponible:
                self._log(
                    f"PROCESO CANCELADO — No hay suficiente RAM. "
                    f"Necesita {ram_requerida_gb}GB pero solo hay {self.ram_disponible}GB libres.",
                    nivel="ERROR"
                )
                self._log("El analista deberá reiniciar el trabajo mañana desde cero.", nivel="ERROR")
                return False

            # -----------------------------------------------------------------
            # PROBLEMA 2: Cuello de botella — ya hay un trabajo corriendo
            # -----------------------------------------------------------------
            if self.trabajos_activos >= CLUSTER_CONFIG["max_trabajos_paralelos"]:
                self._log(
                    f"CUELLO DE BOTELLA — Ya hay {self.trabajos_activos} trabajo(s) en ejecución. "
                    f"El clúster no puede manejar otro trabajo pesado en simultáneo.",
                    nivel="WARN"
                )
                self._log("El analista debe esperar a que el otro proceso termine.", nivel="WARN")
                return False

            # Si pasó los dos filtros, el trabajo puede ejecutarse
            self.ram_disponible -= ram_requerida_gb
            self.trabajos_activos += 1
            self._log(f"Trabajo iniciado. RAM restante en clúster: {self.ram_disponible}GB", nivel="OK")

        # Simulamos la ejecución del trabajo (fuera del lock para permitir concurrencia)
        self._log(f"Ejecutando '{nombre_trabajo}'... (esto tarda {duracion_seg} segundos en la sim.)")
        time.sleep(duracion_seg)

        with self.lock:
            self.ram_disponible += ram_requerida_gb
            self.trabajos_activos -= 1
            self._log(f"Trabajo '{nombre_trabajo}' FINALIZADO. RAM liberada.", nivel="OK")

        return True


# =============================================================================
# DEMOSTRACIÓN DE LOS PROBLEMAS
# =============================================================================

def demo_problema_1_falta_de_memoria():
    """Demuestra el Problema 1: proceso cancelado por falta de RAM."""
    print("\n" + "="*60)
    print("  DEMO — Problema 1: Proceso cancelado por falta de RAM")
    print("="*60)

    cluster = ClusterOnPremise()

    # Primer trabajo: usa casi toda la RAM disponible
    print("\n→ Analista A lanza un trabajo de entrenamiento de modelo:")
    cluster.ejecutar_trabajo(
        nombre_trabajo="Entrenamiento Modelo ML - Dataset Clientes",
        ram_requerida_gb=50,
        duracion_seg=1
    )

    # Segundo trabajo: intenta usar más RAM de la que queda
    print("\n→ Analista B lanza otro trabajo de transformación de datos:")
    exito = cluster.ejecutar_trabajo(
        nombre_trabajo="Transformación Datos - Logs de Red",
        ram_requerida_gb=25,   # Solo quedan 14GB libres → va a fallar
        duracion_seg=1
    )

    if not exito:
        print("\n  💡 CONCLUSIÓN: El analista B perdió horas de trabajo.")
        print("     Al día siguiente deberá reiniciar el proceso desde cero.")


def demo_problema_2_cuello_de_botella():
    """Demuestra el Problema 2: cuello de botella por concurrencia."""
    print("\n" + "="*60)
    print("  DEMO — Problema 2: Cuello de botella por concurrencia")
    print("="*60)

    cluster = ClusterOnPremise()
    resultados = []

    def trabajo_analista(nombre, trabajo, ram, duracion):
        exito = cluster.ejecutar_trabajo(trabajo, ram, duracion)
        resultados.append((nombre, exito))

    # Ambos analistas intentan lanzar su trabajo al mismo tiempo
    hilo_a = threading.Thread(
        target=trabajo_analista,
        args=("Analista A", "Predicción Churn - Modelo Random Forest", 30, 2)
    )
    hilo_b = threading.Thread(
        target=trabajo_analista,
        args=("Analista B", "Segmentación de Clientes - K-Means", 20, 2)
    )

    print("\n→ Analista A y Analista B lanzan trabajos al mismo tiempo:")
    hilo_a.start()
    time.sleep(0.1)  # B empieza levemente después
    hilo_b.start()

    hilo_a.join()
    hilo_b.join()

    fallidos = [n for n, ok in resultados if not ok]
    if fallidos:
        print(f"\n  💡 CONCLUSIÓN: {', '.join(fallidos)} tuvo que esperar.")
        print("     En un equipo de 5 analistas, esto es un problema crítico diario.")


# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================

if __name__ == "__main__":
    print("\n╔══════════════════════════════════════════════════════════╗")
    print("║   SIMULACIÓN DEL SISTEMA ON-PREMISE — SITUACIÓN ACTUAL  ║")
    print("╚══════════════════════════════════════════════════════════╝")

    demo_problema_1_falta_de_memoria()
    demo_problema_2_cuello_de_botella()

    print("\n" + "="*60)
    print("  RESUMEN: Los problemas demostrados justifican la migración")
    print("  a una infraestructura elástica en la nube (GCP).")
    print("="*60 + "\n")
