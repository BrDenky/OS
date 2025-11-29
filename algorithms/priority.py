# Priority Scheduling (Non-Preemptive) algorithm.
# Lower priority number = Higher priority.
from typing import List
from copy import deepcopy
from .models import Process


def priority_scheduler(processes: List[Process]) -> List[Process]:
    processes = deepcopy(processes)
    n = len(processes)
    completed = []
    current_time = 0
    completed_count = 0
    
    while completed_count < n:
        # Find available processes
        # Encontrar procesos disponibles para ejecutar
        available = []
        for process in processes:
            has_arrived = process.arrival_time <= current_time
            not_completed = process not in completed

            if has_arrived and not_completed:
                available.append(process)

        if not available:
            # Filtrar solo los procesos que aún no han sido completados
            pending_processes = []
            for p in processes:
                if p not in completed:
                    pending_processes.append(p)

            # Obtener todos los tiempos de llegada de los procesos pendientes
            arrival_times = []
            for process in pending_processes:
                arrival_times.append(process.arrival_time)

            # Encontrar el tiempo de llegada más temprano
            current_time = min(arrival_times)
            continue
        
        # Select process with highest priority (lowest number)
        # Tie-break: arrival_time, then pid
        selected = min(available, key=lambda p: (p.priority, p.arrival_time, p.pid))
        
        # Registro de inicio y ejecución del proceso completo (sin interrupciones)
        selected.start_time = current_time
        current_time += selected.burst_time

        # Calculo de CT, TTA y WT
        selected.completion_time = current_time
        selected.turnaround_time = selected.completion_time - selected.arrival_time
        selected.waiting_time = selected.turnaround_time - selected.burst_time
        
        # Agregar el proceso a la lista de completados y condición stop while
        completed.append(selected)
        completed_count += 1
    
    return completed