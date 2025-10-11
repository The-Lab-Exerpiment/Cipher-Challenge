import train_data as td
import stats as st
import directories as dr

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

def generate_affine_key(mult, shift):
    key = ""
    
    for char in range(26):
        key += chr(ord('A') + (char*mult + shift) % 26)
    
    return key

def affine_shift(text, mult, shift):
    return mono_substitute(text, generate_affine_key(mult, shift))

def caesar_shift(text, shift):
    return affine_shift(text, 1, shift)

def brute_force_caesar(text):
    og_fitness = -9999999999999
    og_shift = 0
    tetra_frequencies = td.get_tetra_frequencies(dr.tetras())
    
    for shift in range(26):
        fitness = st.tetra_fitness(affine_shift(text, 1, shift), tetra_frequencies)
        
        if fitness > og_fitness:
            og_fitness = fitness
            og_shift = shift
            
    return affine_shift(text, 1, og_shift)

def crib_caesar(text, crib):
    text = td.remove_text(text).lower()
    
    for i in range(len(text) - len(crib) + 1):
        for shift in range(26):
            if text[i:i+len(crib)] == caesar_shift(crib, 26 - shift):
                return caesar_shift(text, shift)
            
    return text.upper()

def chi_squared_caesar(text):
    og_variance = 999999999999999
    og_shift = 0
    tetras = st.normalize_dict(st.monolist(td.get_tetra_frequencies(dr.tetras())))
    
    for shift in range(26):
        variance = variation(st.normalize_dict(st.monolist(caesar_shift(td.get_mono_text(text), shift))), tetras)
        
        if variance < og_variance:
            og_variance = variance
            og_shift = shift
            
    return caesar_shift(text, og_shift)