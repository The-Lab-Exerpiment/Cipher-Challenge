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

def train_words(filename, targetfile):
    words = remove_filler(filename).split(' ')
    
    wordlist = open(targetfile, 'r').read().split('\n')
    
    for word in words:
        if word not in wordlist:
            wordlist.append(word)
    
    wordlist.sort()
    
    open(targetfile, 'w').write("")
    
    target = open(targetfile, 'a')
    
    for word in wordlist:
        target.write(word + '\n')
        
    target.close()
    
def train_word_frequency(filename, targetfile):
    word_frequency = {}
    
    wordlist = remove_filler(filename).split(' ')
    
    for word in wordlist:
        if word not in word_frequency:
            word_frequency[word] = 1
            
        else:
            word_frequency[word] += 1
            
    open(targetfile, 'w').write("")
    
    target = open(targetfile, 'a')
    
    for word in word_frequency:
        target.write(f"{word} {word_frequency[word]}\n")