from abilities import *
from renderable import *
        
width = 1000
height = 600
        
abilityprice = [0, 5, 10, 50] #has the price of each ability for each stage, for stage zero, the price is zero, for stage 1, the price is 5, and so on
evolveprice = [0, 20, 100, 1000] #the same but for evolving
evolveHPgain = [0, 75, 600, 2000] #HP and MaxHP gained when evolving, per stage.
evolveEXP = [0, 20, 100, 1000] #EXP needed to evolve, per stage.
evolveround = [0, 7, 20, 45] #round when everyone evolves.
passed = ability("passed", 3, 0, True, 1, "Does nothing this round", False)

circle0 = circlerenderable(380, 300, 40, (255,0,0))
circle1 = circlerenderable(480, 300, 40, (135,206,250))
circle2 = circlerenderable(580, 300, 40, (10,50,255))
circle3 = circlerenderable(680, 300, 40, (200,206,200))
circle4 = circlerenderable(780, 300, 40, (255,0,100))

#def Fireelemental(own):
 #   a = pet(owner = own, name = "Fire Elemental", color = (255,0,0), HP = 50, MaxHP = 50)
  #  a.ai = attackpet(a)
   # a.abilities.append(ability("FireElementaAttack", 3, 1, False, 2, True, "Offensive", ))
    #return a
    
    

