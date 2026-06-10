"""
=============================================================================
SCRIPT GCP REAL — Subir datos a Cloud Storage
=============================================================================
Este script muestra el código REAL que se usaría para subir datos
al bucket de Cloud Storage en GCP.

REQUISITOS PARA EJECUTARLO EN PRODUCCIÓN:
    pip install google-cloud-storage
    gcloud auth application-default login

NOTA: Sin una cuenta GCP configurada, este script mostrará un error
      de autenticación, lo cual es esperado en un entorno de prueba.
=============================================================================
"""

# ---------------------------------------------------------------------------
# IMPORTS
# En producción, google-cloud-storage debe estar instalado:
#   pip install google-cloud-storage
# ---------------------------------------------------------------------------
try:
    from google.cloud import storage as gcs
    GCP_DISPONIBLE = True
except ImportError:
    GCP_DISPONIBLE = False
    print("⚠️  Librería google-cloud-storage no instalada.")
    print("   Para instalar: pip install google-cloud-storage")
    print("   Ejecutando en modo simulación...\n")

import os


# =============================================================================
# CONFIGURACIÓN — Modificar estos valores según el proyecto GCP real
# =============================================================================

PROYECTO_GCP    = "mi-proyecto-telecom"          # ID del proyecto en GCP
BUCKET_RAW      = "telecom-datamining-raw"        # Datos crudos
BUCKET_PROCESADO = "telecom-datamining-processed" # Datos procesados
REGION          = "us-central1"                   # Región del bucket


# =============================================================================
# FUNCIONES DE CLOUD STORAGE
# =============================================================================

def crear_bucket(nombre_bucket: str, proyecto: str, region: str):
    """
    Crea un bucket en Cloud Storage si no existe.
    
    Args:
        nombre_bucket: Nombre único global del bucket
        proyecto: ID del proyecto GCP
        region: Región donde se creará el bucket (ej: "us-central1")
    """
    if not GCP_DISPONIBLE:
        print(f"[SIMULADO] Bucket creado: gs://{nombre_bucket}/")
        return

    cliente = gcs.Client(project=proyecto)
    bucket = cliente.bucket(nombre_bucket)

    if not bucket.exists():
        bucket = cliente.create_bucket(nombre_bucket, location=region)
        print(f"✅ Bucket creado: gs://{nombre_bucket}/ en {region}")
    else:
        print(f"ℹ️  El bucket ya existe: gs://{nombre_bucket}/")


def subir_archivo(ruta_local: str, nombre_bucket: str, ruta_destino: str):
    """
    Sube un archivo local a Cloud Storage.
    
    Args:
        ruta_local:    Ruta del archivo en la máquina local
        nombre_bucket: Nombre del bucket destino
        ruta_destino:  Ruta dentro del bucket (ej: "datos/clientes.csv")
    
    Ejemplo de uso:
        subir_archivo("datos/clientes.csv", "telecom-raw", "2024/clientes.csv")
        → El archivo queda en: gs://telecom-raw/2024/clientes.csv
    """
    if not GCP_DISPONIBLE:
        print(f"[SIMULADO] Subiendo: {ruta_local} → gs://{nombre_bucket}/{ruta_destino}")
        return

    cliente = gcs.Client()
    bucket = cliente.bucket(nombre_bucket)
    blob = bucket.blob(ruta_destino)
    blob.upload_from_filename(ruta_local)
    print(f"✅ Archivo subido: gs://{nombre_bucket}/{ruta_destino}")


def listar_archivos(nombre_bucket: str, prefijo: str = ""):
    """
    Lista los archivos de un bucket (opcionalmente con filtro de prefijo).
    
    Args:
        nombre_bucket: Nombre del bucket
        prefijo:       Filtro de carpeta (ej: "2024/" para ver solo ese año)
    
    Returns:
        Lista de nombres de archivos en el bucket
    """
    if not GCP_DISPONIBLE:
        archivos_simulados = [
            "2024/clientes_enero.parquet",
            "2024/clientes_febrero.parquet",
            "2024/logs_red.parquet"
        ]
        print(f"[SIMULADO] Archivos en gs://{nombre_bucket}/{prefijo}:")
        for a in archivos_simulados:
            print(f"  - {a}")
        return archivos_simulados

    cliente = gcs.Client()
    blobs = cliente.list_blobs(nombre_bucket, prefix=prefijo)
    archivos = [blob.name for blob in blobs]

    print(f"Archivos en gs://{nombre_bucket}/{prefijo}:")
    for archivo in archivos:
        print(f"  - {archivo}")

    return archivos


def descargar_archivo(nombre_bucket: str, ruta_origen: str, ruta_local: str):
    """
    Descarga un archivo de Cloud Storage al sistema local.
    
    Args:
        nombre_bucket: Nombre del bucket origen
        ruta_origen:   Ruta del archivo en el bucket
        ruta_local:    Dónde guardar el archivo descargado
    """
    if not GCP_DISPONIBLE:
        print(f"[SIMULADO] Descargando: gs://{nombre_bucket}/{ruta_origen} → {ruta_local}")
        return

    cliente = gcs.Client()
    bucket = cliente.bucket(nombre_bucket)
    blob = bucket.blob(ruta_origen)
    blob.download_to_filename(ruta_local)
    print(f"✅ Archivo descargado: {ruta_local}")


# =============================================================================
# FLUJO PRINCIPAL: Ejemplo de uso del pipeline de ingesta
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  SCRIPT GCP: Gestión de datos en Cloud Storage")
    print("=" * 60)

    # Paso 1: Crear los buckets necesarios
    print("\n📦 Paso 1: Crear buckets")
    crear_bucket(BUCKET_RAW, PROYECTO_GCP, REGION)
    crear_bucket(BUCKET_PROCESADO, PROYECTO_GCP, REGION)

    # Paso 2: Subir un archivo de datos (en producción sería el archivo real)
    print("\n⬆️  Paso 2: Subir datos crudos")
    # Creamos un archivo de ejemplo para la demo
    with open("/tmp/clientes_demo.csv", "w") as f:
        f.write("cliente_id,nombre,plan,meses_activo\n")
        f.write("1001,Juan Pérez,Premium,24\n")
        f.write("1002,María López,Básico,6\n")

    subir_archivo(
        ruta_local="/tmp/clientes_demo.csv",
        nombre_bucket=BUCKET_RAW,
        ruta_destino="2024/clientes_demo.csv"
    )

    # Paso 3: Listar los archivos disponibles
    print("\n📋 Paso 3: Verificar archivos en el bucket")
    listar_archivos(BUCKET_RAW, prefijo="2024/")

    print("\n✅ Pipeline de ingesta completado.")
    print(f"   Los datos están listos en gs://{BUCKET_RAW}/2024/")
    print(f"   Dataproc puede ahora leer estos datos para procesarlos.\n")
