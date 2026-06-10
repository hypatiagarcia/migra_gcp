# 💡 Documento 3 — Propuesta de Solución

## 3.1 Solución Propuesta

Se propone realizar una **migración completa a Google Cloud Platform (GCP)**, abandonando el modelo on-premise y adoptando un esquema **cloud-native** donde la capacidad de cómputo y almacenamiento se alquila de forma elástica.

La migración mantiene las **mismas herramientas de desarrollo** que el equipo ya conoce (PySpark), por lo que no se requiere reescribir el código existente.

---

## 3.2 Arquitectura Propuesta en GCP

### Componentes del Sistema

#### 1. Cloud Storage (Reemplaza a Hadoop/HDFS)

| Atributo | Detalle |
|---|---|
| **Función** | Almacenamiento de objetos para datos crudos, procesados e intermedios |
| **Reemplaza** | HDFS (Hadoop Distributed File System) |
| **Capacidad** | Ilimitada, escala automáticamente |
| **Ventaja clave** | Alta durabilidad (99.999999999%), acceso desde cualquier servicio de GCP |

#### 2. Dataproc (Reemplaza al Clúster Hadoop On-Premise)

| Atributo | Detalle |
|---|---|
| **Función** | Clúster administrado para ejecutar trabajos PySpark |
| **Reemplaza** | El clúster físico Hadoop con PySpark |
| **Modalidad** | Clústeres efímeros (se crean para un trabajo y se destruyen al terminar) |
| **Ventaja clave** | Compatibilidad 100% con PySpark; escala en minutos; sin mantenimiento |

#### 3. BigQuery (Capa de Análisis para Gerencia)

| Atributo | Detalle |
|---|---|
| **Función** | Data Warehouse serverless para almacenar tablas finales y hacer consultas SQL |
| **Reemplaza** | Los reportes manuales que se entregaban a gerencia |
| **Modalidad** | Serverless; pago por consulta o por almacenamiento |
| **Ventaja clave** | Consultas sobre terabytes en segundos; accesible sin conocimientos de programación |

---

## 3.3 Flujo de Trabajo en el Sistema Propuesto

```
  Datos Fuente
      │
      ▼
┌─────────────────┐      ┌──────────────────────┐
│  Cloud Storage  │◄─────│  Ingeniero de Datos  │
│  (Datos Crudos) │      │  (Carga los datos)   │
└────────┬────────┘      └──────────────────────┘
         │
         │ Lee datos
         ▼
┌─────────────────┐      ┌──────────────────────┐
│    Dataproc     │◄─────│  Data Scientist       │
│ (PySpark Jobs)  │      │  (Lanza el trabajo)   │
└────────┬────────┘      └──────────────────────┘
         │
         │ Escribe resultados
         ▼
┌─────────────────┐      ┌──────────────────────┐
│  Cloud Storage  │      │                      │
│(Datos Procesados│      │                      │
└────────┬────────┘      └──────────────────────┘
         │
         │ Carga final
         ▼
┌─────────────────┐      ┌──────────────────────┐
│    BigQuery     │◄─────│      Gerencia         │
│  (Tablas        │      │  (Consultas SQL /     │
│   Finales)      │      │   Dashboards)         │
└─────────────────┘      └──────────────────────┘
```

---

## 3.4 Beneficios de la Solución

### Beneficio 1 — Escalabilidad Instantánea
El equipo puede solicitar más nodos de cómputo en minutos, sin burocracia ni esperas de meses. Dataproc permite aumentar el tamaño del clúster con un comando o desde la consola web.

### Beneficio 2 — Estabilidad de los Procesos
Al contar con recursos virtualmente ilimitados, los trabajos nocturnos de entrenamiento ya no serán cancelados. Si un trabajo necesita más RAM, se provisiona automáticamente.

### Beneficio 3 — Trabajo Concurrente
Cada analista puede tener su propio clúster efímero. Ya no hay competencia por recursos: mientras el Analista A entrena un modelo, el Analista B puede transformar datos sin ningún impacto mutuo.

### Beneficio 4 — Reducción de Carga en TI
El equipo de Soporte TI deja de administrar hardware físico. GCP se encarga del mantenimiento, parches, redundancia y disponibilidad. TI puede redirigir su trabajo hacia tareas de mayor valor.

### Beneficio 5 — Acceso a Datos para la Gerencia
BigQuery permite que la gerencia haga consultas SQL directamente sobre las tablas de resultados, en tiempo real, sin depender de reportes manuales del equipo de datos.

### Beneficio 6 — Costo Variable (Pay-as-you-go)
En lugar de pagar por capacidad fija aunque no se use, la empresa paga únicamente por los recursos consumidos. Esto alinea el costo con el uso real del sistema.

---

## 3.5 Riesgos y Mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| Resistencia al cambio por parte del equipo | Media | Medio | Capacitaciones previas a la migración; migración gradual |
| Costos inesperados por mal uso de la nube | Media | Alto | Implementar alertas de presupuesto (Budget Alerts) en GCP |
| Problemas de compatibilidad de código | Baja | Alto | Pruebas de compatibilidad en entorno staging antes de producción |
| Dependencia de un único proveedor (vendor lock-in) | Baja | Medio | Documentar arquitectura de forma agnóstica; usar estándares abiertos |
| Seguridad y privacidad de datos sensibles | Baja | Alto | Cifrado en reposo y tránsito; políticas IAM estrictas; auditorías |
