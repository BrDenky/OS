# Shortest Job First (Preemptive/SRTF) scheduling algorithm.
from typing import List
from copy import deepcopy
from .models import Process


def sjf_preemptive(processes: List[Process]) -> List[Process]:
    processes = deepcopy(processes)
    n = len(processes)
    current_time = 0
    completed_count = 0

    # SRTF: simulate time unit by unit
    while completed_count < n:

        # Step A: find available processes BEFORE executing
        available = [p for p in processes if p.arrival_time <= current_time and p.remaining_time > 0]

        # CPU idle, move time forward
        if not available:
            current_time += 1
            continue

        # Select process with shortest remaining_time
        selected = min(available, key=lambda p: (p.remaining_time, p.arrival_time, p.pid))

        # Set start_time only the first time process is executed
        if selected.start_time == -1:
            selected.start_time = current_time

        # Execute for exactly 1 time unit
        selected.remaining_time -= 1
        current_time += 1

        # Step C: AFTER executing 1 time unit, check if finished
        if selected.remaining_time == 0:
            selected.completion_time = current_time
            selected.turnaround_time = selected.completion_time - selected.arrival_time
            selected.waiting_time = selected.turnaround_time - selected.burst_time
            completed_count += 1

    return processes
