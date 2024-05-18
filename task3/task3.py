import argparse

def implement_cse(code_segment: list[str], output_path=None):
    history = []
    explored = []
    processed_code = []
    tmp_counter = 1

    for position, line in enumerate(code_segment):
        op = line.split('=')[1]
        print(line)
        if op in history and op not in explored:
            first_apperance = True
            processed_code.append(line)
            for p, l in enumerate(processed_code):
                if op in l:
                    print(f"op in line: {op}")
                    if first_apperance:
                        appearance_index = processed_code.index(l)
                        first_apperance = False
                    processed_code[p] = processed_code[p].split('=')[0] + f" = tmp{tmp_counter}"
                    explored.append(op)
            processed_code.insert(appearance_index, f"tmp{tmp_counter} = {op}")
            tmp_counter += 1
                        
        else:
            history.append(op)
            processed_code.append(line)
        
        print(f"history: {history}")
        print(f"explored: {explored}")
        print(f"processed code: {processed_code}")

    if output_path:
        with open(output_path, 'w') as out_fp:
            for line in processed_code:
                out_fp.write(line + '\n')
    else:
        print(code_segment)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Implement common subexpression elimination in TAC input file.")
    parser.add_argument('input_file', type=str, help='Path to the input file containing TAC instructions.')
    parser.add_argument('--output', type=str, help='Path to the output file to save the result.')
    args = parser.parse_args()

    with open(args.input_file, 'r') as file:
        code_segment = [line.strip() for line in file.readlines() if line.strip()]
        print(f"input: {code_segment}")
        implement_cse(code_segment)