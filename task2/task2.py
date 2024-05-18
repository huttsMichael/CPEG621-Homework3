import argparse

def parse_tac(instruction):
    # split the = and any other ops to handle seperately
    result_var, operation_part = instruction.split('=')
    result_var = result_var.strip()
    
    # not fastest structure but it'll work
    for op in latencies.keys():
        if op in operation_part:
            operands = operation_part.split(op)
            dependencies = [operand.strip() for operand in operands if operand.strip().isalpha()]
            return (result_var, op, dependencies)
    
    # fallback return if no operations found
    return (result_var, '?', [])

def calculate_cycles_from_code(instructions_raw, latencies):
    instructions = [parse_tac(instr) for instr in instructions_raw]

    ready_time = {}
    max_cycle = 0

    for result_var, operation, dependencies in instructions:
        start_cycle = 1  # default to 1 if there are no dependencies
        if dependencies:
            # max of ready times of dependencies + 1 to wait until the dependencies are ready
            start_cycle = max(ready_time.get(dep, 0) for dep in dependencies) + 1
        
        # find finish time of operation
        finish_cycle = start_cycle + latencies[operation] - 1
        ready_time[result_var] = finish_cycle
        max_cycle = max(max_cycle, finish_cycle)

    return max_cycle

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Calculate cycles needed for three-address code instructions.")
    parser.add_argument('input_file', type=str, help='Path to the input file containing TAC instructions.')
    args = parser.parse_args()

    latencies = {
        '+': 1,
        '-': 1,
        '?': 2,
        '=': 3,
        '*': 4,
        '/': 4,
        '**': 8
    }

    with open(args.input_file, 'r') as file:
        code_segment = [line.strip() for line in file.readlines() if line.strip()]

    total_cycles = calculate_cycles_from_code(code_segment, latencies)
    print(f"Total cycles needed: {total_cycles}")
