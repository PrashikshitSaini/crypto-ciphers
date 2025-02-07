'''
Student name: Prashikshit Saini
 Course: COSC 4553 - Information Security
 Assignment: #3 - RC4 Stream Cipher
 File name: Saini3.py
 Program Purpose: Encrypts and decrypts a text file using the RC4 stream cipher
 Program Limitations: N/A
 Development Computer: Lenovo Legion 5 Pro
 Operating System: Windows 11 x64 23H2
 Integrated Development Environment (IDE): JetBrains PyCharm
 Compiler: Python 3.9
 Build Directions: None required
 Program's Operational Status: Fully Functional

'''

import sys

# Initialize the lookup table (S) and key table (T) as global variables
S = [i for i in range(256)]
T = [0] * 256


def key_scheduling_algo(key):

    global S, T
    key = key[:256]  # It will only take the first 256 characters
    key_length = len(key)


    for i in range(256):
        T[i] = ord(key[i % key_length]) # ASCII value of each  character of the alphanumeric key is set in this T list.

    j = 0
    for i in range(256):
        j = (j + S[i] + T[i]) % 256
        S[i], S[j] = S[j], S[i] # Swapping the value to create randomness


def pseduo_random_gen_algo(data):

    global S
    i = 0
    j = 0
    result = bytearray()
    # Process each byte in the input data
    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        t = (S[i] + S[j]) % 256
        k = S[t]
        result.append(byte ^ k)  # XOR operator(^) to encrypt/decrypt
    return result


def rc4(key, data):

    global S, T
    # Initialize the lookup table and key table
    S = [i for i in range(256)] 
    T = [0] * 256
    key_scheduling_algo(key)
    return pseduo_random_gen_algo(data)


def main():
    if len(sys.argv) != 4:
        sys.stderr.write(f"Usage: python {sys.argv[0]} <alphanumeric-key> <input file> <output file>\n")
        sys.exit(1)

    key = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]

    try:
        with open(input_file, "rb") as fin: # reading in binary mode
            data = fin.read()
    except IOError as e:
        sys.stderr.write(f"Error opening input file: {e}\n")
        sys.exit(1)


    result = rc4(key, data)


    try:
        with open(output_file, "wb") as fout:
            fout.write(result)
    except IOError as e:
        sys.stderr.write(f"Error writing output file: {e}\n")
        sys.exit(1)


    sys.stderr.write("RC4 stream cipher operation is done\n")


if __name__ == "__main__":
    main()
