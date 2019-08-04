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
        
    def gatherinfo(self):
        if self.creature.stage == 3:
            self.decisionnumber = 2
            
    def decide(self):
        if not self.Qdecided:
            if "Paralyzed" in [i.name for i in self.creature.conditions]:
                for i in range(self.decisionnumber):
                    #self.decisions.append((self.creature, ability("passed", 3, 0, True, 1, False), []))
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
        if self.creature.ability.orbs > self.creature.orbs[self.creature.ability.element]:
            self.verified = False
        if self.creature.ability.name in [i[1].name for i in self.decisions]:
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
                
    def senddecision(self):
        self.verified = True
        self.verify()
        if self.Qdecided == False and self.verified:
            self.decisions.append((self.creature, self.creature.ability, self.creature.target))
            
            self.creature.ability = passed
            self.creature.target = []
            
        elif not self.verified:
            self.creature.ability = passed
            self.creature.target = []
            self.tries += 1
            
        
            
    
        
    
class npcaicomponent(aicomponent):
    def __init__(self, creature):
        super().__init__(creature)
        
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
        
    def decide(self):
        super().decide()
        if self.Qdecided == False:
            self.decided()
            
            if self.creature.ability == passed:
                w = True
                while w:
                    self.creature.chooseability()
                    if not(self.creature.ability in [i[1] for i in self.decisions]):
                        w = False
            self.creature.choosetarget(self.creature.ability.targetnumber, self.creature.ability.selftarget)
            self.senddecision()
        
            self.decided()

        
    def gatherinfo(self):
        super().gatherinfo()
        
class attackwhoattackedme(npcaicomponent):
    def __init__(self,creature):
        super().__init__(creature)
        self.whoattackedme = []
        
    def gatherinfo(self):
        super().gatherinfo()
        for i in gstate.get().log:
            if i[2] == self.creature:
                if not(i[0] in self.whoattackedme) and not(i[0] == self.creature) and not(i[0] == gstate.get().system): 
                    self.whoattackedme.append(i[0])
        
    def decide(self):
        if self.Qdecided == False:#so faz coisas se ainda nao fez nada
            if self.whoattackedme != []: #se alguem o atacou, ele vai atacar esse
                a = [ab for ab in self.creature.abilities if ab.abilitytype == "Offensive"] #escolhe uma habiliade ofensiva
                b = R.randint(0, len(a)-1)
                self.creature.ability = a[b]
                for i in range(self.creature.ability.targetnumber): #ataca quem o atacou
                    f = [p for p in self.whoattackedme if not(p in self.creature.target)]
                    if f != []:
                        c = R.randint(0, len(f)-1)
                        self.creature.target.append(f[c])
                        self.whoattackedme.remove(self.whoattackedme[c])
                    else:
                        d = [p for p in gstate.get().players if (p != self.creature and not(p in self.creature.target))]
                        if d == []:
                            pass
                        else:
                            c = R.randint(0, len(d) - 1)
                            self.creature.target.append(d[c])
                        
            else: #escolhe uma habilidade nao ofensiva que nao esteja em cooldown
                a1 = [ab for ab in self.creature.abilities if (ab.abilitytype == "Defensive" or ab.abilitytype == "Utility")] 
                a = [ab for ab in a1 if ab not in [a[0] for a in self.creature.abilitiesincooldown]]
                if a == []:
                    c = [ab for ab in self.creature.abilities if ab not in [a[0] for a in self.creature.abilitiesincooldown]]
                    b = R.randint(0, len(c)-1)
                    self.creature.ability = c[b]
                else:
                    b = R.randint(0, len(a)-1)
                    self.creature.ability = a[b]

                self.creature.choosetarget(self.creature.ability.targetnumber, self.creature.ability.selftarget)
                
            self.Qdecided = True
            gstate.get().decisionlist.append((self.creature, self.creature.ability, self.creature.target))
                
            
            
            
            