from math import sqrt, log

def variation(measured, expected):
    variation = 0
    
    for i in range(len(measured)):
        variation += (measured[i] - expected[i])**2/expected[i]
        
    return variation

def normalize_dict(items):
    total = 0
    
    for item in items:
        total += items[item]
        
    for item in items:
        items[item] /= total;
        
    return items

def monolist(items):
    monolist = []
    
    for char in range(26):
        monolist.append(items[chr(ord('A') + char)])
        
    return monolist

def dot_product(vec1, vec2):
    total = 0
    
    if len(vec1) == len(vec2):
        
        for i in range(len(vec1)):
            total += vec1[i] * vec2[i]
            
    return total

def magnitude(vec):
    return sqrt(dot_product(vec, vec))

def vector_cos(vec1, vec2):
    if len(vec1) == len(vec2):
        return dot_product(vec1, vec2)/(magnitude(vec1) * magnitude(vec2))
    
def tetra_fitness(text, tetra_frequencies):
    fitness = 0
    
    for i in range(len(text)-3):
        if tetra_frequencies[text[i:i+4]] == 0:
            fitness -= 999999999999
            
        else:
            fitness += log(tetra_frequencies[text[i:i+4]])
            
    return fitness/(len(text)-3)