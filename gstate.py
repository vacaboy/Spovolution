import pygame

class gstate():
	def __init__(self):

		self.players = [] #has all the plyaer
		self.npcs = [] #has all player except craos. note: "player" and "npc" are different classes

		self.abilities = [[],[],[[],[],[]],[],[]] #keeps track of all abilities in the game, each sublist is the abilities of the correspondend stage. the first sublist are the stage 0 abilities and so on
		#the abilities in stage 2 divide into 3 sublists, offensive, defensive and utility
		self.deadcorpses = [] #has all the dead folk
		self.log = [] #isto mantem, ao longo de cada turno, quem da dano a quem. [caster, damage, target]

		self.fonttime = pygame.font.SysFont("comicsans", 50, True)
		self.fontA = pygame.font.SysFont("mayence", 30, False, True)
		self.fontHP = pygame.font.SysFont("comicsans",20 ,False ,True)
		self.fontend = pygame.font.SysFont("mayence", 180, True)
        self.run = True


_s = None

def init():
    global _s
    if _s is not None:
        raise Exception("Initialized gstate more than once")
    _s = gstate()

def get():
    return _s

