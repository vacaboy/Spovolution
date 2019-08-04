import gstate
from creature import *

class simulation:
    def __init__(self):
        pass
        
    def deathcheck(self):
        gstate.get().deadcorpses = gstate.get().deadcorpses + [deadcorpse(p.pos[0], p.pos[1], p.name, p.color, p.HP, p.MaxHP, p.abilitylastused, p.abilitylasttarget, p.EXP, p.EXPtoevolve) for p in gstate.get().players if p.HP <= 0]
        gstate.get().players = [p for p in gstate.get().players if p.HP > 0]
        gstate.get().npcs = [n for n in gstate.get().npcs if n.HP > 0]
        
    def stuff(self, info):
        for p in gstate.get().players:
            p.abilitylastused = []
            p.abilitylasttarget = []
            for d in info:
                if d[0] == p:
                    if d[1].name not in p.abilitylastused:
                        p.abilitylastused.append(d[1].name)
                    p.abilitylasttarget.append([i.name for i in d[2]])
    
    def run(self, info):
        for i in [1,2,3,4]:#ha 4 fazes de combate
            print()
            for a in info:#fazer as decisoes.
                
                if a[1].priority == i:
                    a[1].effect(a[2], a[0])
            print()
                
            for p in gstate.get().players:#as condiçoes atuam.
                for cond in p.conditions:
                    if cond.priority == i:
                        cond.effect()
            print()
                        
            self.deathcheck()
        self.stuff(info)
        
        
        
        
        
        
  