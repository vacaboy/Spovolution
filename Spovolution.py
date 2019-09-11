#teste
import random as R
import sys
import pygame


from globals import *
from creature import player, npc, deadcorpse
#from creature import *
from abilities import *
from state import *
from simulation import simulation
from aicomponent import *

import gstate

pygame.init()
gstate.init()

#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen = pygame.display.set_mode((width, height))
#screen = pygame.display.set_mode((200, 60))

#abilities:
abilities = gstate.get().abilities

abilities[0].append(ability("Tackle",0, 1, False, 2, True, text = "Deals 2 damage", abilitytype =  "Offensive"))
abilities[0].append(ability("Double Edged Sword",0, 1, False, 2, True,"Deals 3 damage and 2 to caster", "Offensive"))
abilities[0].append(ability("chill",0, 0, True, 2, False,"heal 2 damage" , "Defensive"))

abilities[1].append(ability("Uncertain Footing",1, 1, False, 3,True,"deals 7 damage if noone attacks you this round", "Offensive"))
abilities[1].append(ability("Stand Tall",1, 1, False, 3, True,"deals 7 damage if at least 1 attack target you this round", "Offensive"))
abilities[1].append(ability("QuickPoke",1, 3, False, 1, True,"deals 1 damage to every enemy", "Offensive"))
abilities[1].append(ability("Think",1, 0, False, 3, False,"Can i... think...?", "Utility"))


abilities[2][0].append(ability("Spear Throw",2, 1,False, 2, True,"deals 3d12 damage. 55% accuracy", "Offensive"))
abilities[2][0].append(ability("Kick",2, 1,False, 2, True,"deals 2d10 damage", "Offensive"))
abilities[2][0].append(ability("Punch",2, 1,False, 2, True,"deas 9 damage", "Offensive"))
abilities[2][0].append(ability("On The Edge",2, 1,False, 3, True,"deals 30 damage if every offensive ability used this turn targets you.", "Offensive"))
abilities[2][0].append(ability("Blood Drain",2, 1,False, 2, True,"deals 2d8 damage. 75% accuracy. caster heals the same amount as the damage deals. \ncooldown: 1", "Offensive", cooldown = 1))
abilities[2][0].append(ability("Headbutt",2, 1,False, 2, True,"deals 2d12 damage. there is a 10% chance the caster paralyzes himself", "Offensive"))
abilities[2][0].append(ability("Everyone... GET IN HERE!",2, 1, False, 3, True,"deals Xd15 where X is the number of offensive abilities targeting you this round", "Offensive"))
abilities[2][0].append(ability("From The Shadows" ,2, 1, False, 3, True,"deals 6d6 if noone targets you this round", "Offensive"))
abilities[2][0].append(ability("Unleash The Power" ,2, 2, False, 2, True,"channel 4, cooldown 2 \ndeals 4d14 damage to 2 targets", "Offensive", cooldown = 2, channel = 4))

abilities[2][1].append(ability("Rock Solid",2, 0,True, 1, False,"cooldown 5 \nYou take no damage this round ", "Defensive", cooldown = 5))
abilities[2][1].append(ability("Refreshing Waters",2, 0,True, 2, False,"cooldown 1 \nheal 12", "Defensive", cooldown = 1))
abilities[2][1].append(ability("Regenerate",2, 0,True, 3, False,"cooldown 2 \nfor the next 1d10 rounds, heal 3 ", "Defensive", cooldown = 2))
abilities[2][1].append(ability("Shocking Response",2, 0,True, 4, False,"cooldown 2 \nFor the next 2 rounds, attacks agains you deal 5 damage to the attacker and they have a 10% chance to be paralyzed", "Defensive", cooldown = 2))
abilities[2][1].append(ability("Dodge",2, 0,True, 1, False,"attacks against you have 70% less accuracy this round", "Defensive"))
abilities[2][1].append(ability("Flight",2, 0,True, 4, False, "coodlown 5 \nfor the next 1d3 rounds, attacks against you have 80% less chance ","Defensive", cooldown = 5))
abilities[2][1].append(ability("Nature's Call",2, 0,True, 4, False,"cooldown 2 \n for the next 1d10 rounds, you take 3 less damage", "Defensive", cooldown = 2))
abilities[2][1].append(ability("Web Cacoon",2, 0,True, 1, False,"cooldown 3 \nthis round and for the next 3, attacks against you reduce the attacker next round's accuracy by 50%", "Defensive", cooldown = 3))
abilities[2][1].append(ability("High Jump",2, 0,True, 1, False, "cooldown 4 \nattacks made against you this turn miss. you are immobilized and must use an offensive ability next turn","Defensive", cooldown = 4))

abilities[2][2].append(ability("Lullaby",2, 3,False, 3, False,"cooldown 5 \nevery enemy has a 50% chance to fall asleep", "Utility", cooldown = 5))
abilities[2][2].append(ability("Fight Stance",2, 0,True, 3, False,"cooldown 2 \nfor the next 1d6 rounds, you deal 7 more damage", "Utility", cooldown = 2))
#abilities[2][2].append(ability("Unleash the Chains",2, 0,True, 3, False," ", "Utility"))
abilities[2][2].append(ability("Limitless",2, 0,True, 3, False, "usable once \nnext turn you deal double damage","Utility", cooldown = 999))
abilities[2][2].append(ability("Intimidate",2, 3,False, 4, False,"cooldown 1 \nevery enemy, for the next 1d6 rounds, deals 5 less damage", "Utility", cooldown = 1))
abilities[2][2].append(ability("No Pain, No Gain",2, 0,True, 1, False,"cooldown 1 \nthis round and the next, you gain double EXP", "Utility", cooldown = 1))
abilities[2][2].append(ability("Reflective Mirror",2, 0, False, 1, False,"usable once \nevery ability targeting you this round is refleted to the caster.", "Utility", cooldown = 999))
#abilities[2][2].append(ability("Target Enemy",2, 3, False, 3, False," ", "Utility", cooldown = 999))
#abilities[2][2].append(ability("Taunt",2, 3, False, 3, False," ", "Utility", cooldown = 0))
abilities[2][2].append(ability("Wonder",2, 0, False, 4, False,"I wonder what this does...", "Utility"))




#fire:
abilities[3][0][0].append(ability("Fire Blast", 3, 1, False, 2, True,"cooldown 1 \ndeal 45 damage, gain a fire orb", "Offensive", cooldown = 1, element = 0, proficiencyneeded = 5, proficiencygiven = [1.2,0,0,0,0]))
abilities[3][0][0].append(ability("The Floor Is Lava", 3, 3, False, 4, False,"cooldown:4, 2 fire orb used. \nfor the next 4 rounds, every enemy takes 10 damage", "Offensive", cooldown = 4, element = 0, orbs = [2,0,0,0,0],  proficiencygiven = [2,0,0,0,0]))
abilities[3][0][0].append(ability("Fire Rain", 3, 3, False, 2, True,"6 fire orbs used \neach enemy has a 70% chance to take 60 damage", "Offensive", element = 0, orbs = [6,0,0,0,0], proficiencyneeded = 10,  proficiencygiven = [3.5,0,0,0,0]))
abilities[3][0][0].append(ability("Lava Burst", 3, 1, False, 2, True,"1 fire orb used \nwith a 60% chance, the target takes 60 damage and is immobilized", "Offensive", element = 0, orbs = [1,0,0,0,0], proficiencyneeded = 10,  proficiencygiven = [1.5,0,0,0,0]))
abilities[3][0][0].append(ability("Explosion", 3, 3, False, 2, True,"4 fire orbs used \n3 targets take 50 damage and there is a 50% chance they take 50 more damage", "Offensive", element = 0, orbs = [4,0,0,0,0], proficiencyneeded = 25,  proficiencygiven = [6,0,0,0,0]))
abilities[3][0][0].append(ability("Living Inferno", 3, 5, False, 2, True,"channel 3, 5 fire orbs used each channel \nup to 5 targets take 250 damage and 50 more damage for 1+1d4 rounds", "Offensive", channel = 3, element = 0, orbs = [5,0,0,0,0], proficiencyneeded = 50,  proficiencygiven = [10,0,0,0,0]))
abilities[3][0][0].append(ability("Cold Flame", 3, 1, False, 2, True,"3 fire orbs and 1 ice orb used \ndeal 45 damage and the target is iced", "Offensive", element = 0, orbs = [3,1,0,0,0], proficiencyneeded = 10,  proficiencygiven = [4,1.5,0,0,0]))
abilities[3][0][0].append(ability("Mystical Flame", 3, 1, False, 2, True,"3 fire orbs and 1 mind orb used \ndeal 45 damage and there is a 60% chance of the target falling asleep", "Offensive", element = 0, orbs = [3,0,0,0,1], proficiencyneeded = 10,  proficiencygiven = [4,0,0,0,1.5]))
abilities[3][0][0].append(ability("Corrosive Flame", 3, 1, False, 2, True,"3 fire orbs and 1 necro orb used \ntarget loses 80 MaxHP", "Offensive", element = 0, orbs = [3,0,0,1,0], proficiencyneeded = 10,  proficiencygiven = [4,0,0,1.5,0]))
abilities[3][0][0].append(ability("Flame Of Death", 3, 2, False, 2, False,"7 fire orbs and 3 necro orbs used \ntarget loses 50 MaxHP for the next 2+1d8 rounds", "Offensive", element = 0, orbs = [7,0,0,3,0], proficiencyneeded = 30,  proficiencygiven = [8,0,0,3,0]))
abilities[3][0][0].append(ability("Forgetfull Combustion", 3, 4, False, 2, True,"7 fire orbs and 3 mind orbs used \nup to 4 targets take 60 damage and forget(6)", "Offensive", element = 0, orbs = [7,0,0,0,3], proficiencyneeded = 30,  proficiencygiven = [8,0,0,0,3]))
abilities[3][0][0].append(ability("Fire Elemental", 3, 0, False, 4, False,"channel 2. 2 orbs per use. \nYou summon a Fire elemental to fight at your side. Each turn, it deals 30 damage to a random target and gives you a fire orb. It has 50 HP", "Offensive", channel = 2, element = 0, orbs = [2,0,0,0,0], proficiencyneeded = 20,  proficiencygiven = [2,0,0,0,0]))

abilities[3][0][1].append(ability("Wall Of Fire", 3, 1, True, 1, False, "1 fire orb used \nfor this and the next 1+1d4 rounds, attacks against the target have 30% less accuracy and hurt the attacker for 15 damage. Attacks the target makes have 50% less accuracy", "Defensive", element = 0, orbs = [1,0,0,0,0], proficiencyneeded = 5, proficiencygiven = [1.4,0,0,0,0]))
abilities[3][0][1].append(ability("Healing Flames", 3, 0, True, 3, False, "cooldown 2 \nHeal 30 HP, gain a fire orb", "Defensive", element = 0,proficiencyneeded = 25, proficiencygiven = [1.4,0,0,0,0], cooldown = 2))
abilities[3][0][1].append(ability("Fiery Spirit", 3, 0, True, 3, False, "3 fire orbs used \nfor this and the next 1+1d8 rounds, you cant be paralyzed, iced or put to sleep", "Defensive", orbs = [3,0,0,0,0], element = 0,proficiencyneeded = 10, proficiencygiven = [3,0,0,0,0]))
abilities[3][0][1].append(ability("Fire Jet", 3, 0, True, 1, False, "coolown 1. 1 fire orbs used \nAttacks targeting you this turn miss. You are Immobilized, Attacks made against you next turn deal 10 damage to the attacker", "Defensive", element = 0, orbs = [1,0,0,0,0], proficiencyneeded = 20, proficiencygiven = [3,0,0,0,0], cooldown = 1))

abilities[3][0][2].append(ability("Energy Consumption", 3, 0, True, 1, False, "cooldown 5. 5 fire orbs used \nevery elemental offensive ability targeting you this round doesn't target you anymore, and you gain orb equal to the cost of those abilities", "Utility", element = 0, orbs = [5,0,0,0,0],proficiencyneeded = 100, proficiencygiven = [20,0,0,0,0], cooldown = 5))
abilities[3][0][2].append(ability("Blue Flame", 3, 0, True, 3, False, "usable once. 1 fire orbs used per cast. channel 3  \nYour fire turns blue. For the rest of the game, you deal 1.5 damage.", "Utility", element = 0,channel = 3, orbs = [1,0,0,0,0],proficiencyneeded = 50, proficiencygiven = [3.3,0,0,0,0], cooldown = 999))
abilities[3][0][2].append(ability("Absolute Focus", 3, 0, True, 3, False, "cooldown 4.\nYou get 7 random orbs.", "Utility", element = 0, orbs = [0,0,0,0,0],proficiencyneeded = 1, proficiencygiven = [0,0,0,0,0], cooldown = 4))

#Ice:
abilities[3][1][0].append(ability("Ice Blast", 3, 1, False, 2, True,"cooldown 4 \ndeal 10 damage, there is a 70% cheance to freeze the target. gain two ice orb", "Offensive", cooldown = 4, element = 1, proficiencyneeded = 5, proficiencygiven = [0,1.2,0,0,0]))
abilities[3][1][0].append(ability("Ice Elemental", 3, 0, False, 4, False,"7 ice orbs used. \nYou summon a Ice elemental to fight at your side. Each turn, it deals 10 damage to a random target, freezing them and giving you a ice orb. It has 70 HP", "Offensive", element = 1, orbs = [0,7,0,0,0], proficiencyneeded = 40,  proficiencygiven = [0,3,0,0,0]))
abilities[3][1][0].append(ability("Ice Meteor", 3, 2, False, 2, True,"2 ice orbs used \ndeal 40 damage to 2 targets, there is a 20% cheance to freeze them", "Offensive", element = 1, proficiencyneeded = 5, proficiencygiven = [0,1.4,0,0,0], orbs = [0,2,0,0,0]))
abilities[3][1][0].append(ability("Ice Hammer", 3, 1, False, 2, True,"cooldown 2 \ndeal 10 damage to target and freeze it. Gain a ice orb", "Offensive", element = 1, proficiencyneeded = 50, proficiencygiven = [0,2.5,0,0,0]))
abilities[3][1][0].append(ability("Frost", 3, 1, False, 2, False,"3 ice orbs used \nFreeze target 3 times.", "Offensive", element = 1, proficiencyneeded = 10, proficiencygiven = [0,1.3,0,0,0], orbs = [0,3,0,0,0]))
abilities[3][1][0].append(ability("Rotting Icicles", 3, 0, False, 3, True,"1 ice orbs and 1 necro orb used \nfor the next 1+1d4 rounds, a random target will lose 20 MaxHP and has a 50% chance to freeze.", "Offensive", element = 1, proficiencyneeded = 20, proficiencygiven = [0,2,0,1,0], orbs = [0,3,0,1,0]))

abilities[3][1][1].append(ability("Ice Wall", 3, 1, True, 1, False, "1 ice orb used \nfor this and the next 1+1d4 rounds, attacks against the target have 70% chance to freeze the attacker. Attacks the target makes freeze the target ","Defensive", element = 1, orbs = [0,1,0,0,0], proficiencyneeded = 5, proficiencygiven = [0,1.4,0,0,0]))
abilities[3][1][1].append(ability("Ice Tomb", 3, 0, True, 1, False, "7 ice orb used. usable once \nYou become encased in a Ice Tomb. starting this rounds, you regain 30 HP per round and gain 30 EXP per round. You are also paralyed while in this tomb. And Damage you receive is dealt to the tomb instead of you. The Ice tomb has 100 HP.","Defensive", element = 1, orbs = [0,7,0,0,0], proficiencyneeded = 50, proficiencygiven = [0,10,0,0,0], cooldown = 999))
abilities[3][1][1].append(ability("Icy Skin", 3, 0, True, 3, False, "2 iced orbs per use. channel 2. one use only\nFor the rest of the game, attack against you deal 5 less damage. Your freeze stacks go to zero and henever you get frozen, you don't and you gain 10 HP instead.", "Defensive", orbs = [0,2,0,0,0], element = 1,channel = 2, cooldown = 999,proficiencyneeded = 50, proficiencygiven = [0,3.5,0,0,0]))
abilities[3][1][1].append(ability("Ice Armor", 3, 0, True, 3, False, "2 iced orbs per use. channel 2 cooldown 7\nYou create a suit of armor that has 150 HP. Whenever you take damage. the armor takes it instead.", "Defensive", orbs = [0,2,0,0,0], element = 1,channel = 2, cooldown = 7,proficiencyneeded = 20, proficiencygiven = [0,2,0,0,0]))
abilities[3][1][1].append(ability("Predictive Ice", 3, 0, True, 1, False, "3 ice orb and 1 mind orb used.\nThis round, attacks amde against you deal 20 less damage and freeze the atacker. If there was no attack made against you this turn, then you deal 10 damage and freeze all enemies.","Defensive", orbs = [0,3,0,0,1], element = 1, proficiencyneeded = 15, proficiencygiven = [0,3,0,0,1]))

abilities[3][1][2].append(ability("Energy Consumption", 3, 0, True, 1, False, "cooldown 5. 5 ice orbs used \nevery elemental offensive ability targeting you this round doesn't target you anymore, and you gain orb equal to the cost of those abilities", "Utility", element = 1, orbs = [0,5,0,0,0],proficiencyneeded = 100, proficiencygiven = [20,0,0,0,0], cooldown = 5))
abilities[3][1][2].append(ability("Absolute Focus", 3, 0, True, 3, False, "cooldown 4.\nYou get 7 random orbs.", "Utility", element = 1, orbs = [0,0,0,0,0],proficiencyneeded = 1, proficiencygiven = [0,0,0,0,0], cooldown = 4))
abilities[3][1][2].append(ability("True Ice", 3, 0, True, 3, False, "usable once. 2 ice orbs used per cast. channel 3  \nuse 2 ice orbs. channel 3. Your ice is colder than cold itself, when an ability you cast freezes someone, it has a 33% chance to Ice him.", "Utility", element = 1,channel = 3, orbs = [0,2,0,0,0],proficiencyneeded = 60, proficiencygiven = [0,3.5,0,0,0], cooldown = 999))
abilities[3][1][2].append(ability("Icy Floor", 3, 0, True, 3, False, "4 ice orbs \nfor the next 2+1d4 rounds, everyone except you has 50% less accuracy.", "Utility", element = 1,orbs = [0,4,0,0,0],proficiencyneeded = 30, proficiencygiven = [0,2,0,0,0]))
abilities[3][1][2].append(ability("Absolute Zero", 3, 0, True, 3, False, "5 ice orbs per use. channel 2 \nThe air itself becomes frigid. Everything except you receives 15 freeze stacks", "Utility", element = 1,channel = 2,orbs = [0,5,0,0,0],proficiencyneeded = 70, proficiencygiven = [0,2.5,0,0,0]))
abilities[3][1][2].append(ability("Icy Wave", 3, 0, True, 3, False, "2 ice orbs \nevery enemy has a 60% chance of being frozen and a 20% of being iced.", "Utility", element = 1,orbs = [0,2,0,0,0],proficiencyneeded = 10, proficiencygiven = [0,1.2,0,0,0]))
abilities[3][1][2].append(ability("Cool Down", 3, 0, True, 3, False, "4 ice orbs \neveryone that has a freeze stack, gains another 3 freeze stacks", "Utility", element = 1,orbs = [0,4,0,0,0],proficiencyneeded = 13, proficiencygiven = [0,1.4,0,0,0]))
abilities[3][1][2].append(ability("Criostasis", 3, 1, True, 3, False, "4 ice orbs, cooldown 5 \nTarget is Paralyzed.", "Utility", element = 1,orbs = [0,4,0,0,0],proficiencyneeded = 23, proficiencygiven = [0,1.5,0,0,0], cooldown = 5))
abilities[3][1][2].append(ability("Living Ice", 3, 0, True, 3, False, "1 ice orb and 1 mind orb, usable once \nNext turn, the first ability you use from the Ice element is cast twice. The second cast doesn't use orbs.", "Utility", element = 1,orbs = [0,1,0,0,1],proficiencyneeded = 70, proficiencygiven = [0,2,0,0,2], cooldown = 999))


#_________________________________________________________________________________________________________________________________________________________________
#starter packs:
starterpacks = gstate.get().starterpacks

starterpacks[0].append(ability("Fire Burst", 3, 1, False, 2, True,"deal 35 damage. gain a fire orb", "Offensive", element = 0,  proficiencygiven = [1,0,0,0,0]))
starterpacks[0].append(ability("Fire Shield", 3, 0, True, 1, False,"this round, you receive 10 less damage from attakcs and you deal 5 damage to the attacker. gain a fire orb", "Defensive", element = 0,  proficiencygiven = [1,0,0,0,0]))
starterpacks[0].append(ability("Fire Charge", 3, 0, True, 2, False,"gain 2 fire orbs", "Utility", element = 0,  proficiencygiven = [1,0,0,0,0]))

starterpacks[1].append(ability("Icicle Spike", 3, 1, False, 2, True,"deal 25 damage and there is a 50% chance to freeze the target. gain a ice orb", "Offensive", element = 1,  proficiencygiven = [0,1,0,0,0]))
starterpacks[1].append(ability("Ice Shield", 3, 0, True, 1, False,"this round, you receive 10 less damage from attacks and the attacker has a 50% chance of being frozen, gain a ice orb", "Defensive", element = 1,  proficiencygiven = [0,1,0,0,0]))
starterpacks[1].append(ability("Ice Charge", 3, 0, True, 2, False,"gain 2 ice orbs", "Utility", element = 1,  proficiencygiven = [0,1,0,0,0]))

starterpacks[2].append(ability("Discharge", 3, 1, False, 2, True," ", "Offensive", element = 2,  proficiencygiven = [0,0,1,0,0]))
starterpacks[2].append(ability("Wind Shield", 3, 0, True, 1, False," ", "Defensive", element = 2,  proficiencygiven = [0,0,1,0,0]))
starterpacks[2].append(ability("Storm Charge", 3, 0, True, 2, False,"gain 2 tempest orbs", "Utility", element = 2,  proficiencygiven = [0,0,1,0,0]))

starterpacks[3].append(ability("Necrotic Wave", 3, 1, False, 2, True,"target loses 20 MaxHP and you heal 10. gain a necro orb", "Offensive", element = 3,  proficiencygiven = [0,0,0,1,0]))
starterpacks[3].append(ability("Paralyzing Gaze", 3, 1, False, 3, False,"there is a 20% chance you paralyzed the target, gain a necro orb", "Utility", element = 3,  proficiencygiven = [0,0,0,1,0]))
starterpacks[3].append(ability("Necrotic Charge", 3, 0, True, 2, False,"gain 2 necro orbs", "Utility", element = 3,  proficiencygiven = [0,0,0,1,0]))

starterpacks[4].append(ability("Mind Burst", 3, 1, False, 2, True,"target takes 25 damage and there isa 40% chance he forgets(2), gain a mind orb", "Offensive", element = 4,  proficiencygiven = [0,0,0,0,1]))
starterpacks[4].append(ability("Dull Mind", 3, 1, False, 3, False,"there is a 20% chance the target falls asleep. gain a mind orb", "Utility", element = 4,  proficiencygiven = [0,0,0,0,1]))
starterpacks[4].append(ability("Mind Charge", 3, 0, True, 2, False,"gain 2 mind orbs","Utility", element = 4,  proficiencygiven = [0,0,0,0,1]))
#______________________________________________________________________________________________________________________________________________________________________
#buffs:
buffs = gstate.get().buffs

buffs[1][1].append(buff("Double Damage", "Blessing", "Condition", "You deal double damage for 6 rounds", duration = 6))
buffs[1][1].append(buff("Lifesteal", "Blessing", "Condition", "For Life: you have 10% lifesteal", value = 0.1, duration = 999))
buffs[1][1].append(buff("Take Damage", "Curse", "Condition", "For Life: you will receive 3 damage per round.", value = 3, duration = 999))
buffs[1][1].append(buff("Heal Modifier", "Curse", "Condition", "For Life: Heal against you are halfed", value = 0.5, duration = 999))
buffs[1][1].append(buff("More Experience", "Blessing", "Condition", "For Life: you will receive 20% more experience", value = 1.2, duration = 999))
buffs[1][1].append(buff("More Experience", "Curse", "Condition", "For Life: you will receive a 20% less experience", value = 0.8, duration = 999))
buffs[1][1].append(buff("Less Damage", "Curse", "Condition", "For Life: you will Deal 5 less damage", value = 5, duration = 999))
buffs[1][1].append(buff("More Damage", "Blessing", "Condition", "For Life: you will Deal 5 More damage", value = 5, duration = 999))


buffs[1][0].append(buff("Heal", "Blessing", "Condition", "heal 10 HP next round", value = 10, duration = 1))
buffs[1][0].append(buff("Damage", "Curse", "Condition", "take 10 damage next turn", value = 10, duration = 1))
buffs[1][0].append(buff("Less Damage", "Curse", "Condition", "For life: You will deal 2 less damage.", value = 2, duration = 999))
buffs[1][0].append(buff("More Damage", "Blessing", "Condition", "For life: You will deal 2 more damage.", value = 2, duration = 999))
buffs[1][0].append(buff("More Experience", "Blessing", "Condition", "For 3 turns, you will receive double experience", value = 2, duration = 3))
buffs[1][0].append(buff("More Experience", "Curse", "Condition", "For 3 turns, you will receive half experience", value = 0.5, duration = 3))
buffs[1][0].append(buff("Double Damage", "Blessing", "Condition", "You deal double damage next round", duration = 1))
buffs[1][0].append(buff("More Damage", "Blessing", "Condition", "For the next 2 rounds, you deal 10 extra damage", value = 10, duration = 2))
buffs[1][0].append(buff("Less Damage", "Curse", "Condition", "For the next 2 rounds, you deal 10 less damage", value = 10, duration = 2))
buffs[1][0].append(buff("Become Paralyzed", "Curse", "Condition", "For life: there is a 1% chance you get paralyzed at the beginning of the round", value = 0.01, duration = 999))


buffs[2][1].append(buff("Double Damage", "Blessing", "Condition", "You deal double damage for 6 rounds", duration = 6))
buffs[2][1].append(buff("Lifesteal", "Blessing", "Condition", "For Life: you have 10% lifesteal", value = 0.1, duration = 999))
buffs[2][1].append(buff("Take Damage", "Curse", "Condition", "For Life: you will receive 6 damage per round.", value = 6, duration = 999))
buffs[2][1].append(buff("Heal Modifier", "Curse", "Condition", "For Life: Heal against you are halfed", value = 0.5, duration = 999))
buffs[2][1].append(buff("More Experience", "Blessing", "Condition", "For Life: you will receive 20% more experience", value = 1.2, duration = 999))
buffs[2][1].append(buff("More Experience", "Curse", "Condition", "For Life: you will receive a 20% less experience", value = 0.8, duration = 999))
buffs[2][1].append(buff("Less Damage", "Curse", "Condition", "For Life: you will Deal 10 less damage", value = 10, duration = 999))
buffs[2][1].append(buff("More Damage", "Blessing", "Condition", "For Life: you will Deal 10 More damage", value = 10, duration = 999))


buffs[2][0].append(buff("Heal", "Blessing", "Condition", "heal 50 HP next round", value = 50, duration = 1))
buffs[2][0].append(buff("Damage", "Curse", "Condition", "take 50 damage next turn", value = 50, duration = 1))
buffs[2][0].append(buff("Less Damage", "Curse", "Condition", "For life: You will deal 5 less damage.", value = 5, duration = 999))
buffs[2][0].append(buff("More Damage", "Blessing", "Condition", "For life: You will deal 5 more damage.", value = 5, duration = 999))
buffs[2][0].append(buff("More Experience", "Blessing", "Condition", "For 3 turns, you will receive double experience", value = 2, duration = 3))
buffs[2][0].append(buff("More Experience", "Curse", "Condition", "For 3 turns, you will receive half experience", value = 0.5, duration = 3))
buffs[2][0].append(buff("Double Damage", "Blessing", "Condition", "You deal double damage next round", duration = 1))
buffs[2][0].append(buff("More Damage", "Blessing", "Condition", "For the next 2 rounds, you deal 30 extra damage", value = 30, duration = 2))
buffs[2][0].append(buff("Less Damage", "Curse", "Condition", "For the next 2 rounds, you deal 20 less damage", value = 20, duration = 2))
buffs[2][0].append(buff("Become Paralyzed", "Curse", "Condition", "For life: there is a 1% chance you get paralyzed at the beginning of the round", value = 0.01, duration = 999))




#_________________________________________________________________________________________________________________________________________________________________
gstate.get().system = npc(0 ,0, "system", (255,0,0))

craos = player(375, 450, "craos",(255, 0, 255))
craos.ai = playeraicomponent(craos)
craos.owner = gstate.get().system

robly18 = npc(375, 150, "robly18")
robly18.ai = attackwhoattackedme(robly18)
#robly18.ai = randomaicomponent(robly18)
robly18.owner = gstate.get().system

tavos = npc(670,150, "tavos")
tavos.ai = randomaicomponent(tavos)
tavos.owner = gstate.get().system

tomis = npc(670, 450, "tomis")
tomis.ai = randomaicomponent(tomis)
tomis.owner = gstate.get().system

gstate.get().craos = craos

gstate.get().players = [craos, robly18, tavos, tomis]
gstate.get().npcs = [robly18, tavos, tomis]
gstate.get().availabletargets = [craos, robly18, tavos, tomis]

gstate.get().system = npc(0 ,0, "system", (255,0,0))

gstate.get().simulation = simulation()


#roundphase = chooseability(1, 1)
#roundphase = chooseability(6, 1)
roundphase = chooseability(19, 2)
print("round: 1")

#______________________________________________________________________________________________________________________________________________________________________
global run
#main loop
gstate.get().run = True
while gstate.get().run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gstate.get().run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: #nao sei como ver se se clicou no lado esquerdo ou direito do rato... o lado esquerdo é 1 e o lado esquerdo é 3
                
                roundphase = roundphase.receiveevent(event)

            elif event.button == 3:
                print(str(event.pos))
                roundphase = roundphase.receiveevent1(event, screen)
                
        if event.type == pygame.KEYDOWN:
                
                
            if event.key == pygame.K_DELETE:
                gstate.get().run = False
##            elif event.key == pygame.K_g:
##                roundphase.gainabilityforfree(craos)
            elif event.key == pygame.K_n:
                for npc in gstate.get().npcs:
                    print(npc.name)
            elif event.key == pygame.K_a:
                print("clicaste a para ver as habilidades de toda a gente.")
                for player in gstate.get().players:
                    print(player.name)
                    for a in player.abilities:
                        print(a.name)
                    print()
            elif event.key == pygame.K_l:
                for i in gstate.get().log:
                    print(str(i))
            elif event.key == pygame.K_c:
                for c in gstate.get().deadcorpses:
                    print(c.name)


                
            elif event.key == pygame.K_t:
                tomis.abilities = tomis.abilities[1:]
                tomis.abilities.append(ability("Unleash The Power" ,2, 2, False, 2, True, "Offensive", cooldown = 2, channel = 4))
            elif event.key == pygame.K_y:
                tomis.abilities = tomis.abilities[1:]        
                
            elif event.key == pygame.K_v:
                for p in gstate.get().availabletargets:
                    print(p.name)
                print(" pets: " + str([ i.name for i in gstate.get().craos.pets]))
                print([i.HP for i in gstate.get().craos.pets])
                    
            elif event.key == pygame.K_b:
                print()
                print("decisionlist:")
                for d in gstate.get().decisionlist:
                    print(d[0].name + " , " + d[1].name + " , " + str([i.name for i in d[2]]))
                    
            elif event.key == pygame.K_i: #info
                for p in gstate.get().players:
                    print(p.name + " , " + " proficiencies: " + str(p.proficiencies) + " , freezestacks: " + str(p.freezestacks) + " , " + str(p.orbs))
            elif event.key == pygame.K_p:
                for p in gstate.get().players:
                    print(p.name + " , " + " dodge: " + str(p.dodge))
                    
            elif event.key == pygame.K_o:
                for a in gstate.get().abilities[2][0]:
                    gstate.get().craos.abilities.append(a)
            elif event.key == pygame.K_d:
                for a in gstate.get().abilities[2][1]:
                    gstate.get().craos.abilities.append(a)

                    
            elif event.key == pygame.K_u:
                #gstate.get().players[2].abilities = []
                #gstate.get().players[2].abilities.append(ability("Lullaby",2, 3,False, 3, False,"cooldown 5 \nevery enemy has a 50% chance to fall asleep", "Utility"))
                #gstate.get().players[2].abilities.append(ability("Shocking Response",2, 0,True, 4, False,"cooldown 2 \nFor the next 2 rounds, attacks agains you deal 5 damage to the attacker and they have a 10% chance to be paralyzed", "Defensive"))

                gstate.get().players[2].abilities.append(ability("The Floor Is Lava", 3, 3, False, 4, False,"cooldown:4, 2 fire orb used. \nfor the next 4 rounds, every enemy takes 10 damage", "Offensive", cooldown = 4, element = 0, orbs = [2,0,0,0,0],  proficiencygiven = [2,0,0,0,0]))
                gstate.get().players[2].abilities.append(ability("Lava Burst", 3, 1, False, 2, True,"1 fire orb used \nwith a 60% chance, the target takes 60 damage and is immobilized", "Offensive", element = 0, orbs = [1,0,0,0,0], proficiencyneeded = 10,  proficiencygiven = [1.5,0,0,0,0]))

                gstate.get().players[1].abilities.append(ability("The Floor Is Lava", 3, 3, False, 4, False,"cooldown:4, 2 fire orb used. \nfor the next 4 rounds, every enemy takes 10 damage", "Offensive", cooldown = 4, element = 0, orbs = [2,0,0,0,0],  proficiencygiven = [2,0,0,0,0]))
                gstate.get().players[1].abilities.append(ability("Lava Burst", 3, 1, False, 2, True,"1 fire orb used \nwith a 60% chance, the target takes 60 damage and is immobilized", "Offensive", element = 0, orbs = [1,0,0,0,0], proficiencyneeded = 10,  proficiencygiven = [1.5,0,0,0,0]))

                gstate.get().players[3].abilities.append(ability("The Floor Is Lava", 3, 3, False, 4, False,"cooldown:4, 2 fire orb used. \nfor the next 4 rounds, every enemy takes 10 damage", "Offensive", cooldown = 4, element = 0, orbs = [2,0,0,0,0],  proficiencygiven = [2,0,0,0,0]))
                gstate.get().players[3].abilities.append(ability("Lava Burst", 3, 1, False, 2, True,"1 fire orb used \nwith a 60% chance, the target takes 60 damage and is immobilized", "Offensive", element = 0, orbs = [1,0,0,0,0], proficiencyneeded = 10,  proficiencygiven = [1.5,0,0,0,0]))


                
            elif event.key == pygame.K_k:
                for a in gstate.get().abilities[3][0][1]:
                    gstate.get().craos.abilities.append(a)
                gstate.get().craos.orbs[0] += 50
            elif event.key == pygame.K_r:
                gstate.get().craos.abilities = gstate.get().craos.abilities[1:]

            elif event.key == pygame.K_w:
                write(screen, "Isto estame a 1 end", (200, 200), 350, gstate.get().fontA, (0,0,200))


            elif event.key == pygame.K_e:
                gstate.get().craos.EXP += 500
                gstate.get().craos.orbs[1] += 500
                gstate.get().craos.proficiencies[1] += 500
    
##    for p in gstate.get().players:
##        #print(str([i[1].name for i in p.ai.decisions]))
##        p.ai.decide()
##        for pe in p.pets:
##            pe.ai.decide()
        
    roundphase = roundphase.clock()
    roundphase.draw(screen)
    pygame.display.update()
    roundphase = roundphase.effect()

pygame.quit()
