# 💰 Comparativa de Costos: On-Premise vs Google Cloud Platform

## Introducción

El análisis de costos es un factor clave para la toma de decisión de la gerencia. A continuación se presenta una estimación comparativa entre el modelo actual (on-premise) y el modelo propuesto (GCP), considerando costos directos e indirectos.

> ⚠️ **Nota:** Los valores presentados son estimaciones orientativas con fines académicos. En un proyecto real, se requiere una cotización formal con los valores actualizados del mercado local y de GCP.

---

## Costos del Sistema Actual (On-Premise)

### Costos de Capital (CapEx) — Inversión Inicial

| Ítem | Costo Estimado (USD) | Frecuencia |
|---|---|---|
| Servidores físicos (3 nodos) | $30,000 | Cada 4-5 años |
| Discos adicionales por crecimiento de datos | $5,000 | Anual |
| Licencias y software | $3,000 | Anual |
| **Total CapEx Anualizado** | **~$11,000/año** | — |

### Costos Operativos (OpEx) — Gastos Recurrentes

| Ítem | Costo Estimado (USD/mes) | Costo Anual (USD) |
|---|---|---|
| Electricidad (consumo del clúster) | $600 | $7,200 |
| Tiempo de Soporte TI (dedicación parcial) | $1,500 | $18,000 |
| Refrigeración del data center | $300 | $3,600 |
| **Total OpEx** | **$2,400/mes** | **$28,800/año** |

### **Total Sistema Actual: ~$39,800/año**

---

## Costos del Sistema Propuesto (GCP)

### Servicios GCP Utilizados

| Servicio | Uso Estimado | Costo Estimado (USD/mes) |
|---|---|---|
| **Cloud Storage** | 50TB de datos | $1,000 |
| **Dataproc** | 500 horas de clúster/mes (clústeres efímeros) | $1,200 |
| **BigQuery** | 10TB procesados en consultas | $50 |
| **Networking y otros** | — | $150 |
| **Total GCP** | — | **$2,400/mes** |

### Costos Adicionales GCP

| Ítem | Costo |
|---|---|
| Soporte TI (menor dedicación) | $600/mes |
| Capacitación del equipo (única vez) | $5,000 |
| Migración y consultoría (única vez) | $8,000 |

### **Total Sistema GCP (primer año): ~$44,800**
### **Total Sistema GCP (años siguientes): ~$36,000/año**

---

## Tabla Comparativa

| Concepto | On-Premise | GCP (año 1) | GCP (año 2+) |
|---|---|---|---|
| Costo anual total | $39,800 | $44,800 | $36,000 |
| Elasticidad | ❌ Ninguna | ✅ Total | ✅ Total |
| Costo en horas de baja demanda | 💰 Igual (fijo) | 💚 Menor (pay-as-you-go) | 💚 Menor |
| Riesgo de proceso cancelado | ⚠️ Alto | ✅ Bajo | ✅ Bajo |
| Tiempo de TI en mantenimiento | ⚠️ Alto | ✅ Bajo | ✅ Bajo |
| Tiempo de provisión de recursos | ⏳ Meses | ⚡ Minutos | ⚡ Minutos |

---

## Análisis de Retorno de Inversión (ROI)

### Beneficios Cuantificables

| Beneficio | Valor Estimado/Año |
|---|---|
| Ahorro en tiempo de TI liberado | $10,000 |
| Reducción de pérdidas por trabajos cancelados (retrasos) | $8,000 |
| Reducción de electricidad y refrigeración | $10,800 |
| **Total beneficios estimados** | **$28,800/año** |

### Conclusión del Análisis de Costos

> Aunque el primer año puede tener un costo ligeramente superior por los gastos de migración y capacitación, **a partir del segundo año el sistema GCP representa un ahorro neto** en comparación con el modelo on-premise, considerando tanto los costos directos como los beneficios indirectos (productividad, estabilidad, escalabilidad).

```
       Costo
  $50k │
  $45k │         ■ On-Premise
  $40k │   ■     ■ GCP
  $35k │         ■
  $30k │   ■         ■    ■    ■
  $25k │
       └──────────────────────────
            Año 1  Año 2  Año 3  Año 4

  Ahorro acumulado a 3 años: ~$15,000
```
