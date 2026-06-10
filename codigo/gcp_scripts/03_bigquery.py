"""
=============================================================================
SCRIPT GCP REAL — Cargar y consultar datos en BigQuery
=============================================================================
BigQuery es el Data Warehouse donde se almacenan las tablas finales
para que la Gerencia pueda hacer consultas SQL directamente,
sin necesitar intermediarios ni reportes manuales.

REQUISITOS PARA EJECUTARLO EN PRODUCCIÓN:
    pip install google-cloud-bigquery
    gcloud auth application-default login
=============================================================================
"""

try:
    from google.cloud import bigquery
    GCP_DISPONIBLE = True
except ImportError:
    GCP_DISPONIBLE = False
    print("⚠️  Librería google-cloud-bigquery no instalada.")
    print("   Para instalar: pip install google-cloud-bigquery\n")

# Configuración
PROYECTO_GCP = "mi-proyecto-telecom"
DATASET_ID   = "datamining_resultados"
TABLA_CHURN  = "predicciones_churn"
BUCKET_DATOS = "telecom-datamining-processed"


# =============================================================================
# ESQUEMA DE LA TABLA
# Define las columnas y tipos de datos de la tabla en BigQuery.
# =============================================================================

SCHEMA_PREDICCIONES_CHURN = [
    {"name": "cliente_id",      "type": "INTEGER",  "description": "ID único del cliente"},
    {"name": "nombre",          "type": "STRING",   "description": "Nombre del cliente"},
    {"name": "plan",            "type": "STRING",   "description": "Plan contratado"},
    {"name": "meses_activo",    "type": "INTEGER",  "description": "Meses como cliente"},
    {"name": "prob_churn",      "type": "FLOAT",    "description": "Probabilidad de abandono (0-1)"},
    {"name": "segmento_riesgo", "type": "STRING",   "description": "Alto / Medio / Bajo"},
    {"name": "fecha_prediccion","type": "DATE",     "description": "Fecha en que se generó la predicción"},
]


def crear_dataset(dataset_id: str):
    """
    Crea un dataset en BigQuery si no existe.
    Un dataset es como una 'base de datos' que contiene tablas.
    """
    if not GCP_DISPONIBLE:
        print(f"[SIMULADO] Dataset creado: {PROYECTO_GCP}.{dataset_id}")
        return

    cliente = bigquery.Client(project=PROYECTO_GCP)
    dataset_ref = bigquery.Dataset(f"{PROYECTO_GCP}.{dataset_id}")
    dataset_ref.location = "US"

    try:
        cliente.create_dataset(dataset_ref)
        print(f"✅ Dataset creado: {PROYECTO_GCP}.{dataset_id}")
    except Exception:
        print(f"ℹ️  El dataset ya existe: {PROYECTO_GCP}.{dataset_id}")


def cargar_desde_gcs(dataset_id: str, tabla: str, ruta_gcs: str):
    """
    Carga datos desde Cloud Storage directamente a BigQuery.
    
    Args:
        dataset_id: Nombre del dataset en BigQuery
        tabla:      Nombre de la tabla destino
        ruta_gcs:   Ruta del archivo en Cloud Storage
                    Ejemplo: "gs://mi-bucket/resultados/churn.parquet"
    """
    if not GCP_DISPONIBLE:
        print(f"[SIMULADO] Cargando datos desde {ruta_gcs}")
        print(f"           → {PROYECTO_GCP}.{dataset_id}.{tabla}")
        print(f"           → 3 registros cargados ✅")
        return

    cliente = bigquery.Client(project=PROYECTO_GCP)
    tabla_ref = f"{PROYECTO_GCP}.{dataset_id}.{tabla}"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.PARQUET,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,  # Reemplaza datos existentes
        autodetect=True,  # Detecta el esquema automáticamente del parquet
    )

    job = cliente.load_table_from_uri(ruta_gcs, tabla_ref, job_config=job_config)
    job.result()  # Espera a que termine la carga

    tabla_cargada = cliente.get_table(tabla_ref)
    print(f"✅ Cargados {tabla_cargada.num_rows} registros en {tabla_ref}")


def ejecutar_consulta(sql: str, descripcion: str = ""):
    """
    Ejecuta una consulta SQL en BigQuery y muestra los resultados.
    
    En producción, la Gerencia puede hacer esto desde:
    - La consola web de BigQuery (sin código)
    - Looker Studio (dashboard visual)
    - Google Sheets conectado a BigQuery
    - Este script Python
    """
    if not GCP_DISPONIBLE:
        # Datos simulados para mostrar el formato de los resultados
        resultados_simulados = {
            "clientes_alto_riesgo": [
                {"cliente_id": 1001, "nombre": "Juan Pérez", "plan": "Básico",
                 "meses_activo": 3, "prob_churn": 0.91, "segmento_riesgo": "Alto"},
                {"cliente_id": 1002, "nombre": "Ana Gómez", "plan": "Básico",
                 "meses_activo": 5, "prob_churn": 0.78, "segmento_riesgo": "Alto"},
            ],
            "resumen_por_plan": [
                {"plan": "Básico",   "total_clientes": 1200, "churn_promedio": 0.65},
                {"plan": "Standard", "total_clientes": 850,  "churn_promedio": 0.32},
                {"plan": "Premium",  "total_clientes": 420,  "churn_promedio": 0.15},
            ]
        }

        print(f"\n[SIMULADO] Consulta: {descripcion}")
        print(f"SQL: {sql[:80]}...")

        # Mostrar el resultado simulado más relevante
        for key, filas in resultados_simulados.items():
            if any(k in sql.lower() for k in ["alto", "riesgo", "churn"]):
                print(f"\nResultado ({len(filas)} filas):")
                for fila in filas:
                    print(f"  {fila}")
                break
        return

    cliente = bigquery.Client(project=PROYECTO_GCP)
    print(f"\nEjecutando consulta: {descripcion}")

    resultados = cliente.query(sql).result()
    filas = list(resultados)

    print(f"Filas devueltas: {len(filas)}")
    for fila in filas[:10]:  # Mostrar máximo 10 filas
        print(f"  {dict(fila)}")

    return filas


# =============================================================================
# CONSULTAS DE EJEMPLO PARA LA GERENCIA
# Estas son las consultas típicas que la gerencia querría ejecutar.
# =============================================================================

CONSULTAS_GERENCIA = {
    "Clientes con alto riesgo de churn": f"""
        SELECT cliente_id, nombre, plan, meses_activo, prob_churn
        FROM `{PROYECTO_GCP}.{DATASET_ID}.{TABLA_CHURN}`
        WHERE segmento_riesgo = 'Alto'
        ORDER BY prob_churn DESC
        LIMIT 100
    """,

    "Resumen de churn por plan": f"""
        SELECT
            plan,
            COUNT(*) AS total_clientes,
            ROUND(AVG(prob_churn), 2) AS churn_promedio,
            COUNTIF(segmento_riesgo = 'Alto') AS clientes_alto_riesgo
        FROM `{PROYECTO_GCP}.{DATASET_ID}.{TABLA_CHURN}`
        GROUP BY plan
        ORDER BY churn_promedio DESC
    """,

    "Evolución del churn por mes": f"""
        SELECT
            fecha_prediccion,
            COUNT(*) AS total_predicciones,
            ROUND(AVG(prob_churn), 3) AS churn_promedio_dia
        FROM `{PROYECTO_GCP}.{DATASET_ID}.{TABLA_CHURN}`
        GROUP BY fecha_prediccion
        ORDER BY fecha_prediccion DESC
        LIMIT 30
    """,
}


# =============================================================================
# FLUJO PRINCIPAL
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  SCRIPT GCP: Pipeline BigQuery para Análisis de Churn")
    print("=" * 60)

    # Paso 1: Crear el dataset en BigQuery
    print("\n📊 Paso 1: Crear dataset en BigQuery")
    crear_dataset(DATASET_ID)

    # Paso 2: Cargar los datos procesados por Dataproc
    print("\n⬆️  Paso 2: Cargar datos desde Cloud Storage")
    cargar_desde_gcs(
        dataset_id=DATASET_ID,
        tabla=TABLA_CHURN,
        ruta_gcs=f"gs://{BUCKET_DATOS}/2024/resultado_churn/*.parquet"
    )

    # Paso 3: Ejecutar consultas como lo haría la Gerencia
    print("\n🔍 Paso 3: Consultas de análisis para Gerencia")
    for descripcion, sql in CONSULTAS_GERENCIA.items():
        ejecutar_consulta(sql=sql, descripcion=descripcion)

    print("\n" + "=" * 60)
    print("  ✅ Los datos están disponibles en BigQuery.")
    print(f"  La Gerencia puede acceder en:")
    print(f"  https://console.cloud.google.com/bigquery")
    print(f"  Proyecto: {PROYECTO_GCP} → Dataset: {DATASET_ID}")
    print("=" * 60 + "\n")
