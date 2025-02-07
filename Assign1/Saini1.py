'''
Student name: Prashikshit Saini
 Course: COSC 4553 - Information Security
 Assignment: #1 - Simple Arithmetic Cipher
 File name: Saini1.py
 Program Purpose: Encrypts and decrypts a text file using a simple arithmetic cipher and a nonnegative integer key
 Program Limitations: For the key to work in the range of 1-120, there is a need to explicitly set the encoding to 'utf-8'
 Development Computer: Lenovo Legion 5 Pro
 Operating System: Windows 11 x64 23H2
 Integrated Development Environment (IDE): JetBrains PyCharm
 Compiler: Python 3.9
 Build Directions: None required
 Program's Operational Status: Fully Functional
'''





import sys

def encrypt_file(input_file, key):
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            content = file.read()

        encrypted_content = ''.join(chr((ord(char) + key)) for char in content)

        with open('encryptedKey.txt', 'w', encoding='utf-8') as encrypted_file:
            encrypted_file.write(encrypted_content)

        print("File successfully encrypted.")
    except FileNotFoundError:
        print(f"Error:'{input_file}' file not exists.")
    except Exception as e:
        print(f"An error occurred: {e}")

def decrypt_file(input_file, key):

    try:
        with open(input_file, 'r', encoding='utf-8') as encrypted_file:
            encrypted_content = encrypted_file.read()

        decrypted_content = ''.join(chr((ord(char) - key)) for char in encrypted_content)

        with open('decryptedKey.txt', 'w', encoding='utf-8') as decrypted_file:
            decrypted_file.write(decrypted_content)

        print("File successfully decrypted.")
    except FileNotFoundError:
        print(f"Error:'{input_file}' file not exists.")
    except Exception as e:
        print(f"An error occurred: {e}")


# Testing the function indivisually
# encrypt_file("plainText.txt", 5)
# decrypt_file("encryptedKey.txt", 5)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage:")
        print(f"  {sys.argv[0]} -e fileName.txt key  # To encrypt a file")
        print(f"  {sys.argv[0]} -d fileName.txt key  # To decrypt a file")
        sys.exit(1)

    mode = sys.argv[1]
    input_file = sys.argv[2]
    key = int(sys.argv[3])
    if not (0 <= key <= 120):
        raise ValueError("Key must be a nonnegative integer between 0 and 120.")


    try:

        if mode == '-e':
            encrypt_file(input_file, key)
        elif mode == '-d':
            decrypt_file(input_file, key)
        else:
            print("Invalid option. Use -e to encrypt or -d to decrypt.")
    except ValueError:
        print("Error: Key must be an integer.")
