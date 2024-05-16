import os
import mimetypes
import json

def get_dynamic_key(key_path):
    """
    Retrieves the dynamic key stored in a JSON file.

    Args:
        key_path (str): Path to the JSON file containing the key.

    Returns:
        str: The dynamic key.

    Raises:
        FileNotFoundError: If the key JSON file does not exist.
        ValueError: If the key file is not a JSON file, or if the JSON is empty or does not contain the dynamic key.
    """
    # Validate inputs and retrieve dynamic key
    if not os.path.exists(key_path):
        raise FileNotFoundError("Key json file does not exist.")
    
    if not mimetypes.guess_type(key_path)[0] == 'application/json':
        raise ValueError("Key files must be json files.")
    
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
    
    return dynamic_key

def polyalphabetic_substitution(text, dynamic_key):
    """
    Performs polyalphabetic substitution on the given text using the provided dynamic key.

    Args:
        text (str): The text to be encrypted.
        dynamic_key (str): The dynamic key for encryption.

    Returns:
        str: The substituted text after encryption.
    """
    # Perform polyalphabetic substitution
    substituted_text = ""
    key_length = len(dynamic_key)
    for i, char in enumerate(text):
        # Repeats the key if necessary
        key_byte = dynamic_key[i % key_length]  
        # XOR substitution with dynamic key byte
        substituted_char = chr(ord(char) ^ int(key_byte, 16))  
        substituted_text += substituted_char
    print("After polyalphabetic substitution:", substituted_text)
    return substituted_text


def transposition(text):
    """
    Performs transposition on the given text.

    Args:
        text (str): The text to be transposed.

    Returns:
        str: The transposed text.
    """
    # Perform non-linear transposition
    transposed_text = ""
    for i in range(0, len(text), 2):
        transposed_text += text[i]
    for i in range(1, len(text), 2):
        transposed_text += text[i]
        
    print("After transposition:", transposed_text)
    return transposed_text


def encrypt_text(secret_txt, dynamic_key):
    """
    Encrypts the secret text using polyalphabetic substitution and non-linear transposition.

    Args:
        secret_txt (str): The text to be encrypted.
        dynamic_key (str): The dynamic key for encryption.

    Returns:
        str: The encrypted text.
    """
    # Encrypt the secret text
    substituted_text = polyalphabetic_substitution(secret_txt, dynamic_key)
    encrypted_text = transposition(substituted_text)
    print("Encrypted text:", encrypted_text)
    return encrypted_text


def text2binary(text):
    """
    Converts text to binary representation.

    Args:
        text (str): The text to be converted.

    Returns:
        str: The binary representation of the text.
    """
    # Convert text to binary
    binary=''
    for char in text:
        binary += format(ord(char),'08b')#format each character in binary representation
    return binary
    

def encode(secret_path, cover_path, steg_path, key_path):
    """
    Encodes the secret text into the cover text using text steganography.

    Args:
        secret_path (str): Path to the secret text file.
        cover_path (str): Path to the cover text file.
        steg_path (str): Path to save the stego text file.
        key_path (str): Path to the JSON file containing the dynamic key.

    Raises:
        FileNotFoundError: If the secret or cover file does not exist.
        ValueError: If the input files are not text files or if the secret text is empty.
    """
    # Validate inputs and encode the secret text into cover text using steganography
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
    dynamic_key = get_dynamic_key(key_path)

    # Encrypt the secret message
    encrypted_text = encrypt_text(secret_txt, dynamic_key)

    # Embed encrypted text into cover text using zero-width characters
    stego_txt = ""
    encrypted_binary = text2binary(encrypted_text)
    print("Encrypted text converted to bin:", encrypted_binary)

    for i, bit in enumerate(encrypted_binary):
        if i < len(cover_txt):
            stego_txt += cover_txt[i]

        # Even positions map 1->zwj, 0->zwnj
        if i % 2 == 0:
            if bit == '1':
                stego_txt += '\u200d'  # Zero width joiner
            else:
                stego_txt += '\u200c'  # Zero width non-joiner

        # Odd positions map 1->zwnj, 0->zwj
        else:
            if bit == '1':
                stego_txt += '\u200c'  # Zero width non-joiner
            else:
                stego_txt += '\u200d'  # Zero width joiner

    # Add leftover cover text
    for i in range(len(encrypted_binary), len(cover_txt)):
        stego_txt += cover_txt[i]

    # Write the stego text to file
    with open(steg_path, 'w', encoding='utf-8') as steg_file:
        steg_file.write(stego_txt)
    print("Steganography successful. Stego text saved to:", steg_path)
    print("Dynamic key saved to:", key_file_path)

# File paths
secret_file_path = "secret_text.txt"
cover_file_path = "cover_text.txt"
steg_file_path = "steg_text.txt"
key_file_path = "key.json"

# Encoding
encode(secret_file_path, cover_file_path, steg_file_path, key_file_path)
