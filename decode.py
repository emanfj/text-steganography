import os
import mimetypes
import json

def reverse_polyalphabetic_substitution(text, dynamic_key):
    """
    Reverses the polyalphabetic substitution on the given text using the dynamic key.
    """
    original_text = ""
    key_length = len(dynamic_key)
    for i, encrypted_char in enumerate(text):
        key_byte = dynamic_key[i % key_length]  # Repeats the key if necessary
        original_char = chr(ord(encrypted_char) ^ int(key_byte, 16))  # XOR reverse substitution with dynamic key byte
        original_text += original_char
    print("Text after reverse polyalphabetic substitution:", original_text)
    return original_text

def reverse_non_linear_transposition(text):
    """
    Reverses the non-linear transposition on the given text.
    """
    reversed_text = ""
    mid = len(text) // 2
    for i in range(mid):
        reversed_text += text[i]
        if len(text) % 2 == 0:
            reversed_text += text[mid + i]
        else:
            reversed_text += text[mid + i + 1]
    if len(text) % 2 != 0:
        reversed_text += text[mid]
    print("Text after reverse transposition", reversed_text)
    return reversed_text

def decrypt_text(encrypted_text, dynamic_key):
    """
    Decrypts the encrypted text to retrieve the original secret text.
    """
    # Reverse the non-linear transposition
    reversed_transposition = reverse_non_linear_transposition(encrypted_text)
    # Reverse the polyalphabetic substitution
    original_text = reverse_polyalphabetic_substitution(reversed_transposition, dynamic_key)
    return original_text

def binary_to_text(binary):
    """
    Converts binary string to text.
    """
    n = int(binary, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()

def decode(steg_path, key_path):
    """
    Decodes the secret text from the steganograph.
    """
    # Validate inputs
    if not all(map(os.path.exists, [steg_path, key_path])):
        raise FileNotFoundError("Secret or cover file does not exist.")
    
    # Ensure input files are text files
    if not mimetypes.guess_type(steg_path)[0] == 'text/plain':
        raise ValueError("Steg file must be text files.")
    if not mimetypes.guess_type(key_path)[0] == 'application/json':
        raise ValueError("Key files must be json files.")
    
    # Read the secret text from file
    with open(steg_path, 'r', encoding='utf-8') as steg_file:
        steg_text = steg_file.read()

    if not steg_text:
        raise ValueError("Steg text is empty.")

    # Read the key from json file
    with open(key_path, 'r') as key_file:
        key_data = json.load(key_file)

    if not key_data:
        raise ValueError("Key json is empty.")
    
    if not key_data["dynamic_key"]:
        raise ValueError("Key is not provided in JSON.")
    
    dynamic_key = key_data['dynamic_key']
    if not dynamic_key:
        raise ValueError("Key provided is empty.")
    
    # Extract the encrypted text from the steg_text
    encrypted_binary = ""

    # Characters for encoding binary data in the steg text
    ZERO_WIDTH_JOINER = '\u200d'
    ZERO_WIDTH_NON_JOINER = '\u200c'

    # Extract binary data from steg text
    for i, char in enumerate(steg_text):
        current_bit_length = len(encrypted_binary)
        
        add_one =  char == ZERO_WIDTH_JOINER and current_bit_length % 2 == 0 \
                or char == ZERO_WIDTH_NON_JOINER and current_bit_length % 2 == 1
        
        add_zero = char == ZERO_WIDTH_JOINER and current_bit_length % 2 == 1 \
                or char == ZERO_WIDTH_NON_JOINER and current_bit_length % 2 == 0
        
        if add_one:
            encrypted_binary += "1"
        if add_zero:
            encrypted_binary += "0"

    # Convert binary data to text
    encrypted_text = binary_to_text(encrypted_binary)

    # Decrypt the encrypted text
    plaintext = decrypt_text(encrypted_text, dynamic_key)

    return plaintext

# Paths for steg text and key
steg_path = "steg_text.txt"
key_path = "key.json"

# Decode and print the secret text
decode(steg_path, key_path)
