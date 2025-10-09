import train_data as td
        
words = td.get_word_frequencies("Data/word_frequency.txt")

monos = td.get_mono_frequencies("Data/mono_frequency.txt")

tetras = td.get_tetra_frequencies("Data/tetra_frequency.txt")

logtetras = td.get_logtetra_frequencies("Data/tetra_frequency.txt")

running = True

while running:
    cmd = input("\nWhat is your command? ")
    
    if cmd == "quit":
        running = False
        
    elif cmd == "filter":
        print(td.remove_filler("Resources/train.txt"))
        
    elif cmd == "train words":
        td.train_words("Resources/train.txt", "Data/words.txt")
        
    elif cmd == "train word frequ":
        td.train_word_frequency("Resources/train.txt", "Data/word_frequency.txt")
        
    elif cmd == "get words":
        words = td.get_word_frequencies("Data/word_frequency.txt")
        
    elif cmd == "word frequ":
        td.print_frequency(words, "word")
            
    elif cmd == "train mono":
        td.train_mono_frequency("Resources/train.txt", "Data/mono_frequency.txt")
        
    elif cmd == "get mono":
        monos = td.get_mono_frequencies("Data/mono_frequency.txt")
        
    elif cmd == "mono frequ":
        td.print_frequency(monos, "monogram")
            
    elif cmd == "train tetra":
        td.train_tetra_frequency("Resources/train.txt", "Data/tetra_frequency.txt")
        
    elif cmd == "get tetra":
        tetras = td.get_tetra_frequencies("Data/tetra_frequency.txt")
        
    elif cmd == "tetra frequ":
        td.print_frequency(tetras, "tetragram")
        
    elif cmd == "logtetra frequ":
        td.print_frequency(logtetras, "tetragram logarithm")