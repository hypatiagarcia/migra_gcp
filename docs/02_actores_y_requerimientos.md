# 👥 Documento 2 — Actores y Requerimientos del Sistema

## 2.1 Identificación de Actores

En Análisis de Sistemas, un **actor** es toda persona, rol o sistema externo que interactúa con el sistema que estamos analizando o que tiene interés en él.

---

### Actor 1 — Data Scientist / Analista de Datos

| Atributo | Descripción |
|---|---|
| **Rol** | Usuario principal del sistema |
| **Responsabilidades** | Desarrollar y ejecutar modelos de Machine Learning, transformar datos con PySpark, interpretar resultados |
| **Interacción con el sistema** | Carga trabajos de PySpark, consume almacenamiento de datos, genera reportes |
| **Problema que enfrenta** | Sus procesos se cortan sin previo aviso; debe esperar turnos para trabajar |
| **Expectativa del nuevo sistema** | Poder lanzar trabajos en cualquier momento sin preocuparse por la infraestructura |

---

### Actor 2 — Ingeniero de Datos

| Atributo | Descripción |
|---|---|
| **Rol** | Administrador de pipelines y datos |
| **Responsabilidades** | Construir y mantener los pipelines de ingesta y transformación de datos; gestionar las tablas y esquemas |
| **Interacción con el sistema** | Configura flujos de datos, crea tablas, monitorea la calidad de datos |
| **Problema que enfrenta** | La infraestructura inestable interrumpe los pipelines, generando datos incompletos |
| **Expectativa del nuevo sistema** | Pipelines confiables, herramientas de orquestación modernas, almacenamiento escalable |

---

### Actor 3 — Soporte TI

| Atributo | Descripción |
|---|---|
| **Rol** | Administrador de infraestructura |
| **Responsabilidades** | Mantener operativos los servidores físicos, gestionar hardware, responder a incidencias |
| **Interacción con el sistema** | Reinicia servicios caídos, gestiona discos y memoria, coordina compras de hardware |
| **Problema que enfrenta** | Pasa la mayor parte del tiempo apagando incendios en lugar de agregar valor |
| **Expectativa del nuevo sistema** | Reducir la carga operativa; la nube elimina el mantenimiento de hardware físico |

---

### Actor 4 — Gerencia

| Atributo | Descripción |
|---|---|
| **Rol** | Tomador de decisiones / patrocinador del proyecto |
| **Responsabilidades** | Consumir reportes y predicciones; aprobar presupuestos; definir prioridades estratégicas |
| **Interacción con el sistema** | Consulta dashboards y resultados de modelos; aprueba la inversión en infraestructura |
| **Problema que enfrenta** | Los reportes llegan tarde, lo que retrasa decisiones estratégicas del negocio |
| **Expectativa del nuevo sistema** | Datos disponibles en tiempo y forma; capacidad de hacer consultas ad-hoc sobre BigQuery |

---

## 2.2 Matriz de Actores e Impacto

| Actor | Tipo | Nivel de Impacto | Posición ante el Cambio |
|---|---|---|---|
| Data Scientist / Analista | Interno — Usuario | Alto | Favorable (se beneficia directamente) |
| Ingeniero de Datos | Interno — Usuario | Alto | Favorable (mejora herramientas disponibles) |
| Soporte TI | Interno — Operativo | Medio | Neutral/Favorable (menos trabajo de apagafuegos) |
| Gerencia | Interno — Decisor | Alto | Favorable (mejor información para decidir) |

---

## 2.3 Tabla Completa de Requerimientos

### Requerimientos Funcionales

| ID | Descripción | Actor Relacionado | Prioridad |
|---|---|---|---|
| RF-01 | El sistema debe ejecutar trabajos PySpark en la nube sin interrupciones por recursos insuficientes | Data Scientist | Alta |
| RF-02 | El sistema debe soportar la ejecución concurrente de múltiples trabajos pesados | Data Scientist, Ingeniero de Datos | Alta |
| RF-03 | El sistema debe almacenar los datos crudos y procesados de forma persistente y accesible | Ingeniero de Datos | Alta |
| RF-04 | El sistema debe permitir consultas SQL sobre los resultados finales | Gerencia | Alta |
| RF-05 | El sistema debe escalar automáticamente la capacidad de cómputo según la demanda | Todos | Alta |
| RF-06 | El sistema debe generar logs y registros de ejecución de trabajos | Soporte TI, Ingeniero de Datos | Media |
| RF-07 | El sistema debe permitir gestionar permisos y accesos por usuario | Soporte TI | Media |

### Requerimientos No Funcionales

| ID | Descripción | Tipo | Prioridad |
|---|---|---|---|
| RNF-01 | Disponibilidad mínima del 99.5% mensual | Disponibilidad | Alta |
| RNF-02 | El tiempo de provisión de nueva capacidad debe ser < 15 minutos | Rendimiento | Alta |
| RNF-03 | Compatibilidad total con el código PySpark existente (sin reescritura) | Compatibilidad | Alta |
| RNF-04 | Los datos deben estar cifrados en tránsito y en reposo | Seguridad | Alta |
| RNF-05 | Control de acceso basado en roles (RBAC) | Seguridad | Alta |
| RNF-06 | El costo debe ser variable y basado en consumo real (pay-as-you-go) | Costo | Media |
| RNF-07 | El sistema debe contar con respaldo y recuperación ante desastres | Confiabilidad | Media |

---

## 2.4 Diagrama de Contexto del Sistema

El siguiente diagrama muestra cómo los actores interactúan con el sistema:

```
  [Data Scientist] ──────► Enviar trabajos PySpark
                                    │
  [Ingeniero de Datos] ──► Gestionar pipelines y datos
                                    │
                             ┌──────▼──────┐
                             │   SISTEMA   │
                             │  DE DATA    │
                             │   MINING    │
                             └──────┬──────┘
                                    │
  [Gerencia] ◄──────────── Consultar reportes y resultados
                                    │
  [Soporte TI] ◄──────── Monitorear infraestructura
```
