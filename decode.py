import os
import mimetypes
import json

def reverse_polyalphabetic_substitution(text, dynamic_key):
    """
    Reverses the polyalphabetic substitution on the given text using the dynamic key.
    """
    original_text = ""
    key_length = len(dynamic_key)
    for i, char in enumerate(text):
        key_byte = dynamic_key[i % key_length]  # Repeats the key if necessary
        original_char = chr(ord(char) ^ int(key_byte, 16))  # XOR reverse substitution with dynamic key byte
        original_text += original_char
    # print("Original text after reverse polyalphabetic substitution:", original_text)
    return original_text


def reverse_non_linear_transposition(text):
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

    return reversed_text


def decrypt_text(encrypted_text, dynamic_key):
    """
    Decrypts the encrypted text to retrieve the original secret text.
    """
    # Reverse the non-linear transposition
    reversed_transposition = reverse_non_linear_transposition(encrypted_text)
    print("reverse_non_linear_transposition", reversed_transposition)
    # Reverse the polyalphabetic substitution
    original_text = reverse_polyalphabetic_substitution(reversed_transposition, dynamic_key)
    print("reverse_polyalphabetic_substitution", original_text)
    print("Original secret text:", original_text)
    return original_text


def binary2text(binary):
    n = int(binary, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()


def decode(steg_path, key_path):
    """
    decodes the secret text from the stegnograph.
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
        steg_txt = steg_file.read()

    if not steg_txt:
        raise ValueError("Steg text is empty.")

    # Read the key from json file
    with open(key_path, 'r') as key_file:
        data = json.load(key_file)

    if not data:
        raise ValueError("Key json is empty.")
    
    if not data["dynamic_key"]:
        raise ValueError("Key is not provided in JSON.")
    
    dynamic_key = data['dynamic_key']
    if not dynamic_key:
        raise ValueError("Key provided is empty.")
    
    # Extract the encrypted text form the steg_text
    encrypted_binary = ""

    ZERO_WIDTH_JOINER = '\u200d'
    ZERO_WIDTH_NON_JOINER = '\u200c'

    for i, char in enumerate(steg_txt):
        cur_bit = len(encrypted_binary)
        
        add_one =  char == ZERO_WIDTH_JOINER and cur_bit % 2 == 0 \
                or char == ZERO_WIDTH_NON_JOINER and cur_bit % 2 == 1
        
        add_zero = char == ZERO_WIDTH_JOINER and cur_bit % 2 == 1 \
                or char == ZERO_WIDTH_NON_JOINER and cur_bit % 2 == 0
        
        if add_one:
            encrypted_binary += "1"
        if add_zero:
            encrypted_binary += "0"

    encrypted_txt = binary2text(encrypted_binary)

    plain_txt = decrypt_text(encrypted_txt, dynamic_key)

    return plain_txt

steg_path = "steg_text.txt"
key_path = "key.json"

print(decode(steg_path, key_path))
