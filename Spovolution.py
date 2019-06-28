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

#width = pygame.display.info()[current_w]
#print(str(width))

#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen = pygame.display.set_mode((width, height))
#screen = pygame.display.set_mode((200, 60))



#__________________________________________________________________________________________________________________________________________________________________________________

#__________________________________________________________________________________________________________________________________________________________________________________

#_______________________________________________________________________________________________________________________________________________________________________

#______________________________________________________________________________________________________________________________________________________________________

#fonts:

#texts:
#texttackle = fontA.render("Tackle", 1, (0,0,0))
#textchoosetarget = fonttime.render("choose target(s)!", 1, (255,0,0))
#textround = fonttime.render("round:" + str(roundcount), 1, (0, 0, 255))

#______________________________________________________________________________________________________________________________________________________________________
#players:

        
#______________________________________________________________________________________________________________________________________________________________________

#abilities:
abilities = gstate.get().abilities

abilities[0].append(ability("Tackle",0, 1, False, 2, True, "Offensive"))
abilities[0].append(ability("Double Edged Sword",0, 1, False, 2, True, "Offensive"))
abilities[0].append(ability("chill",0, 0, True, 2, False, "Defensive"))

abilities[1].append(ability("Uncertain Footing",1, 1, False, 3, True, "Offensive"))
abilities[1].append(ability("Stand Tall",1, 1, False, 3, True, "Offensive"))
abilities[1].append(ability("QuickPoke",1, 3, False, 1, True, "Offensive"))


#abilities[1].append(ability("teste", 1, 0, True, 3, False))
#abilities[1].append(ability("teste2", 1, 2, True, 3, False))

abilities[2][0].append(ability("Spear Throw",2, 1,False, 2, True, "Offensive"))
abilities[2][0].append(ability("Kick",2, 1,False, 2, True, "Offensive"))
abilities[2][0].append(ability("Punch",2, 1,False, 2, True, "Offensive"))
abilities[2][0].append(ability("On The Edge",2, 1,False, 3, True, "Offensive"))
abilities[2][0].append(ability("Blood Drain",2, 1,False, 2, True, "Offensive"))
abilities[2][0].append(ability("Headbutt",2, 1,False, 2, True, "Offensive"))
abilities[2][0].append(ability("Everyone... GET IN HERE!",2, 1, False, 3, True, "Offensive"))
abilities[2][0].append(ability("From The Shadows" ,2, 1, False, 3, True, "Offensive"))
abilities[2][0].append(ability("Unleash The Power" ,2, 2, False, 2, True, "Offensive", cooldown = 2, channel = 4))


abilities[2][1].append(ability("Rock Solid",2, 0,True, 1, False, "Defensive", cooldown = 5))
abilities[2][1].append(ability("Refreshing Waters",2, 0,True, 2, False, "Defensive"))
abilities[2][1].append(ability("Regenerate",2, 0,True, 3, False, "Defensive"))

abilities[2][2].append(ability("Lullaby",2, 3,False, 3, False, "Utility", cooldown = 5))
abilities[2][2].append(ability("Fight Stance",2, 0,True, 3, False, "Utility"))
abilities[2][2].append(ability("Unleash the Chains",2, 0,True, 3, False, "Utility"))
abilities[2][2].append(ability("Limitless",2, 0,True, 3, False, "Utility", cooldown = 999))
abilities[2][2].append(ability("Intimidate",2, 0,False, 4, False, "Utility", cooldown = 1))
#______________________________________________________________________________________________________________________________________________________________________



craos = player(375, 450, "craos",(255, 0, 255))

robly18 = npc(375, 150, "robly18")

tavos = npc(670,150, "tavos")

tomis = npc(670, 450, "tomis")

gstate.get().craos = craos

gstate.get().players = [craos, robly18, tavos, tomis]
gstate.get().npcs = [robly18, tavos, tomis]



roundphase = chooseability(1)
print("round: 1")

#______________________________________________________________________________________________________________________________________________________________________

#main loop
run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: #nao sei como ver se se clicou no lado esquerdo ou direito do rato... o lado esquerdo é 1 e o lado esquerdo é 3
                
                roundphase = roundphase.receiveevent(event)
                
        if event.type == pygame.KEYDOWN:
                
                
            if event.key == pygame.K_DELETE:
                run = False
            elif event.key == pygame.K_g:
                roundphase.gainabilityforfree(craos)
            elif event.key == pygame.K_p:
                for player in players:
                    print(player.name)
            elif event.key == pygame.K_n:
                for npc in npcs:
                    print(npc.name)
            elif event.key == pygame.K_a:
                print("clicaste a para ver as habilidades de toda a gente.")
                for player in players:
                    print(player.name)
                    for a in player.abilities:
                        print(a.name)
                    print()
            elif event.key == pygame.K_l:
                for i in log:
                    print(str(i))


    roundphase = roundphase.clock()
    roundphase.draw(screen)
    pygame.display.update()
    roundphase = roundphase.effect()

pygame.quit()
