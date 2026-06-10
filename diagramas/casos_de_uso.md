# 🎭 Casos de Uso del Sistema

## Introducción

Los casos de uso describen las interacciones entre los actores y el sistema desde la perspectiva del usuario. Se presentan los casos de uso más relevantes para el sistema propuesto.

---

## Diagrama General de Casos de Uso

```
                        ┌─────────────────────────────────────────────┐
                        │              SISTEMA DE DATA MINING (GCP)    │
                        │                                              │
  [Data Scientist] ─────┤── CU-01: Ejecutar trabajo PySpark            │
                        │── CU-02: Monitorear estado del trabajo       │
                        │                                              │
  [Ingeniero Datos] ────┤── CU-03: Cargar datos a Cloud Storage        │
                        │── CU-04: Gestionar pipelines de datos        │
                        │                                              │
  [Gerencia] ───────────┤── CU-05: Consultar resultados en BigQuery    │
                        │── CU-06: Visualizar dashboards               │
                        │                                              │
  [Soporte TI] ─────────┤── CU-07: Monitorear uso y costos            │
                        │── CU-08: Gestionar permisos y accesos        │
                        │                                              │
                        └─────────────────────────────────────────────┘
```

---

## CU-01: Ejecutar Trabajo PySpark en Dataproc

| Campo | Descripción |
|---|---|
| **ID** | CU-01 |
| **Nombre** | Ejecutar trabajo PySpark |
| **Actor principal** | Data Scientist |
| **Precondiciones** | El usuario tiene credenciales válidas en GCP; el código PySpark está listo |
| **Postcondiciones** | El trabajo se ejecuta exitosamente y los resultados se almacenan en Cloud Storage |

**Flujo Principal:**
1. El Data Scientist sube su script PySpark a Cloud Storage.
2. El Data Scientist accede a la consola de Dataproc o ejecuta un comando `gcloud`.
3. El sistema crea un clúster efímero con los recursos solicitados.
4. El sistema ejecuta el trabajo PySpark sobre los datos en Cloud Storage.
5. El trabajo finaliza y los resultados se escriben en el Bucket de salida.
6. El sistema destruye el clúster para evitar costos innecesarios.
7. El Data Scientist recibe una notificación de éxito.

**Flujos Alternativos:**
- *4a. Si el trabajo falla:* El sistema registra el error en los logs y notifica al usuario. El trabajo puede reintentarse sin pérdida de datos.
- *3a. Si no hay suficientes recursos en la región:* El sistema escala automáticamente o sugiere una región alternativa.

---

## CU-02: Monitorear Estado del Trabajo

| Campo | Descripción |
|---|---|
| **ID** | CU-02 |
| **Nombre** | Monitorear estado del trabajo |
| **Actor principal** | Data Scientist, Ingeniero de Datos |
| **Precondiciones** | Existe al menos un trabajo en ejecución o completado |
| **Postcondiciones** | El usuario visualiza el estado, logs y métricas del trabajo |

**Flujo Principal:**
1. El usuario accede al panel de Dataproc en la consola de GCP.
2. El sistema muestra la lista de trabajos con su estado (En ejecución / Completado / Fallido).
3. El usuario selecciona un trabajo específico.
4. El sistema muestra los logs en tiempo real, métricas de CPU/RAM y tiempo transcurrido.

---

## CU-03: Cargar Datos a Cloud Storage

| Campo | Descripción |
|---|---|
| **ID** | CU-03 |
| **Nombre** | Cargar datos a Cloud Storage |
| **Actor principal** | Ingeniero de Datos |
| **Precondiciones** | El usuario tiene permisos de escritura en el bucket correspondiente |
| **Postcondiciones** | Los datos están disponibles en Cloud Storage para ser procesados |

**Flujo Principal:**
1. El Ingeniero de Datos prepara los archivos de datos desde la fuente original.
2. Utiliza `gsutil` o la consola web de GCP para cargar los archivos al bucket `raw`.
3. El sistema confirma la carga y muestra el checksum de integridad.
4. El Ingeniero registra los metadatos del dataset (fecha, origen, descripción).

---

## CU-04: Gestionar Pipelines de Datos

| Campo | Descripción |
|---|---|
| **ID** | CU-04 |
| **Nombre** | Gestionar pipelines de datos |
| **Actor principal** | Ingeniero de Datos |
| **Precondiciones** | El pipeline está definido y las conexiones a las fuentes están configuradas |
| **Postcondiciones** | El pipeline ejecuta automáticamente según la frecuencia configurada |

**Flujo Principal:**
1. El Ingeniero define el pipeline (origen → transformación → destino) usando Cloud Composer o scripts.
2. El sistema programa la ejecución según la frecuencia configurada (diaria, horaria, etc.).
3. En cada ejecución, el sistema carga datos a Cloud Storage y dispara el trabajo de Dataproc.
4. Al finalizar, los datos procesados se cargan a BigQuery automáticamente.

---

## CU-05: Consultar Resultados en BigQuery

| Campo | Descripción |
|---|---|
| **ID** | CU-05 |
| **Nombre** | Consultar resultados en BigQuery |
| **Actor principal** | Gerencia |
| **Precondiciones** | Las tablas finales están cargadas en BigQuery; el usuario tiene permisos de lectura |
| **Postcondiciones** | El usuario obtiene los resultados de su consulta |

**Flujo Principal:**
1. El gerente accede a la consola de BigQuery o a un dashboard conectado (ej: Looker Studio).
2. El gerente escribe o selecciona una consulta SQL predefinida.
3. El sistema ejecuta la consulta sobre las tablas de resultados.
4. El sistema devuelve los resultados en segundos, independientemente del volumen de datos.
5. El gerente puede exportar los resultados a Google Sheets o descargar como CSV.

---

## CU-07: Monitorear Uso y Costos

| Campo | Descripción |
|---|---|
| **ID** | CU-07 |
| **Nombre** | Monitorear uso y costos |
| **Actor principal** | Soporte TI, Gerencia |
| **Precondiciones** | El proyecto GCP tiene alertas de presupuesto configuradas |
| **Postcondiciones** | El usuario tiene visibilidad sobre el gasto actual y proyectado |

**Flujo Principal:**
1. El usuario accede al panel de Facturación de GCP.
2. El sistema muestra el gasto desglosado por servicio (Dataproc, Cloud Storage, BigQuery).
3. El sistema muestra alertas si el gasto supera umbrales configurados.
4. El usuario puede ajustar configuraciones para optimizar costos (ej: apagar clústeres inactivos).
