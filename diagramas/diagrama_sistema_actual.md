# 🗺️ Diagrama del Sistema Actual (AS-IS)

## Descripción del Sistema Actual

El sistema actual opera enteramente sobre hardware físico propio ubicado en las instalaciones de la empresa. A continuación se describe su arquitectura y sus flujos de datos.

---

## Arquitectura AS-IS

```
╔═══════════════════════════════════════════════════════════════════╗
║              INFRAESTRUCTURA ON-PREMISE (SERVIDORES FÍSICOS)      ║
║                                                                   ║
║   ┌───────────────────────────────────────────────────────────┐   ║
║   │                   CLÚSTER HADOOP                          │   ║
║   │                                                           │   ║
║   │   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   │   ║
║   │   │  Nodo 1     │   │  Nodo 2     │   │  Nodo 3     │   │   ║
║   │   │  (Master)   │   │  (Worker)   │   │  (Worker)   │   │   ║
║   │   │  RAM: 32GB  │   │  RAM: 16GB  │   │  RAM: 16GB  │   │   ║
║   │   └──────┬──────┘   └──────┬──────┘   └──────┬──────┘   │   ║
║   │          └─────────────────┴──────────────────┘          │   ║
║   │                             │                             │   ║
║   │                    ┌────────▼────────┐                   │   ║
║   │                    │   HDFS Storage  │                   │   ║
║   │                    │  (Datos en      │                   │   ║
║   │                    │   discos físicos│                   │   ║
║   │                    └─────────────────┘                   │   ║
║   └───────────────────────────────────────────────────────────┘   ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
                              ▲     ▲
                              │     │
              ┌───────────────┘     └──────────────┐
              │                                    │
   ┌──────────┴──────────┐             ┌──────────┴──────────┐
   │  Data Scientist A   │             │  Data Scientist B   │
   │  (PySpark Job)      │             │  (PySpark Job)      │
   │                     │             │                     │
   │  ⚠️ Si ambos        │             │  ⚠️ Debe esperar    │
   │  corren a la vez,   │             │  a que A termine    │
   │  el clúster colapsa │             │                     │
   └─────────────────────┘             └─────────────────────┘
```

---

## Flujo de Datos AS-IS

```
1. INGESTA DE DATOS
   Fuente de datos ──────────────────────► HDFS (disco físico)
   (archivos CSV, logs, etc.)              Espacio limitado

2. PROCESAMIENTO
   HDFS ────────────────────────────────► PySpark (clúster local)
   (lectura de datos)                      ⚠️ Sin memoria suficiente
                                           ⚠️ Sin CPU disponible
                                           → PROCESO CANCELADO

3. RESULTADOS (cuando no falla)
   PySpark ─────────────────────────────► Archivos en HDFS / CSV
   (tablas transformadas)                  → Entrega manual a gerencia

4. CONSULTA DE GERENCIA
   CSV / Excel ◄────────────────────────  Analista prepara el reporte
   (proceso manual, tardío)               manualmente
```

---

## Problemas Mapeados al Diagrama

| Nodo del Diagrama | Problema |
|---|---|
| Nodo Master (RAM 32GB) | Se queda sin memoria al procesar grandes volúmenes → cancela trabajos |
| Nodos Worker | Sin capacidad de escalar; son físicos y fijos |
| HDFS | Espacio en disco físico limitado; agregar discos tarda meses |
| PySpark concurrente | Si dos analistas ejecutan al mismo tiempo → colapso del clúster |
| Entrega a Gerencia | Proceso manual, sin acceso directo a los datos |

---

## Limitaciones Estructurales del Sistema Actual

1. **Sin elasticidad:** La capacidad es fija. No puede aumentarse ni disminuirse según la demanda.
2. **Sin redundancia automática:** Si un nodo falla, no existe failover automático.
3. **Sin aislamiento de cargas:** Todos los usuarios comparten los mismos recursos físicos.
4. **Ciclo de mejora lento:** Cualquier mejora de hardware requiere compra, instalación y configuración → meses de espera.
5. **Costo fijo elevado:** Se paga por la capacidad máxima instalada, aunque el 80% del tiempo esté subutilizada.
