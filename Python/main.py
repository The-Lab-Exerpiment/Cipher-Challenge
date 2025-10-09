import train_data as td
        
word_frequencies = td.get_word_frequencies("Resources/word_frequency.txt")

running = True

while running:
    cmd = input("What is your command? ")
    
    if cmd == "quit":
        running = False
        
    elif cmd == "filter": # remove after done with testing
        print(td.remove_filler("Resources/train.txt"))
        
    elif cmd == "train words":
        td.train_words("Resources/train.txt", "Resources/words.txt")
        
    elif cmd == "train word frequ":
        td.train_word_frequency("Resources/train.txt", "Resources/word_frequency.txt")
        
    elif cmd == "get words":
        word_frequencies = td.get_word_frequencies("Resources/word_frequency.txt")