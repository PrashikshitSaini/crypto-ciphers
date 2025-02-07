'''
Student name: Prashikshit Saini
 Course: COSC 4553 - Information Security
 Assignment: #2 - Double Transposition Cipher
 File name: Saini2.py
 Program Purpose: Encrypts and decrypts a text file using the double transposition cipher
 Program Limitations: At this moment in this codebase the program is limited to only first 24 characters of the text file. 
                      For the rest of the text in the plaintext file, the program will kind of ignore when encrypting.
 Development Computer: Lenovo Legion 5 Pro
 Operating System: Windows 11 x64 23H2
 Integrated Development Environment (IDE): JetBrains PyCharm
 Compiler: Python 3.9
 Build Directions: None required
 Program's Operational Status: Fully Functional for the first 24 characters given in the plaintext file

'''

import sys

ROWS = 6
COLS = 4
ROW_TRANSPOSE_ORDER = [3, 5, 0, 2, 1, 4]
COL_TRANSPOSE_ORDER = [3, 2, 0, 1]

def print_usage():
    print(f"Usage: python {sys.argv[0]} <-e|-d> <input_file> <output_file>")
    sys.exit(1)

def transpose_rows(table):
    return [table[i] for i in ROW_TRANSPOSE_ORDER]

def transpose_cols(table):
    transposed_table = []
    for row in table:
        transposed_table.append([row[i] for i in COL_TRANSPOSE_ORDER])
    return transposed_table

def fill_table(data, rows, cols):
    table = []
    for i in range(0, len(data), cols):
        row = list(data[i:i + cols])
        while len(row) < cols:
            row.append(' ')  
        table.append(row)
    while len(table) < rows:
        table.append([' '] * cols)  
    return table

def table_to_string(table):
    return ''.join(''.join(row) for row in table)

def encrypt(data):
    table = fill_table(data, ROWS, COLS)
    table = transpose_rows(table)
    table = transpose_cols(table)
    return table_to_string(table)

def decrypt(data):
    # I am trying here to reverse the column and row order first by placing "i" at the index of list[i]
    table = fill_table(data, ROWS, COLS)
    reverse_col_order = [COL_TRANSPOSE_ORDER.index(i) for i in range(COLS)]
    table = [[row[i] for i in reverse_col_order] for row in table]
    reverse_row_order = [ROW_TRANSPOSE_ORDER.index(i) for i in range(ROWS)]
    table = [table[i] for i in reverse_row_order]
    return table_to_string(table)

def main():
    if len(sys.argv) != 4 or sys.argv[1] not in ("-e", "-d"):
        print_usage()

    mode = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]

    try:
        with open(input_file, 'r') as infile:
            input_data = infile.read()
    except FileNotFoundError:
        print(f"Error:'{input_file}'  file not found.")
        sys.exit(1)

    if mode == "-e":
        output_data = encrypt(input_data)
        with open(output_file, 'w') as outfile:
            outfile.write(output_data)
        print("Encryption is done\n")
    elif mode == "-d":
        output_data = decrypt(input_data)
        with open(output_file, 'w') as outfile:
            outfile.write(output_data)
        print("Decryption is done\n")

if __name__ == "__main__":
    main()
