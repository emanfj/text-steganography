#function to convert string characters to binary
def text2binary(text):
    binary=""
    for char in text:
        binary+=format(ord(char),'08b')#format each character in binary representation
    return binary

#function to encode secret text in cover text
def encode(secret,cover,steg):
    #read the secret text from file
    with open(secret, 'r', encoding='utf-8') as secret_file:
        secret_txt = secret_file.read()
    
    #read the cover text from file
    with open(cover, 'r', encoding='utf-8') as cover_file:
        cover_txt = cover_file.read()

    secret_binary=text2binary(secret_txt)
    binary_id=0
    stego_txt=""

    for char in cover_txt:
        if binary_id<len(secret_binary):
            if secret_binary[binary_id]=='1':
                stego_txt+=char+'\u200d' #zero width joiner
            elif secret_binary[binary_id]=='0':
                stego_txt+=char+'\u200c' #zero width non joiner
            binary_id+=1
        else:
            stego_txt += char

        #if cover text is shorter than secret text append the secret text to it
    if binary_id<len(secret_binary):
            #zwj is used as joiner
            stego_txt+='\u200d'.join(secret_binary[binary_id:])

    # return stego_txt

    #write the steg text to file
    with open(steg, 'w', encoding='utf-8') as steg_file:
        steg_file.write(stego_txt)

    
#file paths
secret_file="secret_text.txt"
cover_file="cover_text.txt"
steg_file="steg_text.txt"

encode(secret_file,cover_file,steg_file)
# secret_message = "attack at 3pm"
# secret_message="3 بجے حملہ"
# cover_text = "The average temperature in Islamabad today is 31 with the highest temperature hitting at 3pm with 38 Celsius while the lowest hitting 21 Celsius at 4am. "
# stego_txt = encode(secret_message, cover_text)
# print("Steganograph Text:", stego_txt)