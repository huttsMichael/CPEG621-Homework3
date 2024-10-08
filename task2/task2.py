def parse_tac(instruction: str, latencies):
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
    return (result_var,  '=', [])

def calculate_cycles_from_code(instructions_raw: list[str], latencies):
    instructions = []
    for instr in instructions_raw:
        
        if "BB" in instr or "}" in instr or "else" in instr:
            # basic blocks, gotos, and brackets can be ignore. else handled identical to if.
            continue
        elif "if" in instr:
            result_var = instr.split('(')[1].split(')')[0].strip() # ugly but saves me writing regex
            result = (result_var, "?", [result_var])
        else:
            result = parse_tac(instr, latencies)

        # print(instr, result)
        instructions.append(result)
        

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

def main():
    import argparse
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

if __name__ == '__main__':
    main()
