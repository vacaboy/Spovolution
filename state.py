import random as R
from globals import *
from creature import *
from abilities import *

import gstate
import math


class state():

    def __init__(self, roundcount, stage = 0):
        self.name = "0"
        self.roundcount = roundcount
        self.stage = stage
        self.showing = False
        self.renderables = [textrenderable(300, 10, (255,0,0), gstate.get().fonttime, lambda: self.name + ":" + str(self.time)),
                            textrenderable(300, 30, (0,0,255), gstate.get().fonttime, lambda: "round:" + str(self.roundcount) + "/" + str(evolveround[stage]))]
        self.temporaryrenderables = []
        
    def clock(self):
        self.time1 = self.time1 - 0.1
        self.time = math.ceil(self.time1)
        #self.texttime = gstate.get().fonttime.render(self.name + ":" + str(self.time), 1, (255,0,0))
        for i in range(10):
            pygame.time.delay(10)
    
    def draw(self, screen):
        pygame.draw.rect(screen, (0,0,0), (0,0, width, height))
        gstate.get().craos.drawabilities(screen)
        for r in self.renderables:
            r.draw(screen)
        for player in gstate.get().players:
            player.draw(screen)
        for corpse in gstate.get().deadcorpses:
            corpse.draw(screen)
            
    def effect(self):
        return self
            
    def receiveevent(self, event):
        return self
        
    def receiveevent1(self, event, screen):
        mouseposition = event.pos
        for ren in self.temporaryrenderables:
            self.renderables.remove(ren)
        self.temporaryrenderables = []
        self.showing = False
        for i in range(len(gstate.get().craos.abilities)):
                if  10 <= mouseposition[0]  <= 290 and (10 + (40 * i)) <= mouseposition[1] <= (40 + (40 * i)):
                    a = rectrenderable(mouseposition[0], mouseposition[1], 200, 150, (193,205,205))
                    self.renderables.append(a)
                    self.temporaryrenderables.append(a)
                    self.write(screen, gstate.get().craos.abilities[i].text, (mouseposition[0]+10, mouseposition[1]+10), 180, gstate.get().fontwrite)
                self.showing = True
        return self
        
    def write(self, surface, te, pos, width , font, color=(200,0,0)):
        words = [word.split(' ') for word in te.splitlines()]  # 2D array where each row is a list of words.
        space = font.size(' ')[0]  # The width of a space.
        x, y = pos
        max_width = x + width
        for line in words:
            for wo in line:
                wo_surface = font.render(wo, 0, color)
                wo_width, wo_height = wo_surface.get_size()
                if x + wo_width >= max_width:
                    x = pos[0]  # Reset the x.
                    y += wo_height  # Start on new row.
                a = textrenderable1(x, y, color, font, wo)
                self.renderables.append(a)
                self.temporaryrenderables.append(a)
                x += wo_width + space
            x = pos[0]  # Reset the x.
            y += wo_height  # Start on new row.
       
class chooseability(state):

    def __init__(self, roundcount, stage, time = 900):
        super().__init__(roundcount, stage)
        self.name = "choose ability"
        self.time = time
        self.time1 = time
        self.textgainability = gstate.get().fontA.render("learn ability", 1, (0,0,0))
        #self.textevolve = gstate.get().fontA.render("EVOLVE!", 1, (0,0,0))
        self.textunlearnability = gstate.get().fontA.render("Unlearn ability", 1, (0,0,0))

    def clock(self):
        super().clock()
        if self.time <= 0:
            gstate.get().craos.ability = ability("passed",3, 0, True, 1, False)
            print(str(gstate.get().craos.ability.name))          
            return choosetarget(self.roundcount, self.stage, self.time)
        else:
            return self
            
    def effect(self): 
                #verify if the game ended:
        if len(gstate.get().players) == 0:
            return endgame(self.roundcount, self.stage, "tie")

        else:
            for corpse in gstate.get().deadcorpses:
                if corpse.name == "craos":
                    return endgame(self.roundcount, self.stage, "lose")


        if len(gstate.get().players) == 1 and gstate.get().players[0].name == "craos":
            return endgame(self.roundcount, self.stage, "win")
        else:
            return self


    def draw(self, screen):
        super().draw(screen)
        #escolha de habilidade ou evoluir ou desaprender:
        pygame.draw.rect(screen, (227,207,87), (320, 290, 160, 30))
        #pygame.draw.rect(screen, (227,207,87), (520, 290, 160, 30))
        pygame.draw.rect(screen, (227,207,87), (720, 290, 160, 30))

        screen.blit(self.textgainability, (330, 295))
        #screen.blit(self.textevolve, (530, 295))
        screen.blit(self.textunlearnability, (730, 295))

    

    def receiveevent(self, event):
        mouseposition = event.pos
        print(mouseposition)
        #escolher habilidade
        for i in range(len(gstate.get().craos.abilities)):
            if  10 <= mouseposition[0]  <= 290 and (10 + (40 * i)) <= mouseposition[1] <= (40 + (40 * i)):
                #if gstate.get().craos.abilities[i].cooldown == 0:
                #só podes escolher se a habilidade nao estiver em cooldown
                if not(gstate.get().craos.abilities[i].name in [j[0] for j in gstate.get().craos.abilitiesincooldown]):
                    gstate.get().craos.target = []
                    gstate.get().craos.ability = gstate.get().craos.abilities[i]

                    for player in gstate.get().players:#fazer os efeitos que atuam agora
                        for condition in player.conditions:
                            if condition.priority == "chooseability":
                                condition.effect()
                    
                    return choosetarget(self.roundcount, self.stage, self.time)
                else:
                    print("this ability is in cooldown")

        #ganhar habilidade
        if 320 <= mouseposition[0] <= 480 and 290 <= mouseposition[1] <= 320:
            print("ganhar habilidade")
            if gstate.get().craos.EXP < abilityprice[gstate.get().craos.stage]:
                print("not enough EXP")
            else:
                if gstate.get().craos.stage == 1:
                    self.gainability(gstate.get().craos)
                elif gstate.get().craos.stage == 2:
                    return gainability1(self.roundcount, self.stage, self.time)
                elif gstate.get().craos.stage == 3:
                    return gainability2(self.roundcount, self.stage, self.time)
        #desaprender habilidade:
        elif 720 <= mouseposition[0] <= 880 and 290 <= mouseposition[1] <= 320:
            print("desaprender habilidade")
            return loseability(self.roundcount, self.stage, self.time)
        return self

    def gainability(self, player):
        #verify if the player already has all the abilities:
        a = True
        stageabilities = gstate.get().abilities[player.stage]
        for ab in stageabilities:
            if (not (ab.name in [i.name for i in player.abilities])) and (not (ab.name in [i.name for i in player.unlearnedabilities])):
                a = False
        if a:
            pass
        #verify if the player has enough EXP:
        elif player.EXP < abilityprice[player.stage]:
            pass
        else:
            while not a:
                b = R.randint(0,len(stageabilities) - 1)
                #verificar se o nome da habilidade não está nos nomes das habilidades do jogador
                if (not (stageabilities[b].name in [i.name for i in player.abilities])) and ( not (stageabilities[b].name in [i.name for i in player.unlearnedabilities])):
                #if not (stageabilities[b].name in [i.name for i in player.abilities]):
                
                    player.abilities.append(stageabilities[b].clone())
                    a = True
                    player.EXP -= abilityprice[player.stage]
            
#__________________________________________________________________________________________________________________________________________________________________________________
class choosetarget(state):
    def __init__(self, roundcount, stage, time = 30):
        super().__init__(roundcount, stage)
        self.name = "Choose Target"
        self.time = time
        self.time1 = time
        self.targetnumber = gstate.get().craos.ability.targetnumber
        self.renderables.append(barrenderable(320, 290, 160, 30, (227,207,87), (227,207,87), lambda: (1,1)))
        self.renderables.append(textrenderable(330, 295, (0,0,0), gstate.get().fontA, lambda: "return"))

    def clock(self):
        super().clock()
        #colocar aqui condiçao de se passar o tempo... escolher targets aleatorios e seguir
        # if time <= 0:
                
            # return calculateeffects(self.roundcount)
        # else:
        return self
     
    def effect(self):
    
        if gstate.get().craos.ability.Return:
            print("passou aqui")
            return chooseability(self.roundcount, self.stage, self.time)

        if self.targetnumber <= 0: #se ja estao os targets todos escolhidos, siga em frente

            for player in gstate.get().players: #condiçoes que atuam agora:
                for condition in player.conditions:
                    if condition.priority == "after choosetarget":
                        condition.effect()
                        
            return calculateeffects(self.roundcount, self.stage)
            
        #se a habilidade escolhida é de channel, e não vai fazer o efeito este turno, siga a marinha
        if gstate.get().craos.ability.channel > 0:#se a habilidade escolhida tem channel:
            if gstate.get().craos.ability.name in [i[0] for i in gstate.get().craos.abilitiesinchannel]: #se o player ja esta a dar channel à habilidade
                a = [i[0] == gstate.get().craos.ability.name for i in gstate.get().craos.abilitiesinchannel].index(True)
                if gstate.get().craos.abilitiesinchannel[a][1] >= 2: #se a habilidade nao vai atuar este turno

                    for player in gstate.get().players: #condiçoes que atuam agora:
                        for condition in player.conditions:
                            if condition.priority == "after choosetarget":
                                condition.effect()
                        
                    return calculateeffects(self.roundcount, self.stage)
                else:
                    if ((self.targetnumber >= (len(gstate.get().players) - 1 - len(gstate.get().craos.pets))) and not gstate.get().craos.ability.selftarget): #se a habilidade tem toda a gente como target, siga
                        for p in gstate.get().npcs:    
                            for pe in p.pets:
                                gstate.get().craos.target.append(pe)
                            gstate.get().craos.target.append(p)

                        for player in gstate.get().players: #condiçoes que atuam agora:
                            for condition in player.conditions:
                                if condition.priority == "after choosetarget":
                                    condition.effect()
                          
                        return calculateeffects(self.roundcount, self.stage)
                        
                    elif self.targetnumber >= len(gstate.get().availabletargets):
                        for p in gstate.get().availabletargets:    
                            gstate.get().craos.target.append(p)

                        for player in gstate.get().players: #condiçoes que atuam agora:
                            for condition in player.conditions:
                                if condition.priority == "after choosetarget":
                                    condition.effect()
                          
                        return calculateeffects(self.roundcount, self.stage)

                    
                    
            elif not (gstate.get().craos.ability.name in [i[0] for i in gstate.get().craos.abilitiesinchannel]): #se o player ainda nao esta a dar channel à habilidade:

                for player in gstate.get().players: #condiçoes que atuam agora:
                    for condition in player.conditions:
                        if condition.priority == "after choosetarget":
                            condition.effect()
                            
                return calculateeffects(self.roundcount, self.stage)
            
                
        elif ((self.targetnumber >= (len(gstate.get().availabletargets
        ) - 1 - len(gstate.get().craos.pets))) and not gstate.get().craos.ability.selftarget): #se a habilidade tem toda a gente como target, siga
            for p in gstate.get().npcs:    
                for pe in p.pets:
                    gstate.get().craos.target.append(pe)
                gstate.get().craos.target.append(p)
            

            for player in gstate.get().players: #condiçoes que atuam agora:
                for condition in player.conditions:
                    if condition.priority == "after choosetarget":
                        condition.effect()
              
            return calculateeffects(self.roundcount, self.stage)

        elif self.targetnumber >= len(gstate.get().availabletargets): #se a habilidade tem toda a gente como target, siga
            for p in gstate.get().availabletargets:    
                gstate.get().craos.target.append(p)
            

            for player in gstate.get().players: #condiçoes que atuam agora:
                for condition in player.conditions:
                    if condition.priority == "after choosetarget":
                        condition.effect()
              
            return calculateeffects(self.roundcount, self.stage)
        return self
       
    def receiveevent(self, event):
        mouseposition = event.pos
        for player in gstate.get().players:

            if not gstate.get().craos.ability.selftarget:#verify if you can target yourself:
                if (player == gstate.get().craos) or player in gstate.get().craos.target:
                    pass
                else:
                    if ((mouseposition[0] - player.pos[0])**2 + (mouseposition[1] - player.pos[1])**2) <= 50**2:
                        gstate.get().craos.target.append(player)
                        self.targetnumber -= 1
            else:
                if not player in gstate.get().craos.target:
                    if ((mouseposition[0] - player.pos[0])**2 + (mouseposition[1] - player.pos[1])**2) <= 50**2:
                        gstate.get().craos.target.append(player)
                        self.targetnumber -= 1
        if ((320 <= mouseposition[0] <= 480) and (290 <= mouseposition[1] <= 320)):
            return chooseability(self.roundcount, self.stage, self.time)
        else:
            return self
#__________________________________________________________________________________________________________________________________________________________________________________
class calculateeffects(state):
    def __init__(self, roundcount, stage):
        super().__init__(roundcount, stage)
        self.name = "calculating effects"
        self.time = 30
        self.time1 = 30
        gstate.get().craos.ai.ready = True

    def clock(self):
        super().clock()
        return self

    def effect(self):
        if [p for p in gstate.get().players if p.ai.Qdecided] == gstate.get().players: #se todos ja se decidiram:
            gstate.get().simulation.run(gstate.get().decisionlist)
            return endround(self.roundcount, self.stage)
        else:
            return chooseability(self.roundcount, self.stage)
#________________________________________________________________________________________________________________________________________________________
class endround(state):
    def __init__(self, roundcount, stage):
        super().__init__(roundcount, stage)
        self.name = "endturn"
        self.time = 30
        self.time1 = 30

    def clock(self):
        super().clock()
        return self

    def effect(self):
        for p in gstate.get().players: #conditions that act at the end of the round.
            for c in p.conditions:
                if c.priority == "endround":
                    c.effect()
        
        
        for player in gstate.get().players:
            player.startnewround()
            player.ai.gatherinfo()
            
        for p in gstate.get().players: #conditions that act at the end of the round.
            for c in p.conditions:
                if c.priority == "Afterstartnewround":
                    c.effect()
            
        #print()
        #a = [[l[0].name, l[1], l[2].name] for l in gstate.get().log]
        #print(str(a))
        
        gstate.get().log = []   
        gstate.get().decisionlist = []
        print()
        print("round: " + str(self.roundcount + 1))
        
        if (self.roundcount + 1) == evolveround[1]:
            return buffbet1(self.roundcount + 1, self.stage)
        elif (self.roundcount + 1) == evolveround[2]:
            return buffbet2(self.roundcount + 1, self.stage)
        else:
            return chooseability(self.roundcount + 1, self.stage)
#__________________________________________________________________________________________________________________________________________________________________
class loseability(state):

    def __init__(self, roundcount, stage, time = 30):
        super().__init__(roundcount, stage)
        self.name = "Choose ability to unlearn"
        self.time = time
        self.time1 = time
        self.textreturn = gstate.get().fontA.render("Return", 1, (0,0,0))
        
    def clock(self):
        super().clock()
        if self.time <= 0:
            return chooseability(self.roundcount, self.stage)
        else:
            return self

    def draw(self, screen):
        super().draw(screen)
        #return option:
        pygame.draw.rect(screen, (227,207,87), (320, 290, 160, 30))
        screen.blit(self.textreturn, (330, 295))
        

    

    def receiveevent(self, event):
        mouseposition = event.pos
        print(mouseposition)

        for i in range(len(gstate.get().craos.abilities)):
            if  10 <= mouseposition[0]  <= 290 and (10 + (40 * i)) <= mouseposition[1] <= (40 + (40 * i)):
                gstate.get().craos.unlearnedabilities.append(gstate.get().craos.abilities[i])
                gstate.get().craos.abilities.remove(gstate.get().craos.abilities[i])
                return chooseability(self.roundcount, self.stage, self.time)
            if  320 <= mouseposition[0] <= 480 and 290 <= mouseposition[1] <= 320: #return button
                return chooseability(self.roundcount, self.stage, self.time)
        return self

#_____________________________________________________________________________________________________________________________________________________________________
class evolve1(state):

    def __init__(self, roundcount, stage, time = 30):
        super().__init__(roundcount, stage)
        self.name = "You are Evolving!"
        self.time = time
        self.time1 = time
        self.textoffensive = gstate.get().fontA.render("Offensive", 1, (0,0,0))
        self.textdefensive = gstate.get().fontA.render("Defensive", 1, (0,0,0))
        self.textutility = gstate.get().fontA.render("Utility", 1, (0,0,0))
        self.number = 3 #abilities he gets to choose
        self.renderables.append(textrenderable(330, 295, (0,0,0), gstate.get().fontA, lambda: "Offensive"))
        self.renderables.append(textrenderable(530, 295, (0,0,0), gstate.get().fontA, lambda: "Defensive"))
        self.renderables.append(textrenderable(730, 295, (0,0,0), gstate.get().fontA, lambda: "Utility"))
        # self.renderables.append(rectrenderable(320, 290, 160, 30, (255,48,48)))
        # self.renderables.append(rectrenderable(520, 290, 160, 30, (30, 144, 255)))
        # self.renderables.append(rectrenderable(720, 290, 160, 30, (0,201,87)))
        
    def clock(self):
        super().clock()
        if self.time <= 0:
            return chooseability(self.roundcount, self.stage)
        else:
            return self

    def draw(self, screen):
        super().draw(screen)
        #escolha de tipo de habilidade :
        pygame.draw.rect(screen, (255,48,48), (320, 290, 160, 30))
        pygame.draw.rect(screen, (30,144,255), (520, 290, 160, 30))
        pygame.draw.rect(screen, (0,201,87), (720, 290, 160, 30))


        screen.blit(self.textoffensive, (330, 295))
        screen.blit(self.textdefensive, (530, 295))
        screen.blit(self.textutility, (730, 295))
        

    def effect(self):
        if self.number <= 0:
            for p in gstate.get().players:
                p.HP += evolveHPgain[p.stage]
                p.MaxHP += evolveHPgain[p.stage]
                p.EXPtoevolve = evolveEXP[p.stage + 1]
                p.stage += 1
                if not (p == gstate.get().craos):
                    p.abilities = []
                    self.gainabilityoffensive(p)
                    #p.abilities.append(ability("Unleash The Power" ,2, 2, False, 2, True, "Offensive", cooldown = 2, channel = 4))
                    self.gainabilitydefensive(p)
                    self.gainabilityutility(p)
                    #p.abilities.append(ability("Reflective Mirror",2, 3, False, 1, False, "Utility", cooldown = 999))
                    
                p.startnewround()
                
            gstate.get().decisionlist = []
            return chooseability(self.roundcount, self.stage + 1)
        else:
            return self


    

    def receiveevent(self, event):
        mouseposition = event.pos
        print(mouseposition)
        if  320 <= mouseposition[0]  <= 480 and 290 <= mouseposition[1] <= 320:
            self.gainabilityoffensive(gstate.get().craos)
            self.number -= 1
        elif  520 <= mouseposition[0]  <= 680 and 290 <= mouseposition[1] <= 320:
            self.gainabilitydefensive(gstate.get().craos)
            self.number -= 1
        elif  720 <= mouseposition[0]  <= 880 and 290 <= mouseposition[1] <= 320:
            self.gainabilityutility(gstate.get().craos)
            self.number -= 1
        return self

    def gainabilityoffensive(self, player):
        a = True
        offensiveabilities = gstate.get().abilities[2][0]
        while a:
            b = R.randint(0,len(offensiveabilities) - 1)
            #verificar se o nome da habilidade não está nos nomes das habilidades do jogador
            if not (offensiveabilities[b].name in [i.name for i in player.abilities]):
                player.abilities.append(offensiveabilities[b].clone())
                a = False

    def gainabilitydefensive(self, player):
        a = True
        defensiveabilities = gstate.get().abilities[2][1]
        while a:
            b = R.randint(0,len(defensiveabilities) - 1)
            #verificar se o nome da habilidade não está nos nomes das habilidades do jogador
            if not (defensiveabilities[b].name in [i.name for i in player.abilities]):
                player.abilities.append(defensiveabilities[b].clone())
                a = False


    def gainabilityutility(self, player):
        a = True
        utilityabilities = gstate.get().abilities[2][2]
        while a:
            b = R.randint(0,len(utilityabilities) - 1)
            #verificar se o nome da habilidade não está nos nomes das habilidades do jogador
            if not (utilityabilities[b].name in [i.name for i in player.abilities]):
                player.abilities.append(utilityabilities[b].clone())
                a = False

class evolve2(state):

    def __init__(self, roundcount, stage, time = 300):
        super().__init__(roundcount, stage)
        self.name = "You are Evolving!"
        self.time = time
        self.time1 = time
        self.done = False
        self.renderables.append(circlerenderable(380, 300, 40, (255,0,0)))
        self.renderables.append(circlerenderable(480, 300, 40, (135,206,250)))
        self.renderables.append(circle2)
        self.renderables.append(circle3)
        self.renderables.append(circle4)
        
    def clock(self):
        super().clock()
        if self.time <= 0:
            return chooseability(self.roundcount, self.stage)
        else:
            return self

    def draw(self, screen):
        super().draw(screen)

        

    def effect(self):
        if self.done:
            for p in gstate.get().players:
                p.HP += evolveHPgain[self.stage]
                p.MaxHP += evolveHPgain[self.stage]
                p.EXPtoevolve = evolveEXP[self.stage + 1]
                p.stage = 3
                p.ai.decisionnumber += 1
                if not (p == gstate.get().craos):
                    p.abilities = []
                    #a = R.randint(0,3)
                    a = 0
                    if a == 0:
                        p.element = "Fire"
                    elif a == 1:
                        p.element = "Ice"
                    #elif a == 2:
                    #    p.element = "Tempest"
                    elif a == 2:
                        p.element = "Necrotic"
                    elif a == 3:
                        p.element = "Mind"
                self.gainstarterpack(p)
                
                p.startnewround()
            gstate.get().decisionlist = []
            return chooseability(self.roundcount, self.stage + 1)
        else:
            return self


    

    def receiveevent(self, event):
        mouseposition = event.pos
        print(mouseposition)
        if ((mouseposition[0] - 380)**2 + (mouseposition[1] - 300)**2) <= 40**2:
            gstate.get().craos.element = "Fire"
        elif ((mouseposition[0] - 480)**2 + (mouseposition[1] - 300)**2) <= 40**2:
            gstate.get().craos.element = "Ice"
        elif ((mouseposition[0] - 580)**2 + (mouseposition[1] - 300)**2) <= 40**2:
            gstate.get().craos.element = "Tempest"
        elif ((mouseposition[0] - 680)**2 + (mouseposition[1] - 300)**2) <= 40**2:
            gstate.get().craos.element = "Necrotic"
        elif ((mouseposition[0] - 780)**2 + (mouseposition[1] - 300)**2) <= 40**2:
            gstate.get().craos.element = "Mind"
        self.done = True
        return self
        
    def gainstarterpack(self, creature):
        if creature.element == "Fire":
            creature.starterpacks[0] = True
            for ab in gstate.get().starterpacks[0]:
                creature.abilities.append(ab.clone())
        elif creature.element == "Ice":
            creature.starterpacks[1] = True
            for ab in gstate.get().starterpacks[1]:
                creature.abilities.append(ab.clone())
        elif creature.element == "tempest":
            creature.starterpacks[2] = True
            for ab in gstate.get().starterpacks[2]:
                creature.abilities.append(ab.clone())
        elif creature.element == "Necrotic":
            creature.starterpacks[3] = True
            for ab in gstate.get().starterpacks[3]:
                creature.abilities.append(ab.clone())
        elif creature.element == "Mind":
            creature.starterpacks[4] = True
            for ab in gstate.get().starterpacks[4]:
                creature.abilities.append(ab.clone())
#_____________________________________________________________________________________________________________________________________________________________________
class gainability1(state):

    def __init__(self, roundcount, stage, time = 30):
        super().__init__(roundcount,stage)
        self.name = "choose ability type"
        self.time = time
        self.time1 = time
        self.textoffensive = gstate.get().fontA.render("Offensive", 1, (0,0,0))
        self.textdefensive = gstate.get().fontA.render("Defensive", 1, (0,0,0))
        self.textutility = gstate.get().fontA.render("Utility", 1, (0,0,0))
        
    def clock(self):
        super().clock()
        if self.time <= 0:
            return chooseability(self.roundcount, self.stage, self.time)
        else:
            return self

    def draw(self, screen):
        super().draw(screen)

        if gstate.get().craos.stage == 2:
            #escolha de tipo de habilidade :
            pygame.draw.rect(screen, (255,48,48), (320, 290, 160, 30))
            pygame.draw.rect(screen, (30,144,255), (520, 290, 160, 30))
            pygame.draw.rect(screen, (0,201,87), (720, 290, 160, 30))
    ##        pygame.draw.rect(screen, (227,207,87), (490, 295, 20, 20))
    ##        pygame.draw.line(screen, (255,0,0),(490, 295) , (510, 315))
    ##        pygame.draw.line(screen, (255,0,0),(510, 295) , (490, 315))

            screen.blit(self.textoffensive, (330, 295))
            screen.blit(self.textdefensive, (530, 295))
            screen.blit(self.textutility, (730, 295))

    def receiveevent(self, event):
        mouseposition = event.pos
        print(mouseposition)
        if  320 <= mouseposition[0]  <= 480 and 290 <= mouseposition[1] <= 320:
            self.gainabilityoffensive(gstate.get().craos)
            return chooseability(self.roundcount, self.stage, self.time)
        elif  520 <= mouseposition[0]  <= 680 and 290 <= mouseposition[1] <= 320:
            self.gainabilitydefensive(gstate.get().craos)
            return chooseability(self.roundcount, self.stage, self.time)
        elif  720 <= mouseposition[0]  <= 880 and 290 <= mouseposition[1] <= 320:
            self.gainabilityutility(gstate.get().craos)
            return chooseability(self.roundcount, self.stage, self.time)
        return self

    def gainabilityoffensive(self, player):
        #verify if the player already has all the abilities:
        a = True
        offensiveabilities = gstate.get().abilities[player.stage][0] #a list of the offensive abilities of the second stage
        for ab in offensiveabilities:
            if (not (ab.name in [i.name for i in player.abilities])) and (not (ab.name in [i.name for i in player.unlearnedabilities])):
                a = False
        if a:
            pass
        #verify if the player has enough EXP:
        elif player.EXP < abilityprice[player.stage]:
            pass
        else:
            while not a:
                b = R.randint(0,len(offensiveabilities) - 1)
                #verificar se o nome da habilidade não está nos nomes das habilidades do jogador
                if (not (offensiveabilities[b].name in [i.name for i in player.abilities])) and ( not (offensiveabilities[b].name in [i.name for i in player.unlearnedabilities])): 
                    player.abilities.append(offensiveabilities[b].clone())
                    a = True
                    player.EXP -= abilityprice[player.stage]

    def gainabilitydefensive(self, player):
        #verify if the player already has all the abilities:
        a = True
        defensiveabilities = gstate.get().abilities[player.stage][1]
        for ab in defensiveabilities:
            if (not (ab.name in [i.name for i in player.abilities])) and (not (ab.name in [i.name for i in player.unlearnedabilities])):
                a = False
        if a:
            pass
        #verify if the player has enough EXP:
        elif player.EXP < abilityprice[player.stage]:
            pass
        else:
            while not a:
                b = R.randint(0,len(defensiveabilities) - 1)
                #verificar se o nome da habilidade não está nos nomes das habilidades do jogador
                if (not (defensiveabilities[b].name in [i.name for i in player.abilities])) and ( not (defensiveabilities[b].name in [i.name for i in player.unlearnedabilities])):
                #if not (defensiveabilities[b].name in [i.name for i in player.abilities]):
                    player.abilities.append(defensiveabilities[b].clone())
                    a = True
                    player.EXP -= abilityprice[player.stage]
                    
    def gainabilityutility(self, player):
        #verify if the player already has all the abilities:
        a = True
        utilityabilities = gstate.get().abilities[player.stage][2]
        for ab in utilityabilities:
            if (not (ab.name in [i.name for i in player.abilities])) and (not (ab.name in [i.name for i in player.unlearnedabilities])):
                a = False
        if a:
            pass
        #verify if the player has enough EXP:
        elif player.EXP < abilityprice[player.stage]:
            pass
        else:
            while not a:
                b = R.randint(0,len(utilityabilities) - 1)
                #verificar se o nome da habilidade não está nos nomes das habilidades do jogador
                if (not (utilityabilities[b].name in [i.name for i in player.abilities])) and ( not (utilityabilities[b].name in [i.name for i in player.unlearnedabilities])):
                #if not (utilityabilities[b].name in [i.name for i in player.abilities]):
                    player.abilities.append(utilityabilities[b].clone())
                    a = True
                    player.EXP -= abilityprice[player.stage]
#
class gainability2(state):
    def __init__(self, roundcount, stage, time = 30):
        super().__init__(roundcount,stage)
        self.name = "choose ability type"
        self.time = time
        self.time1 = time
        self.renderables.append(circle0)
        self.renderables.append(circle1)
        self.renderables.append(circle2)
        self.renderables.append(circle3)
        self.renderables.append(circle4)
        self.done1 = False
        self.done2 = False
        self.element = " "
        
    def clock(self):
        super().clock()
        if self.time <= 0:
            return chooseability(self.roundcount, self.stage, self.time)
        else:
            return self

    def draw(self, screen):
        super().draw(screen)

    def effect(self):
        if self.element != " " and not self.done1:
            self.done1 = True
            self.renderables.remove(circle0)
            self.renderables.remove(circle1)
            self.renderables.remove(circle2)
            self.renderables.remove(circle3)
            self.renderables.remove(circle4)
            
            self.renderables.append(rectrenderable(320, 290, 160, 30, (255, 48, 48)))
            self.renderables.append(rectrenderable(520, 290, 160, 30, (30, 144, 255)))
            self.renderables.append(rectrenderable(720, 290, 160, 30, (0, 201, 87)))
            self.renderables.append(textrenderable(330, 295, (0,0,0), gstate.get().fontA, lambda: "Offensive"))
            self.renderables.append(textrenderable(530, 295, (0,0,0), gstate.get().fontA, lambda: "Defensive"))
            self.renderables.append(textrenderable(730, 295, (0,0,0), gstate.get().fontA, lambda: "Utility"))
        return self

    def receiveevent(self, event):
        mouseposition = event.pos
        print(mouseposition)
        if not self.done1:
            if ((mouseposition[0] - 380)**2 + (mouseposition[1] - 300)**2) <= 40**2:
                self.element = 0
            elif ((mouseposition[0] - 480)**2 + (mouseposition[1] - 300)**2) <= 40**2:
                self.element = 1
            elif ((mouseposition[0] - 580)**2 + (mouseposition[1] - 300)**2) <= 40**2:
                self.element = 2
            elif ((mouseposition[0] - 680)**2 + (mouseposition[1] - 300)**2) <= 40**2:
                self.element = 3
            elif ((mouseposition[0] - 780)**2 + (mouseposition[1] - 300)**2) <= 40**2:
                self.element = 4
            if not gstate.get().craos.starterpacks[self.element]:
                self.gainstarterpack(gstate.get().craos, self.element)
                return chooseability(self.roundcount, self.stage, self.time)
            return self
        else:
            if  320 <= mouseposition[0]  <= 480 and 290 <= mouseposition[1] <= 320:
                self.gainabilityoffensive(gstate.get().craos)
                return chooseability(self.roundcount, self.stage, self.time)
            elif  520 <= mouseposition[0]  <= 680 and 290 <= mouseposition[1] <= 320:
                self.gainabilitydefensive(gstate.get().craos)
                return chooseability(self.roundcount, self.stage, self.time)
            elif  720 <= mouseposition[0]  <= 880 and 290 <= mouseposition[1] <= 320:
                self.gainabilityutility(gstate.get().craos)
                return chooseability(self.roundcount, self.stage, self.time)
            return self
            
        

    def gainabilityoffensive(self, player):
        #verify if the player already has all the abilities:
        a = True
        offensiveabilities = gstate.get().abilities[player.stage][self.element][0] #a list of the offensive abilities of the third stage
        for ab in offensiveabilities:
            if (not (ab.name in [i.name for i in player.abilities])) and (not (ab.name in [i.name for i in player.unlearnedabilities])):
                a = False
        if a:
            pass
        #verify if the player has enough EXP:
        elif player.EXP < abilityprice[player.stage]:
            pass
        else:
            #offensiveabilities1 = [ab for ab in offensiveabilities if ab.proficiencyneeded <= player.proficiencies[self.element]]
            if offensiveabilities == []:
                pass
            else:
                while not a:
                    b = R.randint(0,len(offensiveabilities) - 1)
                    #verificar se o nome da habilidade não está nos nomes das habilidades do jogador
                    if (not (offensiveabilities[b].name in [i.name for i in player.abilities])) and ( not (offensiveabilities[b].name in [i.name for i in player.unlearnedabilities])): 
                        c = R.random()
                        d = offensiveabilities[b].proficiencyneeded - player.proficiencies[self.element]
                        print(offensiveabilities[b].name)
                        print(str(offensiveabilities[b].proficiencyneeded))
                        print("c: " + str(c))
                        print("d: " + str(d) + "    1/d:" + str(1/d))
                        print()
                        if d <= 1:
                            d = 1
                        if c < (1 / d):
                            player.abilities.append(offensiveabilities[b].clone())
                            a = True
                            player.EXP -= abilityprice[player.stage]

    def gainabilitydefensive(self, player):
        #verify if the player already has all the abilities:
        a = True
        defensiveabilities = gstate.get().abilities[player.stage][self.element][1]
        for ab in defensiveabilities:
            if (not (ab.name in [i.name for i in player.abilities])) and (not (ab.name in [i.name for i in player.unlearnedabilities])):
                a = False
        if a:
            pass
        #verify if the player has enough EXP:
        elif player.EXP < abilityprice[player.stage]:
            pass
        else:
            #defensiveabilities1 = [ab for ab in defensiveabilities if ab.proficiencyneeded <= player.proficiencies[self.element]]
            if defensiveabilities == []:
                pass
            else:
                while not a:
                    b = R.randint(0,len(defensiveabilities) - 1)
                    #verificar se o nome da habilidade não está nos nomes das habilidades do jogador
                    if (not (defensiveabilities[b].name in [i.name for i in player.abilities])) and ( not (defensiveabilities[b].name in [i.name for i in player.unlearnedabilities])):
                        c = R.random()
                        d = defensiveabilities[b].proficiencyneeded - player.proficiencies[self.element]
                        print(defensiveabilities[b].name)
                        print(str(defensiveabilities[b].proficiencyneeded))
                        print("c: " + str(c))
                        print("d: " + str(d) + "    1/d:" + str(1/d))
                        print()
                        if d <= 1:
                            d = 1
                        if c < (1 / d):
                            player.abilities.append(defensiveabilities[b].clone())
                            a = True
                            player.EXP -= abilityprice[player.stage]
                    
    def gainabilityutility(self, player):
        #verify if the player already has all the abilities:
        a = True
        utilityabilities = gstate.get().abilities[player.stage][self.element][2]
        for ab in utilityabilities:
            if (not (ab.name in [i.name for i in player.abilities])) and (not (ab.name in [i.name for i in player.unlearnedabilities])):
                a = False
        if a:
            pass
        #verify if the player has enough EXP:
        elif player.EXP < abilityprice[player.stage]:
            pass
        else:
            #utilityabilities1 = [ab for ab in utilityeabilities if ab.proficiencyneeded <= player.proficiencies[self.element]]
            if utilityabilities == []:
                pass
            else:
                while not a:
                    b = R.randint(0,len(utilityabilities) - 1)
                    #verificar se o nome da habilidade não está nos nomes das habilidades do jogador
                    if (not (utilityabilities[b].name in [i.name for i in player.abilities])) and ( not (utilityabilities[b].name in [i.name for i in player.unlearnedabilities])):
                        c = R.random()
                        d = utilityabilities[b].proficiencyneeded - player.proficiencies[self.element]
                        print(utilityabilities[b].name)
                        print(str(utilityabilities[b].proficiencyneeded))
                        print("c: " + str(c))
                        print("d: " + str(d) + "    1/d:" + str(1/d))
                        print()
                        if d <= 1:
                            d = 1
                        if c < (1 / d):
                            player.abilities.append(utilityabilities[b].clone())
                            a = True
                            player.EXP -= abilityprice[player.stage]
                        
    def gainstarterpack(self, creature, element):
        if element == 0:
            creature.starterpacks[0] = True
            for ab in gstate.get().starterpacks[0]:
                creature.abilities.append(ab.clone())
        elif element == 1:
            creature.starterpacks[1] = True
            for ab in gstate.get().starterpacks[1]:
                creature.abilities.append(ab.clone())
        elif element == 2:
            creature.starterpacks[2] = True
            for ab in gstate.get().starterpacks[2]:
                creature.abilities.append(ab.clone())
        elif element == 3:
            creature.starterpacks[3] = True
            for ab in gstate.get().starterpacks[3]:
                creature.abilities.append(ab.clone())
        elif element == 4:
            creature.starterpacks[4] = True
            for ab in gstate.get().starterpacks[4]:
                creature.abilities.append(ab.clone())
#
class buffbet1(state):
    def __init__(self, roundcount, stage, time = 30, buffnumber = 1):
        super().__init__(roundcount, stage)
        self.name = "Betting time!"
        self.time = time
        self.time1 = time
        self.buffnumber = buffnumber
        #self.buffnumber = 4
        self.buff = self.pickbuff()
        self.done = False
        #self.done = True
        self.renderables = [textrenderable(300, 10, (255,0,0), gstate.get().fonttime, lambda: self.name + ":" + str(self.time)),
                            textrenderable(300, 30, (0,0,255), gstate.get().fonttime, lambda: "round:" + str(self.roundcount) + "/" + str(evolveround[stage])),
                            rectrenderable(770, 380, 40, 40, (227,207,87)),
                            rectrenderable(830, 380, 40, 40, (227,207,87)),
                            rectrenderable(890, 380, 40, 40, (227,207,87)),
                            rectrenderable(950, 380, 40, 40, (227,207,87)),
                            rectrenderable(770, 460, 40, 40, (227,207,87)),
                            rectrenderable(830, 460, 40, 40, (227,207,87)),
                            rectrenderable(890, 460, 40, 40, (227,207,87)),
                            rectrenderable(950, 460, 40, 40, (227,207,87)),
                            rectrenderable(780, 90, 100 , 30,(227,207,87)),
                            textrenderable(780, 50, (0,255,0), gstate.get().fonttime, lambda : "BET:" + str(gstate.get().craos.bet)),
                            textrenderable(780, 390, (0,0,0), gstate.get().fontA, lambda: "+1"),
                            textrenderable(840, 390, (0,0,0), gstate.get().fontA, lambda: "+5"),
                            textrenderable(890, 390, (0,0,0), gstate.get().fontA, lambda: "+10"),
                            textrenderable(950, 390, (0,0,0), gstate.get().fontA, lambda: "+50"),
                            textrenderable(780, 470, (0,0,0), gstate.get().fontA, lambda: "-1"),
                            textrenderable(840, 470, (0,0,0), gstate.get().fontA, lambda: "-5"),
                            textrenderable(890, 470, (0,0,0), gstate.get().fontA, lambda: "-10"),
                            textrenderable(950, 470, (0,0,0), gstate.get().fontA, lambda: "-50"),
                            textrenderable(780, 95, (0,0,0), gstate.get().fontHP, lambda: "Place your Bet")]
                            
        if self.buff.bufftype1 == "Blessing":
            self.renderables.append(rectrenderable(320, 260, 670, 100, (255,185,15)))
            self.renderables.append(textrenderable(330, 300, (255,0,0), gstate.get().fontA, lambda: self.buff.text))
        elif self.buff.bufftype1 == "Curse":
            self.renderables.append(rectrenderable(320, 260, 670, 100, (138,43,226)))
            self.renderables.append(textrenderable(330, 300, (0,0,255), gstate.get().fontA, lambda: self.buff.text))

                            
    def clock(self):
        super().clock()
        if self.time <= 0:
            pass
        return self
        
    def draw(self, screen):
        super().draw(screen)
        
            
    def effect(self):
        if self.done:
            if self.buffnumber < 4:
                for p in gstate.get().players:
                    p.bet = 0
                return buffbet1(self.roundcount, self.stage, buffnumber = self.buffnumber + 1)
                
            elif self.buffnumber == 4:
                return evolve1(self.roundcount, self.stage)
            else:
                print("wtf?!")
        else:
            return self
            
    def receiveevent(self, event):
        mouseposition = event.pos
        print(str(mouseposition))
        if 770 <= mouseposition[0] <= 810 and 380 <= mouseposition[1] <= 420:
            self.addbet(1)
        elif 830 <= mouseposition[0] <= 870 and 380 <= mouseposition[1] <= 420:
            self.addbet(5)
        elif 890 <= mouseposition[0] <= 930 and 380 <= mouseposition[1] <= 420:
            self.addbet(10)
        elif 950 <= mouseposition[0] <= 990 and 380 <= mouseposition[1] <= 420:
            self.addbet(50)
        elif 770 <= mouseposition[0] <= 810 and 460 <= mouseposition[1] <= 500:
            self.addbet(-1)
        elif 830 <= mouseposition[0] <= 870 and 460 <= mouseposition[1] <= 500:
            self.addbet(-5)
        elif 890 <= mouseposition[0] <= 930 and 460 <= mouseposition[1] <= 500:
            self.addbet(-10)
        elif 950 <= mouseposition[0] <= 990 and 405 <= mouseposition[1] <= 500:
            self.addbet(-50)
        elif 780 <= mouseposition[0] <= 880 and 90 <= mouseposition[1] <= 120:
            if self.buff.bufftype1 == "Blessing":
                self.calculateblessing()
            elif self.buff.bufftype1 == "Curse":
                self.calculatecurse()
        return self
    
    def pickbuff(self):
        if self.buffnumber < 4:
            i = R.randint(0, len(gstate.get().buffs[1][0]) - 1)
            r = gstate.get().buffs[1][0][i]
        elif self.buffnumber == 4:
            i = R.randint(0, len(gstate.get().buffs[1][1]) - 1)
            r = gstate.get().buffs[1][1][i]
        else:
            print("wtf? o.O")
        return r

    
    def addbet(self, n):
        a = gstate.get().craos.bet + n
        if a < 0:
            a = 0
        if a > gstate.get().craos.EXP:
            a = gstate.get().craos.EXP
        gstate.get().craos.bet = a
        
    def calculateblessing(self):
        for n in gstate.get().npcs: #make npc's bet
            a = R.randint(0, n.EXP)
            n.bet = a
        b = 1
        winner = []
        for p in gstate.get().players:
            if p.bet > b:
                winner = [p]
                b = p.bet
            elif p.bet == b:
                winner.append(p)
        for p in gstate.get().players:
            p.EXP -= p.bet
            print(p.name + " placed a bet of " + str(p.bet))
        for w in winner:
            self.buff.effect(w)
            print(w.name + " won this bet!")
        
        self.done = True
        
    def calculatecurse(self):
        for n in gstate.get().npcs: #make npc's bet
            a = R.randint(0, n.EXP)
            n.bet = a
        b = 10000000000
        winner = []
        for p in gstate.get().players:
            if p.bet < b:
                winner = [p]
                b = p.bet
            elif p.bet == b:
                winner.append(p)
        for p in gstate.get().players:
            p.EXP -= p.bet
            print(p.name + " placed a bet of " + str(p.bet))
        for w in winner:
            self.buff.effect(w)
            print(w.name + " lost this bet!")
        
        self.done = True
        
class buffbet2(state):

    def __init__(self, roundcount, stage, time = 30, buffnumber = 1):
        super().__init__(roundcount, stage)
        self.name = "Betting time!"
        self.time = time
        self.time1 = time
        #self.buffnumber = buffnumber
        self.buffnumber = 4
        self.buff = self.pickbuff()
        self.done = True
        #self.done = False
        self.renderables = [textrenderable(300, 10, (255,0,0), gstate.get().fonttime, lambda: self.name + ":" + str(self.time)),
                            textrenderable(300, 30, (0,0,255), gstate.get().fonttime, lambda: "round:" + str(self.roundcount) + "/" + str(evolveround[stage])),
                            rectrenderable(770, 380, 40, 40, (227,207,87)),
                            rectrenderable(830, 380, 40, 40, (227,207,87)),
                            rectrenderable(890, 380, 40, 40, (227,207,87)),
                            rectrenderable(950, 380, 40, 40, (227,207,87)),
                            rectrenderable(770, 460, 40, 40, (227,207,87)),
                            rectrenderable(830, 460, 40, 40, (227,207,87)),
                            rectrenderable(890, 460, 40, 40, (227,207,87)),
                            rectrenderable(950, 460, 40, 40, (227,207,87)),
                            rectrenderable(780, 90, 100 , 30,(227,207,87)),
                            textrenderable(780, 50, (0,255,0), gstate.get().fonttime, lambda : "BET:" + str(gstate.get().craos.bet)),
                            textrenderable(780, 390, (0,0,0), gstate.get().fontA, lambda: "+1"),
                            textrenderable(840, 390, (0,0,0), gstate.get().fontA, lambda: "+5"),
                            textrenderable(890, 390, (0,0,0), gstate.get().fontA, lambda: "+10"),
                            textrenderable(950, 390, (0,0,0), gstate.get().fontA, lambda: "+50"),
                            textrenderable(780, 470, (0,0,0), gstate.get().fontA, lambda: "-1"),
                            textrenderable(840, 470, (0,0,0), gstate.get().fontA, lambda: "-5"),
                            textrenderable(890, 470, (0,0,0), gstate.get().fontA, lambda: "-10"),
                            textrenderable(950, 470, (0,0,0), gstate.get().fontA, lambda: "-50"),
                            textrenderable(780, 95, (0,0,0), gstate.get().fontHP, lambda: "Place your Bet")]
                            
        if self.buff.bufftype1 == "Blessing":
            self.renderables.append(rectrenderable(320, 260, 670, 100, (255,185,15)))
            self.renderables.append(textrenderable(330, 300, (255,0,0), gstate.get().fontA, lambda: self.buff.text))
        elif self.buff.bufftype1 == "Curse":
            self.renderables.append(rectrenderable(320, 260, 670, 100, (138,43,226)))
            self.renderables.append(textrenderable(330, 300, (0,0,255), gstate.get().fontA, lambda: self.buff.text))

                            
    def clock(self):
        super().clock()
        if self.time <= 0:
            pass
        return self
        
    def draw(self, screen):
        super().draw(screen)
        
            
    def effect(self):
        if self.done:
            if self.buffnumber < 4:
                for p in gstate.get().players:
                    p.bet = 0
                return buffbet2(self.roundcount, self.stage, buffnumber = self.buffnumber + 1)
                
            elif self.buffnumber == 4:
                return evolve2(self.roundcount, self.stage)
            else:
                print("wtf?! buffbet2")
        else:
            return self
            
    def receiveevent(self, event):
        mouseposition = event.pos
        print(str(mouseposition))
        if 770 <= mouseposition[0] <= 810 and 380 <= mouseposition[1] <= 420:
            self.addbet(1)
        elif 830 <= mouseposition[0] <= 870 and 380 <= mouseposition[1] <= 420:
            self.addbet(5)
        elif 890 <= mouseposition[0] <= 930 and 380 <= mouseposition[1] <= 420:
            self.addbet(10)
        elif 950 <= mouseposition[0] <= 990 and 380 <= mouseposition[1] <= 420:
            self.addbet(50)
        elif 770 <= mouseposition[0] <= 810 and 460 <= mouseposition[1] <= 500:
            self.addbet(-1)
        elif 830 <= mouseposition[0] <= 870 and 460 <= mouseposition[1] <= 500:
            self.addbet(-5)
        elif 890 <= mouseposition[0] <= 930 and 460 <= mouseposition[1] <= 500:
            self.addbet(-10)
        elif 950 <= mouseposition[0] <= 990 and 405 <= mouseposition[1] <= 500:
            self.addbet(-50)
        elif 780 <= mouseposition[0] <= 880 and 90 <= mouseposition[1] <= 120:
            if self.buff.bufftype1 == "Blessing":
                self.calculateblessing()
            elif self.buff.bufftype1 == "Curse":
                self.calculatecurse()
        return self
    
    def pickbuff(self):
        if self.buffnumber < 4:
            i = R.randint(0, len(gstate.get().buffs[2][0]) - 1)
            r = gstate.get().buffs[2][0][i]
        elif self.buffnumber == 4:
            i = R.randint(0, len(gstate.get().buffs[2][1]) - 1)
            r = gstate.get().buffs[2][1][i]
        else:
            print("wtf? o.O pickbuff buffbet2")
        return r

    
    def addbet(self, n):
        a = gstate.get().craos.bet + n
        if a < 0:
            a = 0
        if a > gstate.get().craos.EXP:
            a = gstate.get().craos.EXP
        gstate.get().craos.bet = a
        
    def calculateblessing(self):
        for n in gstate.get().npcs: #make npc's bet
            a = R.randint(0, n.EXP)
            n.bet = a
        b = 1
        winner = []
        for p in gstate.get().players:
            if p.bet > b:
                winner = [p]
                b = p.bet
            elif p.bet == b:
                winner.append(p)
        for p in gstate.get().players:
            p.EXP -= p.bet
            print(p.name + " placed a bet of " + str(p.bet))
        for w in winner:
            self.buff.effect(w)
            print(w.name + " won this bet!")
        
        self.done = True
        
    def calculatecurse(self):
        for n in gstate.get().npcs: #make npc's bet
            a = R.randint(0, n.EXP)
            n.bet = a
        b = 10000000000
        winner = []
        for p in gstate.get().players:
            if p.bet < b:
                winner = [p]
                b = p.bet
            elif p.bet == b:
                winner.append(p)
        for p in gstate.get().players:
            p.EXP -= p.bet
            print(p.name + " placed a bet of " + str(p.bet))
        for w in winner:
            self.buff.effect(w)
            print(w.name + " lost this bet!")
        
        self.done = True
        
class PVEfight(state):

    def __init__(self, roundcount, stage, time):
        self.name = "Lets Fight Some Circles!"
        self.roundcount = roundcount
        self.stage = stage
        self.time = time 
        self.time1 = time 
        self.subround = 1
        self.renderables = [circlerenderable(500,500, 20, (255,0,0))]
        
    def draw(self, screen):
        pygame.draw.rect(screen, (0,0,0), (0,0, width, height))
        gstate.get().craos.drawabilities(screen)
        for r in self.renderables:
            r.draw(screen)
        gstate.get().craos.draw(screen)
        
class endgame(state):
    def __init__(self, roundcount, stage, victor):
        super().__init__(roundcount, stage)
        self.name = "Endgame"
        self.time = 5
        self.time1 = 5
        self.victor = victor
        self.renderables = []
        self.texttie = textrenderable(0, 0, (255,193,37), gstate.get().fontend, lambda: "Its a Tie! :|")
        self.textlose = textrenderable(0, 0, (255,0,0), gstate.get().fontend, lambda: "LOSER! :(")
        self.textwin = textrenderable(0, 0, (0,255,0), gstate.get().fontend, lambda: "YOU WIN :D")
        self.renderables = [textrenderable(0, 0, (0,255,0), gstate.get().fontend, lambda: "YOU WIN :D")]
        
    def clock(self):
        super().clock()
        if self.time <= 0:
            gstate.get().run = False
            return self
        else:
            return self
        
    
    
    def draw(self, screen):
        #supper().draw(screen)
        if self.victor == "win":
            self.textwin.draw(screen)
        elif self.victor == "tie":
            self.texttie.draw(screen)
        elif self.victor == "lose":
            self.textlose.draw(screen)
            
class startgame(state):
    def __init__(self, roundcount, stage, time = 0):
        super().__init__(roundcount, stage)
        self.name = "Welcome!"
        self.time = time
        self.time1 = time
        self.renderables.append(rectrenderable(320, 290, 160, 30, (227,207,87)))
        self.renderables.append(rectrenderable(720, 290, 160, 30, (227,207,87)))
        
    def clock(self):
        return self
            
    def effect(self): 
        return self


    def draw(self, screen):
        pygame.draw.rect(screen, (0,0,0), (0,0, width, height))
        for r in self.renderables:
            r.draw(screen)
    

    def receiveevent(self, event):
        pass
