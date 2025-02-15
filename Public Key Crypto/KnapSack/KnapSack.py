import sys

def knapsack_encrypt(plaintext, public_key):
    """
    Encrypt the plaintext using the public key.
    Each character in the plaintext is converted to its binary representation.
    Each bit of the binary representation is multiplied by the corresponding element in the public key.
    The sum of these products is the encrypted value for that character.
    """
    ciphertext = []
    for char in plaintext:
        # Convert character to 8-bit binary
        binary_char = format(ord(char), '08b')
        # Encrypt character by summing products of bits and public key elements
        encrypted_char = sum(int(bit) * pk for bit, pk in zip(binary_char, public_key))
        ciphertext.append(encrypted_char)
    return ciphertext

def mod_inverse(a, m):
    """
    Compute the modular inverse of a modulo m using the Extended Euclidean Algorithm.
    """
    # Alternatively, you can use pow(a, -1, m) in Python 3.8+
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError("No modular inverse exists for a = {} modulo m = {}".format(a, m))

def knapsack_decrypt(ciphertext, private_key, n_inv, m):
    """
    Decrypt the ciphertext using the private (superincreasing) key, n_inv, and m.
    n_inv is the modular inverse of n modulo m.
    Each encrypted integer is multiplied by n_inv modulo m to recover c_prime,
    which is then used with a greedy algorithm to recover the original binary string.
    """
    decrypted_text = ""
    for encrypted_char in ciphertext:
        # Use the modular inverse to reverse the modular multiplication during encryption
        c_prime = (encrypted_char * n_inv) % m  
        binary_char = ""
        for pk in reversed(private_key):
            if pk <= c_prime:
                binary_char = '1' + binary_char
                c_prime -= pk
            else:
                binary_char = '0' + binary_char
        decrypted_text += chr(int(binary_char, 2))
    return decrypted_text

def read_file(file_path):
    """
    Read the content of the file specified by file_path.
    """
    with open(file_path, 'r') as file:
        return file.read()

def write_file(file_path, content):
    """
    Write the content to the file specified by file_path.
    """
    with open(file_path, 'w') as file:
        file.write(content)

def main():
    if len(sys.argv) < 6:
        print(f"Usage: python {sys.argv[0]} <-e/-d> <input_file> <output_file> <key_file> <n> <m>")
        return

    # Parse command line arguments
    operation = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    key_file = sys.argv[4]
    n = int(sys.argv[5])
    m = int(sys.argv[6])
    
    # Compute n_inv, the modular inverse of n modulo m
    n_inv = mod_inverse(n, m)

    # Read input text and key from files
    input_text = read_file(input_file)
    key = read_file(key_file).split()
    key = [int(k) for k in key]

    if operation == "-e":
        public_key = key
        # Encrypt the input text using the public key
        encrypted_text = knapsack_encrypt(input_text, public_key)
        # Write the encrypted text to the output file
        write_file(output_file, ' '.join(map(str, encrypted_text)))
    elif operation == "-d":
        private_key = key
        # Convert input text to list of integers (ciphertext)
        ciphertext = list(map(int, input_text.split()))
        # Decrypt the ciphertext using the private key, n_inv, and m
        decrypted_text = knapsack_decrypt(ciphertext, private_key, n_inv, m)
        # Write the decrypted text to the output file
        write_file(output_file, decrypted_text)
    else:
        print("Invalid operation. Use 'encrypt' or 'decrypt'.")

if __name__ == "__main__":
    main()
