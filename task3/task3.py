import logging

def implement_cse(code_segment: list[str], output_path=None, verbose=False):
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO, format='%(message)s')
    history = []
    explored = []
    processed_code = []
    tmp_counter = 1
    end = False

    for position, line in enumerate(code_segment):
        # labels and goto's remain untouched
        if "BB" in line:
            processed_code.append(line)
            continue
        
        # detect condition and begin finishing as CSE implementation is over
        if "if" in line:
            end = True 

        # add any finishing lines without processing further
        if end:
            processed_code.append(line)
            continue

        op = line.split('=')[1]
        if op in history and op not in explored:
            first_apperance = True
            processed_code.append(line)
            for p, l in enumerate(processed_code):
                if op in l:
                    logging.debug(f"op in line: {op}")
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
        
        logging.debug(f"history: {history}")
        logging.debug(f"explored: {explored}")
        logging.debug(f"processed code: {processed_code}")

    if output_path:
        with open(output_path, 'w') as out_fp:
            for line in processed_code:
                out_fp.write(line + '\n')

    return processed_code

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Implement common subexpression elimination in TAC input file.")
    parser.add_argument('input_file', type=str, help='Path to the input file containing TAC instructions.')
    parser.add_argument('--output', type=str, help='Path to the output file to save the result.')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose debug output.')
    args = parser.parse_args()

    with open(args.input_file, 'r') as file:
        code_segment = [line.strip() for line in file.readlines() if line.strip()]
        print(f"input: {code_segment}")
        print(implement_cse(code_segment, verbose=args.verbose))


if __name__ == '__main__':
    main()