#function to convert string characters to binary
def text2binary(text):
    binary=''
    for char in text:
        binary+=format(ord(char),'08b')#format each character in binary representation
    return binary

#function to encode secret text in cover text
def encode(secret_txt,cover_txt):
    secret_binary=text2binary(secret_txt)
    binary_id=0
    stego_txt=''

    for char in cover_txt:
        if binary_id<len(secret_binary):
            if secret_binary[binary_id]=='1':
                stego_txt+=char+'\u200d'
            elif secret_binary[binary_id]=='0':
                stego_txt+=char+'\u200c'
            binary_id+=1
        else:
            stego_text += char

        #if cover text is shorter than secret text append the secret text to it
        if binary_id<len(secret_binary):
            #zwj is used as joiner
            stego_txt+='\u200d'.join(secret_binary[binary_id:])

        return stego_txt
    