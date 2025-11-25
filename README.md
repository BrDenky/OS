# CPU Scheduling Simulator

Simulador de planificación de CPU implementado en Python para Raspberry Pi. Soporta cuatro algoritmos de planificación: FCFS, SJF (preemptive y non-preemptive), Priority Scheduling, y Round Robin.

## Características

- ✅ **First Come First Serve (FCFS)**: Procesos ejecutados en orden de llegada
- ✅ **Shortest Job First (SJF)**: Versión no preemptiva
- ✅ **Shortest Job First Preemptive (SJF_P/SRTF)**: Versión preemptiva
- ✅ **Priority Scheduling (PS)**: Prioridad 0 = más alta
- ✅ **Round Robin (RR)**: Con quantum de tiempo configurable
- 📊 Salida en consola formateada
- 💾 Exportación automática a CSV
- 📈 Cálculo de métricas: completion time, turnaround time, waiting time

## Requisitos

- Python 3.6 o superior
- No requiere librerías externas (solo módulos estándar)

## Instalación en Raspberry Pi

```bash
# Clonar o copiar los archivos al Raspberry Pi
cd ~/Desktop/OS

# Verificar versión de Python
python3 --version

# Dar permisos de ejecución (opcional)
chmod +x scheduler.py
```

## Uso

### Formato General

```bash
python scheduler.py input_file.csv [FCFS|SJF|SJF_P|PS|RR] [q=time_quantum]
```

### Parámetros

- **input_file.csv**: Ruta al archivo CSV de entrada
- **Algoritmo**: 
  - `FCFS` - First Come First Serve
  - `SJF` - Shortest Job First (Non-Preemptive)
  - `SJF_P` - Shortest Job First (Preemptive/SRTF)
  - `PS` - Priority Scheduling
  - `RR` - Round Robin
- **q=value**: Quantum de tiempo en milisegundos (solo para RR)

### Ejemplos de Ejecución

```bash
# First Come First Serve
python scheduler.py sample_input.csv FCFS

# Shortest Job First (Non-Preemptive)
python scheduler.py sample_input.csv SJF

# Shortest Job First (Preemptive)
python scheduler.py sample_input.csv SJF_P

# Priority Scheduling
python scheduler.py sample_input_priority.csv PS

# Round Robin con quantum de 2ms
python scheduler.py sample_input.csv RR q=2

# Round Robin con quantum de 4ms
python scheduler.py sample_input.csv RR q=4
```

## Formato del Archivo CSV de Entrada

### Para FCFS, SJF, SJF_P, y RR

```csv
pid,arrival_time,burst_time
1,0,8
2,1,4
3,2,9
```

### Para Priority Scheduling (PS)

```csv
pid,arrival_time,burst_time,priority
1,0,8,2
2,1,4,1
3,2,9,0
```

**Nota**: En Priority Scheduling, 0 representa la prioridad más alta.

### Descripción de Columnas

- **pid**: ID único del proceso (entero)
- **arrival_time**: Tiempo de llegada en milisegundos (entero)
- **burst_time**: Tiempo de CPU requerido en milisegundos (entero)
- **priority**: Prioridad del proceso (entero, 0 = más alta) - solo para PS

## Salida

El simulador genera dos tipos de salida:

### 1. Consola (Terminal)

Tabla formateada con las siguientes columnas:
- PID
- Arrival Time
- Burst Time
- Priority (solo para PS)
- Completion Time
- Turnaround Time
- Waiting Time

Además, muestra:
- Average Turnaround Time
- Average Waiting Time

### 2. Archivo CSV

Se genera automáticamente un archivo CSV con los resultados:
- `output_fcfs.csv` - Para FCFS
- `output_sjf.csv` - Para SJF
- `output_sjf_preemptive.csv` - Para SJF_P
- `output_priority.csv` - Para PS
- `output_rr.csv` - Para RR

## Cálculo de Métricas

- **Completion Time**: Tiempo en que el proceso termina su ejecución
- **Turnaround Time**: `completion_time - arrival_time`
- **Waiting Time**: `turnaround_time - burst_time`

## Reglas de Desempate

### Priority Scheduling
Cuando múltiples procesos tienen la misma prioridad:
1. Se selecciona el que llegó primero (FCFS - arrival_time)
2. Si también tienen el mismo arrival_time, se selecciona por PID menor

### SJF (ambas variantes)
Cuando múltiples procesos tienen el mismo burst time (o remaining time):
1. Se selecciona el que llegó primero (arrival_time)
2. Si también tienen el mismo arrival_time, se selecciona por PID menor

## Ejemplo de Salida

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

## Archivos del Proyecto

- `scheduler.py` - Programa principal del simulador
- `sample_input.csv` - Datos de prueba sin prioridades
- `sample_input_priority.csv` - Datos de prueba con prioridades
- `README.md` - Esta documentación

## Notas Importantes

1. **SJF vs SJF_P**: 
   - `SJF` es no preemptivo (el proceso se ejecuta hasta completarse)
   - `SJF_P` es preemptivo (puede interrumpirse si llega un proceso con menor tiempo restante)

2. **Round Robin**: Siempre requiere especificar el quantum con `q=valor`

3. **Archivos de salida**: Se sobrescriben automáticamente en cada ejecución

## Solución de Problemas

### Error: "File not found"
Verifica que la ruta al archivo CSV sea correcta.

### Error: "Missing required column"
Asegúrate de que el CSV tenga las columnas requeridas (pid, arrival_time, burst_time, y priority para PS).

### Error: "Invalid quantum value"
Para Round Robin, el quantum debe ser un entero positivo: `q=2`, `q=5`, etc.

## Autor

Proyecto Final - Sistemas Operativos
Implementado para Raspberry Pi
