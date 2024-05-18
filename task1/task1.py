import logging

def show_code(code):
    for line in code:
        print(line)

def generate_basic_blocks(code_segment: list[str], output_path=None, verbose=False):
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO, format='%(message)s')

    bb_counter = 1
    inside_if = False
    inside_else = False
    end_condition = False
    first_line = True

    processed_code = []
    contents_if = []
    contents_else = []

    for line in code_segment:
        line = line.strip()
        if inside_if:
            if "}" in line:
                inside_if = False
                logging.debug(f"ended if: {line}")
                processed_code.append(line)
            else:
                logging.debug(f"inside if contents: {line}")
                contents_if.append(line)

        elif inside_else:
            if "}" in line:
                inside_else = False
                end_condition = True
                logging.debug(f"ended else: {line}")
                processed_code.append(line)
            else:
                logging.debug(f"inside else contents: {line}")
                contents_else.append(line)

        elif end_condition:
            logging.debug(f"end of conditions: {line}")
            end_condition = False
            bb_counter += 1
            contents_if.append(f"goto BB{bb_counter}")
            contents_else.append(f"goto BB{bb_counter}")
            for l in contents_if:
                processed_code.append(l)
            for l in contents_else:
                processed_code.append(l)
            processed_code.append(f"BB{bb_counter}:")
            processed_code.append(line)
            contents_if = []
            contents_else = []

        elif first_line:
            logging.debug(f"first line: {line}")
            first_line = False
            processed_code.append(f"BB{bb_counter}:")
            processed_code.append(line)



        elif "if" in line:
            inside_if = True
            logging.debug(f"hit if: {line}")
            bb_counter += 1
            processed_code.append(line)
            processed_code.append(f"goto BB{bb_counter}")
            contents_if.append(f"BB{bb_counter}:")

        elif "else" in line:
            inside_else = True
            logging.debug(f"hit else: {line}")
            bb_counter += 1
            processed_code.append(line)
            processed_code.append(f"goto BB{bb_counter}")
            contents_else.append(f"BB{bb_counter}:")
            
        else:
            logging.debug(f"nothing triggered: {line}")
            processed_code.append(line)

        logging.debug("process code so far")
        if verbose:
            show_code(processed_code)
            logging.debug("")

    if output_path:
        with open(output_path, 'w') as out_fp:
            for line in processed_code:
                out_fp.write(line + '\n')
    else:
        logging.debug("final output:")
        if verbose:
            show_code(processed_code)

    return processed_code

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate basic blocks from source code.")
    parser.add_argument('input_file', type=str, help='Path to the input source code file.')
    parser.add_argument('--output', type=str, help='Path to the output file to save the result.')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose debug output.')
    args = parser.parse_args()

    with open(args.input_file, 'r') as file:
        code_segment = [line.strip() for line in file.readlines() if line.strip()]
        print(f"input: {code_segment}")
        generate_basic_blocks(code_segment, args.output, args.verbose)

if __name__ == '__main__':
    main()
