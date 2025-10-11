import train_data as td
import stats as st
import keys as ks

import matplotlib.pyplot as plt

cipher = open("Resources/ciphertext.txt", 'r').read().upper()
        
words = td.get_word_frequencies("Data/word_frequency.txt")

monos = td.get_mono_frequencies("Data/mono_frequency.txt")

tetras = td.get_tetra_frequencies("Data/tetra_frequency.txt")

logtetras = td.get_logtetra_frequencies("Data/tetra_frequency.txt")

running = True

while running:
    print('\n', cipher)
    
    cmd = input("\nWhat is your command? ").lower()
    
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
        
    elif cmd == "plot mono":
        alphabet = []
        
        for char in range(26):
            alphabet.append(chr(ord('A') + char))
            
        plt.subplot(2, 1, 1)
        plt.bar(alphabet, st.monolist(st.normalize_dict(monos)), color="blue")
        plt.title("English")
        
        plt.subplot(2, 1, 2)
        plt.bar(alphabet, st.monolist(st.normalize_dict(td.get_mono_text(cipher))), color="green")
        plt.title("Ciphertext")
        
        plt.show()
            
    elif cmd == "train tetra":
        td.train_tetra_frequency("Resources/train.txt", "Data/tetra_frequency.txt")
        
    elif cmd == "get tetra":
        tetras = td.get_tetra_frequencies("Data/tetra_frequency.txt")
        
    elif cmd == "tetra frequ":
        td.print_frequency(tetras, "tetragram")
        
    elif cmd == "logtetra frequ":
        td.print_frequency(logtetras, "tetragram logarithm")
        
    elif cmd == "read":
        cipher = open("Resources/ciphertext.txt", 'r').read().upper()
        
    elif cmd == "chi fitness":
        print(st.variation(st.monolist(st.normalize_dict(td.get_mono_text(cipher))), st.monolist(st.normalize_dict(td.get_mono_frequencies("Data/mono_frequency.txt")))))
        
    elif cmd == "vector fitness":
        print(st.vector_cos(st.monolist(st.normalize_dict(td.get_mono_text(cipher))), st.monolist(st.normalize_dict(td.get_mono_frequencies("Data/mono_frequency.txt")))))
        
    elif cmd == "tetra fitness":
        print(st.tetra_fitness(cipher, st.normalize_dict(tetras)))
        
    elif cmd == "ioc":
        print(st.IOC(cipher))
        
    elif cmd == "iocs":
        try:
            split = int(input("Size of split: "))
                
            for offset in range(split):
                print(f"{offset+1}/{split}: {st.IOC_split(cipher, split, offset)}")
        except:
            print("Invalid input")
            
    elif cmd == "entropy":
        print(st.entropy(cipher))
        
    elif cmd == "invert mono":
        alphakey = input("Enter monoalphabetic key: ")
        print(ks.invert_alpha_key(alphakey))
        
    elif cmd == "sub mono":
        alphakey = input("Enter monoalphabetic key: ")
        cipher = ks.mono_substitute(cipher, alphakey)
        
    elif cmd == "decrypt mono":
        alphakey = input("Enter monoalphabetic key: ")
        cipher = ks.mono_decrypt(cipher, alphakey)
        
    elif cmd == "upper":
        cipher = cipher.upper()