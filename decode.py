import os

# Function to decode the stego text and extract the hidden message
def decode(steg):
    # Read the stego text from file
    try:
        with open(steg, 'r', encoding='utf-8') as steg_file:
            stego_txt = steg_file.read()
    except FileNotFoundError:
        print("Error: Stego file not found.")
        return
    except Exception as e:
        print("Error:", e)
        return


    if not stego_txt:
        print("Error: Stego text is empty.")
        return

    # Initialize variables
    secret_binary = ""
    joiner_count = 0
    non_joiner_count = 0

    # Iterate through each character in the stego text
    for i, char in enumerate(stego_txt):
        if i % 2 == 1:
            # Check for zero width joiners
            if char == '\u200d':
                secret_binary += '1'
                joiner_count += 1
            # Check for zero width non-joiners
            elif char == '\u200c':
                secret_binary += '0'
                non_joiner_count += 1

    # Decode the binary representation to obtain the secret message
    secret_message = binary2text(secret_binary)

    return secret_message

# Function to convert binary string to text
def binary2text(binary):
    text = ""
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        text += chr(int(byte, 2))
    return text

# File paths
steg_file = "text-steganography/steg_text.txt"

# Decode the stego text and extract the hidden message
# Decode the stego text and extract the hidden message
decoded_message = decode(steg_file)
print("Decoded Message:", decoded_message)


