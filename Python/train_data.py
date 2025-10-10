from math import log
import stats as st

def int_to_letter(num):
    return chr(ord('A') + num)

def ints_to_string(nums):
    string = ""
    
    for num in nums:
        string += int_to_letter(num)
        
    return string

def remove_filler(filename, include_hyphens=True, include_spaces=True):
    text = open(filename, 'r').read().upper()
    
    newtext = ""
    
    hyphenated = True
    
    for letter in text:
        if letter >= 'A' and letter <= 'Z':
            newtext += letter
            hyphenated = True
        
        elif (letter == ' ' or letter == '\n') and include_spaces:
            newtext += ' '
            hyphenated = False
            
        elif letter == '-' and hyphenated and include_hyphens:
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
        
    target.close()
        
def get_word_frequencies(filename):
    word_frequency = {}
    
    wordlist = open(filename, 'r').read().split('\n')
    
    for item in wordlist:
        item = item.split(' ')
        
        if len(item) == 2:
            word_frequency[item[0]] = int(item[1])
        
    return word_frequency

def train_mono_frequency(filename, targetfile):
    mono_frequencies = {}
    
    text = remove_filler(filename)
    
    for char in range(0, 26):
        mono_frequencies[chr(ord('A') + char)] = 0
        
    for letter in text:
        if letter in mono_frequencies:
            mono_frequencies[letter] += 1
            
    open(targetfile, 'w').write("")
    
    target = open(targetfile, 'a')
    
    for char in mono_frequencies:
        target.write(f"{char} {mono_frequencies[char]}\n")
        
    target.close()
        
def get_mono_frequencies(filename):
    mono_frequencies = {}
    
    monolist = open(filename, 'r').read().split('\n')
    
    for item in monolist:
        item = item.split(' ')
        
        if len(item) == 2:
            mono_frequencies[item[0]] = int(item[1])
            
    mono_frequencies = st.normalize_dict(mono_frequencies)
        
    return mono_frequencies

def train_tetra_frequency(filename, targetfile):
    tetra_frequencies = {}
    
    text = remove_filler(filename, include_hyphens=False, include_spaces=False)
    
    for ch1 in range(26):
        for ch2 in range(26):
            for ch3 in range(26):
                for ch4 in range(26):
                    tetra_frequencies[ints_to_string([ch1, ch2, ch3, ch4])] = 0
                    
    for i in range(len(text) - 3):
        tetra_frequencies[text[i] + text[i+1] + text[i+2] + text[i+3]] += 1
        
    open(targetfile, 'w').write("")
    
    target = open(targetfile, 'a')
        
    for ch1 in range(26):
        for ch2 in range(26):
            for ch3 in range(26):
                for ch4 in range(26):
                    tetra = ints_to_string([ch1, ch2, ch3, ch4])
                    target.write(f"{tetra} {tetra_frequencies[tetra]}\n")
                    
    target.close()
    
def get_tetra_frequencies(filename):
    tetra_frequencies = {}
    
    tetralist = open(filename, 'r').read().split('\n')
    
    for item in tetralist:
        item = item.split(' ')
        
        if len(item) == 2:
            tetra_frequencies[item[0]] = int(item[1])
            
    return tetra_frequencies

def get_logtetra_frequencies(filename):
    tetra_frequencies = get_tetra_frequencies(filename)
    
    for tetra in tetra_frequencies:
        if tetra_frequencies[tetra] == 0:
            tetra_frequencies[tetra] = -999999
        
        else:
            tetra_frequencies[tetra] = log(tetra_frequencies[tetra])
            
    return tetra_frequencies

def print_frequency(items, name):
    item = input(f"Enter {name} to find frequency of: ").upper()
    
    if item in items:
        print(f"{item}: {items[item]}")
        
    else:
        print(f"{name.capitalize()} not found")
        
def get_mono_text(text):
    text = text.upper()
    mono_frequencies = {}
    
    for char in range(0, 26):
        mono_frequencies[chr(ord('A') + char)] = 0
        
    for letter in text:
        if letter in mono_frequencies:
            mono_frequencies[letter] += 1
            
    return mono_frequencies