def parse_tac(instruction):
    # Split the instruction on '=' to separate the result variable and the operation part
    result_var, operation_part = instruction.split('=')
    result_var = result_var.strip()
    
    # Find the operation and its operands
    for op in latencies.keys():
        if op in operation_part:
            operands = operation_part.split(op)
            dependencies = [operand.strip() for operand in operands if operand.strip().isalpha()]
            return (result_var, op, dependencies)
    
    # In case no operation is found, return no dependencies and an unknown operation (should not happen with valid input)
    return (result_var, '?', [])

def calculate_cycles_from_code(instructions_raw, latencies):
    # Parse instructions
    instructions = [parse_tac(instr) for instr in instructions_raw]

    # Dictionary to keep track of when each variable will be ready
    ready_time = {}
    max_cycle = 0

    for result_var, operation, dependencies in instructions:
        # Determine the earliest cycle this operation can be issued
        start_cycle = 1  # Start at cycle 1 if there are no dependencies
        if dependencies:
            # Max of ready times of dependencies + 1 because we need to wait until the dependencies are ready
            start_cycle = max(ready_time.get(dep, 0) for dep in dependencies) + 1
        
        # Compute the finish time for this operation
        finish_cycle = start_cycle + latencies[operation] - 1
        ready_time[result_var] = finish_cycle
        max_cycle = max(max_cycle, finish_cycle)

    return max_cycle

# Example code segment to process
code_segment = [
    "A = B*1",
    "C = D+E",
    "F = A+C"
]

# Latency table
latencies = {
    '+': 1,
    '-': 1,
    '?': 2,
    '=': 3,
    '*': 4,
    '/': 4,
    '**': 8
}

# Calculate and print the total number of cycles needed for the example
print(calculate_cycles_from_code(code_segment, latencies))
