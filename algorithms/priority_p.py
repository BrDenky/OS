# Priority Scheduling (Non-Preemptive) algorithm.
# Lower priority number = Higher priority.
from typing import List
from copy import deepcopy
from .models import Process
def priority_preemptive(processes: List[Process]) -> List[Process]:
    processes = deepcopy(processes)
    n = len(processes)
    current_time = 0
    completed_count = 0

    while completed_count < n:

        # Processes that have arrived and are not finished
        available = [
            p for p in processes
            if p.arrival_time <= current_time and p.remaining_time > 0
        ]

        # If no process available, CPU idle → advance time
        if not available:
            current_time += 1
            continue

        # Select process with:
        # 1. Highest priority (smallest priority number)
        # 2. If tie → earlier arrival
        # 3. If tie → smaller PID
        selected = min(
            available,
            key=lambda p: (p.priority, p.arrival_time, p.pid)
        )

        # First time the process is ever executed
        if selected.start_time == -1:
            selected.start_time = current_time

        # Execute 1 time unit
        selected.remaining_time -= 1
        current_time += 1

        # If finished
        if selected.remaining_time == 0:
            selected.completion_time = current_time
            selected.turnaround_time = selected.completion_time - selected.arrival_time
            selected.waiting_time = selected.turnaround_time - selected.burst_time
            completed_count += 1

    return processes
