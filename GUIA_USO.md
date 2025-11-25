# Guía de Uso - Simulador de Planificación de CPU

## Ejemplos Prácticos

### Ejemplo 1: Comparar FCFS vs SJF

```bash
# Ejecutar FCFS
python scheduler.py sample_input.csv FCFS

# Ejecutar SJF (Non-Preemptive)
python scheduler.py sample_input.csv SJF

# Ejecutar SJF (Preemptive)
python scheduler.py sample_input.csv SJF_P
```

**Observaciones:**
- FCFS es simple pero puede causar el "convoy effect" (procesos cortos esperan a procesos largos)
- SJF minimiza el tiempo de espera promedio
- SJF_P (preemptivo) puede interrumpir procesos si llega uno más corto

### Ejemplo 2: Priority Scheduling

```bash
python scheduler.py sample_input_priority.csv PS
```

**Nota:** Recuerda que 0 es la prioridad más alta. Los procesos con menor número se ejecutan primero.

### Ejemplo 3: Round Robin con diferentes Quantums

```bash
# Quantum pequeño (2ms) - más cambios de contexto
python scheduler.py sample_input.csv RR q=2

# Quantum mediano (4ms)
python scheduler.py sample_input.csv RR q=4

# Quantum grande (10ms) - se aproxima a FCFS
python scheduler.py sample_input.csv RR q=10
```

**Observaciones:**
- Quantum muy pequeño → muchos cambios de contexto → overhead alto
- Quantum muy grande → se comporta como FCFS
- Quantum óptimo depende del sistema y tipo de procesos

## Crear tus propios archivos de entrada

### Plantilla básica (sin prioridades)

```csv
pid,arrival_time,burst_time
1,0,5
2,2,3
3,4,8
```

### Plantilla con prioridades

```csv
pid,arrival_time,burst_time,priority
1,0,5,2
2,2,3,0
3,4,8,1
```

## Interpretación de Resultados

### Métricas Clave

1. **Completion Time**: Cuándo termina el proceso
   - Útil para saber el tiempo total de ejecución

2. **Turnaround Time**: Tiempo total desde llegada hasta finalización
   - `turnaround_time = completion_time - arrival_time`
   - Mide la experiencia del usuario

3. **Waiting Time**: Tiempo que el proceso espera en la cola
   - `waiting_time = turnaround_time - burst_time`
   - Indica eficiencia del algoritmo

### ¿Qué algoritmo es mejor?

Depende de tus objetivos:

- **Minimizar tiempo de espera promedio**: SJF o SJF_P
- **Fairness (equidad)**: Round Robin
- **Simplicidad**: FCFS
- **Procesos críticos**: Priority Scheduling
- **Sistemas interactivos**: Round Robin con quantum pequeño
- **Sistemas batch**: SJF o FCFS

## Verificación Manual de Resultados

### Ejemplo FCFS con sample_input.csv

Procesos:
```
PID | Arrival | Burst
1   | 0       | 8
2   | 1       | 4
3   | 2       | 9
4   | 3       | 5
5   | 4       | 2
```

Cálculo manual:
```
P1: Start=0, End=8, Turnaround=8-0=8, Waiting=8-8=0
P2: Start=8, End=12, Turnaround=12-1=11, Waiting=11-4=7
P3: Start=12, End=21, Turnaround=21-2=19, Waiting=19-9=10
P4: Start=21, End=26, Turnaround=26-3=23, Waiting=23-5=18
P5: Start=26, End=28, Turnaround=28-4=24, Waiting=24-2=22

Avg Turnaround = (8+11+19+23+24)/5 = 17.00
Avg Waiting = (0+7+10+18+22)/5 = 11.40
```

Verifica que estos valores coincidan con la salida del programa.

## Casos de Prueba Recomendados

### Caso 1: Convoy Effect (FCFS)
Proceso largo llega primero, procesos cortos esperan mucho.

```csv
pid,arrival_time,burst_time
1,0,20
2,1,2
3,2,3
```

### Caso 2: Starvation en Priority
Procesos de baja prioridad pueden esperar indefinidamente.

```csv
pid,arrival_time,burst_time,priority
1,0,5,0
2,1,3,0
3,2,8,5
4,3,2,0
```

### Caso 3: Round Robin vs FCFS
Comparar fairness.

```csv
pid,arrival_time,burst_time
1,0,10
2,0,5
3,0,8
```

Ejecuta:
```bash
python scheduler.py test_case.csv FCFS
python scheduler.py test_case.csv RR q=2
```

## Troubleshooting

### Problema: Los resultados no coinciden con cálculos manuales

**Solución:**
1. Verifica que el archivo CSV no tenga espacios extra
2. Asegúrate de usar el algoritmo correcto
3. Para RR, verifica el quantum
4. Revisa las reglas de desempate (arrival_time, luego pid)

### Problema: "Invalid data in CSV file"

**Solución:**
- Todos los valores deben ser enteros positivos
- No dejes celdas vacías
- Usa comas como separadores, no punto y coma

### Problema: Round Robin toma mucho tiempo

**Solución:**
- Si tienes procesos con burst_time muy largo y quantum muy pequeño, el algoritmo puede tardar
- Considera usar un quantum más grande o reducir los burst_times

## Exportar Resultados

Los archivos CSV generados pueden abrirse en:
- Microsoft Excel
- Google Sheets
- LibreOffice Calc
- Python (pandas)

Ejemplo con pandas:
```python
import pandas as pd

df = pd.read_csv('output_fcfs.csv')
print(df)
print(f"Avg Turnaround: {df['turnaround_time'].mean():.2f}")
print(f"Avg Waiting: {df['waiting_time'].mean():.2f}")
```

## Preguntas Frecuentes

**P: ¿Por qué SJF_P da resultados diferentes a SJF?**
R: SJF_P es preemptivo, puede interrumpir un proceso si llega uno con menor tiempo restante.

**P: ¿Qué pasa si dos procesos tienen la misma prioridad?**
R: Se usa FCFS (arrival_time) como desempate. Si también tienen el mismo arrival_time, se usa el PID.

**P: ¿El quantum en RR debe ser múltiplo de algo?**
R: No, puede ser cualquier entero positivo. Experimenta con diferentes valores.

**P: ¿Puedo usar decimales en los tiempos?**
R: No, todos los tiempos deben ser enteros (milisegundos).

**P: ¿Cómo simulo procesos que llegan al mismo tiempo?**
R: Usa el mismo arrival_time para múltiples procesos.

## Recursos Adicionales

- [Operating System Concepts - Silberschatz](https://www.os-book.com/)
- [CPU Scheduling - GeeksforGeeks](https://www.geeksforgeeks.org/cpu-scheduling-in-operating-systems/)
- [Raspberry Pi Documentation](https://www.raspberrypi.org/documentation/)
