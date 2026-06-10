# 📅 Plan de Migración por Fases

## Introducción

La migración a GCP se planifica en **4 fases** progresivas para minimizar el riesgo y garantizar la continuidad del negocio. El enfoque es una **migración gradual** donde el sistema on-premise y el sistema cloud coexisten temporalmente durante la transición.

**Duración total estimada:** 4 meses

---

## Resumen de Fases

```
Mes 1         Mes 2         Mes 3         Mes 4
┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐
│ FASE 1    │ │ FASE 2    │ │ FASE 3    │ │ FASE 4    │
│           │ │           │ │           │ │           │
│ Preparac. │ │ Migración │ │ Migración │ │ Descomisión│
│ y Config. │ │ de Datos  │ │ Completa  │ │ On-Premise│
└───────────┘ └───────────┘ └───────────┘ └───────────┘
```

---

## FASE 1 — Preparación y Configuración (Mes 1)

**Objetivo:** Dejar listo el entorno GCP antes de mover cualquier dato o proceso.

### Actividades

| # | Actividad | Responsable | Duración |
|---|---|---|---|
| 1.1 | Crear proyecto GCP y configurar facturación con alertas de presupuesto | Soporte TI | 2 días |
| 1.2 | Configurar Identity and Access Management (IAM): roles y permisos por actor | Soporte TI | 3 días |
| 1.3 | Crear los buckets de Cloud Storage (raw, processed, staging) | Ingeniero de Datos | 1 día |
| 1.4 | Configurar el dataset de BigQuery y definir esquemas de tablas | Ingeniero de Datos | 3 días |
| 1.5 | Capacitación del equipo en GCP (Cloud Storage, Dataproc, BigQuery) | Todos | 5 días |
| 1.6 | Probar un trabajo PySpark simple en Dataproc (entorno de prueba) | Data Scientist | 3 días |
| 1.7 | Validar compatibilidad del código PySpark existente con Dataproc | Data Scientist | 4 días |

**Entregable de Fase 1:** Entorno GCP operativo y código validado en un entorno de prueba.

**Criterio de éxito:** Al menos un trabajo PySpark real ejecuta exitosamente en Dataproc contra datos de prueba.

---

## FASE 2 — Migración de Datos (Mes 2)

**Objetivo:** Mover los datos históricos desde HDFS a Cloud Storage sin interrumpir el trabajo diario.

### Actividades

| # | Actividad | Responsable | Duración |
|---|---|---|---|
| 2.1 | Inventariar todos los datasets en HDFS (nombre, tamaño, criticidad) | Ingeniero de Datos | 3 días |
| 2.2 | Priorizar la migración (datos más usados primero) | Ingeniero de Datos + Data Scientist | 1 día |
| 2.3 | Migrar datos históricos de baja prioridad a Cloud Storage | Ingeniero de Datos | 5 días |
| 2.4 | Migrar datos críticos y activos a Cloud Storage | Ingeniero de Datos | 5 días |
| 2.5 | Validar integridad de los datos migrados (checksums, conteos) | Ingeniero de Datos | 3 días |
| 2.6 | Mantener sincronización bidireccional HDFS ↔ Cloud Storage durante la transición | Ingeniero de Datos | Todo el mes |

**Entregable de Fase 2:** 100% de los datos históricos disponibles en Cloud Storage, validados.

**Criterio de éxito:** Los datos en Cloud Storage pasan las verificaciones de integridad y son accesibles desde Dataproc.

---

## FASE 3 — Migración de Procesos y Go-Live (Mes 3)

**Objetivo:** Ejecutar todos los trabajos de producción en GCP y dejar de usar el clúster on-premise.

### Actividades

| # | Actividad | Responsable | Duración |
|---|---|---|---|
| 3.1 | Migrar los pipelines de datos al entorno GCP (Dataproc + Cloud Storage) | Ingeniero de Datos | 5 días |
| 3.2 | Ejecutar los trabajos de ML en Dataproc en paralelo al on-premise (modo espejo) | Data Scientist | 5 días |
| 3.3 | Comparar resultados GCP vs on-premise para validar la consistencia | Data Scientist | 3 días |
| 3.4 | Configurar los pipelines de carga hacia BigQuery | Ingeniero de Datos | 3 días |
| 3.5 | Habilitar acceso de Gerencia a BigQuery y capacitarlos en consultas básicas | Soporte TI | 2 días |
| 3.6 | **Go-Live:** cortar el tráfico del clúster on-premise y operar solo en GCP | Todos | 1 día |
| 3.7 | Monitoreo intensivo durante los primeros 7 días post-Go-Live | Soporte TI | 7 días |

**Entregable de Fase 3:** Sistema productivo funcionando 100% en GCP.

**Criterio de éxito:** Los trabajos nocturnos se ejecutan sin interrupciones durante 7 días consecutivos en GCP.

---

## FASE 4 — Descomisión del Sistema On-Premise (Mes 4)

**Objetivo:** Apagar y retirar el clúster físico de manera ordenada, una vez confirmada la estabilidad del nuevo sistema.

### Actividades

| # | Actividad | Responsable | Duración |
|---|---|---|---|
| 4.1 | Confirmar que no hay trabajos ni datos residuales en HDFS | Ingeniero de Datos | 3 días |
| 4.2 | Realizar backup final del clúster on-premise como respaldo de seguridad | Soporte TI | 2 días |
| 4.3 | Apagar gradualmente los nodos del clúster Hadoop | Soporte TI | 3 días |
| 4.4 | Documentar la arquitectura final del sistema GCP | Ingeniero de Datos | 5 días |
| 4.5 | Evaluar y optimizar costos en GCP (redimensionar clústeres, revisar uso) | Soporte TI | 5 días |
| 4.6 | Cierre del proyecto: presentación final a Gerencia | Todos | 1 día |

**Entregable de Fase 4:** Sistema on-premise descomisionado, documentación completa entregada.

**Criterio de éxito:** Servidores físicos apagados; sistema GCP estable por más de 30 días.

---

## Cronograma Resumido (Gantt Simplificado)

```
Actividad                          Sem1  Sem2  Sem3  Sem4  Sem5  Sem6  Sem7  Sem8  Sem9  Sem10  Sem11  Sem12  Sem13  Sem14  Sem15  Sem16
                                   ────  ────  ────  ────  ────  ────  ────  ────  ────  ─────  ─────  ─────  ─────  ─────  ─────  ─────
FASE 1: Config. y Preparación      ████  ████  ████  ████
FASE 2: Migración de Datos                           ████  ████  ████  ████
FASE 3: Migración Procesos + Go-Live                                   ████  ████  ████  ████
FASE 4: Descomisión On-Premise                                                             ████  █████  █████  █████  █████
```

---

## Gestión de Riesgos del Plan

| Riesgo | Fase | Plan de Contingencia |
|---|---|---|
| Incompatibilidad de código PySpark | Fase 1 | Identificar y corregir antes de avanzar a Fase 2 |
| Pérdida de datos durante la migración | Fase 2 | Mantener HDFS activo hasta validar Cloud Storage |
| Resultados diferentes entre on-premise y GCP | Fase 3 | Modo espejo para detectar diferencias antes del Go-Live |
| Resistencia del equipo al cambio | Todas | Comunicación temprana y capacitaciones continuas |
| Costos inesperados en GCP | Todas | Alertas de presupuesto configuradas desde Fase 1 |
