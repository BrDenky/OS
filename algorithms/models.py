# Shared models and data structures for CPU scheduling algorithms.
from typing import List, Dict, Tuple
from dataclasses import dataclass, field
from copy import deepcopy

# Represents a process with scheduling attributes.
@dataclass
class Process:
    pid: int
    arrival_time: int
    burst_time: int
    priority: int = 0
    remaining_time: int = field(init=False)
    completion_time: int = 0
    turnaround_time: int = 0
    waiting_time: int = 0
    start_time: int = -1
    
    # To preemptive algorithms
    def __post_init__(self):
        self.remaining_time = self.burst_time
