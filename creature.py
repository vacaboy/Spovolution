from globals import *
from abilities import *
import random as R
import pygame
import gstate
from renderable import *
passed = ability("passed", 3, 0, True, 1,"Does nothing this round", False)

class creature:
    def __init__(self, x, y, name = "none", color = "none"):
        self.x, self.y = self.pos = (x, y)
        if color == "none":
            self.color = (R.randint(0,255), R.randint(0,255), R.randint(0,255))
        else:
            self.color = color
            
        if name == "none":
            self.name = R.randint(0,999)
        else:
            self.name = name
        self.thinkingcount = 0
        self.thinkpath = 50
        self.pacifist = True
        self.wondercount = 0
        
        self.EXP = 0
        self.stage = 1
        self.MaxHP = 20
        self.HP = 20
        self.abilities = []
        self.ability = passed
        self.target = []
        self.abilitiesincooldown = []
        self.abilitiesinchannel = []
        self.abilitiesinforget = []
            
        self.conditions = [condition("Freezestacks", self, 1, 999)]
            
        self.attackmultiplier = 1
        self.attackadd = 0
        self.defensemultiplier = 1
        self.defenseadd = 0
        self.healmultiplier = 1
        self.healadd = 0
        self.lifesteal = 0 
        self.accuracy = 1
        self.dodge = 0
        self.EXPmultiplier = 1
        
        self.damaged = False #True or False if this player was damaged this turn or not.
        self.dealtdamage = False #True of False if this player dealt damage this turn or not.
        self.attacksreceived = 0 #keeps track of how many attacks has this player received
        
        
        self.freezestacks = 0
        self.pets = []
        self.renderables = []
        self.orbs = [0,0,0,0,0]
        self.proficiencies = [0,0,0,0,0]
        
    def startnewround(self):
        self.target = []
        self.ability = passed
        self.attackadd = 0
        self.defensemultiplier = 1
        self.defenseadd = 0
        self.healmultiplier = 1
        self.healadd = 0
        self.lifesteal = 0
        self.accuracy = 1
        self.dodge = 0
        if self.HP >self.MaxHP:
            self.HP = self.MaxHP
        if self.MaxHP <= 0:
            self.MaxHP = 1
            
        for ab in self.abilitiesincooldown:
            ab[1] -= 1
            #print(self.name + " has " + ab[0] + " in cooldown for " + str(ab[1]) + " rounds ")
        self.abilitiesincooldown = [ab for ab in self.abilitiesincooldown if ab[1] > 0]
        self.abilitiesinchannel = [ab for ab in self.abilitiesinchannel if (ab[2] == True and ab[1] > 0)]
        for ab in self.abilitiesinchannel:
            ab[2] = False            
        self.conditions = [c for c in self.conditions if c.duration > 0]
        
        for ab in self.abilitiesinforget:
            ab[1] -= 1
        for ab in self.abilitiesinforget:
            if ab[1] == 0:
                self.abilities.append(ab[0].clone())
        self.abilitiesinforget = [ab for ab in self.abilitiesinforget if ab[1] > 0]
        
        self.ai.Qdecided = False
        self.ai.decisions = []
        self.ai.tries = 1
        
        for pe in self.pets:
            pe.startnewround()
        
        
    def draw(self, screen):
        for r in self.renderables:
            r.draw(screen)
        for pe in self.pets:
            pe.draw(screen)
            
    def attack(self, targets, damage, a = 50, accuracy = 1, tolog = True):
        if a == 50:
            a = R.random()
        self.dealtdamage = True 
        d3 = 0
        d1 = ( damage * self.attackmultiplier) + self.attackadd
        if d1 < 0:
            d1 = 0
        for t in targets:
            hit = True
            print("a: " + str(a) +  "   to hit: " +str(self.accuracy * (1 - t.dodge) * accuracy))
            if a <= (self.accuracy * (1 - t.dodge) * accuracy):
                d2 = round( (d1 * t.defensemultiplier) - t.defenseadd )
                if d2 < 0:
                    d2 = 0
                if self.lifesteal != 0:
                    d3 = round(((d2 * self.lifesteal) * self.healmultiplier) + self.healadd)
                    self.HP += d3
                    print(self.name + " regained " + str(d3) + " HP")
                self.EXP += round((d2 * self.EXPmultiplier))
                if not (t == self):
                    t.EXP += round((d2 * t.EXPmultiplier))
                t.HP -= d2
                if tolog:
                    gstate.get().log.append([self, d2, t])
                    t.damaged = True
                    t.attacksreceived += 1
                print(self.name + " dealt " + str(d2) + " damage to " + t.name)
                print(str(damage) + " "  +  str(d1) + " "  + str(d2) + " "  + str(d3))
            else:
                print(self.name + " missed the attack against " + t.name)
                
    def soulattack(self, targets, damage, a = 50, accuracy = 1):
        if a == 50:
            a = R.random()
        d3 = 0
        d1 = damage
        if d1 < 0:
            d1 = 0
        for t in targets:
            hit = True
            if a <= (self.accuracy * (1 - t.dodge) * accuracy):
                self.EXP += round((d1 * self.EXPmultiplier))
                if not (t == self):
                    t.EXP += round((d1 * t.EXPmultiplier))
                t.MaxHP -= d1
                t.attacksreceived += 1
                print(t.name + " lost " + str(d1) + " Max HP")
            else:
                print(self.name + " missed the soul attack against " + t.name)
       
    def heal(self, targets, amount):
        for t in targets:
            h1 = round((amount * t.healmultiplier) + t.healadd)
            t.HP += h1
            print(self.name + " healed " + str(h1) + " to " + t.name)
        
class character(creature):
    def __init__(self, x, y, name = "none", color = "none"):
        super().__init__(x, y, name, color)
        
        self.abilities = []
        self.abilities.append(gstate.get().abilities[0][0].clone())
        self.abilities.append(gstate.get().abilities[0][1].clone())
        self.abilities.append(gstate.get().abilities[0][2].clone())
        #[ability("Tackle",0, 1, False, 2, True, "Offensive"),ability("Double Edged Sword",0, 1, False, 2, True, "Offensive"), ability("chill",0, 0, True, 2, False, "Defensive")]
        
        self.EXPtoevolve = 20
        self.abilitylastused = []
        self.abilitylasttarget = []
        self.unlearnedabilities = []
        
        self.bet = 0
        
        
        self.starterpacks = [False,False,False,False,False]

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
                            textrenderable(x-50, y+95, self.color, fontHP, lambda: str(self.abilitylastused))]
            

    def startnewround(self):
        super().startnewround()
        self.damaged = False
        self.dealtdamage = False
        
        self.attacksreceived = 0
        self.attackmultiplier = 1
        
        self.EXPmultiplier = 1
        self.bet = 0
        
        #print()
        
        
        
        #self.abilitylastused = []
        #self.abilitylasttarget = []
        
        #freezestacks:
        
         
            
        
    def draw(self, screen):
        super().draw(screen)
       
    def drawabilities(self, screen):
        pass
#
class player(character):
        
    def startnewround(self):
        super().startnewround()
        self.ai.ready = False

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
class npc(character):
    def startnewround(self):
        super().startnewround()
    
#______________________________________________________________________________________________________________________________________________________________________
class deadcorpse(character):
    def __init__(self,x ,y, name, color, HP , MaxHP, abilitylastused, abilitylasttarget, EXP, EXPtoevolve):
        super().__init__(x, y, name, color)
        self.HP = HP
        self.MaxHP = MaxHP
        self.abilitylastused = abilitylastused
        self.abilitylasttarget = abilitylasttarget
        self.EXP = EXP
        self.EXPtoevolve = EXPtoevolve
        
        self.renderables.append(textrenderable(x, y, (0,0,0), gstate.get().fontHP, lambda: "R.I.P."))
        self.renderables.remove(self.renderables[2])
        self.renderables.append(barrenderable(x-50, y-80, 100, 10, (255,0,0), (255,0,0), lambda: (0, self.MaxHP)))
#
class monster(creature):
    def __init__(self, x, y, ai, name = "none", color = "none"):
        super().__init__(x, y, name, color)
        self.ai = ai
        
    
class pet(creature):
    def __init__(self, owner, name = "none", color = "none", rend = "rect", HP = 0, MaxHP = 0):
        self.owner = owner
        self.getposition()
        #self.x = 450
        #self.y = 410
        super().__init__(self.x, self.y, name, color)
        self.HP = HP
        self.MaxHP = MaxHP
        if rend == "rect":
            self.renderables.append(rectrenderable(self.x, self.y, 20, 20, self.color))
            self.renderables.append(barrenderable(self.x, self.y-10, 20, 5, (255,0,0), (0,255,0), lambda: (self.HP, self.MaxHP)))
            self.renderables.append(textrenderable(self.x+25, self.y-10, (255,0,0), gstate.get().fontHP, lambda: str(self.HP) + "/" + str(self.MaxHP)))
            
    def getposition(self):
        #pass
        self.x = self.owner.x + 60
        y = self.owner.y + (30 * (len(self.owner.pets) - 1))
        w = True
        while w:
            if y in [i.y for i in self.owner.pets]:
                y = y - 30
            else:
                w = False
        self.y = y
        
        
        