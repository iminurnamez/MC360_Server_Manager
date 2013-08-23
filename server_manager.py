import os
import time
import random
import pickle
import pygame
import praw
import pyimgur
import economy_graph
import fighting

SUBREDDIT = ""
BOT_NAME = ""
BOT_PASSWORD = ""
IMGUR_CLIENT_ID = ""
MOD_NAME = ""
MOD_PASSWORD = ""


class Economy(object):
    def __init__(self):
        self.prices = {"Cactus": .04,
                             "Coal": 2.00,
                             "Cobblestone": .05,
                             "Cooked Fish": .10,
                             "Diamond": 50.00,
                             "Dirt": .05,
                             "Flower": .25,
                             "Gold Ore": 15.00,
                             "Gold Ingot": 16.5,
                             "Gravel": .05,
                             "Iron Ore": 3.00,
                             "Iron Ingot": 3.50,
                             "Leaves": .05,
                             "Leather": 2.50,
                             "Melon Slice": .07,
                             "Mushroom": .25,
                             "Obsidian": 7.50,
                             "Pumpkin": .03,
                             "Redstone Dust": 2.00,
                             "Sand": .05,
                             "Sandstone": .20,
                             "Sapling": .025,
                             "Wood": .05,
                             "Wheat": .05,
                             "Wheat Seeds": .08}

        # index [0] = line color,
        # appended elements will be tuples of floats
        self.price_history = {"Cactus": ["limegreen"],		
                                        "Coal": ["gray16"],
                                        "Cobblestone": ["lightgray"],
                                        "Cooked Fish": ["cyan"],
                                        "Diamond": ["cadetblue1"],
                                        "Dirt": ["chocolate4"],
                                        "Flower": ["yellow"],
                                        "Gold Ore": ["gold"],
                                        "Gold Ingot": ["gold2"],
                                        "Gravel": ["gray29"],
                                        "Iron Ore": ["gray60"],
                                        "Iron Ingot": ["gray40"],
                                        "Leaves": ["darkolivegreen"],
                                        "Leather": ["chocolate1"],
                                        "Melon Slice": ["hotpink"],
                                        "Mushroom": ["red2"],
                                        "Obsidian": ["purple4"],
                                        "Pumpkin": ["orangered"],
                                        "Redstone Dust": ["red"],
                                        "Sand": ["navajowhite"],
                                        "Sandstone": ["peachpuff3"],
                                        "Sapling": ["chartreuse3"],
                                        "Wheat": ["tan2"],
                                        "Wheat Seeds": ["tan4"],
                                        "Wood": ["saddlebrown"]}
                                    
        self.volatilities = ["Calm", "Active", "Frantic"]
        self.volatility_mods = {"Calm": 10, "Active": 20,
                                            "Frantic": 40}
        self.next_volatility = {"Calm": ["Active", "Calm", "Calm"],
                                          "Active": ["Calm", "Active", "Active",
                                                         "Frantic"],
                                          "Frantic": ["Calm", "Active", "Active", "Frantic"]}
        self.volatility = "Calm"

        self.trends = ["Horrendous", "Weak", "Stable", "Strong", "Phenomenal"]
        self.trend_mods = {"Phenomenal": 15, "Strong": 10, "Stable": 1,
                                      "Weak": -5, "Horrendous": -10}
        self.next_trend = {"Phenomenal": ["Phenomenal", "Strong", "Strong",
                                                              "Strong"],
                                     "Strong": ["Phenomenal", "Strong", "Strong", "Stable"],
                                     "Stable": ["Weak", "Stable", "Stable", "Strong"],
                                     "Weak": ["Stable", "Weak", "Weak", "Horrendous"],
                                     "Horrendous": ["Stable", "Weak", "Weak", "Horrendous"]}
        self.trend = "Stable"
        self.cycle_count = 0
        self.checked_ids = []
        self.citizens = {"RebuiltOak624": {"QCE Account": 100,
                                                            "Username": "iminurnamez",
                                                            "District": "Norhigashi",
                                                            "Title": "Citizen",
                                                            "Trade Hold": False,
                                                            "Gladiator Wins": 0,
                                                            "Gladiator Losses": 0,
                                                            "Inventory": {"Cactus": 0,		
                                                                                  "Coal": 0,
                                                                                  "Cobblestone": 0,
                                                                                  "Cooked Fish": 0,
                                                                                  "Diamond": 0,
                                                                                  "Dirt": 0,
                                                                                  "Flower": 0,
                                                                                  "Gold Ore": 0,
                                                                                  "Gold Ingot": 0,
                                                                                  "Gravel": 0,
                                                                                  "Iron Ore": 0,
                                                                                  "Iron Ingot": 0,
                                                                                  "Leaves": 0,
                                                                                  "Leather": 0,
                                                                                  "Melon Slice": 0,
                                                                                  "Mushroom": 0,
                                                                                  "Obsidian": 0,
                                                                                  "Pumpkin": 0,
                                                                                  "Redstone Dust": 0,
                                                                                  "Sand": 0,
                                                                                  "Sandstone": 0,
                                                                                  "Sapling": 0,
                                                                                  "Wheat": 0,
                                                                                  "Wheat Seeds": 0,
                                                                                  "Wood": 0}}}
        self.fights = []


    def update(self):
        self.previous_prices = {}
        for commodity in self.prices:
            self.previous_prices[commodity] = self.prices[commodity]
            self.trend = random.choice(self.next_trend[self.trend])
            self.volatility = random.choice(self.next_volatility[self.volatility])

        for item in self.prices:
            if random.randint(1, 100) < self.volatility_mods[self.volatility]:
                x = 50
                if self.prices[item] > self.base_prices[item] * 3:
                    x = 10
                elif self.prices[item] > self.base_prices[item] * 2:
                    x = 15
                elif self.prices[item] > self.base_prices[item] * 1.5:
                    x = 25
                elif self.prices[item] > self.base_prices[item] * 1.25:
                    x = 40
                elif self.prices[item] < self.base_prices[item] * .8:
                    x = 60
                elif self.prices[item] < self.base_prices[item] * .6:
                    x = 75
                elif self.prices[item] < self.base_prices[item] * .4:
                    x = 85
                elif self.prices[item] < self.base_prices[item] * .3:
                    x = 90
                x += self.trend_mods[self.trend]
                if random.randint(1, 100) < x:
                    self.prices[item] += self.prices[item] * random.uniform(0.0, 0.2)
                else:
                    self.prices[item] -= self.prices[item] * random.uniform(0.0, 0.2)
        for item in self.prices:
            self.price_history[item].append((self.cycle_count, self.prices[item]))
        self.cycle_count += 1


def post_prices(economy):
    bot = praw.Reddit(user_agent = BOT_NAME)
    bot.login(BOT_NAME, BOT_PASSWORD)
    
    text = "Economic Condition: {0}".format(economy.trend)
    text += "\n\nPrice Volatility: {0}".format(economy.volatility)
    text += "\n\nCommodity|Price|Change\n:---|---:|---:"
    for item in economy.prices:
        price = "{0:.2f}".format(economy.prices[item]).lstrip("0")
        text += "\n{0}|{1}|{2:+.4f}".format(item, price, economy.prices[item] -
                                                                   economy.previous_prices[item])
    text += "\n\nDisplayed prices are rounded to nearest hundredth"
    text += "\n\n**Graphs**\n\n"
    for commodity in economy.prices:
        economy_graph.single_commodity_graph(economy, commodity)
        path = os.path.join(commodity + ".png")
        imgur = pyimgur.Imgur(IMGUR_CLIENT_ID)
        uploaded_image = imgur.upload_image(path, title=commodity)
        text += "[{0}]({1}) ".format(commodity, uploaded_image.link)
        os.remove(os.path.join(commodity + ".png"))
    bot.submit(SUBREDDIT, "QCE Price Update", text)


def add_citizen(economy):
    gamertag = raw_input("Enter gamertag:")
    username = raw_input("Enter username:")
    district_map = {"1": "Utaratay",
                             "2": "Norhigashi",
                             "3": "Suletela",
                             "4": "Demacia"}
    print "\n1. Utaratay\n2. Norhigashi\n3. Suletela\n4. Demacia"
    district = district_map[raw_input("Choose district:")]
    title_map = {"1": "Citizen","2":"Governor"}
    print "\n1. Citizen\n2. Governor"
    title = title_map[raw_input("Choose title:")]
    economy.citizens[gamertag] = {"QCE Account": 0,
                                                     "Username": username,
                                                     "District": district,
                                                     "Title": title,
                                                     "Trade Hold": False,
                                                     "Gladiator Wins": 0,
                                                     "Gladiator Losses": 0,
                                                     "Inventory": {"Cactus": 0,		
                                                                           "Coal": 0,
                                                                           "Cobblestone": 0,
                                                                           "Cooked Fish": 0,
                                                                           "Diamond": 0,
                                                                           "Dirt": 0,
                                                                           "Flower": 0,
                                                                           "Gold Ore": 0,
                                                                           "Gold Ingot": 0,
                                                                           "Gravel": 0,
                                                                           "Iron Ore": 0,
                                                                           "Iron Ingot": 0,
                                                                           "Leaves": 0,
                                                                           "Leather": 0,
                                                                           "Melon Slice": 0,
                                                                           "Mushroom": 0,
                                                                           "Obsidian": 0,
                                                                           "Pumpkin": 0,
                                                                           "Redstone Dust": 0,
                                                                           "Sand": 0,
                                                                           "Sandstone": 0,
                                                                           "Sapling": 0,
                                                                           "Wheat": 0,
                                                                           "Wheat Seeds": 0,
                                                                           "Wood": 0}}
    print "{0} {1} added to {2}".format(title, gamertag, district)

def remove_citizen(economy):
    gamertag = raw_input("Enter gamertag:")
    if gamertag in economy.citizens:
        print "Are you sure you want to delete {0}?".format(gamertag)
        if raw_input(">") in ("y", "Y", "yes", "Yes"):
            del economy.citizens[gamertag]
            print "{0} has been removed".format(gamertag)
    
def change_citizenship(economy):
    gamertag = raw_input("Enter gamertag:")
    if gamertag in economy.citizens:
        new_district = raw_input("Enter new district:")
        print "Are you sure you want to change {0}'s district to {1}?".format(
                  gamertag, new_district)
        if raw_input(">") in ("y", "Y", "yes", "Yes"):
            economy.citizens[gamertag]["District"] = new_district
            print "{0} is now a citizen of {1}".format(gamertag, new_district)

def change_reddit_username(economy):
    gamertag = raw_input("Enter the gamertag:")
    new_username = raw_input("Enter the new username:")
    print "Change {0}'s username from {1} to {2}?".format(gamertag,
               economy.citizens[gamertag]["Username"], new_username)
    if raw_input(">") in ("Y", "y", "yes", "Yes"):
        economy.citizens[gamertag]["Username"] = new_username
        print "{0}'s username is now {1}".format(gamertag,
                   economy.citizens[gamertag]["Username"])

def change_gamertag(economy):
    gamertag = raw_input("Enter the gamertag you want to change:")
    new_gamertag = raw_input("Enter the new gamertag:")
    print "Change {0}'s gamertag to {1}?".format(gamertag, new_gamertag)
    if raw_input(">") in ("Y", "y", "yes", "Yes"):
        economy.citizens[new_gamertag] = {}														
        for k in economy.citizens[gamertag]:	
            economy.citizens[new_gamertag][k] = economy.citizens[gamertag][k]
        del economy.citizens[gamertag]
        print "{0}'s gamertag has been changed to {1}".format(gamertag, new_gamertag)


def change_title(economy):
    gamertag = raw_input("Enter the gamertag whose title you want to change:")
    new_title = raw_input("Enter {0}'s new title:")
    print "Change {0}'s title to {1}?".format(gamertag, new_title)
    if raw_input(">") in ("Y", "y", "yes", "Yes"):
        economy.citizens[gamertag]["Title"] = new_title
        print "{0} is now a {1}".format(gamertag, economy.citizens[gamertag]["Title"])

def print_citizen_roster(economy):
    for citizen in economy.citizens:
        print "\n{0:30} {1}".format(citizen, economy.citizens[citizen]["District"])
    
def citizen_menu(economy):
    menu_map = {"1": add_citizen,
    "2": change_citizenship,
    "3": change_title,
    "4": change_reddit_username,
    "5": change_gamertag,
    "6": remove_citizen,
    "7": print_citizen_roster}
    
    while True:
        print """
        Choose an option
        1) Add citizen
        2) Change district
        3) Change title
        4) Change reddit username
        5) Change gamertag
        6) Remove citizen
        7) Citizen Roster
        9) Quit"""
        citizen_option = raw_input("\n>")
        if citizen_option == "9":
            return
        elif citizen_option in ["1", "2", "3", "4", "5", "6", "7"]:
            menu_map[citizen_option](economy)
        else:
            print "Invalid option"             

def economy_handler(economy): 
    economy.update()
    post_prices(economy)	
    
def trade_handler(economy, author, gamertag, transaction_type, commodity, quantity):
    if economy.citizens[gamertag]["Username"] != str(author):
        return "Username/gamertag authorization failed"
    if economy.citizens[gamertag]["Trade Hold"]:
        return "Your trading rights are currently suspended"
    if transaction_type == "BUY":
        if economy.prices[commodity] * quantity <= economy.citizens[gamertag]["QCE Account"]:
            economy.citizens[gamertag]["QCE Account"] -= economy.prices[commodity] * quantity
            economy.citizens[gamertag]["Inventory"][commodity] += quantity
            return "Transaction Completed: {0} {1} has been credited to your QCE account".format(
                         quantity, commodity)
        else:
            return "Insufficient Funds"
    elif transaction_type == "SELL":
        if economy.citizens[gamertag]["Inventory"][commodity] >= quantity:
            economy.citizens[gamertag]["QCE Account"] += economy.prices[commodity] * quantity
            economy.citizens[gamertag]["Inventory"][commodity] -= quantity
            return "Transaction Completed: ${0:.2f} has been credited to your QCE account".format(
                         economy.prices[commodity] * quantity)
        else:
            return "Insufficient Commodity Amount"

def withdrawal(economy, gamertag):
    commodity = raw_input("\t\tEnter \"cash\" or Commodity name to withdraw:\n\t\t>")
    if commodity in ["Cash", "cash", "$"]:
        try:
           qty = float(raw_input("\t\tEnter withdrawal amount:"))
        except ValueError:
            print "Error: Expecting a float"
        if economy.citizens[gamertag]["QCE Account"] >= qty:
            economy.citizens[gamertag]["QCE Account"] -= qty
            print "\n\t\t${0} withdrawn from {1}'s account\n".format(qty, gamertag)
        else:
            print "Insufficient funds"
        
    elif commodity in economy.citizens[gamertag]["Inventory"].keys():
        qty = int(raw_input("\t\tEnter withdrawal amount:"))
        if economy.citizens[gamertag]["Inventory"][commodity] >= qty:
            economy.citizens[gamertag]["Inventory"][commodity] -= qty
            print "\n\t\t{0} {1} withdrawn from {2}'s account\n".format(qty, commodity, gamertag)
        else:
            print "Insufficient commodity amount"
        
def deposit(economy, gamertag):        
    commodity = raw_input("\t\tEnter \"cash\" or Commodity name to deposit\n\t\t>")
    if commodity == "cash":
        qty = float(raw_input("\t\tEnter deposit amount:"))
        economy.citizens[gamertag]["QCE Account"] += qty
        print "\n\t\t${0} deposited to {1}'s account\n".format(qty, gamertag)
    else:
        qty = int(raw_input("\t\tEnter deposit amount:"))
        try:
            economy.citizens[gamertag]["Inventory"][commodity] += qty
            print "\n\t\t{0} {1} deposited to {2}'s account\n".format(qty, commodity, gamertag)
        except KeyError:
            print "Invalid commodity"
        
def in_game_buy(economy, gamertag):
    commodity = raw_input("\t\tEnter Commodity name:")
    if commodity in economy.prices.keys():
        qty = int(raw_input("Enter purchase amount:"))
        if economy.citizens[gamertag]["QCE Account"] >= qty * economy.prices[commodity]:
            economy.citizens[gamertag]["QCE Account"] -= qty * economy.prices[commodity]
            print "{0} purchased {1} {2} for ${3:.2f}".format(gamertag, qty, commodity,
                       qty * economy.prices[commodity])
        else:
            print "Insufficient funds"
    else:
        print "Invalid commodity"
        
def in_game_sell(economy, gamertag):
    commodity = raw_input("\t\tEnter Commodity name:")
    if commodity in economy.citizens[gamertag]["Inventory"].keys():
        qty = int(raw_input("\t\tEnter sale amount:"))
        total_sale = qty * economy.prices[commodity]
        economy.citizens[gamertag]["QCE Account"] += total_sale
        print "\n\t\t{0} {1} sold by {2} for ${3:.2f}\n".format(qty,
                  commodity, gamertag, total_sale)
    else:
        print "Invalid commodity"
        
def impose_trade_ban(economy, gamertag):
    if not economy.citizens[gamertag]["Trade Hold"]:
        economy.citizens[gamertag]["Trade Hold"] = True
        print "Trading ban imposed on {0}".format(gamertag)
    else:
        print "{0} is already banned from trading".format(gamertag)
        
def lift_trade_ban(economy, gamertag):
    if economy.citizens[gamertag]["Trade Hold"]:
        economy.citizens[gamertag]["Trade Hold"] = False
        print "{0} is authorized to trade"
    else:
        print "{0} is not banned from trading"
        
def display_account_balance(economy, gamertag):
    print "\n\n\nBalance: ${0:.2f}\n".format(
              economy.citizens[gamertag]["QCE Account"])
    for commodity in economy.citizens[gamertag]["Inventory"]:
        print "{0:20}\t{1:>8}".format(commodity,
                  economy.citizens[gamertag]["Inventory"][commodity])            
            
def exchange_handler(economy):
    gamertag = raw_input("Enter gamertag:")
    exchange_map = {"1": withdrawal,
                                 "2": deposit,
                                 "3": in_game_buy,
                                 "4": in_game_sell,
                                 "5": impose_trade_ban,
                                 "6": lift_trade_ban,
                                 "7": display_account_balance}
    while True:
        option = raw_input("""
        Current Account: {0}
        Choose transaction type:
        1) Withdrawal
        2) Deopsit
        3) Buy Items
        4) Sell Items
        5) Impose Trade Ban
        6) Lift Trade Ban
        7) Display Account
        8) Different gamertag
        9) Quit
        >""".format(gamertag))		
        if option == "9":
            return
        elif option == "8":
            gamertag = raw_input("Enter new gamertag:")
        elif option in ["1", "2", "3", "4", "5", "6", "7"]:
            exchange_map[option](economy, gamertag)    
        
def display_gladiator_record(economy):
    gladiator = raw_input("Enter gladiator's gamertag:")
    print "Wins: {0}  Losses: {1}".format(economy.citizens[gladiator]["Gladiator Wins"], 
               economy.citizens[gladiator]["Gladiator Losses"])

def setup_fight(economy):	
    gladiator1 = raw_input("Enter the first gladiator's gamertag:")
    gladiator2 = raw_input("Enter the second gladiator's gamertag:")
    if economy.citizens[gladiator1]["District"] == economy.citizens[gladiator2]["District"]:
        print "Gladiators are from the same district"
    else:
        bot = praw.Reddit(user_agent = BOT_NAME)
        bot.login(BOT_NAME, BOT_PASSWORD)
        fight = fighting.GladiatorFight(economy, gladiator1, gladiator2)
        economy.fights.append(fight)
        text = "{0} ".format(fight.marquee)
        text += "\n\nGladiator|W-L|Payout\n:---|:---:|---:"
        text += "\n{0}|{1}-{2}|{3:.2f}".format(gladiator1,
                      economy.citizens[gladiator1]["Gladiator Wins"],
                      economy.citizens[gladiator1]["Gladiator Losses"], fight.payouts[gladiator1])
        text += "\n{0}|{1}-{2}|{3:.2f}".format(gladiator2,
                      economy.citizens[gladiator2]["Gladiator Wins"],
                      economy.citizens[gladiator2]["Gladiator Losses"], fight.payouts[gladiator2])
        bot.submit(SUBREDDIT, "Gladiator Match: {0} vs. {1}".format(gladiator1, gladiator2, text))
    
def resolve_gladiator_match(economy):
    fight_map = {}
    i = 1
    for fight in economy.fights:
        fight_map[i] = fight
        print "{0}. {1}".format(i, fight.marquee)
        i += 1
    fight_num = int(raw_input("Choose fight to resolve:"))
    fight_map[fight_num].resolve_fight(economy)
    
def post_gladiator_records(economy):
    bot = praw.Reddit(user_agent = BOT_NAME)
    bot.login(BOT_NAME, BOT_PASSWORD)
    text = "Gladiator|W-L|District\n:---|:---:|:---"
    for citizen in economy.citizens:
        text += "\n{0}|{1}-{2}|{3}".format(citizen, economy.citizens[citizen]["Gladiator Wins"],
        economy.citizens[citizen]["Gladiator Losses"], economy.citizens[citizen]["District"])
    bot.submit(SUBREDDIT, "Gladiator Records", text)
    
def gladiator_menu(economy):
    gladiator_map = {"1": setup_fight,
                                "2": display_gladiator_record,
                                "3": resolve_gladiator_match,
                                "4": post_gladiator_records}
    print "\n\nGladiator Options"
    print "1. Set up new fight"
    print "2. Display Gladiator Record"
    print "3. Resolve fight"
    print "4. Post fighter records"
    option = raw_input("\nChoose an option:")
    if option in ["1", "2", "3", "4"]:
        gladiator_map[option](economy)
    
def run_bot(economy):
    bot = praw.Reddit(user_agent = BOT_NAME)
    bot.login(BOT_NAME, BOT_PASSWORD)
    while True:
        try:
            submissions = bot.get_subreddit(SUBREDDIT).get_new()
            for submission in submissions:
                if submission.id not in economy.checked_ids and "#" in submission.title:
                    title = submission.title
                    author = str(submission.author)
                    gamertag = str(submission.author_flair_text)
                    reply = ""
                    for commodity in economy.prices:
                        if commodity in title and "#GRAPH" not in title:
                            if commodity == "Wheat" and "Wheat Seeds" in title:
                                pass
                            else:
                                try:
                                    quantity = int(submission.selftext)
                                except ValueError:
                                    economy.checked_ids.append(submission.id)
                                    reply += "Post text must be a number"
                                    break
                            if "#BUY" in title:
                                reply += trade_handler(economy, author, gamertag, "BUY", commodity, quantity)
                            elif "SELL" in title:
                                reply += trade_handler(economy, author, gamertag, "SELL", commodity, quantity)
                                break
                    if "#ACCT INQ" in title:
                        if economy.citizens[gamertag]["Username"] != author:
                            reply += "Username/gamertag authorization failed"
                        else:
                            reply += "Balance: {0:.2f}".format(economy.citizens[gamertag]["QCE Account"])
                            reply += "\n\nCommodity|Inventory"
                            reply += "\n:---|---:"
                            for commodity in economy.prices:
                                reply += "\n{0}|{1}".format(commodity,
                                                economy.citizens[gamertag]["Inventory"][commodity])
                    if "#GRAPH" in title:
                        for commodity in economy.prices:
                            if commodity in title:
                                if commodity == "Wheat" and "Wheat Seeds" in title:
                                    pass
                                else:
                                    economy_graph.single_commodity_graph(economy, commodity)
                                    path = os.path.join(commodity + ".png")
                                    imgur = pyimgur.Imgur(IMGUR_CLIENT_ID)
                                    uploaded_image = imgur.upload_image(path, title=commodity)
                                    print(uploaded_image.link)
                                    reply += "[Graph]({0})".format(uploaded_image.link)
                                    os.remove(os.path.join(commodity + ".png"))
                    if "#BET" in title:
                        if economy.citizens[gamertag]["Username"] != author:
                            reply += "Username/gamertag authorization failed"
                        else:	
                            try:
                                bet_amount = float(submission.selftext)
                            except ValueError:
                                economy.checked_ids.append(submission.id)
                                reply += "Post text must be a number"
                            if economy.citizens[gamertag]["QCE Account"] < bet_amount:
                                reply += "Insufficient funds"
                            else:
                                fighter = ""
                                for fight in economy.fights:
                                    if fight.gladiator1 in title or fight.gladiator2 in title:
                                        if fight.gladiator1 in title:
                                            fighter = fight.gladiator1
                                        else:
                                            fighter = fight.gladiator2
                                            fight.bets.append([gamertag, fighter, bet_amount]) 
                                            economy.citizens[gamertag]["QCE Account"] -= bet_amount
                                            reply += "${0:.2f} bet placed on {1}".format(bet_amount, fighter) 
                                            break
                    economy.checked_ids.append(submission.id)			
                    if len(reply) > 1:
                        submission.add_comment(reply)
            time.sleep(300)
            print "Looking at posts"
        except:
            print "Bot Error"
            return
        
def clean_up_sub(economy):	
    print "This will remove posts from the subreddit. Are you sure?"
    if raw_input(">") in ("y", "Y", "yes", "Yes"):
        bot = praw.Reddit(user_agent = SUBREDDIT + "Mod")
        bot.login(MOD_NAME, MOD_PASSWORD)
        submissions = bot.get_subreddit(SUBREDDIT).get_new()
        for submission in submissions:
            if submission.id in economy.checked_ids:
                submission.remove()

def calc_building_cost(economy):
    width = int(raw_input("Enter building width:"))
    length = int(raw_input("Enter building length:"))
    height = int(raw_input("Enter building height:"))
    material = raw_input("Enter building material:")
    num_blocks  = (2 * length + 2 * width) * height
    materials_cost = num_blocks * economy.prices[material]
    labor_cost = num_blocks * .001
    print "Pay upon completion: ${0}".format(materials_cost + labor_cost)

def main():
    try:
        economy = pickle.load(open("economy_save.pickle", "rb"))
    except IOError:
        print "Couldn't load economy_save.pickle"
        print "Are you sure you want to start over?"
        if input(">") in ["y", "yes", "Y", "Yes"]:
            pass
        else:
            return
        economy = Economy()
        for i in range(50):		# seeds the price history for graphs
            economy.update()
    
    option_map = {"1": economy_handler,
                            "2": run_bot,
                            "3": citizen_menu,
                            "4": exchange_handler,
                            "5": gladiator_menu,
                            "6": calc_building_cost,
                            "7": economy_graph.show_graph,
                            "9":  clean_up_sub}
                            
    print """
    1) Update Economy
    2) Run Bot
    3) Citizens Menu
    4) Manage Accounts
    5) Gladiators Menu
    6) Building Cost Calculator
    7) Interactive Graph
    8) Single Commodity Graph
    9) Clean Up Subreddit
    2) Quit without saving"""
    option = raw_input("\nEnter option number:")
   
    if option == "42":
        return
    elif option == "8":
        commodity = raw_input("Enter commodity name:")
        economy_graph.single_commodity_graph(economy, commodity)
    elif option in ["1", "2", "3", "4", "5", "6", "7", "9"]: 
        option_map[option](economy)
    pickle.dump(economy, open("economy_save.pickle", "wb"))
    
    
if __name__ == "__main__":		
    main()
