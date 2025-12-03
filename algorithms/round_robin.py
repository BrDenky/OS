# Round Robin scheduling algorithm with time quantum.
from typing import List
from copy import deepcopy
from .models import Process


def round_robin_scheduler(processes: List[Process], quantum: int) -> List[Process]:
    processes = deepcopy(processes)
    n = len(processes)
    current_time = 0 # initial time CPU
    queue = [] # ready queue
    completed_count = 0
    arrived_indices = set() # indices of processes that have arrived
    
    # Sort by arrival time for initial processing
    # enumerate make a list of tuples (index, process)
    sorted_processes = sorted(enumerate(processes), key=lambda x: (x[1].arrival_time, x[1].pid))
    
    while completed_count < n:
        # View if there are arrived processes that are not in queue
        for idx, process in sorted_processes:
            if process.arrival_time <= current_time and idx not in arrived_indices:
                queue.append(process)
                arrived_indices.add(idx)
        
        # No process in queue, jump to next arrival time       
        if not queue:
            next_arrival = min((p.arrival_time for i, p in sorted_processes if i not in arrived_indices), default=current_time)
            current_time = next_arrival
            continue
        
        # Get next process from queue (FIFO)
        current_process = queue.pop(0)
        
        # This only hapens once, when process have never been executed
        if current_process.start_time == -1:
            current_process.start_time = current_time
        
        # Choose the minimun execution time between quantum or remaining time
        execution_time = min(quantum, current_process.remaining_time)
        current_process.remaining_time -= execution_time
        current_time += execution_time # Add this execution time to the CPU time
        

        # This second scan ensures that no process arriving in the middle of the quantum is lost.
        for idx, process in sorted_processes:
            if process.arrival_time <= current_time and idx not in arrived_indices:
                queue.append(process)
                arrived_indices.add(idx)
        
        # Check if process is not finished, add back to queue
        if current_process.remaining_time > 0:
            queue.append(current_process)
        else:
            # Process completed - Calculate CT, TTA and WT
            current_process.completion_time = current_time
            current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
            current_process.waiting_time = current_process.turnaround_time - current_process.burst_time

            completed_count += 1
    
    return processes