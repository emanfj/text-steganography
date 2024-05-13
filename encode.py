import os
import mimetypes
import random
import json

def generate_dynamic_key():
    """
    Generates a dynamic encryption key using OS-provided randomness.
    """
    dynamic_key = os.urandom(16).hex()  # Generates a 128-bit (16-byte) dynamic key
    # print("Dynamic Key:", dynamic_key)
    return dynamic_key

def polyalphabetic_substitution(text, dynamic_key):
    """
    Performs polyalphabetic substitution on the given text using the dynamic key.
    """
    substituted_text = ""
    key_length = len(dynamic_key)
    for i, char in enumerate(text):
        key_byte = dynamic_key[i % key_length]  # Repeats the key if necessary
        substituted_char = chr(ord(char) ^ int(key_byte, 16))  # XOR substitution with dynamic key byte
        substituted_text += substituted_char
    return substituted_text

def non_linear_transposition(text, dynamic_key):
    """
    Performs non-linear transposition on the given text using the dynamic key.
    """
    transposed_text = ""
    key_length = len(dynamic_key)
    for i, char in enumerate(text):
        key_byte = dynamic_key[i % key_length]  # Repeats the key if necessary
        transposed_char_index = (i - int(key_byte, 16)) % len(text)  # Reverse transposition using key byte
        transposed_text += text[transposed_char_index]
    return transposed_text

def mixing(text, seed):
    """
    Performs mixing by shuffling characters in the text based on a seed.
    """
    random.seed(seed)  # Set the random seed for reproducibility
    mixed_text = list(text)
    random.shuffle(mixed_text)
    return ''.join(mixed_text)

def encrypt_text(secret_txt, dynamic_key):
    """
    Encrypts the secret text using polyalphabetic substitution, non-linear transposition, and deterministic mixing.
    """
    substituted_text = polyalphabetic_substitution(secret_txt, dynamic_key)
    transposed_text = non_linear_transposition(substituted_text, dynamic_key)
    encrypted_text = mixing(transposed_text, dynamic_key)
    return encrypted_text


def encode(secret_path, cover_path, steg_path):
    """
    Encodes the secret text into the cover text using text steganography.
    """
    # Validate inputs
    if not all(map(os.path.exists, [secret_path, cover_path])):
        raise FileNotFoundError("Secret or cover file does not exist.")
    
    # Ensure input files are text files
    if not all(map(lambda x: mimetypes.guess_type(x)[0] == 'text/plain', [secret_path, cover_path])):
        raise ValueError("Input files must be text files.")

    # Read the secret text from file
    with open(secret_path, 'r', encoding='utf-8') as secret_file:
        secret_txt = secret_file.read()

    if not secret_txt:
        raise ValueError("Secret text is empty.")

    # Read the cover text from file
    with open(cover_path, 'r', encoding='utf-8') as cover_file:
        cover_txt = cover_file.read()

    if not cover_txt:
        raise ValueError("Cover text is empty.")

    # Generate dynamic key
    dynamic_key = generate_dynamic_key()

    # Encrypt the secret message
    encrypted_text = encrypt_text(secret_txt, dynamic_key)

    # Save dynamic key to a separate file
    key_file_path = steg_path.replace('.txt', '_key.json')
    with open(key_file_path, 'w') as key_file:
        json.dump({'dynamic_key': dynamic_key}, key_file)

    # Embed encrypted text into cover text using zero-width characters
    stego_txt = ""
    joiner_count = 0
    non_joiner_count = 0
    for i, char in enumerate(cover_txt):
        stego_txt += char
        if i % 2 == 0:
            if joiner_count < len(encrypted_text) and encrypted_text[joiner_count] == '1':
                stego_txt += '\u200d'  # Zero width joiner
            else:
                stego_txt += '\u200c'  # Zero width non-joiner
            joiner_count += 1
        else:
            if non_joiner_count < len(encrypted_text) and encrypted_text[non_joiner_count] == '1':
                stego_txt += '\u200c'  # Zero width non-joiner
            else:
                stego_txt += '\u200d'  # Zero width joiner
            non_joiner_count += 1

    # Write the stego text to file
    with open(steg_path, 'w', encoding='utf-8') as steg_file:
        steg_file.write(stego_txt)

    print("Steganography successful. Stego text saved to:", steg_path)
    print("Dynamic key saved to:", key_file_path)

# File paths
secret_file_path = "secret_text_urdu.txt"
cover_file_path = "cover_text_2.txt"
steg_file_path = "steg_text.txt"

# Encoding
encode(secret_file_path, cover_file_path, steg_file_path)
