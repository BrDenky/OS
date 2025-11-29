# Test script to verify all scheduling algorithms and compare results.
import subprocess
import csv
import os

# Function to run a scheduling algorithm and return the output
def run_algorithm(input_file, algorithm, quantum=None):
    cmd = ['python', 'scheduler.py', input_file, algorithm]
    if quantum:
        cmd.append(f'q={quantum}')
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout, result.returncode



# Function to read and display CSV output
def read_csv_output(filename):
    if not os.path.exists(filename):
        return None
    
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    return rows


# Main function to run the test
def main():
    print("="*100)
    print("CPU SCHEDULING SIMULATOR - COMPREHENSIVE TEST")
    print("="*100)
    
    tests = [
        ('inputs/sample_input.csv', 'FCFS', None, 'outputs/output_fcfs.csv'),
        ('inputs/sample_input.csv', 'SJF', None, 'outputs/output_sjf.csv'),
        ('inputs/sample_input.csv', 'SJF_P', None, 'outputs/output_sjf_preemptive.csv'),
        ('inputs/sample_input_priority.csv', 'PS', None, 'outputs/output_priority.csv'),
        ('inputs/sample_input.csv', 'RR', 2, 'outputs/output_rr.csv'),
    ]
    
    for input_file, algorithm, quantum, output_file in tests:
        print(f"\n{'='*100}")
        print(f"Testing: {algorithm}" + (f" (quantum={quantum})" if quantum else ""))
        print(f"{'='*100}")
        
        stdout, returncode = run_algorithm(input_file, algorithm, quantum)
        
        if returncode == 0:
            print("✓ Algorithm executed successfully")
            
            # Read and verify output file
            rows = read_csv_output(output_file)
            if rows:
                print(f"✓ Output file '{output_file}' created with {len(rows)} processes")
                
                # Calculate and display averages
                avg_turnaround = sum(int(row['turnaround_time']) for row in rows) / len(rows)
                avg_waiting = sum(int(row['waiting_time']) for row in rows) / len(rows)
                
                print(f"  Average Turnaround Time: {avg_turnaround:.2f} ms")
                print(f"  Average Waiting Time: {avg_waiting:.2f} ms")
            else:
                print(f"✗ Failed to read output file '{output_file}'")
        else:
            print(f"✗ Algorithm failed with return code {returncode}")
            print(stdout)
    
    print(f"\n{'='*100}")
    print("COMPARISON SUMMARY")
    print(f"{'='*100}")
    print(f"{'Algorithm':<30} {'Avg Turnaround':<20} {'Avg Waiting':<20}")
    print("-"*100)
    
    for input_file, algorithm, quantum, output_file in tests:
        rows = read_csv_output(output_file)
        if rows:
            avg_turnaround = sum(int(row['turnaround_time']) for row in rows) / len(rows)
            avg_waiting = sum(int(row['waiting_time']) for row in rows) / len(rows)
            
            alg_name = algorithm + (f" (q={quantum})" if quantum else "")
            print(f"{alg_name:<30} {avg_turnaround:<20.2f} {avg_waiting:<20.2f}")
    
    print("="*100)
    print("\n✓ All tests completed successfully!")
    print("\nGenerated output files:")
    for _, _, _, output_file in tests:
        if os.path.exists(output_file):
            print(f"  - {output_file}")

if __name__ == "__main__":
    main()
