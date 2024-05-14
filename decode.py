import os
import mimetypes
import json

def reverse_non_linear_transposition(text, dynamic_key):
    """
    Reverses the non-linear transposition on the given text using the dynamic key.
    """
    transposed_text = ""
    key_length = len(dynamic_key)
    for i, char in enumerate(text):
        key_byte = dynamic_key[i % key_length]  # Repeats the key if necessary
        transposed_char_index = (i + int(key_byte, 16)) % len(text)  # Reverse transposition using key byte
        transposed_text += text[transposed_char_index]
    return transposed_text

def reverse_polyalphabetic_substitution(text, dynamic_key):
    """
    Reverses the polyalphabetic substitution on the given text using the dynamic key.
    """
    substituted_text = ""
    key_length = len(dynamic_key)
    for i, char in enumerate(text):
        key_byte = dynamic_key[i % key_length]  # Repeats the key if necessary
        substituted_char = chr(ord(char) ^ int(key_byte, 16))  # XOR substitution with dynamic key byte
        substituted_text += substituted_char
    return substituted_text

def decrypt_text(encrypted_text, dynamic_key):
    """
    Decrypts the encrypted text using polyalphabetic substitution and non-linear transposition.
    """
    transposed_text = reverse_non_linear_transposition(encrypted_text, dynamic_key)
    decrypted_text = reverse_polyalphabetic_substitution(transposed_text, dynamic_key)
    return decrypted_text

def decode(steg_path, key, output_path):
    """
    Decodes the secret text from the stego text using the provided key.
    """
    # Validate inputs
    if not os.path.exists(steg_path):
        raise FileNotFoundError("Stego file does not exist.")

    # Ensure the stego file is a text file
    if mimetypes.guess_type(steg_path)[0] != 'text/plain':
        raise ValueError("Stego file must be a text file.")

    # Read the stego text from file
    with open(steg_path, 'r', encoding='utf-8') as steg_file:
        stego_txt = steg_file.read()

    if not stego_txt:
        raise ValueError("Stego text is empty.")

    # Extract the encrypted text from the stego text
    encrypted_text = ""
    for char in stego_txt:
        if char == '\u200d':  # Zero width joiner
            encrypted_text += '1'
        elif char == '\u200c':  # Zero width non-joiner
            encrypted_text += '0'

    # Decrypt the encrypted text
    decrypted_text = decrypt_text(encrypted_text, key)

    # Write the decrypted text to file
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(decrypted_text)

# File paths
steg_file_path = "steg_text.txt"
output_file_path = "decoded_text.txt"

# Key
key = "de525315a83994b5fa8f4c9ced8145f8"

# Decoding
decode(steg_file_path, key, output_file_path)