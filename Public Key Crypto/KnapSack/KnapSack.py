import sys

def knapsack_encrypt(plaintext, public_key):
    """
    Encrypt the plaintext (UTF-8) using the public key.
    The plaintext is first encoded as UTF-8 bytes.
    Each byte is converted to its 8-bit binary representation.
    Each bit is multiplied by the corresponding element in the public key.
    The sum of these products is the encrypted value for that byte.
    """
    ciphertext = []
    plaintext_bytes = plaintext.encode('utf-8')
    for byte in plaintext_bytes:
        binary_byte = format(byte, '08b')
        encrypted_byte = sum(int(bit) * pk for bit, pk in zip(binary_byte, public_key))
        ciphertext.append(encrypted_byte)
    return ciphertext

def mod_inverse(a, m):
    """
    Compute the modular inverse of a modulo m using the Extended Euclidean Algorithm.
    """
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError("No modular inverse exists for a = {} modulo m = {}".format(a, m))

def knapsack_decrypt(ciphertext, private_key, n_inv, m):
    """
    Decrypt the ciphertext using the private (superincreasing) key, n_inv, and m.
    Each encrypted integer is multiplied by n_inv modulo m to recover c_prime.
    The greedy algorithm reconstructs the original 8-bit binary string for each byte.
    The resulting byte sequence is decoded from UTF-8.
    """
    decrypted_bytes = []
    for encrypted_val in ciphertext:
        c_prime = (encrypted_val * n_inv) % m
        binary_byte = ""
        for pk in reversed(private_key):
            if pk <= c_prime:
                binary_byte = '1' + binary_byte
                c_prime -= pk
            else:
                binary_byte = '0' + binary_byte
        decrypted_bytes.append(int(binary_byte, 2))
    # Convert the list of byte integers to a bytes object and decode as UTF-8
    return bytes(decrypted_bytes).decode('utf-8')

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
        # Compute public key: each public key element = (n * private key element) mod m
        public_key = [(n * w) % m for w in key]
        # Encrypt using the public key
        encrypted_text = knapsack_encrypt(input_text, public_key)
        write_file(output_file, ' '.join(map(str, encrypted_text)))
    elif operation == "-d":
        private_key = key
        # Convert input text to list of integers (ciphertext)
        ciphertext = list(map(int, input_text.split()))
        # Decrypt using the private key, n_inv, and m
        decrypted_text = knapsack_decrypt(ciphertext, private_key, n_inv, m)
        write_file(output_file, decrypted_text)
    else:
        print("Invalid operation. Use '-e' or '-d'.")

if __name__ == "__main__":
    main()
