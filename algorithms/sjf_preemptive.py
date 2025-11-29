# Shortest Job First (Preemptive/SRTF) scheduling algorithm.
from typing import List
from copy import deepcopy
from .models import Process


def sjf_preemptive(processes: List[Process]) -> List[Process]:
    processes = deepcopy(processes)
    n = len(processes)
    current_time = 0
    completed_count = 0
    # last_process = None
    
    # Find the maximum time we need to simulate
    max_time = max(p.arrival_time + p.burst_time for p in processes) * 2
    
    while completed_count < n and current_time < max_time:
        # Find available processes
        available = [p for p in processes if p.arrival_time <= current_time and p.remaining_time > 0]
        
        if not available:
            current_time += 1
            continue
        
        # Select process with shortest remaining time (tie-break: arrival_time, then pid)
        selected = min(available, key=lambda p: (p.remaining_time, p.arrival_time, p.pid))
        
        if selected.start_time == -1:
            selected.start_time = current_time
        
        # Execute for 1 time unit
        selected.remaining_time -= 1
        current_time += 1
        
        if selected.remaining_time == 0:
            selected.completion_time = current_time
            selected.turnaround_time = selected.completion_time - selected.arrival_time
            selected.waiting_time = selected.turnaround_time - selected.burst_time
            completed_count += 1
    
    return processes