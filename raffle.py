import random
import json




def add_bids(bids_list):
    gamertag = raw_input("Enter Gamertag:")
    try:
        num_bids = int(raw_input("Enter number of chances purchased:"))
        for i in range(num_bids):
            bids_list.append(gamertag)
    except ValueError:
        print "Input must be an integer"
    
    
def draw_winner(bids_list):
    winner = random.choice(bids_list)
    print "{0} has won the raffle".format(winner)    
    
    
def main():
    try:
        with open("villager_raffle.json", "r") as infile:
            raffle_bids = json.load(infile)
    except IOError:
        print "IOError: Couldn't load json data"
        raffle_bids = []
    
    while True:
        print """
            1) Add bids
            2) Draw winner"""
        option = raw_input(">")
        if option == "1":
            add_bids(raffle_bids)
        elif option == "2":
            draw_winner(raffle_bids)
        elif option == "3":
            with open("villager_raffle.json", "w") as outfile:
                json.dump(raffle_bids, outfile)
            return

if __name__ == "__main__":
    main()