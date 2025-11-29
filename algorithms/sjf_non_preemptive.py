# Shortest Job First (Non-Preemptive) scheduling algorithm.
from typing import List
from copy import deepcopy
from .models import Process


def sjf_non_preemptive(processes: List[Process]) -> List[Process]:
    processes = deepcopy(processes)
    n = len(processes)
    completed = []
    current_time = 0
    completed_count = 0
    
    while completed_count < n:
        # Find available processes
        available = [p for p in processes if p.arrival_time <= current_time and p not in completed]
        
        if not available:
            # No process available, jump to next arrival
            current_time = min(p.arrival_time for p in processes if p not in completed)
            continue
        
        # Select process with shortest burst time (tie-break: arrival_time, then pid)
        selected = min(available, key=lambda p: (p.burst_time, p.arrival_time, p.pid))
        
        # Registro de inicio y ejecución del proceso completo (sin interrupciones)
        selected.start_time = current_time
        current_time += selected.burst_time

        # Calculo de CT, TTA y WT
        selected.completion_time = current_time
        selected.turnaround_time = selected.completion_time - selected.arrival_time
        selected.waiting_time = selected.turnaround_time - selected.burst_time
        
        completed.append(selected)
        completed_count += 1
    
    return completed