
def calc_win_percentage(wins, losses):
	total = float(wins) + losses
	try:
		win_percentage = float(wins) / total
	except ZeroDivisionError:
		win_percentage = .5
	if win_percentage == 0:
		win_percentage = .1
	return win_percentage

class GladiatorFight(object):
	def __init__(self, economy, gladiator1, gladiator2):
		self.gladiator1 = gladiator1
		self.gladiator2 = gladiator2
		self.gladiators = [gladiator1, gladiator2]
		self.marquee = "{0} vs {1}".format(self.gladiator1, self.gladiator2)
		self.bets = []
		self.payouts = {}
		self.calc_odds(economy)
		
	def calc_odds(self, economy):
		glad1_win_rate = calc_win_percentage(economy.citizens[self.gladiator1]["Gladiator Wins"],
												economy.citizens[self.gladiator1]["Gladiator Losses"])
		glad2_win_rate = calc_win_percentage(economy.citizens[self.gladiator2]["Gladiator Wins"],
												economy.citizens[self.gladiator2]["Gladiator Losses"])
		print glad1_win_rate
		print glad2_win_rate
		total = glad1_win_rate + glad2_win_rate
		self.payouts[self.gladiator1] = total/glad1_win_rate
		self.payouts[self.gladiator2] = total/glad2_win_rate
	
	def add_bet(self, bettor_gamertag, pick_gamertag, amount):
		self.bets.append([bettor_gamertag, pick_gamertag, amount])
	
	def process_bets(self, economy):
		for bet in self.bets:
			if bet[1] == self.winner:
				win_amount = bet[2] * self.payouts[self.winner]
				economy.citizens[bet[0]]["QCE Account"] += win_amount
			self.bets.remove(bet)
	
	def resolve_fight(self, economy):
		print "1. {0}".format(self.gladiator1)
		print "2. {0}".format(self.gladiator2)
		winner_choice = raw_input("Enter the winner's number:")
		if winner_choice == "1":
			self.winner = self.gladiator1
			self.loser = self.gladiator2
		elif winner_choice == "2":
			self.winner = self.gladiator2
			self.loser = self.gladiator1
		economy.citizens[self.winner]["Gladiator Wins"] += 1
		economy.citizens[self.loser]["Gladiator Losses"] += 1
		print "Gladiator records updated"
		self.process_bets(economy)
		economy.fights.remove(self)
		
	
	
