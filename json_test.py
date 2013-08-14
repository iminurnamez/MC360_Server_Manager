import json

class Economy(object):
    def __init__(self):
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
                                                        
example_economy = Economy()		

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, Economy):
            return super(MyEncoder, self).default(obj)

        return obj.__dict__

economy_save = json.dump(example_economy, open("economy_save.py", "w"), cls=MyEncoder)


my_instance = Economy()
my_instance.__dict__.update(json.load(open("economy_save.py", "r")))
print my_instance.citizens["RebuiltOak624"]["QCE Account"]