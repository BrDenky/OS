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
        available = [p for p in processes if p.arrival_time <= current_time and p not in completed]

        if not available:
            # No process available, jump to next arrival
            current_time = min(p.arrival_time for p in processes if p not in completed)
            continue
        
        # Select process with highest priority (lowest number)
        # Tie-break: arrival_time, then pid
        selected = min(available, key=lambda p: (p.priority, p.arrival_time, p.pid))
        
        # Log of the start and execution of the entire process (without interruptions)
        selected.start_time = current_time
        current_time += selected.burst_time

        # Calculate CT, TTA and WT
        selected.completion_time = current_time
        selected.turnaround_time = selected.completion_time - selected.arrival_time
        selected.waiting_time = selected.turnaround_time - selected.burst_time
        
        # Add the process to the completed list
        completed.append(selected)
        completed_count += 1
    
    return completed