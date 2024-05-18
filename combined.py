import argparse
from task1 import task1
from task2 import task2
from task3 import task3



def segment_building_blocks(code_segment: list[str]):
    split_code = {}
    current_block = ""
    for line in code_segment:
        if "BB" in line and "goto" not in line:
            current_block = line
            split_code[current_block] = []
        else:
            split_code[current_block].append(line)
    return split_code


    
def run_all(code_segment):
    t1 = task1.generate_basic_blocks(code_segment)
    print(f"task 1 output: {t1}")

    t1_split = segment_building_blocks(t1)
    print(f"split by block: {t1_split}")

    latencies = {
        '+': 1,
        '-': 1,
        '?': 2,
        '=': 3,
        '*': 4,
        '/': 4,
        '**': 8
    }
    # t2_complete_latency = task2.calculate_cycles_from_code(code_segment, latencies)
    # print(f"total latency: {t2_complete_latency} cycles")

    t1_block_latency = {}
    for block in t1_split:
        t1_block_latency[block] = task2.calculate_cycles_from_code(t1_split[block], latencies)

    print(f"pre-CSE per-block latency: {t1_block_latency}")

    t3_split = {}
    for block in t1_split:
        t3_split[block] = task3.implement_cse(t1_split[block])

    print(f"post-CSE blocks: {t3_split}")

    t3_block_latency = {}
    for block in t3_split:
        t3_block_latency[block] = task2.calculate_cycles_from_code(t3_split[block], latencies)

    print(f"post-CSE per-block latency: {t1_block_latency}")

    t1_total_latency = 0
    for block in t1_block_latency:
        t1_total_latency += t1_block_latency[block]

    print(f"pre-CSE total latency: {t1_total_latency}")

    t3_total_latency = 0
    for block in t3_block_latency:
        t3_total_latency += t3_block_latency[block]

    
    print(f"post-CSE total latency: {t3_total_latency}")



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Implement common subexpression elimination in TAC input file.")
    parser.add_argument('input_file', type=str, help='Path to the input file containing TAC instructions.')
    parser.add_argument('--output', type=str, help='Path to the output file to save the result.')
    args = parser.parse_args()

    with open(args.input_file, 'r') as file:
        code_segment = [line.strip() for line in file.readlines() if line.strip()]
        print(f"initial input: {code_segment}")
        run_all(code_segment)
        