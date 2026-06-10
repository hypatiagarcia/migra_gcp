# 📌 Documento 1 — Descripción del Problema

## 1.1 Situación Actual

El departamento de **Data Mining** de la empresa de telecomunicaciones opera sobre una infraestructura **on-premise** (servidores físicos propios). Utilizan un clúster Hadoop para almacenamiento de datos y PySpark para transformaciones y entrenamiento de modelos de Machine Learning.

Esta infraestructura fue suficiente en años anteriores, pero el **crecimiento exponencial del volumen de datos durante el último año** la llevó al límite de su capacidad.

---

## 1.2 Problemas Identificados

### Problema 1 — Corte de Procesos (Fallo por Recursos)

| Campo | Detalle |
|---|---|
| **Descripción** | Los servidores se quedan sin RAM o CPU durante la noche al entrenar modelos o transformar datos pesados, y el proceso se cancela. |
| **Consecuencia directa** | Al día siguiente hay que reiniciar el proceso desde cero, perdiendo horas de cómputo. |
| **Tipo de problema** | Capacidad de hardware insuficiente |
| **Frecuencia** | Recurrente (nocturno) |

### Problema 2 — Cuello de Botella por Concurrencia

| Campo | Detalle |
|---|---|
| **Descripción** | Si dos analistas ejecutan procesos pesados simultáneamente, el clúster se vuelve muy lento o colapsa. |
| **Consecuencia directa** | Los analistas deben turnarse para trabajar, reduciendo la productividad del equipo. |
| **Tipo de problema** | Escalabilidad horizontal inexistente |
| **Frecuencia** | Diaria |

### Problema 3 — Mantenimiento Lento y Costoso

| Campo | Detalle |
|---|---|
| **Descripción** | Ampliar la infraestructura (discos, memoria, procesadores) requiere meses de burocracia, alto costo y tiempo del equipo de TI. |
| **Consecuencia directa** | La empresa no puede responder ágilmente al crecimiento del negocio. |
| **Tipo de problema** | Rigidez organizacional e infraestructural |
| **Frecuencia** | Cada vez que se necesita escalar |

---

## 1.3 Análisis de Impacto

### ¿Cuál es el problema principal?
> Los servidores físicos quedaron subdimensionados para el volumen de datos actual, y la burocracia interna impide escalar la infraestructura en tiempo útil.

### ¿Qué consecuencias tiene para el negocio?

- **Retrasos operativos:** los analistas pierden horas reiniciando procesos fallidos.
- **Decisiones tardías:** la gerencia no recibe los reportes y predicciones a tiempo.
- **Subutilización del talento:** el equipo técnico pierde tiempo en tareas de soporte en lugar de agregar valor.
- **Costos ocultos:** electricidad, tiempo de TI y hardware con vida útil limitada.

### ¿Qué áreas están afectadas?

| Área | Impacto |
|---|---|
| Data Mining | No pueden trabajar con fluidez ni en paralelo |
| Soporte TI | Dedican tiempo excesivo a reiniciar servidores y parches de emergencia |
| Gerencia | No disponen de datos actualizados para tomar decisiones estratégicas |

---

## 1.4 Árbol de Problemas (Causa — Problema — Efecto)

```
                    ┌────────────────────────────────┐
                    │        EFECTOS / SÍNTOMAS       │
                    ├────────────────────────────────┤
                    │ • Reportes llegan tarde         │
                    │ • Decisiones gerenciales lentas │
                    │ • Analistas improductivos       │
                    └────────────┬───────────────────┘
                                 │
                    ┌────────────▼───────────────────┐
                    │       PROBLEMA CENTRAL          │
                    ├────────────────────────────────┤
                    │  Infraestructura física         │
                    │  insuficiente y no escalable    │
                    └────────────┬───────────────────┘
                                 │
                    ┌────────────▼───────────────────┐
                    │          CAUSAS RAÍZ            │
                    ├────────────────────────────────┤
                    │ • Crecimiento imprevisto de     │
                    │   datos en el último año        │
                    │ • Modelo de infraestructura     │
                    │   on-premise sin elasticidad    │
                    │ • Burocracia lenta para         │
                    │   aprobación de hardware        │
                    └────────────────────────────────┘
```

---

## 1.5 Requerimientos Detectados (Preliminares)

A partir del análisis de problemas, se identifican los siguientes requerimientos de alto nivel:

### Requerimientos Funcionales
- **RF-01:** El sistema debe poder ejecutar procesos de PySpark sin interrupciones por falta de recursos.
- **RF-02:** El sistema debe permitir la ejecución simultánea de procesos pesados por múltiples analistas.
- **RF-03:** El sistema debe permitir consultas sobre datos finales por parte de la gerencia.
- **RF-04:** El sistema debe escalar su capacidad de cómputo bajo demanda.

### Requerimientos No Funcionales
- **RNF-01:** La disponibilidad del sistema debe ser ≥ 99.5% mensual.
- **RNF-02:** El tiempo de provisión de nueva capacidad debe ser menor a 15 minutos.
- **RNF-03:** El sistema debe mantener la compatibilidad con el código PySpark existente.
- **RNF-04:** Los datos deben estar protegidos con controles de acceso por rol.
- **RNF-05:** El costo debe ser predecible y basado en consumo real.
