# 💻 Código del Proyecto

Esta carpeta contiene todos los scripts del trabajo práctico, organizados en dos grupos.

---

## 📁 Estructura

```
codigo/
├── simulacion/                         ← Corren sin ninguna dependencia externa
│   ├── 01_sistema_onpremise.py         Simula los problemas del sistema actual
│   ├── 02_sistema_gcp.py               Simula el sistema propuesto en GCP
│   └── 03_comparacion.py              Ejecuta ambos y muestra tabla comparativa
│
├── gcp_scripts/                        ← Código real para GCP (requiere cuenta GCP)
│   ├── 01_cloud_storage.py            Sube/descarga datos en Cloud Storage
│   ├── 02_dataproc_pyspark.py         Lanza trabajos PySpark en Dataproc
│   └── 03_bigquery.py                 Carga y consulta datos en BigQuery
│
└── data/
    └── generar_datos.py               Genera un CSV de clientes de ejemplo
```

---

## ▶️ Cómo ejecutar las simulaciones

Las simulaciones **no requieren ninguna instalación especial**, solo Python 3.

```bash
# 1. Generar datos de ejemplo
python data/generar_datos.py

# 2. Ver los problemas del sistema actual
python simulacion/01_sistema_onpremise.py

# 3. Ver cómo los resuelve GCP
python simulacion/02_sistema_gcp.py

# 4. Comparación directa lado a lado
python simulacion/03_comparacion.py
```

---

## ☁️ Cómo ejecutar los scripts reales de GCP

Los scripts de GCP necesitan una cuenta de Google Cloud Platform activa.

### Prerrequisitos

```bash
# Instalar dependencias
pip install google-cloud-storage google-cloud-dataproc google-cloud-bigquery

# Autenticarse con GCP
gcloud auth application-default login
```

### Configuración
Antes de ejecutar, editar estas variables en cada script:
```python
PROYECTO_GCP = "mi-proyecto-telecom"   # ← Tu ID de proyecto GCP
REGION       = "us-central1"            # ← La región que prefieras
```

### Ejecución
```bash
# 1. Subir datos a Cloud Storage
python gcp_scripts/01_cloud_storage.py

# 2. Procesar datos con PySpark en Dataproc
python gcp_scripts/02_dataproc_pyspark.py

# 3. Consultar resultados en BigQuery
python gcp_scripts/03_bigquery.py
```

> **Nota:** Sin una cuenta GCP configurada, los scripts funcionan en modo simulación y muestran el resultado esperado sin conectarse a ningún servicio real.

---

## 🔗 Relación entre scripts y documentos del proyecto

| Script | Documento relacionado |
|---|---|
| `01_sistema_onpremise.py` | `docs/01_descripcion_problema.md` |
| `02_sistema_gcp.py` | `docs/03_propuesta_solucion.md` |
| `03_comparacion.py` | `propuesta/comparativa_costos.md` |
| `gcp_scripts/01_cloud_storage.py` | `diagramas/diagrama_sistema_propuesto.md` |
| `gcp_scripts/02_dataproc_pyspark.py` | `diagramas/casos_de_uso.md` (CU-01) |
| `gcp_scripts/03_bigquery.py` | `diagramas/casos_de_uso.md` (CU-05) |
