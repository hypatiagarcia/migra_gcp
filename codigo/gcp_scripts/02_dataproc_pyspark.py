"""
=============================================================================
SCRIPT GCP REAL — Ejecutar trabajo PySpark en Dataproc
=============================================================================
Este script muestra cómo lanzar un trabajo PySpark en Google Dataproc.
Incluye dos partes:

    PARTE A: El script PySpark que corre DENTRO del clúster Dataproc
             (transforma los datos de clientes y genera predicciones)

    PARTE B: El script Python que LANZA el trabajo desde tu máquina
             usando la API de Dataproc

REQUISITOS PARA EJECUTARLO EN PRODUCCIÓN:
    pip install google-cloud-dataproc pyspark
    gcloud auth application-default login
=============================================================================
"""

# =============================================================================
# PARTE A: SCRIPT PYSPARK
# Este es el código que corre DENTRO del clúster Dataproc.
# Es idéntico al que ya usaban on-premise, sin ningún cambio.
# =============================================================================

PYSPARK_JOB_CODE = '''
"""
Job PySpark: Transformación y análisis de datos de clientes.
Este script es compatible tanto con el clúster on-premise como con Dataproc.
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, avg, count, datediff, current_date
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import RandomForestClassifier

# -------------------------------------------------------------------------
# Inicializar SparkSession
# En Dataproc, esta sesión se conecta automáticamente al clúster GCP.
# -------------------------------------------------------------------------
spark = SparkSession.builder \\
    .appName("Analisis_Churn_Clientes") \\
    .getOrCreate()

# -------------------------------------------------------------------------
# 1. LEER DATOS DESDE CLOUD STORAGE
# En on-premise sería: spark.read.parquet("hdfs://nodo1/datos/clientes.parquet")
# En GCP con Dataproc:  spark.read.parquet("gs://bucket-raw/clientes.parquet")
# -------------------------------------------------------------------------
INPUT_PATH  = "gs://telecom-datamining-raw/2024/clientes.parquet"
OUTPUT_PATH = "gs://telecom-datamining-processed/2024/resultado_churn/"

print(f"Leyendo datos desde: {INPUT_PATH}")
df = spark.read.parquet(INPUT_PATH)

print(f"Total de registros: {df.count()}")
df.printSchema()

# -------------------------------------------------------------------------
# 2. TRANSFORMACIONES
# -------------------------------------------------------------------------
# Calcular antigüedad del cliente en días
df = df.withColumn(
    "antiguedad_dias",
    datediff(current_date(), col("fecha_alta"))
)

# Clasificar clientes por segmento de riesgo según meses activos
df = df.withColumn(
    "segmento_riesgo",
    when(col("meses_activo") < 6, "Alto")
    .when(col("meses_activo") < 24, "Medio")
    .otherwise("Bajo")
)

# Calcular métricas agregadas por plan
resumen_por_plan = df.groupBy("plan").agg(
    count("cliente_id").alias("total_clientes"),
    avg("meses_activo").alias("promedio_meses"),
)

print("\\nResumen por plan:")
resumen_por_plan.show()

# -------------------------------------------------------------------------
# 3. GUARDAR RESULTADOS EN CLOUD STORAGE
# Dataproc escribe directamente en GCS; no se necesita código especial.
# -------------------------------------------------------------------------
print(f"Guardando resultados en: {OUTPUT_PATH}")
df.write.mode("overwrite").parquet(OUTPUT_PATH)

print("✅ Job completado exitosamente.")
spark.stop()
'''


# =============================================================================
# PARTE B: LANZADOR DEL TRABAJO EN DATAPROC
# Este código se ejecuta desde tu máquina local para enviar el job a GCP.
# =============================================================================

try:
    from google.cloud import dataproc_v1
    GCP_DISPONIBLE = True
except ImportError:
    GCP_DISPONIBLE = False

# Configuración del proyecto
PROYECTO_GCP = "mi-proyecto-telecom"
REGION       = "us-central1"
CLUSTER_NAME = "cluster-datamining"
BUCKET_SCRIPTS = "telecom-datamining-scripts"


def crear_cluster_dataproc(nombre_cluster: str):
    """
    Crea un clúster Dataproc con configuración para PySpark.
    
    La clave aquí es usar clústeres EFÍMEROS:
    - Se crea cuando hay un trabajo
    - Se destruye cuando termina
    - Solo se paga por el tiempo de uso real
    """
    if not GCP_DISPONIBLE:
        print(f"[SIMULADO] Clúster Dataproc creado: {nombre_cluster}")
        print(f"  - Región: {REGION}")
        print(f"  - Master: n1-standard-4 (4 vCPUs, 15GB RAM)")
        print(f"  - Workers: 2x n1-standard-4 (auto-scaling hasta 10)")
        return

    cliente = dataproc_v1.ClusterControllerClient(
        client_options={"api_endpoint": f"{REGION}-dataproc.googleapis.com:443"}
    )

    cluster = {
        "project_id": PROYECTO_GCP,
        "cluster_name": nombre_cluster,
        "config": {
            "master_config": {
                "num_instances": 1,
                "machine_type_uri": "n1-standard-4",
            },
            "worker_config": {
                "num_instances": 2,
                "machine_type_uri": "n1-standard-4",
            },
            # Auto-scaling: Dataproc agrega workers automáticamente si hay carga
            "secondary_worker_config": {
                "num_instances": 0,
                "is_preemptible": True,    # Instancias spot = más baratas
            },
        },
    }

    operacion = cliente.create_cluster(
        request={"project_id": PROYECTO_GCP, "region": REGION, "cluster": cluster}
    )
    resultado = operacion.result()
    print(f"✅ Clúster creado: {resultado.cluster_name}")


def lanzar_pyspark_job(nombre_cluster: str, ruta_script_gcs: str):
    """
    Lanza un trabajo PySpark en el clúster Dataproc.
    
    Args:
        nombre_cluster:   Nombre del clúster donde ejecutar el job
        ruta_script_gcs:  Ruta del script en Cloud Storage
                          Ejemplo: "gs://mi-bucket/scripts/mi_job.py"
    """
    if not GCP_DISPONIBLE:
        print(f"[SIMULADO] Trabajo PySpark lanzado en clúster: {nombre_cluster}")
        print(f"  - Script: {ruta_script_gcs}")
        print(f"  - Estado: RUNNING → SUCCEEDED")
        return

    cliente = dataproc_v1.JobControllerClient(
        client_options={"api_endpoint": f"{REGION}-dataproc.googleapis.com:443"}
    )

    job = {
        "placement": {"cluster_name": nombre_cluster},
        "pyspark_job": {
            "main_python_file_uri": ruta_script_gcs,
        },
    }

    operacion = cliente.submit_job_as_operation(
        request={"project_id": PROYECTO_GCP, "region": REGION, "job": job}
    )
    resultado = operacion.result()
    print(f"✅ Job completado: {resultado.reference.job_id}")
    print(f"   Estado final: {resultado.status.state.name}")


def destruir_cluster(nombre_cluster: str):
    """
    Destruye el clúster Dataproc al terminar el trabajo.
    IMPORTANTE: Sin este paso, el clúster seguiría facturando aunque esté inactivo.
    """
    if not GCP_DISPONIBLE:
        print(f"[SIMULADO] Clúster destruido: {nombre_cluster} — facturación detenida 💰")
        return

    cliente = dataproc_v1.ClusterControllerClient(
        client_options={"api_endpoint": f"{REGION}-dataproc.googleapis.com:443"}
    )
    operacion = cliente.delete_cluster(
        request={"project_id": PROYECTO_GCP, "region": REGION, "cluster_name": nombre_cluster}
    )
    operacion.result()
    print(f"✅ Clúster eliminado: {nombre_cluster}")


# =============================================================================
# FLUJO PRINCIPAL: Ciclo completo de un trabajo en Dataproc
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  SCRIPT GCP: Pipeline completo con Dataproc + PySpark")
    print("=" * 60)

    print("\n📄 El código PySpark que se ejecutará en Dataproc:")
    print("-" * 50)
    print(PYSPARK_JOB_CODE[:500] + "\n  [... ver archivo completo ...]\n")

    print("🔄 Flujo de ejecución:")
    print("-" * 50)

    print("\n1️⃣  Crear clúster Dataproc...")
    crear_cluster_dataproc(CLUSTER_NAME)

    print("\n2️⃣  Lanzar trabajo PySpark...")
    lanzar_pyspark_job(
        nombre_cluster=CLUSTER_NAME,
        ruta_script_gcs=f"gs://{BUCKET_SCRIPTS}/jobs/analisis_churn.py"
    )

    print("\n3️⃣  Destruir clúster (detener facturación)...")
    destruir_cluster(CLUSTER_NAME)

    print("\n✅ Pipeline completado.")
    print("   Los resultados están disponibles en Cloud Storage.")
    print("   Próximo paso: cargar a BigQuery con el script 03_bigquery.py\n")
