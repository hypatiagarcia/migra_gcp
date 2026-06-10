# 📊 Resumen Ejecutivo — Propuesta de Migración a la Nube

**Para:** Gerencia General  
**De:** Equipo de Análisis de Sistemas  
**Asunto:** Migración de la Infraestructura de Data Mining a Google Cloud Platform  
**Fecha:** Junio 2025  

---

## ¿Cuál es el problema?

El departamento de Data Mining **no puede operar con eficiencia** porque la infraestructura física quedó chica para el volumen actual de datos.

Esto provoca:
- Trabajos que se cortan a mitad de la noche → hay que empezar de cero al día siguiente
- Analistas que no pueden trabajar en paralelo → pérdida de productividad
- Reportes que llegan tarde a Gerencia → **decisiones estratégicas demoradas**

---

## ¿Qué proponemos?

**Migrar a Google Cloud Platform (GCP)**, una plataforma de nube pública que permite alquilar potencia de cómputo y almacenamiento por internet, pagando solo por lo que se usa.

| Hoy (On-Premise) | Mañana (GCP) |
|---|---|
| Servidores físicos fijos | Recursos ilimitados y elásticos |
| Hadoop/HDFS | Cloud Storage |
| Clúster PySpark compartido | Dataproc (clústeres independientes por analista) |
| Reportes manuales y tardíos | BigQuery (consultas en tiempo real) |

> El código que el equipo ya tiene en PySpark **no necesita reescribirse**. La migración es de infraestructura, no de lógica de negocio.

---

## ¿Qué beneficios obtenemos?

### Para el equipo de Data Mining
✅ Procesos que **no se cortan** por falta de recursos  
✅ Varios analistas trabajando **en paralelo** sin interferencias  
✅ Resultados disponibles **más rápido**

### Para la Gerencia
✅ Acceso **directo y en tiempo real** a los resultados via BigQuery  
✅ Sin depender de que un analista prepare un reporte manual  
✅ Decisiones más ágiles y basadas en datos actualizados

### Para la empresa
✅ **Ahorro económico** a partir del segundo año  
✅ Equipo de TI puede enfocarse en tareas de mayor valor  
✅ Infraestructura que **crece con el negocio** sin burocracia

---

## ¿Cuánto cuesta y cuándo se recupera la inversión?

| | Año 1 | Año 2 | Año 3 |
|---|---|---|---|
| Costo On-Premise (actual) | $39,800 | $39,800 | $39,800 |
| Costo GCP (propuesto) | $44,800* | $36,000 | $36,000 |
| **Diferencia** | -$5,000 | **+$3,800** | **+$3,800** |

> *El mayor costo del año 1 incluye la inversión única en migración y capacitación ($13,000).  
> **A partir del año 2, GCP es más barato.**

**Ahorro acumulado a 3 años: ~$2,600 en costos directos + beneficios indirectos no cuantificados (productividad, estabilidad, velocidad de decisión).**

---

## ¿Cuánto tiempo toma la migración?

**4 meses** organizados en fases graduales para no interrumpir las operaciones:

```
Mes 1: Preparar el entorno GCP y capacitar al equipo
Mes 2: Mover los datos a la nube (sin tocar la operación)
Mes 3: Ejecutar los procesos en GCP (modo paralelo) → Go-Live
Mes 4: Apagar los servidores físicos y optimizar
```

---

## ¿Qué aprobación se necesita?

Para iniciar el proyecto se solicita:

1. ✅ **Aprobación del presupuesto** para el primer año (~$44,800)
2. ✅ **Asignación del equipo** para las actividades de migración (Ingenieros de Datos + TI)
3. ✅ **Acuerdo con GCP** (se puede hacer directamente en cloud.google.com)

---

## Recomendación

> El equipo de Análisis de Sistemas recomienda **aprobar la migración a GCP** cuanto antes. Cada mes que se retrasa la decisión, la empresa sigue operando con riesgo de pérdida de datos, retrasos en reportes y sobrecarga del equipo de TI.
>
> La migración está bien planificada, usa tecnología probada globalmente y el equipo tiene las capacidades para ejecutarla con el soporte adecuado.

---

*Documento elaborado como Trabajo Práctico Final — Materia: Análisis de Sistemas — Ingeniería Informática*
