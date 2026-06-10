"""
=============================================================================
SIMULACIÓN: Sistema en la Nube — Google Cloud Platform (Solución Propuesta)
=============================================================================
Este script simula el comportamiento del sistema migrado a GCP, demostrando
cómo se resuelven los problemas del sistema on-premise:

    ✅ Sin cortes por falta de recursos (auto-scaling)
    ✅ Múltiples analistas trabajando en paralelo sin conflictos
    ✅ Clústeres efímeros: se crean y destruyen automáticamente
    ✅ Pago solo por lo que se usa

NOTA: Es una simulación educativa. Para el código real de GCP, ver la
      carpeta /gcp_scripts/
=============================================================================
"""

import time
import random
import threading
from datetime import datetime


# =============================================================================
# CLASE: CloudStorage (simula Google Cloud Storage)
# Almacenamiento de objetos ilimitado y escalable.
# =============================================================================

class CloudStorage:
    """
    Simula Google Cloud Storage.
    Diferencias clave respecto a HDFS on-premise:
    - Capacidad prácticamente ilimitada
    - Alta durabilidad (Google garantiza 99.999999999%)
    - Accesible desde cualquier servicio de GCP
    """
    def __init__(self):
        self.buckets = {
            "raw": {},        # Datos crudos / originales
            "processed": {},  # Datos transformados por PySpark
            "staging": {}     # Datos intermedios del pipeline
        }
        self._log("Cloud Storage inicializado — capacidad: ilimitada ✅")

    def _log(self, msg):
        print(f"  [CloudStorage] {msg}")

    def subir_archivo(self, bucket, nombre, contenido):
        """Sube un archivo al bucket especificado."""
        self.buckets[bucket][nombre] = contenido
        self._log(f"gs://{bucket}/{nombre} — subido correctamente ✅")

    def leer_archivo(self, bucket, nombre):
        """Lee un archivo de un bucket."""
        dato = self.buckets[bucket].get(nombre)
        if dato:
            self._log(f"gs://{bucket}/{nombre} — leído correctamente ✅")
        return dato

    def listar_archivos(self, bucket):
        """Lista todos los archivos de un bucket."""
        archivos = list(self.buckets[bucket].keys())
        self._log(f"gs://{bucket}/ — {len(archivos)} archivo(s): {archivos}")
        return archivos


# =============================================================================
# CLASE: DataprocCluster (simula Google Dataproc)
# Clúster PySpark administrado, elástico y efímero.
# =============================================================================

class DataprocCluster:
    """
    Simula un clúster de Google Dataproc.
    Diferencias clave respecto al clúster on-premise:
    - Se crea en minutos (no en meses)
    - Escala automáticamente según la carga
    - Cada analista puede tener su propio clúster independiente
    - Al terminar el trabajo, el clúster se destruye (no se paga más)
    """

    _instancias_activas = 0  # Contador global de clústeres activos

    def __init__(self, nombre, workers=2):
        self.nombre = nombre
        self.workers = workers
        self.activo = False
        self.storage = None  # Se conectará a CloudStorage

    def _log(self, msg, nivel="INFO"):
        simbolos = {"INFO": "  ", "OK": "✅", "ERROR": "❌", "SCALE": "⚡"}
        print(f"  [Dataproc:{self.nombre}] {simbolos.get(nivel, '')} {msg}")

    def conectar_storage(self, storage: CloudStorage):
        """Conecta el clúster a una instancia de Cloud Storage."""
        self.storage = storage

    def crear_cluster(self):
        """
        Provisiona el clúster en GCP.
        En la realidad esto toma ~2 minutos. Aquí lo simulamos en segundos.
        """
        self._log(f"Creando clúster con {self.workers} workers...")
        time.sleep(0.5)  # Simula el tiempo de provisión
        self.activo = True
        DataprocCluster._instancias_activas += 1
        self._log(f"Clúster creado y listo — workers: {self.workers}", nivel="OK")
        self._log(f"Clústeres activos en total: {DataprocCluster._instancias_activas}")

    def destruir_cluster(self):
        """
        Destruye el clúster al terminar el trabajo.
        IMPORTANTE: En GCP, destruir el clúster detiene la facturación.
        """
        self.activo = False
        DataprocCluster._instancias_activas -= 1
        self._log(f"Clúster destruido — facturación detenida 💰", nivel="OK")

    def escalar(self, nuevos_workers):
        """
        Escala el clúster agregando o quitando workers.
        En on-premise esto tardaría meses. En GCP: segundos.
        """
        workers_anteriores = self.workers
        self.workers = nuevos_workers
        self._log(
            f"Auto-scaling: {workers_anteriores} → {nuevos_workers} workers ⚡",
            nivel="SCALE"
        )

    def ejecutar_pyspark(self, nombre_trabajo, input_bucket, output_bucket,
                          ram_requerida_gb, duracion_seg):
        """
        Ejecuta un trabajo PySpark en el clúster.
        A diferencia del on-premise, NUNCA se cancela por falta de recursos:
        el clúster escala automáticamente si es necesario.
        """
        if not self.activo:
            self._log("El clúster no está activo. Llama a crear_cluster() primero.", nivel="ERROR")
            return False

        self._log(f"Iniciando trabajo: '{nombre_trabajo}'")
        self._log(f"Leyendo datos desde: gs://{input_bucket}/")

        # Auto-scaling automático si el trabajo requiere muchos recursos
        # En on-premise esto causaría una cancelación; en GCP se escala sin problema
        if ram_requerida_gb > 40:
            self._log(f"Alta demanda detectada ({ram_requerida_gb}GB RAM requerida)")
            self.escalar(self.workers * 2)

        # Leer datos desde Cloud Storage
        if self.storage:
            archivos = self.storage.listar_archivos(input_bucket)
            self._log(f"Archivos disponibles para procesar: {len(archivos)}")

        # Simular procesamiento
        self._log(f"Procesando datos con PySpark... ({duracion_seg}s en simulación)")
        time.sleep(duracion_seg)

        # Escribir resultados a Cloud Storage
        if self.storage:
            resultado = {
                "trabajo": nombre_trabajo,
                "registros_procesados": random.randint(100_000, 5_000_000),
                "estado": "COMPLETADO"
            }
            self.storage.subir_archivo(
                output_bucket,
                f"resultado_{nombre_trabajo.replace(' ', '_').lower()}.json",
                resultado
            )

        self._log(f"Trabajo '{nombre_trabajo}' COMPLETADO exitosamente ✅", nivel="OK")
        return True


# =============================================================================
# CLASE: BigQuery (simula Google BigQuery)
# Data Warehouse serverless para consultas analíticas.
# =============================================================================

class BigQuery:
    """
    Simula Google BigQuery.
    Permite a la gerencia consultar los resultados de los modelos
    directamente con SQL, sin intermediarios ni reportes manuales.
    """
    def __init__(self):
        self.tablas = {}
        self._log("BigQuery inicializado — listo para consultas SQL ✅")

    def _log(self, msg):
        print(f"  [BigQuery] {msg}")

    def cargar_tabla(self, nombre_tabla, datos):
        """Carga datos en una tabla de BigQuery."""
        self.tablas[nombre_tabla] = datos
        self._log(f"Tabla '{nombre_tabla}' cargada — {len(datos)} registros")

    def consultar(self, sql_simulado, tabla):
        """
        Simula la ejecución de una consulta SQL.
        En GCP real, esto puede procesar terabytes en segundos.
        """
        self._log(f"Ejecutando: {sql_simulado}")
        time.sleep(0.2)  # Simula latencia de consulta
        resultado = self.tablas.get(tabla, [])
        self._log(f"Consulta completada — {len(resultado)} fila(s) devueltas ✅")
        return resultado


# =============================================================================
# DEMOSTRACIÓN: El mismo escenario del on-premise, ahora en GCP
# =============================================================================

def demo_solucion_gcp():
    print("\n╔══════════════════════════════════════════════════════════╗")
    print("║   SIMULACIÓN DEL SISTEMA EN GCP — SOLUCIÓN PROPUESTA    ║")
    print("╚══════════════════════════════════════════════════════════╝")

    # -------------------------------------------------------------------------
    # 1. Inicializar el almacenamiento en la nube
    # -------------------------------------------------------------------------
    print("\n── PASO 1: Configurar Cloud Storage ──────────────────────")
    storage = CloudStorage()
    storage.subir_archivo("raw", "clientes_2024.parquet", {"filas": 2_000_000})
    storage.subir_archivo("raw", "logs_red_2024.parquet", {"filas": 50_000_000})

    # -------------------------------------------------------------------------
    # 2. Dos analistas trabajan en PARALELO sin ningún conflicto
    # -------------------------------------------------------------------------
    print("\n── PASO 2: Dos analistas trabajan al mismo tiempo ────────")
    print("   (Esto colapsaba el clúster on-premise. En GCP: sin problema)")

    cluster_a = DataprocCluster("AnalisiA", workers=4)
    cluster_b = DataprocCluster("AnalisiB", workers=4)
    cluster_a.conectar_storage(storage)
    cluster_b.conectar_storage(storage)

    resultados = []

    def trabajo_analista_a():
        cluster_a.crear_cluster()
        ok = cluster_a.ejecutar_pyspark(
            nombre_trabajo="Predicción Churn Clientes",
            input_bucket="raw",
            output_bucket="processed",
            ram_requerida_gb=50,   # Antes causaba cancelación; ahora auto-escala
            duracion_seg=1
        )
        cluster_a.destruir_cluster()
        resultados.append(("Analista A", ok))

    def trabajo_analista_b():
        cluster_b.crear_cluster()
        ok = cluster_b.ejecutar_pyspark(
            nombre_trabajo="Segmentación de Clientes K-Means",
            input_bucket="raw",
            output_bucket="processed",
            ram_requerida_gb=30,
            duracion_seg=1
        )
        cluster_b.destruir_cluster()
        resultados.append(("Analista B", ok))

    hilo_a = threading.Thread(target=trabajo_analista_a)
    hilo_b = threading.Thread(target=trabajo_analista_b)

    hilo_a.start()
    hilo_b.start()
    hilo_a.join()
    hilo_b.join()

    exitosos = [n for n, ok in resultados if ok]
    print(f"\n  ✅ Ambos trabajos completados: {exitosos}")

    # -------------------------------------------------------------------------
    # 3. Cargar resultados a BigQuery para que Gerencia pueda consultarlos
    # -------------------------------------------------------------------------
    print("\n── PASO 3: Cargar resultados a BigQuery ──────────────────")
    bq = BigQuery()
    bq.cargar_tabla("predicciones_churn", [
        {"cliente_id": 1001, "prob_churn": 0.87, "segmento": "Alto riesgo"},
        {"cliente_id": 1002, "prob_churn": 0.12, "segmento": "Bajo riesgo"},
        {"cliente_id": 1003, "prob_churn": 0.65, "segmento": "Riesgo medio"},
    ])

    # -------------------------------------------------------------------------
    # 4. Gerencia consulta los resultados directamente
    # -------------------------------------------------------------------------
    print("\n── PASO 4: Gerencia consulta resultados (sin intermediarios)")
    resultado = bq.consultar(
        sql_simulado="SELECT * FROM predicciones_churn WHERE prob_churn > 0.7",
        tabla="predicciones_churn"
    )
    print(f"  Clientes con alto riesgo de churn encontrados: {len(resultado)}")

    # -------------------------------------------------------------------------
    # RESUMEN FINAL
    # -------------------------------------------------------------------------
    print("\n" + "="*60)
    print("  RESUMEN DE LA DEMOSTRACIÓN GCP")
    print("="*60)
    print("  ✅ Procesos ejecutados sin cancelaciones por falta de RAM")
    print("  ✅ Dos analistas trabajaron en paralelo sin conflictos")
    print("  ✅ Auto-scaling activado automáticamente cuando fue necesario")
    print("  ✅ Clústeres destruidos al terminar (sin costo ocioso)")
    print("  ✅ Gerencia consultó resultados directamente en BigQuery")
    print("="*60 + "\n")


if __name__ == "__main__":
    demo_solucion_gcp()
