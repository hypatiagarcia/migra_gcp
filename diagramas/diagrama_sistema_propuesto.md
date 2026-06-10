# 🚀 Diagrama del Sistema Propuesto (TO-BE)

## Descripción del Sistema Propuesto

El sistema propuesto migra toda la infraestructura a **Google Cloud Platform (GCP)**, adoptando un modelo cloud-native donde los recursos se provisionan bajo demanda, son elásticos y están completamente administrados por el proveedor.

---

## Arquitectura TO-BE

```
╔═══════════════════════════════════════════════════════════════════════╗
║                     GOOGLE CLOUD PLATFORM (GCP)                       ║
║                                                                       ║
║  ┌─────────────────────────────────────────────────────────────────┐  ║
║  │                        CLOUD STORAGE                            │  ║
║  │                                                                 │  ║
║  │   ┌──────────────────┐         ┌──────────────────────┐        │  ║
║  │   │  Bucket: Raw     │         │  Bucket: Processed   │        │  ║
║  │   │  (Datos crudos)  │         │  (Datos procesados)  │        │  ║
║  │   └──────────────────┘         └──────────────────────┘        │  ║
║  └────────────────────────┬────────────────────┬───────────────────┘  ║
║                           │                    │                       ║
║                    Lee    │                    │ Escribe               ║
║                           │                    │                       ║
║  ┌────────────────────────▼────────────────────▼───────────────────┐  ║
║  │                    DATAPROC (PySpark)                            │  ║
║  │                                                                  │  ║
║  │  Clúster A (Analista 1)    Clúster B (Analista 2)               │  ║
║  │  ┌────────────────────┐    ┌────────────────────┐               │  ║
║  │  │  Master + Workers  │    │  Master + Workers  │               │  ║
║  │  │  (Auto-scaling)    │    │  (Auto-scaling)    │               │  ║
║  │  │  ✅ Sin conflictos │    │  ✅ Sin conflictos │               │  ║
║  │  └────────────────────┘    └────────────────────┘               │  ║
║  └──────────────────────────────────┬──────────────────────────────┘  ║
║                                     │                                  ║
║                              Carga  │ final                            ║
║                                     │                                  ║
║  ┌──────────────────────────────────▼──────────────────────────────┐  ║
║  │                          BIGQUERY                                │  ║
║  │                                                                  │  ║
║  │   Tablas finales accesibles vía SQL                              │  ║
║  │   ✅ Sin conocimientos de programación para consultar            │  ║
║  └──────────────────────────────────────────────────────────────────┘  ║
╚═══════════════════════════════════════════════════════════════════════╝
         ▲              ▲              ▲                  ▲
         │              │              │                  │
   [Ing. Datos]  [Data Scientist A] [Data Scientist B]  [Gerencia]
   Carga datos   Lanza PySpark Job  Lanza PySpark Job   Consulta SQL
```

---

## Flujo de Datos TO-BE

```
1. INGESTA DE DATOS
   Fuente de datos ──────────────────────► Cloud Storage (Bucket Raw)
   (archivos CSV, logs, etc.)              Capacidad ilimitada
                                           Alta durabilidad (11 nueves)

2. PROCESAMIENTO
   Cloud Storage ───────────────────────► Dataproc (Clúster PySpark)
   (lectura eficiente)                     ✅ Auto-scaling activado
                                           ✅ Múltiples clústeres paralelos
                                           ✅ Sin riesgo de cancelación

3. ALMACENAMIENTO DE RESULTADOS
   Dataproc ────────────────────────────► Cloud Storage (Bucket Processed)
   (resultados del modelo)                 → Datos persistentes y versionados

4. CARGA A DATA WAREHOUSE
   Cloud Storage ───────────────────────► BigQuery
   (tablas finales)                        ✅ Accesibles en segundos

5. CONSULTA DE GERENCIA
   BigQuery ◄───────────────────────────  Gerencia (Consulta SQL directa)
   (sin intermediarios)                    Dashboard en tiempo real
```

---

## Comparación AS-IS vs TO-BE

| Dimensión | Sistema Actual (AS-IS) | Sistema Propuesto (TO-BE) |
|---|---|---|
| **Almacenamiento** | HDFS en discos físicos (fijo) | Cloud Storage (ilimitado) |
| **Cómputo** | Clúster Hadoop compartido | Dataproc (clústeres independientes) |
| **Escalabilidad** | Manual, tarda meses | Automática, en minutos |
| **Concurrencia** | Colapso al usar en paralelo | Clústeres aislados por usuario |
| **Mantenimiento** | TI dedica tiempo a hardware | Gestionado por GCP |
| **Acceso a datos (Gerencia)** | Reportes manuales y tardíos | BigQuery: consultas en tiempo real |
| **Costo** | Fijo (se paga aunque no se use) | Variable (pay-as-you-go) |
| **Disponibilidad** | Dependiente de hardware físico | SLA 99.9%+ garantizado por GCP |
| **Compatibilidad código** | PySpark local | PySpark en Dataproc (100% compatible) |
