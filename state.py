import random as R
from globals import *
from creature import *
from abilities import *
import gstate
import math

class state():

    def __init__(self, roundcount):
        self.roundcount = roundcount
        self.renderables = []
        
    def clock(self):
        self.time1 = self.time1 - 0.1
        self.time = math.ceil(self.time1)
        self.texttime = gstate.get().fonttime.render(self.name + ":" + str(self.time), 1, (255,0,0))
        for i in range(10):
            pygame.time.delay(10)
    
    def draw(self, screen):
        pygame.draw.rect(screen, (0,0,0), (0,0, width, height))
        gstate.get().craos.drawabilities(screen)
        screen.blit(self.texttime, (300, 10))
        screen.blit(self.textround, (300, 30))
        for r in self.renderables:
            r.draw(screen)
        for player in gstate.get().players:
            player.draw(screen)
        for corpse in gstate.get().deadcorpses:
            corpse.draw(screen)
            
    def effect(self):
        return self
            
    def receiveevent(self):
        return self
       
class chooseability(state):

    def __init__(self, roundcount, time = 900):
        super().__init__(roundcount)
        self.name = "choose ability"
        self.time = time
        self.time1 = time
        self.texttime = gstate.get().fonttime.render(self.name + ":" + str(self.time), 1, (255,0,0))
        self.textround = gstate.get().fonttime.render("round:" + str(self.roundcount), 1, (0, 0, 255))
        self.textgainability = gstate.get().fontA.render("learn ability", 1, (0,0,0))
        self.textevolve = gstate.get().fontA.render("EVOLVE!", 1, (0,0,0))
        self.textunlearnability = gstate.get().fontA.render("Unlearn ability", 1, (0,0,0))

    def clock(self):
        super().clock()
        if self.time <= 0:
            gstate.get().craos.ability = ability("passed",3, 0, True, 1, False)
            print(str(gstate.get().craos.ability.name))
            
            for npc in gstate.get().npcs:#npc's tambem escolhem as habilidades
                        npc.chooseability()            
            return choosetarget(self.roundcount, self.time)
        else:
            return self
            
    def effect(self): 
                #verify if the game ended:
        if len(gstate.get().players) == 0:
            return endgame(self.roundcount, "tie")

        else:
            for corpse in gstate.get().deadcorpses:
                if corpse.name == "craos":
                    return endgame(self.roundcount, "lose")


        if len(gstate.get().players) == 1 and gstate.get().players[0].name == "craos":
            return endgame(self.roundcount, "win")
        else:
            return self


    def draw(self, screen):
        super().draw(screen)
        #escolha de habilidade ou evoluir ou desaprender:
        pygame.draw.rect(screen, (227,207,87), (320, 290, 160, 30))
        pygame.draw.rect(screen, (227,207,87), (520, 290, 160, 30))
        pygame.draw.rect(screen, (227,207,87), (720, 290, 160, 30))

        screen.blit(self.textgainability, (330, 295))
        screen.blit(self.textevolve, (530, 295))
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
                    for npc in gstate.get().npcs:#npc's tambem escolhem as habilidades
                        npc.chooseability()

                    for player in gstate.get().players:#fazer os efeitos que atuam agora
                        for condition in player.conditions:
                            if condition.priority == "chooseability":
                                condition.effect()
                    return choosetarget(self.roundcount, self.time)
                else:
                    print("this ability is in cooldown")# for" " + str(gstate.get().craos.abilitiesincooldown[i]) + " turns.")

        #ganhar habilidade
        if 320 <= mouseposition[0] <= 480 and 290 <= mouseposition[1] <= 320:
            print("ganhar habilidade")
            if gstate.get().craos.EXP < abilityprice[gstate.get().craos.stage]:
                print("not enough EXP")
            else:
                if gstate.get().craos.stage == 1:
                    self.gainability(gstate.get().craos)
                elif gstate.get().craos.stage == 2:
                    return gainability2(self.roundcount, self.time)
        #evoluir            
        elif 520 <= mouseposition[0] <= 680 and 290 <= mouseposition[1] <= 320:
            print("evoluir")
            return self.evolve(gstate.get().craos)
        #desaprender habilidade:
        elif 720 <= mouseposition[0] <= 880 and 290 <= mouseposition[1] <= 320:
            print("desaprender habilidade")
            return loseability(self.roundcount, self.time)
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

    def gainabilityforfree(self, player):
        #verify if the player already has all the abilities:
        a = True
        stageabilities = gstate.get().abilities[player.stage]
        for ab in stageabilities:
            if (not (ab.name in [i.name for i in player.abilities])) and (not (ab.name in [i.name for i in player.unlearnedabilities])):
                a = False
        if a:
            pass
        else:
            while not a:
                b = R.randint(0,len(stageabilities) - 1)
                print()
                print(b)
                print()
                #verificar se o nome da habilidade não está nos nomes das habilidades do jogador
                if (not (stageabilities[b].name in [i.name for i in player.abilities])) and ( not (stageabilities[b].name in [i.name for i in player.unlearnedabilities])):
                #if not (stageabilities[b].name in [i.name for i in player.abilities]):
                    player.abilities.append(stageabilities[b].clone())
                    a = True
                  

    def evolve(self, player):
        #verify if the player has enough EXP:
        if player.EXP < evolveprice[player.stage]:
            print("Not enought EXP")
            return self
        elif player.stage == 2:
            print("ainda nao esta implementado evoluires mais :(")
            return self
        else:
            player.EXP -= evolveprice[player.stage]
            player.HP += evolveHPgain[player.stage]
            player.MaxHP += evolveHPgain[player.stage]
            player.EXPtoevolve = evolveEXP[player.stage + 1]
            player.stage += 1
            return evolve1(self.roundcount, self.time)
            
#__________________________________________________________________________________________________________________________________________________________________________________
class choosetarget(state):
    def __init__(self, roundcount, time = 30):
        super().__init__(roundcount)
        #self.caster = caster
        #self.target = []
        #self.ability = ability
        self.name = "Choose Target"
        self.time = time
        self.time1 = time
        self.texttime = gstate.get().fonttime.render(self.name + ":" + str(self.time), 1, (255,0,0))
        self.textround = gstate.get().fonttime.render("round:" + str(self.roundcount), 1, (0, 0, 255))
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
            return chooseability(self.roundcount, self.time)

        if self.targetnumber <= 0: #se ja estao os targets todos escolhidos, siga em frente
            
            for npc in gstate.get().npcs: #escolher target dos gstate.get().npcs
                npc.choosetarget(npc.ability.targetnumber, npc.ability.selftarget)

            for player in gstate.get().players: #condiçoes que atuam agora:
                for condition in player.conditions:
                    if condition.priority == "after choosetarget":
                        condition.effect()
                        
            return calculateeffects(self.roundcount)
            
        #se a habilidade escolhida é de channel, e não vai fazer o efeito este turno, siga a marinha
        if gstate.get().craos.ability.channel > 0:#se a habilidade escolhida tem channel:
            if gstate.get().craos.ability.name in [i[0] for i in gstate.get().craos.abilitiesinchannel]: #se o player ja esta a dar channel à habilidade
                a = [i[0] == gstate.get().craos.ability.name for i in gstate.get().craos.abilitiesinchannel].index(True)
                print(str(gstate.get().craos.abilitiesinchannel[a]))
                if gstate.get().craos.abilitiesinchannel[a][1] >= 2: #se a habilidade nao vai atuar este turno
                    for npc in gstate.get().npcs: #escolher target dos gstate.get().npcs
                        npc.choosetarget(npc.ability.targetnumber, npc.ability.selftarget)

                    for player in gstate.get().players: #condiçoes que atuam agora:
                        for condition in player.conditions:
                            if condition.priority == "after choosetarget":
                                condition.effect()
                        
                    return calculateeffects(self.roundcount)
                else:
                    if ((self.targetnumber >= (len(gstate.get().players) - 1)) and not gstate.get().craos.ability.selftarget): #se a habilidade tem toda a gente como target, siga
                        for p in gstate.get().npcs:    
                            gstate.get().craos.target.append(p)
                        for npc in gstate.get().npcs:#escolher o target dos gstate.get().npcs
                            npc.choosetarget(npc.ability.targetnumber, npc.ability.selftarget)

                        for player in gstate.get().players: #condiçoes que atuam agora:
                            for condition in player.conditions:
                                if condition.priority == "after choosetarget":
                                    condition.effect()
                          
                        return calculateeffects(self.roundcount)
                        
                    elif self.targetnumber >= len(gstate.get().players):
                        for p in gstate.get().players:    
                            gstate.get().craos.target.append(p)
                        for npc in gstate.get().npcs:#escolher o target dos gstate.get().npcs
                            npc.choosetarget(npc.ability.targetnumber, npc.ability.selftarget)

                        for player in gstate.get().players: #condiçoes que atuam agora:
                            for condition in player.conditions:
                                if condition.priority == "after choosetarget":
                                    condition.effect()
                          
                        return calculateeffects(self.roundcount)

                    
                    
            elif not (gstate.get().craos.ability.name in [i[0] for i in gstate.get().craos.abilitiesinchannel]): #se o player ainda nao esta a dar channel à habilidade:
                for npc in gstate.get().npcs: #escolher target dos gstate.get().npcs
                    npc.choosetarget(npc.ability.targetnumber, npc.ability.selftarget)

                for player in gstate.get().players: #condiçoes que atuam agora:
                    for condition in player.conditions:
                        if condition.priority == "after choosetarget":
                            condition.effect()
                            
                return calculateeffects(self.roundcount)
            
                
        elif ((self.targetnumber >= (len(gstate.get().players) - 1)) and not gstate.get().craos.ability.selftarget): #se a habilidade tem toda a gente como target, siga
            for p in gstate.get().npcs:    
                gstate.get().craos.target.append(p)
            
            for npc in gstate.get().npcs:#escolher o target dos gstate.get().npcs
                npc.choosetarget(npc.ability.targetnumber, npc.ability.selftarget)

            for player in gstate.get().players: #condiçoes que atuam agora:
                for condition in player.conditions:
                    if condition.priority == "after choosetarget":
                        condition.effect()
              
            return calculateeffects(self.roundcount)

        elif self.targetnumber >= len(gstate.get().players): #se a habilidade tem toda a gente como target, siga
            for p in gstate.get().players:    
                gstate.get().craos.target.append(p)
            
            for npc in gstate.get().npcs:#escolher o target dos gstate.get().npcs
                npc.choosetarget(npc.ability.targetnumber, npc.ability.selftarget)

            for player in gstate.get().players: #condiçoes que atuam agora:
                for condition in player.conditions:
                    if condition.priority == "after choosetarget":
                        condition.effect()
              
            return calculateeffects(self.roundcount)
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
            return chooseability(self.roundcount, self.time)
        else:
            return self
#__________________________________________________________________________________________________________________________________________________________________________________
class calculateeffects(state):
    def __init__(self, roundcount):
        super().__init__(roundcount)
        self.name = "calculating effects"
        self.time = 30
        self.time1 = 30
        self.texttime = gstate.get().fonttime.render(self.name + ":" + str(self.time), 1, (255,0,0))
        self.textround = gstate.get().fonttime.render("round:" + str(self.roundcount), 1, (0, 0, 255))

    def clock(self):
        super().clock()
        return calculateeffects(self.roundcount)

    def effect(self):
        #phase 1 of combat:
        for player in gstate.get().players:#effects of priority 1 abilities
            if player.ability.priority == 1:
                player.ability.effect(player.target, player)
                
            for condition in player.conditions: #conditions with priority 1
                if condition.priority == 1:
                    condition.effect()

        self.deathcheck() #check if anyone died
        
        # for player in gstate.get().players: #check if anyone died
            # if player.HP <= 0:
                # gstate.get().deadcorpses.append(deadcorpse(player.pos[0], player.pos[1], player.name, player.color, player.HP, player.MaxHP, player.abilitylastused, player.abilitylasttarget, player.EXP, player.EXPtoevolve))
                # gstate.get().players.remove(player)
        # for npc in gstate.get().npcs:
            # if npc.HP <=0:
                # gstate.get().npcs.remove(npc)




        
        #phase 2 of combat:     
        for player in gstate.get().players:#effects of priority 2 abilities
            if player.ability.priority == 2:
                player.ability.effect(player.target, player)
                
            for condition in player.conditions: #conditions of priority 2
                if condition.priority == 2:
                    condition.effect()

        self.deathcheck() #check if anyone died
        
        # for player in gstate.get().players: #check if anyone died
            # if player.HP <= 0:
                # gstate.get().deadcorpses.append(deadcorpse(player.pos[0], player.pos[1], player.name, player.color, player.HP, player.MaxHP, player.abilitylastused, player.abilitylasttarget, player.EXP, player.EXPtoevolve))
                # gstate.get().players.remove(player)
        # for npc in gstate.get().npcs:
            # if npc.HP <=0:
                # gstate.get().npcs.remove(npc)
        


        #phase 3 of combat    
        for player in gstate.get().players:#effects of priority 3 abilities
            if player.ability.priority == 3:
                player.ability.effect(player.target, player)

            for condition in player.conditions: #conditions of priority 3
                if condition.priority == 3:
                    condition.effect()
            
        self.deathcheck() #check if anyone died
        

        #phase 4 of combat    
        for player in gstate.get().players:#effects of priority 4 abilities
            if player.ability.priority == 4:
                player.ability.effect(player.target, player)

            for condition in player.conditions: #conditions of priority 4
                if condition.priority == 4:
                    condition.effect()
            
        self.deathcheck() #check if anyone died
        # for player in gstate.get().players: 
            # if player.HP <= 0:
                # gstate.get().deadcorpses.append(deadcorpse(player.pos[0], player.pos[1], player.name, player.color, player.HP, player.MaxHP, player.abilitylastused, player.abilitylasttarget, player.EXP, player.EXPtoevolve))
                # if player.name in [i.name for i in gstate.get().npcs]:
                    # gstate.get().players.remove(player)
                    # gstate.get().npcs.remove(player)
                # else:
                    # gstate.get().players.remove(player)
                
        



        #level up the npc's
        if gstate.get().craos.stage == 2:
            for npc in gstate.get().npcs:
                if npc.stage == 1:
                    if npc.EXP >=evolveprice[npc.stage]:
                        npc.EXP -= evolveprice[npc.stage]
                        npc.HP += evolveHPgain[npc.stage]
                        npc.MaxHP += evolveHPgain[npc.stage]
                        npc.EXPtoevolve = evolveEXP[npc.stage + 1]
                        npc.stage += 1
                        npc.abilities = []
                        self.gainabilityoffensive(npc)
                        self.gainabilityoffensive(npc)
                        self.gainabilitydefensive(npc)
        
        
        
        #print([[a[0].name, a[1], a[2].name] for a in gstate.get().log])
        print([[a.name, a.priority, a.duration] for a in gstate.get().craos.conditions])
        for p in gstate.get().players: #conditions that act at the end of the round.
            for c in p.conditions:
                if condition.priority == "endround":
                    c.effect()
        
        
        for player in gstate.get().players:
            player.startnewround()
            
        gstate.get().log = []   
        print()
        print("round: " + str(self.roundcount + 1))
       
        return chooseability(self.roundcount + 1)
        

    def deathcheck(self):
        gstate.get().deadcorpses = gstate.get().deadcorpses + [deadcorpse(p.pos[0], p.pos[1], p.name, p.color, p.HP, p.MaxHP, p.abilitylastused, p.abilitylasttarget, p.EXP, p.EXPtoevolve) for p in gstate.get().players if p.HP <= 0]
        gstate.get().players = [p for p in gstate.get().players if p.HP > 0]
        gstate.get().npcs = [n for n in gstate.get().npcs if n.HP > 0]
        
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

#_____________________________________________________________________________________________________________________________________________________________________
class loseability(state):

    def __init__(self, roundcount, time = 30):
        super().__init__(roundcount)
        self.name = "Choose ability to unlearn"
        self.time = time
        self.time1 = time
        self.texttime = gstate.get().fonttime.render(self.name + ":" + str(self.time), 1, (255,0,0))
        self.textround = gstate.get().fonttime.render("round:" + str(self.roundcount), 1, (0, 0, 255))
        self.textreturn = gstate.get().fontA.render("Return", 1, (0,0,0))
        
    def clock(self):
        super().clock()
        if self.time <= 0:
            return chooseability(self.roundcount)
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
                return chooseability(self.roundcount, self.time)
            if  320 <= mouseposition[0] <= 480 and 290 <= mouseposition[1] <= 320: #return button
                return chooseability(self.roundcount, self.time)
        return self

#_____________________________________________________________________________________________________________________________________________________________________
class evolve1(state):

    def __init__(self, roundcount, time = 30):
        super().__init__(roundcount)
        self.name = "You are Evolving!"
        self.time = time
        self.time1 = time
        self.texttime = gstate.get().fonttime.render(self.name + ":" + str(self.time), 1, (255,0,0))
        self.textround = gstate.get().fonttime.render("round:" + str(self.roundcount), 1, (0, 0, 255))
        self.textoffensive = gstate.get().fontA.render("Offensive", 1, (0,0,0))
        self.textdefensive = gstate.get().fontA.render("Defensive", 1, (0,0,0))
        self.textutility = gstate.get().fontA.render("Utility", 1, (0,0,0))
        self.number = 3 #abilities he gets to choose
        
    def clock(self):
        super().clock()
        if self.time <= 0:
            return chooseability(self.roundcount)
        else:
            return self

    def draw(self, screen):
        super().draw(screen)

        if gstate.get().craos.stage == 2:
            #escolha de tipo de habilidade :
            pygame.draw.rect(screen, (255,48,48), (320, 290, 160, 30))
            pygame.draw.rect(screen, (30,144,255), (520, 290, 160, 30))
            pygame.draw.rect(screen, (0,201,87), (720, 290, 160, 30))


            screen.blit(self.textoffensive, (330, 295))
            screen.blit(self.textdefensive, (530, 295))
            screen.blit(self.textutility, (730, 295))
        

    def effect(self):
        if self.number <= 0:
            for npc in gstate.get().npcs:
                if npc.EXP >=evolveprice[npc.stage]:
                    print("1")
                    npc.EXP -= evolveprice[npc.stage]
                    npc.HP += evolveHPgain[npc.stage]
                    npc.MaxHP += evolveHPgain[npc.stage]
                    npc.EXPtoevolve = evolveEXP[npc.stage + 1]
                    npc.stage += 1
                    npc.abilities = []
                    print("2")
                    self.gainabilityoffensive(npc)
                    self.gainabilityoffensive(npc)
                    self.gainabilitydefensive(npc)
            print("3")
            return chooseability(self.roundcount, self.time + 15)
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

#_____________________________________________________________________________________________________________________________________________________________________
class gainability2(state):

    def __init__(self, roundcount, time = 30):
        super().__init__(roundcount)
        self.name = "choose ability type"
        self.time = time
        self.time1 = time
        self.texttime = gstate.get().fonttime.render(self.name + ":" + str(self.time), 1, (255,0,0))
        self.textround = gstate.get().fonttime.render("round:" + str(self.roundcount), 1, (0, 0, 255))
        self.textoffensive = gstate.get().fontA.render("Offensive", 1, (0,0,0))
        self.textdefensive = gstate.get().fontA.render("Defensive", 1, (0,0,0))
        self.textutility = gstate.get().fontA.render("Utility", 1, (0,0,0))
        
    def clock(self):
        super().clock()
        if self.time <= 0:
            return chooseability(self.roundcount, self.time)
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
            return chooseability(self.roundcount, self.time)
        elif  520 <= mouseposition[0]  <= 680 and 290 <= mouseposition[1] <= 320:
            self.gainabilitydefensive(gstate.get().craos)
            return chooseability(self.roundcount, self.time)
        elif  720 <= mouseposition[0]  <= 880 and 290 <= mouseposition[1] <= 320:
            self.gainabilityutility(gstate.get().craos)
            return chooseability(self.roundcount, self.time)
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
class endgame(state):
    def __init__(self, roundcount, victor):
        super().__init__(roundcount)
        self.name = "Endgame"
        self.time = 5
        self.time1 = 5
        self.victor = victor
        self.renderables = []
        self.texttime = gstate.get().fonttime.render(self.name + ":" + str(self.time), 1, (255,0,0))
        self.textround = gstate.get().fonttime.render("round:" + str(self.roundcount), 1, (0, 0, 255))
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
            
            
            
            