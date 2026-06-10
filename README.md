# 🌐 Migración a la Nube — Caso de Estudio: Empresa de Telecomunicaciones

**Materia:** Análisis de Sistemas  
**Carrera:** Ingeniería Informática  
**Tipo:** Trabajo Práctico Final  

---

## 📋 Descripción del Proyecto

Este repositorio contiene el análisis completo de un caso de estudio real sobre la **migración de infraestructura on-premise a la nube pública (Google Cloud Platform)** para el departamento de Data Mining de una empresa de telecomunicaciones.

El proyecto aplica metodologías de Análisis de Sistemas para identificar problemas, modelar el sistema actual, proponer soluciones y documentar el proceso de transición tecnológica.

---

## 📁 Estructura del Repositorio

```
📦 proyecto-migracion-nube/
├── 📄 README.md                        ← Este archivo
├── 📁 docs/
│   ├── 01_descripcion_problema.md      ← Relevamiento y análisis del problema
│   ├── 02_actores_y_requerimientos.md  ← Identificación de actores y requerimientos
│   └── 03_propuesta_solucion.md        ← Propuesta técnica detallada
├── 📁 diagramas/
│   ├── diagrama_sistema_actual.md      ← Descripción textual del sistema actual (AS-IS)
│   ├── diagrama_sistema_propuesto.md   ← Descripción textual del sistema futuro (TO-BE)
│   └── casos_de_uso.md                ← Casos de uso principales
├── 📁 propuesta/
│   ├── comparativa_costos.md           ← Análisis de costos on-premise vs nube
│   └── plan_migracion.md               ← Plan de migración por fases
└── 📁 presentacion/
    └── resumen_ejecutivo.md            ← Resumen para la gerencia
```

---

## 🎯 Objetivos del Trabajo

1. Aplicar técnicas de relevamiento y análisis de sistemas al caso dado
2. Identificar actores, problemas y requerimientos del sistema actual
3. Modelar el sistema actual (AS-IS) y el sistema propuesto (TO-BE)
4. Elaborar una propuesta de solución fundamentada técnicamente
5. Analizar el impacto y viabilidad de la migración

---

## 🛠️ Tecnologías Involucradas

| Sistema Actual (On-Premise) | Sistema Propuesto (GCP) |
|---|---|
| Servidores físicos propios | Google Cloud Platform |
| Hadoop (HDFS) | Cloud Storage |
| PySpark en clúster local | Dataproc |
| Reportes manuales | BigQuery |

---

## 👥 Actores del Sistema

- **Data Scientists / Analistas** — Programan en PySpark, consumen el sistema
- **Ingenieros de Datos** — Administran pipelines y tablas
- **Soporte TI** — Mantienen la infraestructura física
- **Gerencia** — Consumen resultados, aprueban presupuesto

---

## 📚 Cómo navegar este proyecto

Se recomienda leer los documentos en este orden:

1. `docs/01_descripcion_problema.md` — Entender el contexto
2. `docs/02_actores_y_requerimientos.md` — Identificar involucrados
3. `diagramas/diagrama_sistema_actual.md` — Ver cómo funciona hoy
4. `docs/03_propuesta_solucion.md` — Leer la solución propuesta
5. `diagramas/diagrama_sistema_propuesto.md` — Ver la arquitectura futura
6. `propuesta/plan_migracion.md` — Entender los pasos de transición
7. `presentacion/resumen_ejecutivo.md` — Resumen final
