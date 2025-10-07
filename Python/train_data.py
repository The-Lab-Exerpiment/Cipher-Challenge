def remove_filler(filename):
    text = open(filename, 'r').read().upper()
    
    newtext = ""
    
    hyphenated = True
    
    for letter in text:
        if letter >= 'A' and letter <= 'Z':
            newtext += letter
            hyphenated = True
        
        elif letter == ' ' or letter == '\n':
            newtext += ' '
            hyphenated = False
            
        elif letter == '-' and hyphenated:
            newtext += letter
        
    return newtext

def train_words(filename, target):
    words = remove_filler(filename).split(' ')
    
    wordlist = open(target, 'r').read().split('\n')
    
    for word in words:
        if word not in wordlist:
            wordlist.append(word)
    
    wordlist.sort()
    
    open(target, 'w').write("")
    
    targetfile = open(target, 'a')
    
    for word in wordlist:
        targetfile.write(word + '\n')
        
    targetfile.close()