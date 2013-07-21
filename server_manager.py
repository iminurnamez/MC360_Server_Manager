import os
import random
import pickle
import pygame
import praw
import pyimgur
import economy_graph
import fighting

class Economy(object):
	def __init__(self):
		self.base_prices = {"Cactus": .04,
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
						"Wheat": .05,
						"Wheat Seeds": .08,}
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
						"Wheat Seeds": ["tan4"]}
						
		self.volatilities = ["Calm", "Active", "Frantic"]
		self.volatility_mods = {"Calm": 10,
								"Active": 20,
								"Frantic": 40}
		self.next_volatility = {"Calm": ["Active", "Calm", "Calm"],
								"Active": ["Calm", "Active", "Active", "Frantic"],
								"Frantic": ["Calm", "Active", "Active", "Frantic"]}
		self.volatility = "Calm"
		
		self.trends = ["Horrendous", "Weak", "Stable", "Strong", "Phenomenal"]
		self.trend_mods = {"Phenomenal": 15,
							"Strong": 10,
							"Stable": 1,
							"Weak": -5,
							"Horrendous": -10}
		self.next_trend = {"Phenomenal": ["Phenomenal", "Strong", "Strong", "Strong"],
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
														"Wheat Seeds": 0}}}
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
	sub_name = "Quadraria"
	bot_name = "QuadrarianEconomy"
	bot_password = ""
	
	bot = praw.Reddit(user_agent = bot_name)
	bot.login(bot_name, bot_password)
	text = "Economic Condition: {0}".format(economy.trend)
	text += "\n\nPrice Volatility: {0}".format(economy.volatility)
	text += "\n\nCommodity|Price|Change\n:---|---:|---:"
	for item in economy.prices:
		price = "{0:.2f}".format(economy.prices[item]).lstrip("0")
		text += "\n{0}|{1}|{2:+.4f}".format(item, price, economy.prices[item] - economy.previous_prices[item])
	text += "\n\nDisplayed prices are rounded to nearest hundredth"
	bot.submit(sub_name, "QCE Price Update", text)
		
def add_citizen(economy):
	gamertag = raw_input("Enter gamertag:")
	username = raw_input("Enter username:")
	district = raw_input("Enter district:")
	title = raw_input("Enter title:")
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
											"Wheat Seeds": 0}}
	print "Citizen added"
			
def remove_citizen(economy):
	gamertag = raw_input("Enter gamertag:")
	if gamertag in economy.citizens:
		double_check = raw_input("Are you sure you want to delete {0}?".format(gamertag))
		if double_check in ("y", "Y", "yes", "Yes"):
			del economy.citizens[gamertag]
			print "{0} has been removed".format(gamertag)
			
def change_citizenship(economy):
	gamertag = raw_input("Enter gamertag:")
	if gamertag in economy.citizens:
		new_district = raw_input("Enter new district:")
		double_check = raw_input("Are you sure you want to change {0}'s district to {1}?".format(gamertag, new_district))
		if double_check in ("y", "Y", "yes", "Yes"):
			economy.citizens[gamertag]["District"] = new_district
			print "{0} is now a citizen of {1}".format(gamertag, new_district)
			
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
			return "Transaction Completed: {0} {1} has been credited to your QCE account".format(quantity, commodity)
		else:
			return "Insufficient Funds"
	elif transaction_type == "SELL":
		if economy.citizens[gamertag]["Inventory"][commodity] >= quantity:
			economy.citizens[gamertag]["QCE Account"] += economy.prices[commodity] * quantity
			economy.citizens[gamertag]["Inventory"][commodity] -= quantity
			return "Transaction Completed: ${0:.2f} has been credited to your QCE account".format(economy.prices[commodity] * quantity)
		else:
			return "Insufficient Commodity Amount"

def exchange_handler(economy):
	gamertag = raw_input("\t\tEnter gamertag:")
		
	while True:
		option = raw_input("\t\tCurrent Account: {0}\n\
		Choose transaction type:\n\
		1) Withdrawal\n\
		2) Deopsit\n\
		3) Change gamertag\n\
		4) Display Account\n\
		9) Quit\n\t\t>".format(gamertag))
		
		if option == "1":
			commodity = raw_input("\t\tEnter \"Cash\" or Commodity name to withdraw:\n\t\t>")
			qty = int(raw_input("\t\tEnter withdrawal amount:"))
			if commodity == "Cash":
				if economy.citizens[gamertag]["QCE Account"] >= qty:
					economy.citizens[gamertag]["QCE Account"] -= qty
					print "\n\t\t${0} withdrawn from {1}'s account\n".format(qty, gamertag)
				else:
					print "Insufficient funds"
			elif commodity in economy.citizens[gamertag]["Inventory"].keys():
				if economy.citizens[gamertag]["Inventory"][commodity] >= qty:
					economy.citizens[gamertag]["Inventory"][commodity] -= qty
					print "\n\t\t{0} {1} withdrawn from {2}'s account\n".format(qty, commodity, gamertag)
				else:
					print "Insufficient commodity amount"
		
		elif option == "2":
			commodity = raw_input("\t\tEnter \"Cash\" or Commodity name to deposit\n\t\t>")
			qty = int(raw_input("\t\tEnter deposit amount:"))
			if commodity == "Cash":
				economy.citizens[gamertag]["QCE Account"] += qty
				print "\n\t\t${0} deposited to {1}'s account\n".format(qty, gamertag)
			else:
				economy.citizens[gamertag]["Inventory"][commodity] += qty
				print "\n\t\t{0} {1} deposited to {2}'s account\n".format(qty, commodity, gamertag)
			
		elif option == "3":
			gamertag = raw_input("\t\tEnter gamertag:")
			
		elif option == "4":
			print "\n\n\n\t\tBalance: ${0:.2f}\n".format(economy.citizens[gamertag]["QCE Account"])
			for commodity in economy.citizens[gamertag]["Inventory"]:
				print "\t\t{0:20}\t{1:>8}".format(commodity, economy.citizens[gamertag]["Inventory"][commodity])
				
		elif option == "9":
			return


	
	


def display_gladiator_record(economy):
	gladiator = raw_input("Enter gladiator's gamertag:")
	print "Wins: {0}  Losses: {1}".format(economy.citizens[gladiator]["Gladiator Wins"], 
			economy.citizens[gladiator]["Gladiator Losses"])
	
def gladiator_menu(economy):
	print "\n\nGladiator Options"
	print "1. Set up new fight"
	print "2. Display Gladiator Record"
	print "3. Resolve fight"
	option = raw_input("\nChoose an option:")
	
	if option == "1":
		sub_name = "Quadraria"
		bot_name = "QuadrarianEconomy"
		bot_password = ""
				
		gladiator1 = raw_input("Enter the first gladiator's gamertag:")
		gladiator2 = raw_input("Enter the second gladiator's gamertag:")
		if economy.citizens[gladiator1]["District"] == economy.citizens[gladiator2]["District"]:
			print "Gladiators are from the same district"
		else:
			bot = praw.Reddit(user_agent = bot_name)
			bot.login(bot_name, bot_password)
			fight = fighting.GladiatorFight(economy, gladiator1, gladiator2)
			economy.fights.append(fight)
			text = "{0} ".format(fight.marquee)
			text += "\n\nGladiator|W-L|Payout\n:---|:---:|---:"
			text += "\n{0}|{1}-{2}|{3:.2f}".format(gladiator1, economy.citizens[gladiator1]["Gladiator Wins"],
										economy.citizens[gladiator1]["Gladiator Losses"], fight.payouts[gladiator1])
			text += "\n{0}|{1}-{2}|{3:.2f}".format(gladiator2, economy.citizens[gladiator2]["Gladiator Wins"],
										economy.citizens[gladiator2]["Gladiator Losses"], fight.payouts[gladiator2])
			bot.submit(sub_name, "Gladiator Match", text)
	
	elif option == "2":
		display_gladiator_record(economy)
		
	elif option == "3":
		fight_map = {}
		i = 1
		for fight in economy.fights:
			fight_map[i] = fight
			print "{0}. {1}".format(i, fight.marquee)
			i += 1
		fight_num = int(raw_input("Choose fight to resolve:"))
		fight_map[fight_num].resolve_fight(economy)
		
def run_bot(economy):
	sub_name = "Quadraria"
	bot_name = "QuadrarianEconomy"
	bot_password = "" 
	imgur_client_id = ""
	
	bot = praw.Reddit(user_agent = bot_name)
	bot.login(bot_name, bot_password)
	submissions = bot.get_subreddit(sub_name).get_new()
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
						reply += "\n{0}|{1}".format(commodity, economy.citizens[gamertag]["Inventory"][commodity])
			if "#GRAPH" in title:
				for commodity in economy.prices:
					if commodity in title:
						if commodity == "Wheat" and "Wheat Seeds" in title:
							pass
						else:
							economy_graph.single_commodity_graph(economy, commodity)
							path = os.path.join(commodity + ".png")
							imgur = pyimgur.Imgur(imgur_client_id)
							uploaded_image = imgur.upload_image(path, title=commodity)
							print(uploaded_image.link)
							reply += "[Graph]({0})".format(uploaded_image.link)
							os.remove(os.path.join(commodity + ".png"))
			if "#BET" in title:
				if economy.citizens[gamertag]["Username"] != author:
					reply += "Username/gamertag authorization failed"
				else:	
					try:
						bet_amount = int(submission.selftext)
					except ValueError:
						economy.checked_ids.append(submission.id)
						reply += "Post text must be a whole number"
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
								reply += "${0} bet placed on {1}".format(bet_amount, fighter) 
								break
			
			economy.checked_ids.append(submission.id)			
			if len(reply) > 1:
				submission.add_comment(reply)

def clean_up_sub(economy):
	sub_name = "Quadraria"
	mod_name = "iminurnamez"
	mod_password = ""
	
	bot = praw.Reddit(user_agent = sub_name + "Mod")
	bot.login(mod_name, mod_password)
	submissions = bot.get_subreddit(sub_name).get_new()
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
		economy = Economy()
	
	option = int(raw_input("\n\n\n1) Update Economy\n\n2) Draw Graph\n\n3) Single Commodity Graph\n\n4) \
Run Bot\n\n5) Manage Citizens\n\n6) Manage Accounts\n\n7) Building Cost Calculator\n\n8) Clean Up Sub\n\n9) Gladiator options\n\nEnter option number:"))
	if option == 1:
		economy_handler(economy)
	elif option == 2:
		economy_graph.show_graph(economy)
	elif option == 3:
		commodity = raw_input("Enter commodity name:")
		economy_graph.single_commodity_graph(economy, commodity)
	elif option == 4:
		run_bot(economy)
	elif option == 5:
		citizen_option = raw_input("\n\t\tChoose an option\n\t\t1) Add citizen\n\t\t2) Remove citizen\n\t\t")
		if citizen_option == "1":
			add_citizen(economy)
		elif citizen_option == "2":
			remove_citizen(economy)
	elif option == 6:
		exchange_handler(economy)
	elif option == 7:
		calc_building_cost(economy)
	elif option == 8:
		if raw_input("This will remove posts from the subreddit. Are you sure?") in ("y", "Y", "yes", "Yes"):
			clean_up_sub(economy)
	elif option == 9:
		gladiator_menu(economy)
	pickle.dump(economy, open("economy_save.pickle", "wb"))

if __name__ == "__main__":		
	main()
