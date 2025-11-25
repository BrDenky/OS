# Proyecto Final - Sistemas Operativos
## Simulador de Planificación de CPU

### 📋 Resumen del Proyecto

Este proyecto implementa un simulador completo de planificación de CPU en Python, diseñado para ejecutarse en Raspberry Pi. El simulador soporta cinco algoritmos de planificación diferentes y proporciona análisis detallado de métricas de rendimiento.

### ✅ Algoritmos Implementados

1. **FCFS (First Come First Serve)**
   - Algoritmo no preemptivo
   - Procesos ejecutados en orden de llegada
   - Simple pero puede causar "convoy effect"

2. **SJF (Shortest Job First) - Non-Preemptive**
   - Selecciona el proceso con menor burst time
   - Minimiza tiempo de espera promedio
   - No interrumpe procesos en ejecución

3. **SJF_P (Shortest Job First) - Preemptive (SRTF)**
   - Versión preemptiva de SJF
   - Puede interrumpir si llega proceso más corto
   - Óptimo para minimizar tiempo de espera

4. **PS (Priority Scheduling)**
   - Basado en prioridades (0 = más alta)
   - Desempate: arrival_time → pid
   - No preemptivo

5. **RR (Round Robin)**
   - Quantum de tiempo configurable
   - Equitativo para todos los procesos
   - Ideal para sistemas interactivos

### 📊 Características

- ✅ Lectura de procesos desde archivos CSV
- ✅ Cálculo automático de métricas:
  - Completion Time
  - Turnaround Time
  - Waiting Time
- ✅ Salida formateada en consola
- ✅ Exportación automática a CSV
- ✅ Promedios de turnaround y waiting time
- ✅ Manejo robusto de errores
- ✅ Reglas de desempate bien definidas

### 📁 Archivos del Proyecto

#### Archivos Principales
- **scheduler.py** (14.8 KB)
  - Programa principal del simulador
  - Implementación de todos los algoritmos
  - Parser de argumentos CLI
  - Sistema de métricas y exportación

#### Archivos de Prueba
- **sample_input.csv** - 5 procesos sin prioridades
- **sample_input_priority.csv** - 5 procesos con prioridades
- **example_input.csv** - 7 procesos para pruebas extensivas
- **test_scheduler.py** - Script de pruebas automatizadas

#### Documentación
- **README.md** - Documentación principal en español
- **GUIA_USO.md** - Guía detallada con ejemplos prácticos
- **QUICK_REFERENCE.md** - Referencia rápida de comandos

#### Archivos de Salida (generados)
- output_fcfs.csv
- output_sjf.csv
- output_sjf_preemptive.csv
- output_priority.csv
- output_rr.csv

### 🚀 Uso Rápido

```bash
# FCFS
python scheduler.py sample_input.csv FCFS

# SJF (Non-Preemptive)
python scheduler.py sample_input.csv SJF

# SJF (Preemptive)
python scheduler.py sample_input.csv SJF_P

# Priority Scheduling
python scheduler.py sample_input_priority.csv PS

# Round Robin
python scheduler.py sample_input.csv RR q=2

# Ejecutar todas las pruebas
python test_scheduler.py
```

### 📈 Ejemplo de Salida

```
====================================================================================================
CPU Scheduling Algorithm: First Come First Serve (FCFS)
====================================================================================================
PID     Arrival     Burst       Completion     Turnaround     Waiting     
----------------------------------------------------------------------------------------------------
1       0           8           8              8              0           
2       1           4           12             11             7           
3       2           9           21             19             10          
4       3           5           26             23             18          
5       4           2           28             24             22          
----------------------------------------------------------------------------------------------------
Average Turnaround Time: 17.00 ms
Average Waiting Time: 11.40 ms
====================================================================================================

Results saved to: output_fcfs.csv
```

### 🔍 Formato de Entrada CSV

#### Sin Prioridades (FCFS, SJF, SJF_P, RR)
```csv
pid,arrival_time,burst_time
1,0,8
2,1,4
3,2,9
```

#### Con Prioridades (PS)
```csv
pid,arrival_time,burst_time,priority
1,0,8,2
2,1,4,1
3,2,9,0
```

### 📊 Formato de Salida CSV

```csv
pid,arrival_time,burst_time,completion_time,turnaround_time,waiting_time
1,0,8,8,8,0
2,1,4,12,11,7
3,2,9,21,19,10
```

### 🎯 Reglas de Implementación

#### Desempate en Priority Scheduling
1. Menor número de prioridad (0 es más alta)
2. Si empatan: menor arrival_time (FCFS)
3. Si aún empatan: menor PID

#### Desempate en SJF/SJF_P
1. Menor burst_time (o remaining_time para preemptivo)
2. Si empatan: menor arrival_time
3. Si aún empatan: menor PID

### ✅ Verificación y Pruebas

El proyecto incluye:
- ✅ Datos de prueba para cada algoritmo
- ✅ Script de pruebas automatizado
- ✅ Ejemplos de verificación manual
- ✅ Casos de prueba para edge cases

### 🎓 Objetivos Cumplidos

- [x] Implementación de FCFS
- [x] Implementación de SJF (Non-Preemptive)
- [x] Implementación de SJF (Preemptive/SRTF)
- [x] Implementación de Priority Scheduling
- [x] Implementación de Round Robin
- [x] Lectura desde CSV
- [x] Cálculo de completion_time
- [x] Cálculo de turnaround_time
- [x] Cálculo de waiting_time
- [x] Salida formateada en consola
- [x] Exportación a CSV
- [x] Manejo de errores
- [x] Documentación completa
- [x] Casos de prueba

### 🔧 Requisitos Técnicos

- **Python**: 3.6 o superior
- **Librerías**: Solo módulos estándar (sys, csv, dataclasses, copy)
- **Plataforma**: Compatible con Raspberry Pi y cualquier sistema con Python
- **Sin dependencias externas**: No requiere pip install

### 📝 Notas Importantes

1. **Todos los tiempos en milisegundos** (enteros)
2. **Prioridad 0 = más alta** en Priority Scheduling
3. **SJF vs SJF_P**: Dos implementaciones diferentes (preemptivo y no preemptivo)
4. **Round Robin**: Requiere especificar quantum obligatoriamente
5. **Archivos de salida**: Se sobrescriben en cada ejecución

### 🎉 Características Adicionales

- Código bien documentado con docstrings
- Uso de dataclasses para mejor organización
- Validación robusta de entrada
- Mensajes de error descriptivos
- Formato de tabla alineado y legible
- Cálculo de promedios automático

### 📚 Recursos Incluidos

1. **README.md**: Guía de instalación y uso básico
2. **GUIA_USO.md**: Ejemplos prácticos y casos de uso
3. **QUICK_REFERENCE.md**: Referencia rápida de comandos
4. **test_scheduler.py**: Suite de pruebas automatizadas
5. **Múltiples archivos CSV de ejemplo**: Para diferentes escenarios

---

**Proyecto completado y listo para demostración en Raspberry Pi** ✅

Total de líneas de código: ~450 líneas (scheduler.py)
Total de archivos: 13
Documentación: 3 archivos markdown completos
