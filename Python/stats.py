def variation(measured, expected):
    variation = 0
    
    for i in range(len(measured)):
        variation += (measured[i] - expected[i])**2/expected[i]
        
    return variation