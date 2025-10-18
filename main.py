import train_data as td
import stats as st
import keys as ks
import directories as dr

import matplotlib.pyplot as plt

cipher = open(dr.cipher(), 'r').read().upper()
        
words = td.get_word_frequencies(dr.words())

monos = td.get_mono_frequencies(dr.monos())

tetras = td.get_tetra_frequencies(dr.tetras())

logtetras = td.get_logtetra_frequencies(dr.tetras())

running = True

while running:
    print('\n', cipher)
    
    cmd = input("\nWhat is your command? ").lower()
    
    if cmd == "quit":
        running = False
        
    elif cmd == "filter":
        print(td.remove_filler(dr.train()))
        
    elif cmd == "train words":
        td.train_words(dr.train(), dr.words_raw())
        
    elif cmd == "train word frequ":
        td.train_word_frequency(dr.train(), dr.words())
        
    elif cmd == "get words":
        words = td.get_word_frequencies(dr.words())
        
    elif cmd == "word frequ":
        td.print_frequency(words, "word")
            
    elif cmd == "train mono":
        td.train_mono_frequency(dr.train(), dr.monos())
        
    elif cmd == "get mono":
        monos = td.get_mono_frequencies(dr.monos())
        
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
        td.train_tetra_frequency(dr.train(), dr.tetras())
        
    elif cmd == "get tetra":
        tetras = td.get_tetra_frequencies(dr.tetras())
        
    elif cmd == "tetra frequ":
        td.print_frequency(tetras, "tetragram")
        
    elif cmd == "logtetra frequ":
        td.print_frequency(logtetras, "tetragram logarithm")
        
    elif cmd == "read":
        cipher = open(dr.cipher(), 'r').read().upper()
        
    elif cmd == "chi fitness":
        print(st.variation(st.monolist(st.normalize_dict(td.get_mono_text(cipher))), st.monolist(st.normalize_dict(td.get_mono_frequencies(dr.monos())))))
        
    elif cmd == "vector fitness":
        print(st.vector_cos(st.monolist(st.normalize_dict(td.get_mono_text(cipher))), st.monolist(st.normalize_dict(td.get_mono_frequencies(dr.monos())))))
        
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
            
    elif cmd == "plot ioc":
        try:
            limit = int(input("Enter maximum range of data: "))
            nums = []
            iocs = []
            
            for i in range(limit):
                split = i+1
                nums.append(split)
                average_ioc = 0
                
                for offset in range(split):
                    average_ioc += st.IOC_split(cipher, split, offset) / split
                    
                iocs.append(average_ioc)
                
            plt.bar(nums, iocs)
            plt.title("IoC's")
            plt.show()
            
        except:
            print("Invalid limit")
            
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
        
    elif cmd == "cshift":
        try:
            shift = int(input("Enter shift: "))
            cipher = ks.affine_shift(cipher, 1, shift)
        
        except:
            print("Invalid shift")
            
    elif cmd == "force caesar":
        cipher = ks.brute_force_caesar(cipher)
        
    elif cmd == "crib caesar":
        crib = input("Enter crib: ")
        cipher = ks.crib_caesar(cipher, crib)
        
    elif cmd == "chi caesar":
        cipher = ks.chi_squared_caesar(cipher)
        
    elif cmd == "angle caesar":
        cipher = ks.angle_caesar(cipher)
        
    elif cmd == "inv":
        print(st.mod_inverse(int(input("number: ")), int(input("base: "))))
        
    elif cmd == "affine":
        try:
            mult = int(input("Enter multiplier: "))
            shift = int(input("Enter shift: "))
            cipher = ks.affine_shift(cipher, mult, shift)
        
        except:
            print("Invalid input")
            
    elif cmd == "decrypt affine":
        try:
            mult = int(input("Enter multiplier: "))
            shift = int(input("Enter shift: "))
            cipher = ks.affine_decrypt(cipher, mult, shift)

        except:
            print("Invalid input")
            
    elif cmd == "force affine":
        cipher = ks.brute_force_affine(cipher)
        
    elif cmd == "crib affine":
        crib = input("Enter crib: ")
        cipher = ks.crib_affine(cipher, crib)
        
    elif cmd == "angle affine":
        cipher = ks.angle_affine(cipher)
        
    elif cmd == "sub key":
        key = input("Enter keyword: ")
        filltype = input("Enter fill method (continue, last): ")
        
        print(ks.generate_sub_key(key, fill=filltype))
        
    elif cmd == "encrypt sub":
        key = input("Enter keyword: ")
        filltype = input("Enter fill method (continue, last): ")
        
        cipher = ks.mono_substitute(cipher, ks.generate_sub_key(key, fill=filltype))
        
    elif cmd == "decrypt sub":
        key = input("Enter keyword: ")
        filltype = input("Enter fill method (continue, last): ")
        
        cipher = ks.mono_decrypt(cipher, ks.generate_sub_key(key, fill=filltype))
        
    elif cmd == "hill sub":
        cipher = ks.stochastic_hill_climb_mono(cipher)
        
    elif cmd == "sub poly":
        try:
            split = int(input("Enter split number: "))
            
            keys = []
            for i in range(split):
                key = input(f"Monoalphabetic key {i+1}: ")
                keys.append(key)
            
            cipher = ks.poly_substitute(cipher, keys)
            
        except:
            print("Invalid input")
        
    elif cmd == "decrypt poly":
        try:
            split = int(input("Enter split number: "))
            
            keys = []
            for i in range(split):
                key = input(f"Monoalphabetic key {i+1}: ")
                keys.append(ks.invert_alpha_key(key))
            
            cipher = ks.poly_substitute(cipher, keys)

        except:
            print("Invalid input")
            
    elif cmd == "vigenere":
        key = input("Enter key: ")
        cipher = ks.vigenere(cipher, key)
        
    elif cmd == "decrypt vig":
        key = input("Enter key: ")
        cipher = ks.vigenere_decrypt(cipher, key)
        
    elif cmd == "force vigenere":
        try:
            lower = int(input("Enter lower limit for length of keyword: "))
            upper = int(input("Enter upper limit of length of keyword: "))
            cipher = ks.brute_force_vigenere(cipher, lower, upper)

        except:
            print("Invalid input")
            
    elif cmd == "hill vigenere":
        try:
            period = int(input("Enter period of key: "))
            cipher = ks.hill_climb_vigenere(cipher, period)
            
        except:
            print("Invalid input")
        
    elif cmd == "angle vigenere":
        try:
            period = int(input("Enter period of key: "))
            cipher = ks.angle_vigenere(cipher, period)
        except:
            print("Invalid input")
        
    elif cmd == "beaufort":
        key = input("Enter keyword: ")
        cipher = ks.beaufort(cipher, key)
        
    elif cmd == "force beaufort":
        try:
            lower = int(input("Enter lower limit for length of keyword: "))
            upper = int(input("Enter upper limit of length of keyword: "))
            cipher = ks.brute_force_beaufort(cipher, lower, upper)

        except:
            print("Invalid input")
            
    elif cmd == "hill beaufort":
        try:
            period = int(input("Enter period of key: "))
            cipher = ks.hill_climb_beaufort(cipher, period)
            
        except:
            print("Invalid input")
            
    elif cmd == "angle beaufort":
        try:
            period = int(input("Enter period of key: "))
            cipher = ks.angle_beaufort(cipher, period)
            
        except:
            print("Invalid input")
            
    elif cmd == "invert key":
        key = input("Enter key: ")
        print(ks.invert_key(key))
        
    elif cmd == "porta":
        key = input("Enter key: ")
        cipher = ks.porta(cipher, key)
        
    elif cmd == "hill porta":
        try:
            period = int(input("Enter period of key: "))
            cipher = ks.hill_climb_template(cipher, period, lambda text, key: ks.porta(text, key))
            
        except:
            print("Invalid input")
            
    elif cmd == "angle porta":
        try:
            period = int(input("Enter period of key: "))
            cipher = ks.angle_template(cipher, period, lambda text, key: ks.porta(text, key))
        
        except:
            print("Invalid input")
            
    elif cmd == "poly affine":
        try:
            period = int(input("Enter period: "))
            
            for offset in range(period):
                mult = int(input(f"Enter multiplier {offset+1}: "))
                shift = int(input(f"Enter shift {offset+1}: "))
                cipher = ks.period_affine(cipher, mult, shift, period, offset)

        except:
            print("Invalid input")
            
    elif cmd == "decrypt poly aff":
        try:
            period = int(input("Enter period: "))
            
            for offset in range(period):
                mult = int(input(f"Enter multiplier {offset+1}: "))
                shift = int(input(f"Enter shift {offset+1}: "))
                cipher = ks.decrypt_period_affine(cipher, mult, shift, period, offset)
        
        except:
            print("Invalid input")
                
    elif cmd == "angle poly aff":
        try:
            period = int(input("Enter period: "))
            cipher = ks.angle_period_affine(cipher, period)

        except:
            print("Invalid input")
            
    elif cmd == "quagmire 1":
        key_plain = input("Enter plaintext key: ")
        key_period = input("Enter period key: ")
        print(ks.generate_quagmire1_keys(key_plain, key_period))