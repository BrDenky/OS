#!/usr/bin/env python3
"""
Visual comparison of all scheduling algorithms.
Shows side-by-side comparison of metrics for the same input.
"""

import subprocess
import csv
import os

def run_and_get_metrics(input_file, algorithm, quantum=None):
    """Run algorithm and extract average metrics."""
    cmd = ['python', 'scheduler.py', input_file, algorithm]
    if quantum:
        cmd.append(f'q={quantum}')
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Determine output file
    output_files = {
        'FCFS': 'output_fcfs.csv',
        'SJF': 'output_sjf.csv',
        'SJF_P': 'output_sjf_preemptive.csv',
        'PS': 'output_priority.csv',
        'RR': 'output_rr.csv'
    }
    
    output_file = output_files.get(algorithm)
    if not output_file or not os.path.exists(output_file):
        return None
    
    # Read metrics
    with open(output_file, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    if not rows:
        return None
    
    avg_turnaround = sum(int(row['turnaround_time']) for row in rows) / len(rows)
    avg_waiting = sum(int(row['waiting_time']) for row in rows) / len(rows)
    
    return {
        'algorithm': algorithm + (f' (q={quantum})' if quantum else ''),
        'avg_turnaround': avg_turnaround,
        'avg_waiting': avg_waiting,
        'processes': len(rows)
    }

def main():
    print("\n" + "="*100)
    print("CPU SCHEDULING ALGORITHMS - PERFORMANCE COMPARISON")
    print("="*100)
    
    # Test with sample_input.csv
    print(f"\n{'Dataset: sample_input.csv (5 processes)'}")
    print("-"*100)
    
    algorithms = [
        ('sample_input.csv', 'FCFS', None),
        ('sample_input.csv', 'SJF', None),
        ('sample_input.csv', 'SJF_P', None),
        ('sample_input.csv', 'RR', 2),
        ('sample_input.csv', 'RR', 4),
    ]
    
    results = []
    for input_file, algorithm, quantum in algorithms:
        metrics = run_and_get_metrics(input_file, algorithm, quantum)
        if metrics:
            results.append(metrics)
    
    # Display results
    print(f"\n{'Algorithm':<30} {'Avg Turnaround (ms)':<25} {'Avg Waiting (ms)':<25}")
    print("-"*100)
    for r in results:
        print(f"{r['algorithm']:<30} {r['avg_turnaround']:<25.2f} {r['avg_waiting']:<25.2f}")
    
    # Find best algorithms
    best_turnaround = min(results, key=lambda x: x['avg_turnaround'])
    best_waiting = min(results, key=lambda x: x['avg_waiting'])
    
    print("\n" + "="*100)
    print("ANALYSIS")
    print("="*100)
    print(f"✓ Best Average Turnaround Time: {best_turnaround['algorithm']} ({best_turnaround['avg_turnaround']:.2f} ms)")
    print(f"✓ Best Average Waiting Time: {best_waiting['algorithm']} ({best_waiting['avg_waiting']:.2f} ms)")
    
    # Test with example_input.csv (more processes)
    print(f"\n{'='*100}")
    print(f"{'Dataset: example_input.csv (7 processes)'}")
    print("-"*100)
    
    algorithms2 = [
        ('example_input.csv', 'FCFS', None),
        ('example_input.csv', 'SJF', None),
        ('example_input.csv', 'SJF_P', None),
        ('example_input.csv', 'PS', None),
        ('example_input.csv', 'RR', 3),
        ('example_input.csv', 'RR', 5),
    ]
    
    results2 = []
    for input_file, algorithm, quantum in algorithms2:
        metrics = run_and_get_metrics(input_file, algorithm, quantum)
        if metrics:
            results2.append(metrics)
    
    print(f"\n{'Algorithm':<30} {'Avg Turnaround (ms)':<25} {'Avg Waiting (ms)':<25}")
    print("-"*100)
    for r in results2:
        print(f"{r['algorithm']:<30} {r['avg_turnaround']:<25.2f} {r['avg_waiting']:<25.2f}")
    
    # Find best algorithms
    best_turnaround2 = min(results2, key=lambda x: x['avg_turnaround'])
    best_waiting2 = min(results2, key=lambda x: x['avg_waiting'])
    
    print("\n" + "="*100)
    print("ANALYSIS")
    print("="*100)
    print(f"✓ Best Average Turnaround Time: {best_turnaround2['algorithm']} ({best_turnaround2['avg_turnaround']:.2f} ms)")
    print(f"✓ Best Average Waiting Time: {best_waiting2['algorithm']} ({best_waiting2['avg_waiting']:.2f} ms)")
    
    print("\n" + "="*100)
    print("KEY INSIGHTS")
    print("="*100)
    print("• SJF/SJF_P typically minimize average waiting time")
    print("• FCFS is simple but can have high waiting times (convoy effect)")
    print("• Round Robin provides fairness but may have higher average times")
    print("• Priority Scheduling is effective when process priorities are well-defined")
    print("• Preemptive algorithms (SJF_P, RR) are better for interactive systems")
    print("="*100 + "\n")

if __name__ == "__main__":
    main()
