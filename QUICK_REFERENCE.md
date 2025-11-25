# CPU Scheduler - Quick Reference

## Command Syntax
```bash
python scheduler.py <input.csv> <ALGORITHM> [q=quantum]
```

## Algorithms

| Code   | Name                          | Preemptive | Needs Priority | Needs Quantum |
|--------|-------------------------------|------------|----------------|---------------|
| FCFS   | First Come First Serve        | No         | No             | No            |
| SJF    | Shortest Job First            | No         | No             | No            |
| SJF_P  | Shortest Job First (Preempt)  | Yes        | No             | No            |
| PS     | Priority Scheduling           | No         | Yes            | No            |
| RR     | Round Robin                   | Yes        | No             | Yes           |

## Quick Examples
```bash
# FCFS
python scheduler.py input.csv FCFS

# SJF (Non-Preemptive)
python scheduler.py input.csv SJF

# SJF (Preemptive)
python scheduler.py input.csv SJF_P

# Priority Scheduling
python scheduler.py input_priority.csv PS

# Round Robin (quantum=2)
python scheduler.py input.csv RR q=2
```

## CSV Format

### Basic (FCFS, SJF, SJF_P, RR)
```csv
pid,arrival_time,burst_time
1,0,8
2,1,4
```

### With Priority (PS)
```csv
pid,arrival_time,burst_time,priority
1,0,8,2
2,1,4,0
```
**Note:** 0 = highest priority

## Output Files
- `output_fcfs.csv` - FCFS results
- `output_sjf.csv` - SJF results
- `output_sjf_preemptive.csv` - SJF_P results
- `output_priority.csv` - PS results
- `output_rr.csv` - RR results

## Metrics Formulas
```
Completion Time = Time when process finishes
Turnaround Time = Completion Time - Arrival Time
Waiting Time = Turnaround Time - Burst Time
```

## Tie-Breaking Rules
1. **Priority Scheduling**: priority → arrival_time → pid
2. **SJF/SJF_P**: burst_time (or remaining_time) → arrival_time → pid
3. **FCFS**: arrival_time → pid

## Common Quantum Values (RR)
- **q=1**: Very responsive, high overhead
- **q=2-4**: Balanced for most cases
- **q=10+**: Approaches FCFS behavior

## Troubleshooting
| Error | Solution |
|-------|----------|
| File not found | Check file path |
| Missing column | Verify CSV headers |
| Invalid quantum | Use positive integer: q=2 |
| No quantum for RR | Add q=value parameter |

## Test Your Implementation
```bash
# Run all tests
python test_scheduler.py

# Manual verification
python scheduler.py sample_input.csv FCFS
# Check output_fcfs.csv matches expected values
```
