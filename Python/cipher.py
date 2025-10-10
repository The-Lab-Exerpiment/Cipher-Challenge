import train_data as td

filename = "Resources/ciphertext.txt"

def remove_filler(text):
    temp = ""
    
    for letter in text.upper():
        if letter >= 'A' and letter <= 'Z':
            temp += letter
            
    return temp

ciphertext = remove_filler(open(filename, 'r').read())

def get_cipher():
    return ciphertext