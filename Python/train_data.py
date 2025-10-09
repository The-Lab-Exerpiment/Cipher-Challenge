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
        
def get_word_frequencies(filename):
    word_frequency = {}
    
    wordlist = open(filename, 'r').read().split('\n')
    
    for item in wordlist:
        item = item.split(' ')
        
        if len(item) == 2:
            word_frequency[item[0]] = int(item[1])
        
    return word_frequency

def train_mono_frequencies(filename, targetfile):
    mono_frequencies = {}
    
    text = remove_filler(filename)
    
    for char in range(0, 26):
        mono_frequencies[chr(ord('A') + char)] = 0
        
    for letter in text:
        if letter in mono_frequencies:
            mono_frequencies[letter] += 1
            
    open(targetfile, 'w').write("")
    
    target = open(targetfile, 'a');
    
    for char in mono_frequencies:
        target.write(f"{char} {mono_frequencies[char]}\n")