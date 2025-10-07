import train_data as td

running = True

while running:
    cmd = input("What is your command? ")
    
    if cmd == "quit":
        running = False
        
    elif cmd == "filter": # remove after done with testing
        print(td.remove_filler("Resources/train.txt"))