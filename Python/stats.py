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