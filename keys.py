import train_data as td
import stats as st
import directories as dr

import random

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
    if st.mod_inverse(mult, 26) == 0:
        return text
    
    return mono_substitute(text, generate_affine_key(mult, shift))

def generate_affine_decrypt(mult, shift):
    key = ""
    
    for char in range(26):
        key += chr(ord('A') + ((char - shift) * st.mod_inverse(mult, 26)) % 26)
        
    return key

def affine_decrypt(text, mult, shift):
    if st.mod_inverse(mult, 26) == 0:
        return text
    
    return mono_substitute(text, generate_affine_decrypt(mult, shift))

def brute_force_affine(text):
    og_fitness = -9999999999999
    og_mult = 0
    og_shift = 0
    
    for mult in range(26):
        if st.mod_inverse(mult, 26) != 0:
            for shift in range(26):
                fitness = st.tetra_fitness(affine_shift(text, mult, shift), td.get_tetra_frequencies(dr.tetras()))
                
                if fitness >= og_fitness:
                    og_fitness = fitness
                    og_mult = mult
                    og_shift = shift
                
    return affine_shift(text, og_mult, og_shift)

def crib_affine(text, crib):
    text = td.remove_text(text).lower()
    crib = td.remove_text(crib).lower()
    
    for i in range(len(text) - len(crib) + 1):
        for i1 in range(len(crib)):
            for i2 in range(i1+1, len(crib)):
                t1, t2, c1, c2 = ord(text[i+i1])-ord('a'), ord(text[i+i2])-ord('a'), ord(crib[i1])-ord('a'), ord(crib[i2])-ord('a')
                
                mult = ((t1-t2) * st.mod_inverse((c1-c2), 26)) % 26
                
                if mult != 0:
                    shift = t1 - c1 * mult
                    
                    if text[i:i+len(crib)] == affine_shift(crib, mult, shift):
                        return affine_decrypt(text, mult, shift)
    
    return text.upper()

def angle_affine(text):
    og_angle = 0
    og_mult = 0
    og_shift = 0
    mono_frequencies = st.monolist(st.normalize_dict(td.get_mono_frequencies(dr.monos())))
    
    for mult in range(26):
        if st.mod_inverse(mult, 26) != 0:
            for shift in range(26):
                angle = st.vector_cos(st.monolist(st.normalize_dict(td.get_mono_text(affine_decrypt(text, mult, shift)))), mono_frequencies)

                if angle > og_angle:
                    og_angle = angle
                    og_mult = mult
                    og_shift = shift
                    
    return affine_decrypt(text, og_mult, og_shift)

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
    mono_frequencies = st.monolist(st.normalize_dict(td.get_mono_frequencies(dr.monos())))
    
    for shift in range(26):
        variance = st.variation(st.monolist(st.normalize_dict(td.get_mono_text(caesar_shift(text, shift)))), mono_frequencies)
        
        if variance < og_variance:
            og_variance = variance
            og_shift = shift
            
    return caesar_shift(text, og_shift)

def angle_caesar(text):
    og_angle = 0
    og_shift = 0
    mono_frequencies = st.monolist(st.normalize_dict(td.get_mono_frequencies(dr.monos())))
    
    for shift in range(26):
        angle = st.vector_cos(st.monolist(st.normalize_dict(td.get_mono_text(caesar_shift(text, shift)))), mono_frequencies)
        
        if angle > og_angle:
            og_angle = angle
            og_shift = shift
            
    return caesar_shift(text, og_shift)

def generate_sub_key(key, fill=""):
    subkey = ""
    key = td.remove_text(key).upper()
    fill = fill.lower()
    
    for letter in key:
        if letter not in subkey:
            subkey += letter
            
    shift = 0
    
    if fill == "continue":
        shift = ord(subkey[len(subkey)-1]) - ord('A')
        
    elif fill == "last":
        for char in range(26):
            letter = chr(ord('A') + char)
            if letter in subkey:
                shift = char
                
    for char in range(26):
        letter = chr((char + shift) % 26 + ord('A'))
        
        if letter not in subkey:
            subkey += letter
            
    return subkey

def stochastic_hill_key_mono(text, limit=10000):
    tetra_frequencies = td.get_tetra_frequencies(dr.tetras())
    key = []
    
    for char in range(26):
        key.append(chr(ord('A') + char))
        
    random.shuffle(key)
    og_fitness = st.tetra_fitness(mono_substitute(text, st.list_to_str(key)), tetra_frequencies)
    
    count = 0
    
    while count < limit:
        child_key = key.copy()
        
        i1, i2 = random.randint(0,25), random.randint(0,25)
        child_key[i1], child_key[i2] = child_key[i2], child_key[i1]
        
        fitness = st.tetra_fitness(mono_substitute(text, st.list_to_str(child_key)), tetra_frequencies)
        
        if fitness > og_fitness:
            og_fitness = fitness
            key = child_key.copy()
            count = 0
        
        count += 1
        
    return st.list_to_str(key)

def stochastic_hill_climb_mono(text, limit=50):
    tetra_frequencies = td.get_tetra_frequencies(dr.tetras())
    og_fitness = st.tetra_fitness(text, tetra_frequencies)
    og_key = ""
    
    for i in range(limit):
        key = stochastic_hill_key_mono(text)
        fitness = st.tetra_fitness(mono_substitute(text, key), tetra_frequencies)
        
        if fitness > og_fitness:
            og_fitness = fitness
            og_key = key
            print(f"{i+1}/{limit}: {invert_alpha_key(og_key).upper()}")
            
    print(f"Best key: {invert_alpha_key(og_key).upper()}")
    
    return mono_substitute(text, og_key)

def poly_substitute(text, keys):
    split = len(keys)
    print(split)
    text = td.split_text(text, split)
    print(text)
    
    for i in range(split):
        text[i] = mono_substitute(text[i], keys[i])
        
    return td.join_blocks(text)