import random as R
from creature import *

class aicomponent:
    def __init__(self, creature):
        self.creature = creature
        self.Qdecided = False
        self.decisions = []
        self.decisionnumber = 1
        
    def gatherinfo(self):
        if self.creature.stage == 3:
            self.decisionnumber = 2
            
    def decide(self):
        if "Paralyzed" in [i.name for i in self.creature.conditions]:
            for i in range(self.decisionnumber):
                self.decisions.append((self.creature, ability("passed", 3, 0, True, 1, False), []))
                
    def decided(self):
        if len(self.decisions) == self.decisionnumber:
            self.Qdecided = True
            for d in self.decisions:
                gstate.get().decisionlist.append(d)
            self.decisions = []
            
    
        
    
class npcaicomponent(aicomponent):
    def __init__(self, creature):
        super().__init__(creature)
        
    def decide(self):
        super().decide()
        
        self.decided()
            
        if self.Qdecided == False:
            w = True
            while w:
                self.creature.chooseability()
                if not(self.creature.ability in [i[1] for i in self.decisions]):
                    w = False
            self.creature.choosetarget(self.creature.ability.targetnumber, self.creature.ability.selftarget)
            self.decisions.append((self.creature, self.creature.ability, self.creature.target)) 
        
        self.decided()

        
    def gatherinfo(self):
        super().gatherinfo()
            


class playeraicomponent(aicomponent):
    def __init__(self, creature):
        super().__init__(creature)
        self.ready = False
        
    def decide(self):
        super().decide()
        if self.ready == True:
            if self.creature.ability in [i[1] for i in self.decisions]:
                print("You can't use the same ability twice in a turn!")
                self.ready = False
            else:
                self.decided()
                    
                if self.Qdecided == False:
                    self.decisions.append((self.creature, self.creature.ability, self.creature.target))
                self.ready = False
                
                self.decided()

        
        
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
                
            
            
            
            