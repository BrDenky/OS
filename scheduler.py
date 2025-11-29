# CPU Scheduling
import sys
import csv
from typing import List, Dict
from algorithms import (
    Process,
    fcfs_scheduler,
    sjf_non_preemptive,
    sjf_preemptive,
    priority_scheduler,
    round_robin_scheduler
)

# Function to read processes from CSV file
def read_processes_from_csv(filename: str) -> List[Process]:
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


# Function to calculate average turnaround time and waiting time
def calculate_averages(processes: List[Process]) -> Dict[str, float]:
    n = len(processes)
    avg_turnaround = sum(p.turnaround_time for p in processes) / n
    avg_waiting = sum(p.waiting_time for p in processes) / n
    
    return {
        'avg_turnaround_time': avg_turnaround,
        'avg_waiting_time': avg_waiting
    }


# Function to print scheduling results in a formatted table
def print_results(processes: List[Process], algorithm: str, has_priority: bool = False):
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



# Function to save scheduling results to a CSV file
# def save_to_csv(processes: List[Process], filename: str, has_priority: bool = False):
#     # Sort by PID for output
#     sorted_processes = sorted(processes, key=lambda p: p.pid)
    
#     with open(filename, 'w', newline='') as file:
#         if has_priority:
#             fieldnames = ['pid', 'arrival_time', 'burst_time', 'priority', 
#                          'completion_time', 'turnaround_time', 'waiting_time']
#         else:
#             fieldnames = ['pid', 'arrival_time', 'burst_time', 
#                          'completion_time', 'turnaround_time', 'waiting_time']
        
#         writer = csv.DictWriter(file, fieldnames=fieldnames)
#         writer.writeheader()
        
#         for p in sorted_processes:
#             row = {
#                 'pid': p.pid,
#                 'arrival_time': p.arrival_time,
#                 'burst_time': p.burst_time,
#                 'completion_time': p.completion_time,
#                 'turnaround_time': p.turnaround_time,
#                 'waiting_time': p.waiting_time
#             }
#             if has_priority:
#                 row['priority'] = p.priority
            
#             writer.writerow(row)
    
#     print(f"Results saved to: {filename}")




# Main Function to parse arguments and run the scheduler
def main():
    # if len(sys.argv) < 3:
    #     print("Usage: python scheduler.py input_file.csv [FCFS|SJF|SJF_P|PS|RR] [q=time_quantum]")
    #     print("\nAlgorithms:")
    #     print("  FCFS   - First Come First Serve")
    #     print("  SJF    - Shortest Job First (Non-Preemptive)")
    #     print("  SJF_P  - Shortest Job First (Preemptive/SRTF)")
    #     print("  PS     - Priority Scheduling")
    #     print("  RR     - Round Robin (requires q=quantum parameter)")
    #     print("\nExample: python scheduler.py input.csv RR q=2")
    #     sys.exit(1)
    
    input_file = sys.argv[1]
    algorithm = sys.argv[2].upper()
    
    # Read processes from csv
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
    #save_to_csv(result_processes, output_file, has_priority)


if __name__ == "__main__":
    main()
