def remove_filler(filename):
    text = open(filename, 'r').read().upper()
    
    newtext = ""
    
    for letter in text:
        if(letter >= 'A' and letter <= 'Z') or letter==' ':
            newtext += letter
        
    return newtext
