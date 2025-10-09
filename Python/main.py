import train_data as td
        
words = td.get_word_frequencies("Data/word_frequency.txt")

running = True

while running:
    cmd = input("\nWhat is your command? ")
    
    if cmd == "quit":
        running = False
        
    elif cmd == "filter": # remove after done with testing
        print(td.remove_filler("Resources/train.txt"))
        
    elif cmd == "train words":
        td.train_words("Resources/train.txt", "Data/words.txt")
        
    elif cmd == "train word frequ":
        td.train_word_frequency("Resources/train.txt", "Data/word_frequency.txt")
        
    elif cmd == "get words":
        word_frequencies = td.get_word_frequencies("Data/word_frequency.txt")
        
    elif cmd == "word frequ":
        word = input("Enter word to find frequency of: ").upper()
        
        if word in words:
            print(f"{word}: {words[word]}")
            
        else:
            print("Word not found")
            
    elif cmd == "train mono":
        td.train_mono_frequencies("Resources/train.txt", "Data/mono_frequency.txt")