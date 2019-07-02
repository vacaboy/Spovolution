#teste
import random as R
import sys
import pygame

from globals import *
from creature import player, npc, deadcorpse
from abilities import *
from state import *

import gstate

pygame.init()
gstate.init()

#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen = pygame.display.set_mode((width, height))
#screen = pygame.display.set_mode((200, 60))



#abilities:
abilities = gstate.get().abilities

abilities[0].append(ability("Tackle",0, 1, False, 2, True, "Offensive"))
abilities[0].append(ability("Double Edged Sword",0, 1, False, 2, True, "Offensive"))
abilities[0].append(ability("chill",0, 0, True, 2, False, "Defensive"))

abilities[1].append(ability("Uncertain Footing",1, 1, False, 3, True, "Offensive"))
abilities[1].append(ability("Stand Tall",1, 1, False, 3, True, "Offensive"))
abilities[1].append(ability("QuickPoke",1, 3, False, 1, True, "Offensive"))

abilities[2][0].append(ability("Spear Throw",2, 1,False, 2, True, "Offensive"))
abilities[2][0].append(ability("Kick",2, 1,False, 2, True, "Offensive"))
abilities[2][0].append(ability("Punch",2, 1,False, 2, True, "Offensive"))
abilities[2][0].append(ability("On The Edge",2, 1,False, 3, True, "Offensive"))
abilities[2][0].append(ability("Blood Drain",2, 1,False, 2, True, "Offensive", cooldown = 1))
abilities[2][0].append(ability("Headbutt",2, 1,False, 2, True, "Offensive"))
abilities[2][0].append(ability("Everyone... GET IN HERE!",2, 1, False, 3, True, "Offensive"))
abilities[2][0].append(ability("From The Shadows" ,2, 1, False, 3, True, "Offensive"))
abilities[2][0].append(ability("Unleash The Power" ,2, 2, False, 2, True, "Offensive", cooldown = 2, channel = 4))

abilities[2][1].append(ability("Rock Solid",2, 0,True, 1, False, "Defensive", cooldown = 5))
abilities[2][1].append(ability("Refreshing Waters",2, 0,True, 2, False, "Defensive", cooldown = 1))
abilities[2][1].append(ability("Regenerate",2, 0,True, 3, False, "Defensive", cooldown = 2))
abilities[2][1].append(ability("Shocking Response",2, 0,True, 4, False, "Defensive", cooldown = 2))
abilities[2][1].append(ability("Dodge",2, 0,True, 1, False, "Defensive"))
abilities[2][1].append(ability("Flight",2, 0,True, 4, False, "Defensive", cooldown = 5))
abilities[2][1].append(ability("Nature's Call",2, 0,True, 4, False, "Defensive", cooldown = 2))
abilities[2][1].append(ability("Web Cacoon",2, 0,True, 1, False, "Defensive", cooldown = 3))
abilities[2][1].append(ability("High Jump",2, 0,True, 1, False, "Defensive"))

abilities[2][2].append(ability("Lullaby",2, 3,False, 3, False, "Utility", cooldown = 5))
abilities[2][2].append(ability("Fight Stance",2, 0,True, 3, False, "Utility", cooldown = 2))
#abilities[2][2].append(ability("Unleash the Chains",2, 0,True, 3, False, "Utility"))
abilities[2][2].append(ability("Limitless",2, 0,True, 3, False, "Utility", cooldown = 999))
abilities[2][2].append(ability("Intimidate",2, 3,False, 4, False, "Utility", cooldown = 1))
abilities[2][2].append(ability("No Pain, No Gain",2, 0,True, 1, False, "Utility"))
#______________________________________________________________________________________________________________________________________________________________________
#buffs:
buffs = gstate.get().buffs

buffs[1][1].append(buff("Double Damage", "Blessing", "Condition", "You deal double damage for 6 rounds", duration = 6))
buffs[1][1].append(buff("Lifesteal", "Blessing", "Condition", "For Life: you have 10% lifesteal", value = 0.1, duration = 999))
buffs[1][1].append(buff("Take Damage", "Curse", "Condition", "For Life: you will receive 3 damage per round.", value = 3, duration = 999))
buffs[1][1].append(buff("Heal Modifier", "Curse", "Condition", "For Life: Heal against you are halfed", value = 0.5, duration = 999))
buffs[1][1].append(buff("More Experience", "Blessing", "Condition", "For Life: you will receive 20% more experience", value = 1.2, duration = 999))
buffs[1][1].append(buff("More Experience", "Curse", "Condition", "For Life: you will receive a 20% less experience", value = 0.8, duration = 999))

##buffs[1][1].append(buff("Take Damage", "Curse", "Condition", "For Life: you will receive a 3 damage attack per round.", value = 3, duration = 999))


buffs[1][0].append(buff("Heal", "Blessing", "Condition", "heal 10 HP next round", value = 10, duration = 1))
buffs[1][0].append(buff("Damage", "Curse", "Condition", "take 10 damage next turn", value = 10, duration = 1))
buffs[1][0].append(buff("Less Damage", "Curse", "Condition", "For life: You will deal 2 less damage.", value = 2, duration = 999))
buffs[1][0].append(buff("More Damage", "Blessing", "Condition", "For life: You will deal 2 more damage.", value = 2, duration = 999))

buffs[1][0].append(buff("More Experience", "Blessing", "Condition", "For 5 turns, you will receive double experience", value = 2, duration = 5))
buffs[1][0].append(buff("More Experience", "Curse", "Condition", "For 5 turns, you will receive half experience", value = 0.5, duration = 5))
##
##buffs[1][0].append(buff("More Damage", "Blessing", "Condition", "For life: You will deal 2 more damage.", value = 2, duration = 999))
##buffs[1][0].append(buff("More Damage", "Blessing", "Condition", "For life: You will deal 2 more damage.", value = 2, duration = 999))
##
##buffs[1][0].append(buff("More Damage", "Blessing", "Condition", "For life: You will deal 2 more damage.", value = 2, duration = 999))
##buffs[1][0].append(buff("More Damage", "Blessing", "Condition", "For life: You will deal 2 more damage.", value = 2, duration = 999))
##
##buffs[1][0].append(buff("More Damage", "Blessing", "Condition", "For life: You will deal 2 more damage.", value = 2, duration = 999))
##buffs[1][0].append(buff("More Damage", "Blessing", "Condition", "For life: You will deal 2 more damage.", value = 2, duration = 999))


#______________________________________________________________________________________________________________________________________________________________
craos = player(375, 450, "craos",(255, 0, 255))

robly18 = npc(375, 150, "robly18")

tavos = npc(670,150, "tavos")

tomis = npc(670, 450, "tomis")

gstate.get().craos = craos

gstate.get().players = [craos, robly18, tavos, tomis]
gstate.get().npcs = [robly18, tavos, tomis]

gstate.get().system = npc(0 ,0, "system", (255,0,0))


roundphase = chooseability(1, 1)
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
                
        if event.type == pygame.KEYDOWN:
                
                
            if event.key == pygame.K_DELETE:
                gstate.get().run = False
##            elif event.key == pygame.K_g:
##                roundphase.gainabilityforfree(craos)
            elif event.key == pygame.K_p:
                for player in gstate.get().players:
                    print(player.name)
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
            elif event.key == pygame.K_f:
                for p in gstate.get().players:
                    p.accuracy = 0
            elif event.key == pygame.K_g:
                for p in gstate.get().players:
                    p.accuracy = 0.5
            elif event.key == pygame.K_v:
                for p in gstate.get().players:
                    p.dodge = 1
            elif event.key == pygame.K_b:
                for p in gstate.get().players:
                    p.dodge = 0.5
            elif event.key == pygame.K_z:
                for p in gstate.get().players:
                    print([p.name, p.accuracy, p.dodge])
            elif event.key == pygame.K_o:
                for a in gstate.get().abilities[2][0]:
                    gstate.get().craos.abilities.append(a)
            elif event.key == pygame.K_d:
                for a in gstate.get().abilities[2][1]:
                    gstate.get().craos.abilities.append(a)
            elif event.key == pygame.K_u:
                for a in gstate.get().abilities[2][2]:
                    gstate.get().craos.abilities.append(a)
            elif event.key == pygame.K_t:
                gstate.get().craos.abilities = gstate.get().craos.abilities[1:]


    roundphase = roundphase.clock()
    roundphase.draw(screen)
    pygame.display.update()
    roundphase = roundphase.effect()

pygame.quit()
