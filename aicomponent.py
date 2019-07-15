import random as R
from creature import *

class aicomponent:
    def __init__(self, creature):
        self.creature = creature
        self.Qdecided = False
    
        
    
class npcaicomponent(aicomponent):
    def __init__(self, creature):
        super().__init__(self, creature)
        
    def decide(self):
        self.creature.chooseability()
        self.creature.choosetarget(self.creature.ability.targetnumber, self.creature.ability.selftarget)
        self.Qdecided = True
        gstate.get().decisionlist.append((self.creature, self.creature.ability, self.creature.target))
        
    def gatherinfo(self):
        pass
            
    def decided(self):
        pass


class playeraicomponent(aicomponent):
    def __init__(self, creature):
        super().__init__(self, creature)
        self.ready = False
        
    def decide(self):
        if self.ready == True:
            self.Qdecided = True
            self.ready = False
            gstate.get().decisionlist.append((self.creature, self.creature.ability, self.creature.target))
        
    def decided(self):
        return False
        
        
        
class attackwhoattackedme(npcaicomponent):
    def __init__(self,creature):
        super().__init__(self,creature)
        self.whoattackedme = []
        
    def gatherinfo(self):
        for i in gstate.get().log:
            if i[2] == self.creature:
                if not(i[0] in self.whoattackedme):
                    self.whoattackedme.append(i[0])
        
    def decide(self):
        if self.Qdecided == False:#so faz coisas se ainda nao fez nada
            if self.whoattackedme != []: #se alguem o atacou, ele vai atacar esse
                a = [ab for ab in self.creature.abilities if ab.abilitytype == "Offensive"] #escolhe uma habiliade ofensiva
                b = R.randint(0, len(a)-1)
                self.creature.ability = a[b]
                for i in range(self.creature.ability.targetnumber): #ataca quem o atacou
                    if self.whoattackedme != []:
                        c = R.randint(0, len(self.whoattackedme)-1)
                        self.creature.target.append(self.whoattackedme[c])
                        self.whoattackedme.remove(whoattackedme[c])
                    else:
                        d = [p for p in gstate.get().players if (p != self.creature and not(p in self.creature.target))]
                        c = R.randint(0, len(d) - 1)
                        self.creature.target.append(d[c])
                        
            else:
                a = [ab for ab in self.creature.abilities if (ab.abilitytype == "Defensive" or ab.abilitytype == "Utility")]
                b = R.randint(0, len(a)-1)
                self.creature.ability = a[b]
                self.creature.choosetarget(self.creature, self.creature.ability.targetnumber, self.creature.ability.selftarget)
                
            self.Qdecided = True
            gstate.get().decisionlist.append((self.creature, self.creature.ability, self.creature.target))
                
            
            
            
            