import argparse

def show_code(code):
    for line in code:
        print(line)


def generate_basic_blocks(path):
    bb_counter = 1
    inside_if = False
    inside_else = False
    end_condition = False
    first_line = True

    processed_code = []
    contents_if = []
    contents_else = []

    with open(path) as fp:
        for line in fp:
            if "\n" in line:
                line = line.replace("\n", "")
            if inside_if:
                if "}" in line:
                    inside_if = False
                    print(f"ended if: {line}")
                    processed_code.append(line)
                else:
                    print(f"inside if contents: {line}")
                    contents_if.append(line)

            elif inside_else:
                if "}" in line:
                    inside_else = False
                    end_condition = True
                    print(f"ended else: {line}")
                    processed_code.append(line)
                else:
                    print(f"inside else contents: {line}")
                    contents_else.append(line)

            elif end_condition:
                print(f"end of conditions: {line}")
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
                print(f"first line: {line}")
                first_line = False

            elif "if" in line:
                inside_if = True
                print(f"hit if: {line}")
                bb_counter += 1
                processed_code.append(line)
                processed_code.append(f"goto BB{bb_counter}")
                contents_if.append(f"BB{bb_counter}:")

            elif "else" in line:
                inside_else = True
                print(f"hit else: {line}")
                bb_counter += 1
                processed_code.append(line)
                processed_code.append(f"goto BB{bb_counter}")
                contents_else.append(f"BB{bb_counter}:")
                
            else:
                print(f"nothing triggered: {line}")
                processed_code.append(line)

            print("process code so far")
            show_code(processed_code)
            print()

    print("final output:")
    print(processed_code)
                

file_path_0 = "../infile_0.txt"
file_path_1 = "../infile_1.txt"

generate_basic_blocks(file_path_0)
generate_basic_blocks(file_path_1)


