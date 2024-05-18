import argparse
from task1 import task1
from task2 import task2
from task3 import task3



def segment_building_blocks(code_segment: list[str]):
    split_code = {}
    current_block = ""
    for line in code_segment:
        if "BB" in line:
            current_block = line
            split_code[current_block] = []
        else:
            split_code[current_block].append(line)
    return split_code


    
def run_all(code_segment):
    t1 = task1.generate_basic_blocks(code_segment)
    print(f"task 1 output: {t1}")

    latencies = {
        '+': 1,
        '-': 1,
        '?': 2,
        '=': 3,
        '*': 4,
        '/': 4,
        '**': 8
    }
    t2 = task2.calculate_cycles_from_code(code_segment, latencies)
    print(f"task 2 output: {t2}")

    t1_split = segment_building_blocks(t1)
    print(f"split by block: {t1_split}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Implement common subexpression elimination in TAC input file.")
    parser.add_argument('input_file', type=str, help='Path to the input file containing TAC instructions.')
    parser.add_argument('--output', type=str, help='Path to the output file to save the result.')
    args = parser.parse_args()

    with open(args.input_file, 'r') as file:
        code_segment = [line.strip() for line in file.readlines() if line.strip()]
        print(f"initial input: {code_segment}")
        run_all(code_segment)
        