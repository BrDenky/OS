# First Come First Serve (FCFS) scheduling algorithm.
from typing import List
from copy import deepcopy
from .models import Process


def fcfs_scheduler(processes: List[Process]) -> List[Process]:
    processes = deepcopy(processes)
    processes.sort(key=lambda p: (p.arrival_time, p.pid)) # Ordena por AT, y si AT es igual, ordena por PID
    
    current_time = 0 # Tiempo actual CPU
    for process in processes:
        # Si el CPU esta en idle, avanzamos al tiempo de llegada del proceso
        if current_time < process.arrival_time:
            current_time = process.arrival_time

        # Registro de inicio y ejecución del proceso completo (sin interrupciones)
        process.start_time = current_time
        current_time += process.burst_time

        # Calculo de CT, TTA y WT
        process.completion_time = current_time
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time
    
    return processes