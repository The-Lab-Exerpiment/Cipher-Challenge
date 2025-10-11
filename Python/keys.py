def invert_alpha_key(key):
    reverse_key = ""
    
    if len(key) == 26:
        try:
            key = key.upper()
            
            for char in range(26):
                reverse_key += chr(ord('a') + key.find(chr(ord('A') + char)))
        except:
            return "Invalid key"
                
    return reverse_key

def mono_substitute(text, key):
    text = text.upper()
    key = key.lower()
    
    if len(key) != 26:
        return text
    
    ciphertext = ""
    
    for letter in text:
        index = ord(letter) - ord('A')
        
        if index >= 0 and index <= 26 and key[index] >= 'a' and key[index] <= 'z':
            ciphertext += key[index]
            
        else:
            ciphertext += letter
            
    return ciphertext

def mono_decrypt(text, key):
    return mono_substitute(text, invert_alpha_key(key))