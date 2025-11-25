#!/usr/bin/env python3
"""
CPU Scheduling Simulator
Implements FCFS, SJF (preemptive & non-preemptive), Priority Scheduling, and Round Robin algorithms.
"""

import sys
import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass, field
from copy import deepcopy


@dataclass
class Process:
    """Represents a process with scheduling attributes."""
    pid: int
    arrival_time: int
    burst_time: int
    priority: int = 0
    remaining_time: int = field(init=False)
    completion_time: int = 0
    turnaround_time: int = 0
    waiting_time: int = 0
    start_time: int = -1
    
    def __post_init__(self):
        self.remaining_time = self.burst_time


def read_processes_from_csv(filename: str) -> List[Process]:
    """Read processes from CSV file."""
    processes = []
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                pid = int(row['pid'])
                arrival_time = int(row['arrival_time'])
                burst_time = int(row['burst_time'])
                priority = int(row.get('priority', 0))
                
                processes.append(Process(
                    pid=pid,
                    arrival_time=arrival_time,
                    burst_time=burst_time,
                    priority=priority
                ))
        return processes
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except KeyError as e:
        print(f"Error: Missing required column {e} in CSV file.")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: Invalid data in CSV file - {e}")
        sys.exit(1)


def fcfs_scheduler(processes: List[Process]) -> List[Process]:
    """First Come First Serve scheduling algorithm."""
    processes = deepcopy(processes)
    processes.sort(key=lambda p: (p.arrival_time, p.pid))
    
    current_time = 0
    for process in processes:
        if current_time < process.arrival_time:
            current_time = process.arrival_time
        
        process.start_time = current_time
        current_time += process.burst_time
        process.completion_time = current_time
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time
    
    return processes


def sjf_non_preemptive(processes: List[Process]) -> List[Process]:
    """Shortest Job First (Non-Preemptive) scheduling algorithm."""
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
        
        selected.start_time = current_time
        current_time += selected.burst_time
        selected.completion_time = current_time
        selected.turnaround_time = selected.completion_time - selected.arrival_time
        selected.waiting_time = selected.turnaround_time - selected.burst_time
        
        completed.append(selected)
        completed_count += 1
    
    return completed


def sjf_preemptive(processes: List[Process]) -> List[Process]:
    """Shortest Job First (Preemptive/SRTF) scheduling algorithm."""
    processes = deepcopy(processes)
    n = len(processes)
    current_time = 0
    completed_count = 0
    last_process = None
    
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


def priority_scheduler(processes: List[Process]) -> List[Process]:
    """Priority Scheduling (Non-Preemptive) - Lower number = Higher priority."""
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
        
        selected.start_time = current_time
        current_time += selected.burst_time
        selected.completion_time = current_time
        selected.turnaround_time = selected.completion_time - selected.arrival_time
        selected.waiting_time = selected.turnaround_time - selected.burst_time
        
        completed.append(selected)
        completed_count += 1
    
    return completed


def round_robin_scheduler(processes: List[Process], quantum: int) -> List[Process]:
    """Round Robin scheduling algorithm."""
    processes = deepcopy(processes)
    n = len(processes)
    current_time = 0
    queue = []
    completed_count = 0
    arrived_indices = set()
    
    # Sort by arrival time for initial processing
    sorted_processes = sorted(enumerate(processes), key=lambda x: (x[1].arrival_time, x[1].pid))
    
    while completed_count < n:
        # Add newly arrived processes to queue
        for idx, process in sorted_processes:
            if process.arrival_time <= current_time and idx not in arrived_indices:
                queue.append(process)
                arrived_indices.add(idx)
        
        if not queue:
            # No process in queue, jump to next arrival
            next_arrival = min((p.arrival_time for i, p in sorted_processes if i not in arrived_indices), default=current_time)
            current_time = next_arrival
            continue
        
        # Get next process from queue
        current_process = queue.pop(0)
        
        if current_process.start_time == -1:
            current_process.start_time = current_time
        
        # Execute for quantum or remaining time, whichever is smaller
        execution_time = min(quantum, current_process.remaining_time)
        current_process.remaining_time -= execution_time
        current_time += execution_time
        
        # Add newly arrived processes during execution
        for idx, process in sorted_processes:
            if process.arrival_time <= current_time and idx not in arrived_indices:
                queue.append(process)
                arrived_indices.add(idx)
        
        if current_process.remaining_time > 0:
            # Process not finished, add back to queue
            queue.append(current_process)
        else:
            # Process completed
            current_process.completion_time = current_time
            current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
            current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
            completed_count += 1
    
    return processes


def calculate_averages(processes: List[Process]) -> Dict[str, float]:
    """Calculate average turnaround time and waiting time."""
    n = len(processes)
    avg_turnaround = sum(p.turnaround_time for p in processes) / n
    avg_waiting = sum(p.waiting_time for p in processes) / n
    
    return {
        'avg_turnaround_time': avg_turnaround,
        'avg_waiting_time': avg_waiting
    }


def print_results(processes: List[Process], algorithm: str, has_priority: bool = False):
    """Print scheduling results in a formatted table."""
    print(f"\n{'='*100}")
    print(f"CPU Scheduling Algorithm: {algorithm}")
    print(f"{'='*100}")
    
    # Header
    if has_priority:
        header = f"{'PID':<8}{'Arrival':<12}{'Burst':<12}{'Priority':<12}{'Completion':<15}{'Turnaround':<15}{'Waiting':<12}"
    else:
        header = f"{'PID':<8}{'Arrival':<12}{'Burst':<12}{'Completion':<15}{'Turnaround':<15}{'Waiting':<12}"
    
    print(header)
    print('-' * 100)
    
    # Sort by PID for display
    sorted_processes = sorted(processes, key=lambda p: p.pid)
    
    # Data rows
    for p in sorted_processes:
        if has_priority:
            row = f"{p.pid:<8}{p.arrival_time:<12}{p.burst_time:<12}{p.priority:<12}{p.completion_time:<15}{p.turnaround_time:<15}{p.waiting_time:<12}"
        else:
            row = f"{p.pid:<8}{p.arrival_time:<12}{p.burst_time:<12}{p.completion_time:<15}{p.turnaround_time:<15}{p.waiting_time:<12}"
        print(row)
    
    # Averages
    averages = calculate_averages(processes)
    print('-' * 100)
    print(f"Average Turnaround Time: {averages['avg_turnaround_time']:.2f} ms")
    print(f"Average Waiting Time: {averages['avg_waiting_time']:.2f} ms")
    print(f"{'='*100}\n")


def save_to_csv(processes: List[Process], filename: str, has_priority: bool = False):
    """Save scheduling results to CSV file."""
    # Sort by PID for output
    sorted_processes = sorted(processes, key=lambda p: p.pid)
    
    with open(filename, 'w', newline='') as file:
        if has_priority:
            fieldnames = ['pid', 'arrival_time', 'burst_time', 'priority', 
                         'completion_time', 'turnaround_time', 'waiting_time']
        else:
            fieldnames = ['pid', 'arrival_time', 'burst_time', 
                         'completion_time', 'turnaround_time', 'waiting_time']
        
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        
        for p in sorted_processes:
            row = {
                'pid': p.pid,
                'arrival_time': p.arrival_time,
                'burst_time': p.burst_time,
                'completion_time': p.completion_time,
                'turnaround_time': p.turnaround_time,
                'waiting_time': p.waiting_time
            }
            if has_priority:
                row['priority'] = p.priority
            
            writer.writerow(row)
    
    print(f"Results saved to: {filename}")


def main():
    """Main function to parse arguments and run the scheduler."""
    if len(sys.argv) < 3:
        print("Usage: python scheduler.py input_file.csv [FCFS|SJF|SJF_P|PS|RR] [q=time_quantum]")
        print("\nAlgorithms:")
        print("  FCFS   - First Come First Serve")
        print("  SJF    - Shortest Job First (Non-Preemptive)")
        print("  SJF_P  - Shortest Job First (Preemptive/SRTF)")
        print("  PS     - Priority Scheduling")
        print("  RR     - Round Robin (requires q=quantum parameter)")
        print("\nExample: python scheduler.py input.csv RR q=2")
        sys.exit(1)
    
    input_file = sys.argv[1]
    algorithm = sys.argv[2].upper()
    
    # Read processes
    processes = read_processes_from_csv(input_file)
    
    if not processes:
        print("Error: No processes found in input file.")
        sys.exit(1)
    
    # Run the selected algorithm
    result_processes = None
    algorithm_name = ""
    has_priority = False
    
    if algorithm == "FCFS":
        result_processes = fcfs_scheduler(processes)
        algorithm_name = "First Come First Serve (FCFS)"
        output_file = "output_fcfs.csv"
    
    elif algorithm == "SJF":
        result_processes = sjf_non_preemptive(processes)
        algorithm_name = "Shortest Job First (Non-Preemptive)"
        output_file = "output_sjf.csv"
    
    elif algorithm == "SJF_P":
        result_processes = sjf_preemptive(processes)
        algorithm_name = "Shortest Job First (Preemptive/SRTF)"
        output_file = "output_sjf_preemptive.csv"
    
    elif algorithm == "PS":
        result_processes = priority_scheduler(processes)
        algorithm_name = "Priority Scheduling"
        has_priority = True
        output_file = "output_priority.csv"
    
    elif algorithm == "RR":
        # Parse quantum
        if len(sys.argv) < 4 or not sys.argv[3].startswith('q='):
            print("Error: Round Robin requires time quantum parameter (q=value)")
            print("Example: python scheduler.py input.csv RR q=2")
            sys.exit(1)
        
        try:
            quantum = int(sys.argv[3].split('=')[1])
            if quantum <= 0:
                raise ValueError("Quantum must be positive")
        except (ValueError, IndexError):
            print("Error: Invalid quantum value. Must be a positive integer.")
            sys.exit(1)
        
        result_processes = round_robin_scheduler(processes, quantum)
        algorithm_name = f"Round Robin (Quantum = {quantum} ms)"
        output_file = "output_rr.csv"
    
    else:
        print(f"Error: Unknown algorithm '{algorithm}'")
        print("Valid algorithms: FCFS, SJF, SJF_P, PS, RR")
        sys.exit(1)
    
    # Display and save results
    print_results(result_processes, algorithm_name, has_priority)
    save_to_csv(result_processes, output_file, has_priority)


if __name__ == "__main__":
    main()
