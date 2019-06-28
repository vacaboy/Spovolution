from globals import *
from abilities import *
import random as R
import pygame
import gstate
from renderable import playerrenderable, textrenderable, barrenderable

class creature:
    def __init__(self, x, y, name = "none", color = "none"):
        self.x, self.y = self.pos = (x, y)
        self.MaxHP = 20
        self.HP = 20
        self.abilities = [ability("Tackle",0, 1, False, 2, True, "Offensive"),ability("Double Edged Sword",0, 1, False, 2, True, "Offensive"), ability("chill",0, 0, True, 2, False, "Defensive")]
        self.EXP = 0
        self.stage = 1
        self.EXPtoevolve = 20
        self.abilitylastused = " "
        self.abilitylasttarget = " "
        self.ability = " "
        self.target = []
        self.damaged = False #True or False if this player was damaged this turn or not.
        self.dealtdamage = False #True of False if this player dealt damage this turn or not.
        self.attacksreceived = 0 #keeps track of how many attacks has this player received
        self.conditions = []
        self.unlearnedabilities = []
        self.abilitiesincooldown = []
        self.abilitiesinchannel = []
        
        if color == "none":
            self.color = (R.randint(0,255), R.randint(0,255), R.randint(0,255))
        else:
            self.color = color
            
        if name == "none":
            self.name = R.randint(0,999)
        else:
            self.name = name

        fontHP = gstate.get().fontHP

        self.renderables = [playerrenderable(self),
                            textrenderable(x + 55, y, self.color, fontHP, lambda: self.name),

                            barrenderable(x-50, y-80, 100, 10, (255,0,0), (0,255,0), lambda: (self.HP, self.MaxHP)),
                            textrenderable(x+55, y-80, (255,0,0), fontHP, lambda: str(self.HP) + "/" + str(self.MaxHP)),

                            barrenderable(x-50, y-60, 100, 10, (0,0,255), (0,0,255), lambda: (self.EXP, self.EXPtoevolve*2), True),
                            textrenderable(x+55, y-60, (0,0,255), fontHP, lambda: str(self.EXP) + "/" + str(self.EXPtoevolve)),

                            textrenderable(x-55, y+55, self.color, fontHP, lambda: "ability last used:"),
                            textrenderable(x-55, y+65, self.color, fontHP, lambda: "target:"),
                            textrenderable(x-55, y+80, self.color, fontHP, lambda: str(self.abilitylasttarget)),
                            textrenderable(x-50, y+95, self.color, fontHP, lambda: self.abilitylastused)]
            

    def startnewround(self):

        self.damaged = False
        self.dealtdamage = False
        self.target = []
        self.attacksreceived = 0
        if self.HP >self.MaxHP:
            self.HP = self.MaxHP
        for ab in self.abilitiesincooldown:
            ab[1] -= 1
            print(self.name + " has " + ab[0] + " in cooldown for " + str(ab[1]) + " rounds ")
        for ab in self.abilitiesincooldown:
            if ab[1] == 0:
                self.abilitiesincooldown.remove(ab)

        for ab in self.abilitiesinchannel:
            if ab[2] == False or ab[1] == 0:
                print(self.name + " stopped channeling " + ab[0])
                self.abilitiesinchannel.remove(ab)
            else:
                ab[2] = False
            
        
    def draw(self, screen):
        for r in self.renderables:
            r.draw(screen)
       
    def drawabilities(self, screen):
        pass

class player(creature):


    def drawabilities(self, screen):
        pygame.draw.rect(screen, (255,246,143),(0 ,0 ,300 , height)) #ability tab
        for ab in self.abilities:
            
            pygame.draw.rect(screen, (139,69,19),(10,(10 + 40 * self.abilities.index(ab)), 280, 30))
            if ab.abilitytype == "0": #criar o nome dela:
                textability = gstate.get().fontA.render(ab.name, 1, (0,0,0))
                
            elif ab.abilitytype == "Offensive":
                textability = gstate.get().fontA.render(ab.name, 1, (255,48,48))

            elif ab.abilitytype == "Defensive":
                textability = gstate.get().fontA.render(ab.name, 1, (30,144,255))

            elif ab.abilitytype == "Utility":
                textability = gstate.get().fontA.render(ab.name, 1, (0,201,87))

            screen.blit(textability,(30, 15 + 40 * self.abilities.index(ab)))

            if ab.name in [i[0] for i in self.abilitiesincooldown]:
                pygame.draw.line(screen, (255,0,0), (10, 10 + 40 * self.abilities.index(ab)), (290, 40 + 40 * self.abilities.index(ab)) )
                pygame.draw.line(screen, (255,0,0), (10, 40 + 40 * self.abilities.index(ab)), (290, 10 + 40 * self.abilities.index(ab)) )
#______________________________________________________________________________________________________________________________________________________________________

class npc(creature):

    def chooseability(self):
        a = True
        while a:
            b = R.randint(0, len(self.abilities)-1)
            if not (self.abilities[b].name in [i[0] for i in self.abilitiesincooldown]):
                self.ability = self.abilities[b]
                a = False

    def choosetarget(self, n, selftarget):
        self.target = []
        if selftarget: #se te podes dar target a ti mesmo
            if n >= len(gstate.get().players): #se o numero targets for maior ou igual que o numero de gstate.get().players, entao os targets sao todos os gstate.get().players:
                for p in gstate.get().players:
                    self.target.append(p)
            else:
                while n > 0: #se nao, vamos escolher gstate.get().players
                    a = R.randint(0, len(gstate.get().players)-1)
                    if gstate.get().players[a] in self.target:
                        pass
                    else:
                        self.target.append(gstate.get().players[a])
                        n -= 1
        else:#se nao de podes dar target a ti mesmo...
            if n >= (len(gstate.get().players) - 1): #entao se o numero de targets for maior ou igual que o numero de gstate.get().players - 1, entao os targets sao todos os inimigos
                for p in gstate.get().players:
                    if p == self:
                        pass
                    else:
                        self.target.append(p)
            else:
                while n > 0:#se nao, vamos escolher inimigos
                    a = R.randint(0, len(gstate.get().players)-1)
                    if (gstate.get().players[a] in self.target) or (gstate.get().players[a] == self):
                        pass
                    else:
                        self.target.append(gstate.get().players[a])
                        n -= 1
        if self.ability.channel > 0: #se a habilidade escolhida tem channel:
            if self.ability.name in [i[0] for i in self.abilitiesinchannel]: #se o player ja esta a dar channel à habilidade
                a = [i[0] == self.ability.name for i in self.abilitiesinchannel].index(True)
                if self.abilitiesinchannel[a][1] > 1: #se a habilidade nao vai atuar este turno
                    self.target = []
            elif not (self.ability.name in [i[0] for i in self.abilitiesinchannel]): #se o player ainda nao esta a dar channel à habilidade:
                self.target = []
       
    
#______________________________________________________________________________________________________________________________________________________________________
class deadcorpse(creature):
    def __init__(self,x ,y, name, color, HP , MaxHP, abilitylastused, abilitylasttarget, EXP, EXPtoevolve):
        super().__init__(x, y, name, color)
        self.HP = HP
        self.MaxHP = MaxHP
        self.abilitylastused = abilitylastused
        self.abilitylasttarget = abilitylasttarget
        self. EXP = EXP
        self.EXPtoevolve = EXPtoevolve
        self.renderables.append(textrenderable(x, y, (0,0,0), gstate.get().fontHP, "R.I.P.")