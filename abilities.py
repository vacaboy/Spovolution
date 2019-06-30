from globals import *
import random as R
import gstate

class condition(object):
    def __init__(self, name, target, priority, duration):
        self.name = name
        self.target = target
        self.priority = priority
        self.duration = duration

    def effect(self):
        if self.name == "teste":
            if self.target.ability.damage:
                print("dás mais 3 de dano")
                for target in self.target.target:
                    target.HP -=3
                    self.target.EXP += 3
        
        elif self.name == "Paralyzed":
            print(self.target.name + " is paralyzed this round")
            self.target.ability = ability("passed", 3, 0, True, 1, False)

        elif self.name == "Rock Solid":
            self.target.defensemultiplier = 0
            print("because of Rock Solid, " + str(self.target.name) + " took no damage")


        elif self.name == "Regenerate":
            print(self.target.name + " regenerates 3 HP")
            self.target.heal([self.target], 3)

        elif self.name == "Fight Stance":
            self.target.attackadd = 7
            print(self.target.name + " deals 7 more damage this turn")


        elif self.name == "Limitless":
            self.target.attackmultiplier = 2
            print(self.target.name + " dealt double extra damage because of Limiless")

        elif self.name == "Asleep":
            
            a = R.randint(1,100)
            print("coisas de sleep:")
            print(str(a))
            if self.duration == 5 and a <= 30:
                self.duration = 1
            elif self.duration == 4 and a <= 50:
                self.duration = 1
            elif self.duration == 3 and a <= 70:
                self.duration = 1
            elif self.duration == 2 and a <= 80:
                self.duration = 1
            elif self.duration == 1 and a <= 90:
                self.duration = 1
            else:
                self.target.ability = ability("passed", 3, 0, True, 1, False)
                print(self.target.name + " is Asleep this round")

        elif self.name == "Intimidated":
            self.target.attackadd = -5
            print(self.target.name + " dealt minus 5 damage")
                


        self.duration -= 1
        if self.duration == 0:
            if self.name == "Asleep":
                print(self.target.name + " Woke UP!")
            self.target.conditions.remove(self)
            
            

#______________________________________________________________________________________________________________________________________________________________________
class ability(object): 
    def __init__(self, name, phase, targetnumber, selftarget, priority, damage, abilitytype = "0", worked = False, cooldown = 0, channel = 0):
        self.name = name
        self.phase = phase
        self.priority = priority #can be 1, 2 or 3. If it's effects are calculated before, during the batle, or after.
        self.targetnumber = targetnumber # the number of targets the ability has.
        self.selftarget = selftarget # its suposed to be True or False, if the caster can target himself or not.
        self.damage = damage #suposed to be True or False
        self.abilitytype = abilitytype
        self.worked = worked
        self.cooldown = cooldown
        self.channel = channel
##    def startnewround(self):
##        self.worked = False
##        if self.cooldown >= 1:
##            self.cooldown -= 1
##            print(self.name + str(self.cooldown))

    def clone(self):
        print(self.name)
        return ability(self.name, self.phase, self.targetnumber, self.selftarget, self.priority, self.damage, self.abilitytype, self.worked, self.cooldown, self.channel)     
        
        
    def effect(self, targets, caster):
        caster.abilitylasttarget = self.name
        caster.abilitylasttarget = [p.name for p in targets]
        print(caster.name + " used "+ self.name)
        
        if self.name == "Tackle":
            caster.attack(targets, 2)
            

        elif self.name == "Double Edged Sword":
            caster.attack(targets, 3)
            caster.attack([caster], 2)

        elif self.name == "Stand Tall":
            if caster.attacksreceived >= 2:
                caster.attack(targets, 8)
            else:
                print("but it failed")
            

            
        elif self.name == "Uncertain Footing":
            if caster.attacksreceived == 0:
                caster.attack(targets, 7) 
            else:
                print("but it failed")
            

        elif self.name == "QuickPoke":
            caster.attack(targets, 1)
        

                
        elif self.name == "chill":
            caster.heal([caster], 2) 
            

        elif self.name == "Spear Throw":
            a = R.randint(1, 100)
            if a <= 55:
                b=R.randint(1,12)
                c=R.randint(1,12)
                d=R.randint(1,12)
                e = b + c + d
                caster.attack(targets, e)
            elif 55 < a <= 65:
                print("but he missed by a tiny bit")
            elif 65 < a <= 90:
                print("but he missed")
            else:
                print("but he missed horrobly")


        elif self.name == "Kick":
            a = R.randint(1,10)
            b = R.randint(1,10)
            c = a + b
            caster.attack(targets, c)
       

        elif self.name == "Punch":
            caster.attack(targets, 9)
            

        elif self.name == "Blood Drain":
            d = R.randint(1,100)
            if d <= 75:
                a = R.randint(1,8)
                b = R.randint(1,8)
                c = a + b
                caster.lifesteal = 1
                caster.attack(targets, c)
            else:
                print("but he missed")
            caster.abilitiesincooldown.append(["Blood Drain", 1 + 1])
            
        elif self.name == "Headbutt":
            d = R.randint(1,100)
            if d <= 10:
                caster.conditions.append(condition("Paralyzed", caster, "chooseability", 1))
                print(caster.name + " paralyzed himself with Headbutt")
            a = R.randint(1,11)
            b = R.randint(1,11)
            c = a + b
            caster.attack(targets, c)
                
        elif self.name == "On The Edge":
            a = 0
            b = 0
            for p in gstate.get().players:
                if p == caster:
                    pass
                else:
                    if p.ability.abilitytype == "Offensive":
                        a += 1
                    if caster in p.target:
                        b += 1    
            if a == b and a > 0:
                caster.attack(targets, 30)
            else:
                print("but it failed")


        
        elif self.name == "Everyone... GET IN HERE!":
            a = 0
            for p in gstate.get().players: #calcular quantos ataques te tao a dar target
                if p == caster:
                    pass
                elif (caster in p.target) and p.ability.abilitytype == "Offensive":
                    a = a + 1
            n = 15 * a
            caster.attack(targets, n)        

        elif self.name == "From The Shadows":
            a = 0
            for p in gstate.get().players: #verificar quantas pessoas te deram target:
                if p == caster:
                    pass
                elif caster in p.target:
                    a = a + 1
            if a == 0:
                n = 0
                for i in range(6):
                    b = R.randint(1,6)
                    n = n + b
                caster.attack(targets, n)
            else:
                print("but failed")

        elif self.name == "Unleash The Power":
            if  not (self.name in [i[0] for i in caster.abilitiesinchannel]): #verificar se o player ja esta a dar channel à habilidade
                caster.abilitiesinchannel.append([self.name, self.channel - 1, True])
                #este "True" é verdadeiro ou falso consuante esta habilidade foi usada esta ronda, visto que se a habilidade channel nao for usada uma ronda, entao o channel para.
                print(caster.name + " began channeling " + self.name + " for 4 rounds")
                 
            else: #a é o indice das habilidades que estao em channel que é o desta habilidade
                a = [i[0] == "Unleash The Power" for i in caster.abilitiesinchannel].index(True)
                if caster.abilitiesinchannel[a][1] == 1: #se o channel chegou ao fim, a habilidade atua
                    caster.abilitiesinchannel[a][1] -= 1
                    b = R.randint(1,14)
                    c = R.randint(1,14)
                    d = R.randint(1,14)
                    e = R.randint(1,14)
                    f = b + c + d + e
                    caster.abilitiesincooldown.append(["Unleash The Power", 3 + 1])
                    caster.attack(targets, f)
                else:
                    caster.abilitiesinchannel[a][1] -= 1
                    caster.abilitiesinchannel[a][2] = True
                     
                    print("Only " + str(caster.abilitiesinchannel[a][1]) + " turns left until " + caster.name + " Unleashes The Power")
                    
        elif self.name == "Refreshing Waters":
            caster.heal([caster], 12) 
            caster.abilitiesincooldown.append(["Refreshing Waters", 1 + 1])
             

        elif self.name == "Rock Solid":
            caster.conditions.append(condition("Rock Solid", caster, 1, 1))
             
            caster.abilitiesincooldown.append(["Rock Solid", 5 + 1])

        elif self.name == "Regenerate":
            a = R.randint(1,10)
            caster.conditions.append(condition("Regenerate", caster, "after choosetarget", a))
             
            print(caster.name + " will regenerate 3 HP per turn for " + str(a) + " turns")
            caster.abilitiesincooldown.append(["Regenerate", 1 + 1])

        elif self.name == "Fight Stance":
            a = R.randint(1,6)
            caster.conditions.append(condition("Fight Stance", caster, "chooseability", a))
            print(caster.name + " will deal 7 more damage for " + str(a) + " turns because of Fight Stance")

        elif self.name == "Limitless":
            caster.conditions.append(condition("Limitless", caster, "chooseability", 1))
             
            caster.abilitiesincooldown.append(["Limitless", 999])
            print(caster.name + " will deal double damage next turn because of Limitless")

        elif self.name == "Lullaby":
            print(caster.name + " sang a Lullaby")
            caster.abilitiesincooldown.append(["Lullaby", 5 + 1])
            for player in gstate.get().players:
                if player == caster:
                    pass
                else:
                    a = R.randint(1,2)
                    if a == 1:
                        player.conditions.append(condition("Asleep", player, "chooseability", 5))
                        print(caster.name + " put " + player.name + " to Sleep. ")

        elif self.name == "Intimidate":
            caster.abilitiesincooldown.append(["Intimidate", 1 + 1])
            a = R.randint(1,6)
            for player in gstate.get().players:
                if player == caster:
                    pass
                else:
                    player.conditions.append(condition("Intimidated", player, "chooseability", a))
                    print(caster.name + " intimidated " + player.name + " for " + str(a) + " rounds ")
            
        elif self.name == "teste":
            caster.abilitylasttarget = [player.name for player in targets]
            caster.conditions.append(condition("teste", caster, 3, 4))


        elif self.name == "teste2":
            caster.abilitylasttarget = [player.name for player in targets]
            for target in targets:
                target.conditions.append(condition("Paralyzed", target, "chooseability", 1))
                    
        elif self.name == "passed":
            caster.abilitylasttarget = []
             
            print(caster.name + " did nothing.")
            pass
        caster.abilitylastused = self.name