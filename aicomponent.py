import random as R
from creature import *
from globals import *
#decision: (creature, ability, targets)
class aicomponent:
    def __init__(self, creature):
        self.creature = creature
        self.Qdecided = False
        self.decisions = []
        self.decisionnumber = 1
        self.verified = True
        self.tries = 1
        
    def startnewround(self):
        self.Qdecided = False
        self.decisions = []
        self.tries = 1
        
    
    def gatherinfo(self):
        if self.creature.stage == 3:
            self.decisionnumber = 2
            
    def decide(self):
        if not self.Qdecided:
            if "Paralyzed" in [i.name for i in self.creature.conditions]:
                for i in range(self.decisionnumber):
                    self.decisions.append((self.creature, passed, []))

                        
                
    def decided(self):
        if len(self.decisions) == self.decisionnumber:
            self.Qdecided = True
            for d in self.decisions:
                #if d[2] == []:
                gstate.get().decisionlist.append(d)
                #for t in d[2]:
                 #   gstate.get().decisionlist.append((d[0], d[1], [t]))
            self.decisions = []
        if self.tries > 5000:
            self.Qdecided = True
            for i in range(self.decisionnumber):
                self.decisions.append((self.creature, passed, []))
            return " "
            
    def verify(self):
        for i in [0,1,2,3,4]: #verificar se tens orbs suficientes para usar a habilidade
            if self.creature.ability.orbs[i] + self.creature.orbsplanningtobeused[i] > self.creature.orbs[i]:
                self.verified = False
        if self.creature.ability.name in [i[1].name for i in self.decisions]: #ver se ja usaste esta habilidade
            self.verified = False
        if "High Jump" in [i.name for i in self.creature.conditions]:
            if self.creature.ability.abilitytype != "Offensive":
                self.verified = False
        if "Taunt" in [i.name for i in self.creature.conditions]:
            if self.creature.ability.abilitytype != "Offensive":
                self.verified = False
            for p in gstate.get().players:
                for cond in p.conditions:
                    if cond.name == "Taunt Origin":
                        pla = p
            if pla not in self.creature.target:
                self.verified = False
        for t in self.creature.target:
            if t not in gstate.get().availabletargets:
                self.verified = False
                
    def senddecision(self):
        self.verified = True
        self.verify()
        if self.Qdecided == False and self.verified:
            self.decisions.append((self.creature, self.creature.ability, self.creature.target))
            for i in [0,1,2,3,4]:
                self.creature.orbsplanningtobeused[i] += self.creature.ability.orbs[i]
            self.creature.ability = passed
            self.creature.target = []
            
        elif not self.verified:
            self.creature.ability = passed
            self.creature.target = []
            self.tries += 1
            
class npcaicomponent(aicomponent):
    def __init__(self, creature):
        super().__init__(creature)
        self.learn = True
        
    def startnewround(self):
        super().startnewround()
        self.learn = True
        
    def decide(self):
        super().decide()
        if not self.Qdecided:
            if self.creature.abilitiesinchannel != [] and self.tries < 10:
                a = R.randint(0, len(self.creature.abilitiesinchannel) - 1)
                self.creature.ability = self.creature.abilitiesinchannel[a][3].clone()
            

        
    def gatherinfo(self):
        super().gatherinfo()
            
class playeraicomponent(aicomponent):
    def __init__(self, creature):
        super().__init__(creature)
        self.ready = False
        self.name = "playeraicomponent"
        
    def decide(self):
        super().decide()
        self.decided()
        if self.ready == True:
            if self.creature.ability in [i[1] for i in self.decisions]:
                print("You can't use the same ability twice in a turn!")
            else:
                self.decided()
                self.senddecision()
                if self.verified == False:
                    print("This option is not valid")
                self.decided()
            self.ready = False

class randomaicomponent(npcaicomponent):
    def __init__(self, creature):
        super().__init__(creature)
        self.name = "randomaicomponent"
        
    def decide(self):
        super().decide()
        if not self.Qdecided:

            self.decided()
            if self.creature.ability.name == "passed":
                
                w = True
                while w:
                    self.chooseability()
                    if not(self.creature.ability in [i[1] for i in self.decisions]):
                        w = False
            self.choosetarget(self.creature.ability.targetnumber, self.creature.ability.selftarget)
            self.senddecision()
        
            self.decided()
            
        if self.learn:
            if self.creature.EXP >= abilityprice[self.creature.stage]:
                a = R.random()
                if a < 0.5:
                    pass
                else:
                    self.gainability()
                self.learn = False
        
    def gatherinfo(self):
        super().gatherinfo()
        
    def chooseability(self):
        a = True
        while a:
            b = R.randint(0, len(self.creature.abilities)-1)
            if not (self.creature.abilities[b].name in [i[0] for i in self.creature.abilitiesincooldown]):
                self.creature.ability = self.creature.abilities[b]
                a = False

    def choosetarget(self, n, selftarget):
        self.creature.target = []
        if selftarget: #se te podes dar target a ti mesmo
            if n >= len(gstate.get().availabletargets): #se o numero targets for maior ou igual que o numero de gstate.get().players, entao os targets sao todos os gstate.get().players:
                for p in gstate.get().availabletargets:
                    self.creature.target.append(p)
            else:
                while n > 0: #se nao, vamos escolher gstate.get().players
                    a = R.randint(0, len(gstate.get().availabletargets)-1)
                    if gstate.get().availabletargets[a] in self.creature.target:
                        pass
                    else:
                        self.creature.target.append(gstate.get().availabletargets[a])
                        n -= 1
        else:#se nao de podes dar target a ti mesmo
            if n >= (len(gstate.get().availabletargets) - 1): #entao se o numero de targets for maior ou igual que o numero de gstate.get().players - 1, entao os targets sao todos os inimigos
                for p in gstate.get().availabletargets:
                    if p == self.creature:
                        pass
                    elif p.owner.name == self.creature.name:
                        pass
                    else:
                        self.creature.target.append(p)
            else:
                while n > 0:#se nao, vamos escolher inimigos
                    a = R.randint(0, len(gstate.get().availabletargets)-1)
                    if (gstate.get().availabletargets[a] in self.creature.target) or (gstate.get().availabletargets[a] == self.creature) or (gstate.get().availabletargets[a].owner.name == self.creature.name):
                        pass
                    else:
                        self.creature.target.append(gstate.get().availabletargets[a])
                        n -= 1
        if self.creature.ability.channel > 0: #se a habilidade escolhida tem channel:
            if self.creature.ability.name in [i[0] for i in self.creature.abilitiesinchannel]: #se o player ja esta a dar channel à habilidade
                a = [i[0] == self.creature.ability.name for i in self.creature.abilitiesinchannel].index(True)
                if self.creature.abilitiesinchannel[a][1] >= 2: #se a habilidade nao vai atuar este turno
                    self.creature.target = []
            elif not (self.creature.ability.name in [i[0] for i in self.creature.abilitiesinchannel]): #se o player ainda nao esta a dar channel à habilidade:
                self.creature.target = []
                
    def gainability(self):
        if self.creature.stage == 1:
            a = [i for i in gstate.get().abilities[1] if i.name not in [j.name for j in self.creature.abilities]]
            if len(a) > 0:
                b = R.randint(0, len(a) - 1)
            
        elif self.creature.stage == 2:
            c = R.randint(0,2)
            a = [i for i in gstate.get().abilities[2][c] if i.name not in [j.name for j in self.creature.abilities]]
            if len(a) > 0:
                b = R.randint(0, len(a) - 1)
            
        elif self.creature.stage == 3:
            w = True
            c = self.creature.element
            f = [0,1,2]
            while w:
                g = R.randint(0, len(f) - 1)
                d = f[g]
                a = [i for i in gstate.get().abilities[3][c][d] if i.name not in [j.name for j in self.creature.abilities]]
                if a == []:
                    f.remove(d)
                else:
                    w = False
                if f == []:
                    w = False
            r = False
            if a == []:
                r = True
            while not r:
                b = R.randint(0,len(a) - 1)
                e = R.random()
                d = a[b].proficiencyneeded - self.creature.proficiencies[c]
                if d <= 1:
                    d = 1
                if e < (1 / d):
                    r = True
        if a != []:
            self.creature.abilities.append(a[b].clone())
            print(self.creature.name + " learned: " + a[b].name)
            self.creature.EXP -= abilityprice[self.creature.stage]
        
class smartaicomponent1(npcaicomponent):
    def __init__(self, creature):
        super().__init__(creature)
        self.learn = True
        
    def startnewround(self):
        super().startnewround()
        self.learn = True
        
    def decide(self):
        super().decide()
        if not self.Qdecided:

            self.decided()
            if self.creature.ability.name == "passed":
                
                w = True
                while w:
                    self.chooseability()
                    if not(self.creature.ability in [i[1] for i in self.decisions]):
                        w = False
            self.choosetarget(self.creature.ability.targetnumber, self.creature.ability.selftarget)
            self.senddecision()
        
            self.decided()
            
        if self.learn:
            if self.creature.EXP >= abilityprice[self.creature.stage]:
                a = R.random()
                if a < 0.5:
                    pass
                else:
                    self.gainability()
                self.learn = False
        
    def gatherinfo(self):
        super().gatherinfo()
        
    def chooseability(self):
        a = True
        while a:
            b = R.randint(0, len(self.creature.abilities)-1)
            if not (self.creature.abilities[b].name in [i[0] for i in self.creature.abilitiesincooldown]):
                self.creature.ability = self.creature.abilities[b]
                a = False

    def choosetarget(self, n, selftarget):
        self.creature.target = []
        if selftarget: #se te podes dar target a ti mesmo
            if n >= len(gstate.get().availabletargets): #se o numero targets for maior ou igual que o numero de gstate.get().players, entao os targets sao todos os gstate.get().players:
                for p in gstate.get().availabletargets:
                    self.creature.target.append(p)
            else:
                while n > 0: #se nao, vamos escolher gstate.get().players
                    a = R.randint(0, len(gstate.get().availabletargets)-1)
                    if gstate.get().availabletargets[a] in self.creature.target:
                        pass
                    else:
                        self.creature.target.append(gstate.get().availabletargets[a])
                        n -= 1
        else:#se nao de podes dar target a ti mesmo
            if n >= (len(gstate.get().availabletargets) - 1 - len(self.creature.pets)): #entao se o numero de targets for maior ou igual que o numero de gstate.get().players - 1, entao os targets sao todos os inimigos
                for p in gstate.get().availabletargets:
                    if p == self.creature:
                        pass
                    elif p.owner.name == self.creature.name:
                        pass
                    else:
                        self.creature.target.append(p)
            else:
                while n > 0:#se nao, vamos escolher inimigos
                    a = R.randint(0, len(gstate.get().availabletargets)-1 - len(self.creature.pets))
                    if (gstate.get().availabletargets[a] in self.creature.target) or (gstate.get().availabletargets[a] == self.creature) or (gstate.get().availabletargets[a].owner.name == self.creature.name):
                        pass
                    else:
                        self.creature.target.append(gstate.get().availabletargets[a])
                        n -= 1
        if self.creature.ability.channel > 0: #se a habilidade escolhida tem channel:
            if self.creature.ability.name in [i[0] for i in self.creature.abilitiesinchannel]: #se o player ja esta a dar channel à habilidade
                a = [i[0] == self.creature.ability.name for i in self.creature.abilitiesinchannel].index(True)
                if self.creature.abilitiesinchannel[a][1] >= 2: #se a habilidade nao vai atuar este turno
                    self.creature.target = []
            elif not (self.creature.ability.name in [i[0] for i in self.creature.abilitiesinchannel]): #se o player ainda nao esta a dar channel à habilidade:
                self.creature.target = []
                
    def gainability(self):
        if self.creature.stage == 1:
            a = [i for i in gstate.get().abilities[1] if i.name not in [j.name for j in self.creature.abilities]]
            if len(a) > 0:
                b = R.randint(0, len(a) - 1)
            
        elif self.creature.stage == 2:
            c = R.randint(0,2)
            a = [i for i in gstate.get().abilities[2][c] if i.name not in [j.name for j in self.creature.abilities]]
            if len(a) > 0:
                b = R.randint(0, len(a) - 1)
            
        elif self.creature.stage == 3:
            w = True
            c = self.creature.element
            f = [0,1,2]
            while w:
                g = R.randint(0, len(f) - 1)
                d = f[g]
                a = [i for i in gstate.get().abilities[3][c][d] if i.name not in [j.name for j in self.creature.abilities]]
                if a == []:
                    f.remove(d)
                else:
                    w = False
                if f == []:
                    w = False
            r = False
            if a == []:
                r = True
            while not r:
                b = R.randint(0,len(a) - 1)
                e = R.random()
                d = a[b].proficiencyneeded - self.creature.proficiencies[c]
                if d <= 1:
                    d = 1
                if e < (1 / d):
                    r = True
        if a != []:
            self.creature.abilities.append(a[b].clone())
            print(self.creature.name + " learned: " + a[b].name)
            self.creature.EXP -= abilityprice[self.creature.stage]



class attackpet(aicomponent):
    def __init__(self, creature):
        super().__init__(creature)
        self.name = "attackpet"
        
    def decide(self):
        super().decide()
        if self.Qdecided == False:
            self.decided()
            
            if self.creature.ability.name == "passed":
                print(1)
                w = True
                while w:
                    self.chooseability()
                    if not(self.creature.ability in [i[1] for i in self.decisions]):
                        w = False
            self.choosetarget(self.creature.ability.targetnumber, self.creature.ability.selftarget)
            self.senddecision()
        
            self.decided()

        
#    def gatherinfo(self):
#        super().gatherinfo()
        
    def chooseability(self):
        a = True
        while a:
            b = R.randint(0, len(self.creature.abilities)-1)
            if not (self.creature.abilities[b].name in [i[0] for i in self.creature.abilitiesincooldown]):
                self.creature.ability = self.creature.abilities[b]
                a = False

    def choosetarget(self, n, selftarget):
        self.creature.target = []
        b = [self.creature.owner] + [i for i in self.creature.owner.pets]
        atargets = [i for i in gstate.get().availabletargets if i not in b]
        if selftarget: #se te podes dar target a ti mesmo
            if n >= len(atargets): #se o numero targets for maior ou igual que o numero de gstate.get().players, entao os targets sao todos os gstate.get().players:
                for p in atargets:
                    self.creature.target.append(p)
            else:
                while n > 0: #se nao, vamos escolher gstate.get().players
                    a = R.randint(0, len(atargets)-1)
                    if atargets[a] in self.creature.target:
                        pass
                    else:
                        self.creature.target.append(atargets[a])
                        n -= 1
        else:#se nao de podes dar target a ti mesmo
            if n >= len(atargets): #entao se o numero de targets for maior ou igual que o numero de gstate.get().players - 1, entao os targets sao todos os inimigos
                for p in atargets:
                    if p == self.creature:
                        pass
                    elif p.owner.name == self.creature.name:
                        pass
                    elif p.name == self.creature.owner.name:
                        pass
                    else:
                        self.creature.target.append(p)
            else:
                while n > 0:#se nao, vamos escolher inimigos
                    a = R.randint(0, len(atargets)-1)
                    self.creature.target.append(atargets[a])
                    n -= 1

            
            
            
class attackwhoattackedme(npcaicomponent): #if someone attacked him in the past, he will attack him once. if no one attack him in the past. he will use a defensive ability.
    def __init__(self,creature):
        super().__init__(creature)
        self.whoattackedme = []
        self.name = "attackwhoattackedmeaicomponent"
        
    def gatherinfo(self):
        super().gatherinfo()
        for i in gstate.get().log:
            if i[2] == self.creature:
                if not(i[0] in self.whoattackedme) and not(i[0] == self.creature) and not(i[0] == gstate.get().system): 
                    self.whoattackedme.append(i[0])
        
    def decide(self):
        super().decide()
        if not self.Qdecided:

            self.decided()
            if self.creature.ability.name == "passed":
                
                w = True
                while w:
                    self.chooseability()
                    if not(self.creature.ability in [i[1] for i in self.decisions]):
                        w = False
            self.choosetarget(self.creature.ability.targetnumber, self.creature.ability.selftarget)
            self.senddecision()
        
            self.decided()
            
        if self.learn:
            if self.creature.EXP >= abilityprice[self.creature.stage]:
                a = R.random()
                if a < 0.5:
                    pass
                else:
                    self.gainability()
                self.learn = False
                
    def chooseability(self):
        a = True
        y = 1
        while a:
            y = y + 1 
            print(str(y))
            if self.whoattackedme != []:
                if y < 5:
                    offensivelist = [i for i in self.creature.abilities if (i.abilitytype == "Offensive" and i.phase == self.creature.stage)]
                    #print(str(len(offensivelist)))
                    b = R.randint(0, len(offensivelist) - 1)
                    if ((not (offensivelist[b].name in [i[0] for i in self.creature.abilitiesincooldown])) and (offensivelist[b].channel == 0) and  not (offensivelist[b].name in [i[1].name for i in self.decisions])):
                        if offensivelist[b].targetnumber <= len(self.whoattackedme):
                            self.creature.ability = offensivelist[b]
                            print("aqui")
                            a = False
                elif 5 <= y < 10:
                    offensivelist = [i for i in self.creature.abilities if i.abilitytype == "Offensive"]
                    b = R.randint(0, len(offensivelist) - 1)
                    if ((not (offensivelist[b].name in [i[0] for i in self.creature.abilitiesincooldown])) and (offensivelist[b].channel == 0)):
                        if offensivelist[b].targetnumber <= len(self.whoattackedme):
                            self.creature.ability = offensivelist[b]
                            a = False
                elif 10 <= y < 15:
                    otherlist = [i for i in self.creature.abilities if i.abilitytype == "Defensive" and i.phase == self.creature.stage]
                    b = R.randint(0, len(otherlist) - 1)
                    if ((not (otherlist[b].name in [i[0] for i in self.creature.abilitiesincooldown])) and (otherlist[b].channel == 0)):
                        self.creature.ability = otherlist[b]
                        a = False
                else:
                    otherlist = [i for i in self.creature.abilities if i.abilitytype == "Defensive"]
                    b = R.randint(0, len(otherlist) - 1)
                    if ((not (otherlist[b].name in [i[0] for i in self.creature.abilitiesincooldown])) and (otherlist[b].channel == 0)):
                        self.creature.ability = otherlist[b]
                        a = False
            else:
                if y < 5:
                    otherlist = [i for i in self.creature.abilities if i.abilitytype == "Defensive" and i.phase == self.creature.stage]
                    b = R.randint(0, len(otherlist) - 1)
                    if ((not (otherlist[b].name in [i[0] for i in self.creature.abilitiesincooldown])) and (otherlist[b].channel == 0)):
                        self.creature.ability = otherlist[b]
                        a = False
                elif y < 10:
                    otherlist = [i for i in self.creature.abilities if i.abilitytype == "Defensive"]
                    b = R.randint(0, len(otherlist) - 1)
                    if ((not (otherlist[b].name in [i[0] for i in self.creature.abilitiesincooldown])) and (otherlist[b].channel == 0)):
                        self.creature.ability = otherlist[b]
                        a = False
                elif y < 20:
                    otherlist = [i for i in self.creature.abilities if i.abilitytype == "Utility"]
                    b = R.randint(0, len(otherlist) - 1)
                    if ((not (otherlist[b].name in [i[0] for i in self.creature.abilitiesincooldown])) and (otherlist[b].channel == 0)):
                        self.creature.ability = otherlist[b]
                        a = False
                else:
                    otherlist = [i for i in self.creature.abilities if i.abilitytype == "Offensive"]
                    b = R.randint(0, len(otherlist) - 1)
                    if ((not (otherlist[b].name in [i[0] for i in self.creature.abilitiesincooldown])) and (otherlist[b].channel == 0)):
                        self.creature.ability = otherlist[b]
                        a = False
                    
    def choosetarget(self, n, selftarget):
        self.creature.target = []
        if self.whoattackedme == []:
            if selftarget: #se te podes dar target a ti mesmo
                if n >= len(gstate.get().availabletargets): #se o numero targets for maior ou igual que o numero de gstate.get().players, entao os targets sao todos os gstate.get().players:
                    for p in gstate.get().availabletargets:
                        self.creature.target.append(p)
                else:
                    while n > 0: #se nao, vamos escolher gstate.get().players
                        a = R.randint(0, len(gstate.get().availabletargets)-1)
                        if gstate.get().availabletargets[a] in self.creature.target:
                            pass
                        else:
                            self.creature.target.append(gstate.get().availabletargets[a])
                            n -= 1
            else:#se nao de podes dar target a ti mesmo
                if n >= (len(gstate.get().availabletargets) - 1 - len(self.creature.pets)): #entao se o numero de targets for maior ou igual que o numero de gstate.get().players - 1, entao os targets sao todos os inimigos
                    for p in gstate.get().availabletargets:
                        if p == self.creature:
                            pass
                        elif p.owner.name == self.creature.name:
                            pass
                        else:
                            self.creature.target.append(p)
                else:
                    while n > 0:#se nao, vamos escolher inimigos
                        a = R.randint(0, len(gstate.get().availabletargets)-1 - len(self.creature.pets))
                        if (gstate.get().availabletargets[a] in self.creature.target) or (gstate.get().availabletargets[a] == self.creature) or (gstate.get().availabletargets[a].owner.name == self.creature.name):
                            pass
                        else:
                            self.creature.target.append(gstate.get().availabletargets[a])
                            n -= 1
            if self.creature.ability.channel > 0: #se a habilidade escolhida tem channel:
                if self.creature.ability.name in [i[0] for i in self.creature.abilitiesinchannel]: #se o player ja esta a dar channel à habilidade
                    a = [i[0] == self.creature.ability.name for i in self.creature.abilitiesinchannel].index(True)
                    if self.creature.abilitiesinchannel[a][1] >= 2: #se a habilidade nao vai atuar este turno
                        self.creature.target = []
                elif not (self.creature.ability.name in [i[0] for i in self.creature.abilitiesinchannel]): #se o player ainda nao esta a dar channel à habilidade:
                    self.creature.target = []
                    
        else:
            if selftarget: #se te podes dar target a ti mesmo
                if n >= len(gstate.get().availabletargets): #se o numero targets for maior ou igual que o numero de gstate.get().players, entao os targets sao todos os gstate.get().players:
                    for p in gstate.get().availabletargets:
                        self.creature.target.append(p)
                    self.whoattackedme = []
                else:
                    while n > 0: #se nao, vamos escolher gstate.get().players
                        if len(self.whoattackedme) != 0:
                            a = R.randint(0, len(self.whoattackedme)-1)
                            if self.whoattackedme[a] in self.creature.target:
                                pass
                            else:
                                self.creature.target.append(self.whoattackedme[a])
                                n -= 1
                                print("2")
                                self.whoattackedme.remove(self.whoattackedme[a])
                        else:
                            a = R.randint(0, len(gstate.get().availabletargets)-1)
                            if gstate.get().availabletargets[a] in self.creature.target:
                                pass
                            else:
                                self.creature.target.append(gstate.get().availabletargets[a])
                                n -= 1
                                print("1")
                                self.whoattackedme.remove(self.whoattackedme[a])
            else:#se nao de podes dar target a ti mesmo
                if n >= (len(gstate.get().availabletargets) - 1 - len(self.creature.pets)): #entao se o numero de targets for maior ou igual que o numero de gstate.get().players - 1, entao os targets sao todos os inimigos
                    for p in gstate.get().availabletargets:
                        if p == self.creature:
                            pass
                        elif p.owner.name == self.creature.name:
                            pass
                        else:
                            self.creature.target.append(p)
                    self.whoattackedme = []
                else:
                    while n > 0:#se nao, vamos escolher inimigos
                        if len(self.whoattackedme) > 0:
                            a = R.randint(0, len(self.whoattackedme) - 1)
                            if (self.whoattackedme[a] in self.creature.target) or (self.whoattackedme[a] == self.creature) or (self.whoattackedme[a].owner.name == self.creature.name):
                                pass
                            else:
                                self.creature.target.append(self.whoattackedme[a])
                                n -= 1
                                print("4")
                                self.whoattackedme.remove(self.whoattackedme[a])
                        else:
                            a = R.randint(0, len(gstate.get().availabletargets) - 1)
                            if (gstate.get().availabletargets[a] in self.creature.target) or (gstate.get().availabletargets[a] == self.creature) or (gstate.get().availabletargets[a].owner.name == self.creature.name):
                                pass
                            else:
                                self.creature.target.append(gstate.get().availabletargets[a])
                                n -= 1
                                print("3")
                                self.whoattackedme.remove(self.whoattackedme[a])
                                
    def gainability(self):
        if self.creature.stage == 1:
            a = [i for i in gstate.get().abilities[1] if i.name not in [j.name for j in self.creature.abilities]]
            if len(a) > 0:
                b = R.randint(0, len(a) - 1)
            
        elif self.creature.stage == 2:
            c = R.randint(0,2)
            a = [i for i in gstate.get().abilities[2][c] if i.name not in [j.name for j in self.creature.abilities]]
            if len(a) > 0:
                b = R.randint(0, len(a) - 1)
            
        elif self.creature.stage == 3:
            w = True
            c = self.creature.element
            f = [0,1,2]
            while w:
                g = R.randint(0, len(f) - 1)
                d = f[g]
                a = [i for i in gstate.get().abilities[3][c][d] if i.name not in [j.name for j in self.creature.abilities]]
                if a == []:
                    f.remove(d)
                else:
                    w = False
                if f == []:
                    w = False
            r = False
            if a == []:
                r = True
            while not r:
                b = R.randint(0,len(a) - 1)
                e = R.random()
                d = a[b].proficiencyneeded - self.creature.proficiencies[c]
                if d <= 1:
                    d = 1
                if e < (1 / d):
                    r = True
        if a != []:
            self.creature.abilities.append(a[b].clone())
            print(self.creature.name + " learned: " + a[b].name)
            self.creature.EXP -= abilityprice[self.creature.stage]
                
        # if self.Qdecided == False:#so faz coisas se ainda nao fez nada
            # if self.whoattackedme != []: #se alguem o atacou, ele vai atacar esse
                # a = [ab for ab in self.creature.abilities if ab.abilitytype == "Offensive"] #escolhe uma habiliade ofensiva
                # b = R.randint(0, len(a)-1)
                # self.creature.ability = a[b]
                # for i in range(self.creature.ability.targetnumber): #ataca quem o atacou
                    # f = [p for p in self.whoattackedme if not(p in self.creature.target)]
                    # if f != []:
                        # c = R.randint(0, len(f)-1)
                        # self.creature.target.append(f[c])
                        # self.whoattackedme.remove(self.whoattackedme[c])
                    # else:
                        # d = [p for p in gstate.get().players if (p != self.creature and not(p in self.creature.target))]
                        # if d == []:
                            # pass
                        # else:
                            # c = R.randint(0, len(d) - 1)
                            # self.creature.target.append(d[c])
                        
            # else: #escolhe uma habilidade nao ofensiva que nao esteja em cooldown
                # a1 = [ab for ab in self.creature.abilities if (ab.abilitytype == "Defensive" or ab.abilitytype == "Utility")] 
                # a = [ab for ab in a1 if ab not in [a[0] for a in self.creature.abilitiesincooldown]]
                # if a == []:
                    # c = [ab for ab in self.creature.abilities if ab not in [a[0] for a in self.creature.abilitiesincooldown]]
                    # b = R.randint(0, len(c)-1)
                    # self.creature.ability = c[b]
                # else:
                    # b = R.randint(0, len(a)-1)
                    # self.creature.ability = a[b]

                # self.creature.choosetarget(self.creature.ability.targetnumber, self.creature.ability.selftarget)
                
            # self.Qdecided = True
            # gstate.get().decisionlist.append((self.creature, self.creature.ability, self.creature.target))
                