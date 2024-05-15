import os
import json

def generate_dynamic_key():
    """
    Generates a dynamic encryption key using OS-provided randomness.
    """
    dynamic_key = os.urandom(16).hex()  # Generates a 128-bit (16-byte) dynamic key
    print("Dynamic Key:", dynamic_key)
    return dynamic_key


def create_json_file(file_path):    
    # Generate dynamic key
    dynamic_key = generate_dynamic_key()
    
    # Save dynamic key to a separate file
    with open(file_path, 'w') as key_file:
        json.dump({'dynamic_key': dynamic_key}, key_file)


key_file_path = "key.json"
create_json_file(key_file_path)
