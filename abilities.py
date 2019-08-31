from globals import *
import random as R
import gstate
import math


#channel [ability.name, turns left, True or False, ability]

class condition(object):
    def __init__(self, name, target, priority, duration, value = 0, caster = " "):
        self.name = name
        self.target = target
        self.priority = priority
        self.duration = duration
        self.value = value
        self.caster = caster

    def effect(self):
        if self.name == "teste":
            if self.target.ability.damage:
                print("dás mais 3 de dano")
                for target in self.target.target:
                    target.HP -=3
                    self.target.EXP += 3
        
        elif self.name == "Paralyzed":
            pass
            #print(self.target.name + " is paralyzed this round")
            #self.target.ability = ability("passed", 3, 0, True, 1, False)
            
        elif self.name == "Become Paralyzed":
            a = R.random()
            if a < self.value:
                #print(self.target.name + " is paralyzed next round")
                self.target.conditions.append(condition("Paralyzed", a[0], 3, 1))
                #self.target.ability = ability("passed", 3, 0, True, 1, False)
            
        elif self.name == "Immobilized":
            print(self.target.name + " tis immobilized")
            self.target.defensemultiplier *= 1.5
            
        elif self.name == "Anti-Immobilized":
            #print(self.target.name + " takes 150% damage this turn")
            self.target.defensemultiplier *= 1/1.5
            
        elif self.name == "Accuracy":
            self.target.accuracy *= self.value
            #print(self.target.name + " has " + str(self.value * 100) + "% less accuracy.")
            
        elif self.name == "Take Damage":
            if self.caster != " ":
                self.caster.attack([self.target], self.value, a = 0)
            else:
                gstate.get().system.attack([self.target], self.value, a = 0)
                
        elif self.name == "Take Soul Damage":
            if self.caster != " ":
                self.caster.soulattack([selt.targets], self.value, a = 0)
            else:
                gstate.get().system.soulattack([self.target], self.value, a = 0)


            
        elif self.name == "Take Heal":
            gstate.get().system.heal([self.target], self.value)
            
        elif self.name == "Heal Modifier":
            self.target.healmultiplier *= 0.5
            
        elif self.name == "More Experience":
            self.target.EXPmultiplier *= self.value 
            #print(self.target.name + " gains " + str(self.value) + " EXP")

            
        elif self.name == "Rock Solid":
            self.target.defensemultiplier = 0
            #print("because of Rock Solid, " + str(self.target.name) + " took no damage")


        elif self.name == "Regenerate":
            #print("Regenerate:")
            gstate.get().system.heal([self.target], 3)

        elif self.name == "Fight Stance":
            self.target.attackadd += 7
            #print(self.target.name + " deals 7 more damage this turn")


        elif self.name == "Limitless":
            self.target.attackmultiplier *= 2
            #print(self.target.name + " dealt double extra damage because of Limiless")
            
        elif self.name == "Double Damage":
            self.target.attackmultiplier *= 2
            #print(self.target.name + " dealt double extra damage")
            
        elif self.name == "Half Damage":
            self.target.attackmultiplier *= 1/2
            #print(self.target.name + " dealt double extra damage")

        elif self.name == "Asleep":
            
            a = R.randint(1,100)
            print("coisas de sleep:")
            print(str(a))
            if self.duration == 5 and a <= 30:
                self.duration = 1
                print(self.target.name + " Woke UP!")
            elif self.duration == 4 and a <= 50:
                self.duration = 1
                print(self.target.name + " Woke UP!")
            elif self.duration == 3 and a <= 70:
                self.duration = 1
                print(self.target.name + " Woke UP!")
            elif self.duration == 2 and a <= 80:
                self.duration = 1
                print(self.target.name + " Woke UP!")
            elif self.duration == 1 and a <= 90:
                self.duration = 1
                print(self.target.name + " Woke UP!")
            else:
                self.target.conditions.append(condition("Paralyzed", self.target, 1, 1))
                #self.target.ability = ability("Asleep", 3, 0, True, 1, False)
                print(self.target.name + " is Asleep this round")

        elif self.name == "Intimidated":
            self.target.attackadd -= 5
            #print(self.target.name + " dealt minus 5 damage")
    
        elif self.name == "Shocking Response":
            for a in gstate.get().log:
                if a[2] == self.target:
                    c = round( (5 - a[0].defenseadd) * a[0].defensemultiplier )
                    a[0].HP -= c
                    #print(a[0].name + " took " + str(c) + " damage because of shocking response")
                    b = R.randint(1,100)
                    #print("shocking response dice: " + str(b))
                    if b <= 10:
                        a[0].conditions.append(condition("Paralyzed", a[0], 1, 1))
                        print(a[0].name + " got paralyzed because of Shocking Response from " + a[2].name)
                
        elif self.name == "Flight":
            self.target.dodge = 1 - ( (1 - self.target.dodge) * (1 - 0.8) )
            #print(self.target.name + " is flying!")
            
        elif self.name == "Nature's Call":
            self.target.defenseadd += 3
            #print(self.target.name + " takes 3 less damage this turn.")
            
        elif self.name == "Web Cacoon":
            for a in gstate.get().log:
                if a[2] == self.target:
                    a[0].conditions.append(condition("Accuracy", a[0], 1, 1, value = 0.5))
                    
        elif self.name == "High Jump":
            pass
            
        elif self.name == "Lifesteal":
            self.target.lifesteal += self.value
            #print(self.target.name + " has 10% lifesteal")
            
        elif self.name == "Less Damage":
            self.target.attackadd -= self.value
            #print(self.target.name + " deals " + str(self.value) + " less damage this turn")
            
        elif self.name == "More Damage":
            self.target.attackadd += self.value
            #print(self.target.name + " deals " + str(self.value) + " more damage this turn")
            
        elif self.name == "More Defense":
            self.target.defenseadd +=self.value
            #print(self.target.name + " receives " + str(self.value) + " less damage this turn")
                
        elif self.name == "More Dodge":
            self.target.dodge = 1 - ((1 - self.target.dodge) * (1 - self.value))
            
        elif self.name == "Less Dodge":
            pass
            
        elif self.name == "More Accuracy":
            pass
        
        elif self.name == "Less Accuracy":
            self.target.accuracy *= self.value
            
        elif self.name == "Get Thorns":
            self.target.conditions.append(condition("Thorns", self.target, 3, 1, value = self.value))
            
        elif self.name == "Thorns":
            for a in gstate.get().log:
                if a[2] == self.target:
                    self.target.attack([a[0]], self.value, a = 0, tolog = False)
                    
        elif self.name == "Ice Thorns":
            for a in gstate.get().log:
                if a[2] == self.target:
                    b = R.random()
                    if b <= self.value:
                        a[0].freezestacks += 1
                        print(a[0].name + " was frozen ")
                        
        elif self.name == "Taunt":
            pass
            
        elif self.name == "Taunt Origin":
            pass
            
        elif self.name == "Forget":
            abilitiesused = []
            for d in gstate.get().decisionlist:
                if d[0] == self.target:
                    abilitiesused.append(d[1].clone())
            a = R.randint(0, len(abilitiesused) - 1)
            if not abilitiesused[a].name == "passed":
                self.target.abilitiesinforget.append([abilitiesused[a], self.value + 1])
                na = abilitiesused[a].name
                b = [i.name == na for i in self.target.abilities].index(True)
                print(self.target.name + " forgot " + self.target.abilities[b].name + " for " + str(self.value) + " turns")
                self.target.abilities = self.target.abilities[:b] + self.target.abilities[b+1:]
            
        elif self.name == "Iced":
            self.target.ai.decisionnumber -= 1
            print(self.target.name + " became ICED")
            
        elif self.name == "Fiery Spirit":
            self.target.conditions = [co for co in self.target.conditions if not(co.name == "Iced" or co.name == "Asleep" or co.name == "Paralyzed")]
                
            
            
        elif self.name == "Freezestacks":
            if self.target.freezestacks > 0:
                if 1 <= self.target.freezestacks <= 5:
                    gstate.get().system.attack([self.target], 5, a = 0)
                if 6 <= self.target.freezestacks <= 10:
                    gstate.get().system.attack([self.target], 10, a = 0)
                if 11 <= self.target.freezestacks <= 15:
                    gstate.get().system.attack([self.target], 15, a = 0)
                if 16 <= self.target.freezestacks <= 20:
                    gstate.get().system.attack([self.target], 20, a = 0)
                if 21 <= self.target.freezestacks <= 25:
                    gstate.get().system.attack([self.target], 25, a = 0)
                if 26 <= self.target.freezestacks <= 30:
                    gstate.get().system.attack([self.target], 30, a = 0)
        
            


        self.duration -= 1

            
            

#______________________________________________________________________________________________________________________________________________________________________
class ability(object): 
    def __init__(self, name, phase, targetnumber, selftarget, priority, damage, text = " ", abilitytype = "0", worked = False, cooldown = 0, channel = 0, Return = False, element = 0, orbs = [0,0,0,0,0], proficiencyneeded = 0, proficiencygiven = [0,0,0,0,0], value = 0):
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
        self.Return = Return 
        self.element = element
        self.orbs = orbs
        self.proficiencyneeded = proficiencyneeded
        self.proficiencygiven = proficiencygiven
        self.value = value
        self.text = text
        
    def clone(self):
        #print(self.name)
        return ability(self.name, self.phase, self.targetnumber, self.selftarget, self.priority, self.damage, self.text, self.abilitytype, self.worked, self.cooldown, self.channel, self.Return, self.element, self.orbs, self.proficiencyneeded, self.proficiencygiven, self.value)     
        
        
    def effect(self, targets, caster):
        caster.abilitylasttarget = self.name
        caster.abilitylasttarget = [p.name for p in targets]
        print(caster.name + " used "+ self.name)
        if self.cooldown > 0 and self.channel == 0:
            caster.abilitiesincooldown.append([self.name, self.cooldown + 1])
        
        for i in [0,1,2,3,4]:
            if self.orbs[i] > 0:  #orbs
                caster.orbs[i] -= self.orbs[i]
                print(caster.name + " spent " + str(self.orbs[i]) + " orbs ")
            
            if self.proficiencygiven[i] > 0: #proficiencies 
                caster.proficiencies[i] += self.proficiencygiven[i]
        
        if self.name == "Attack":
            caster.attack(targets, self.value)
        
        elif self.name == "Tackle":
            caster.attack(targets, 2)
            
        elif self.name == "Double Edged Sword":
            caster.attack(targets, 3)
            caster.attack([caster], 2)

        elif self.name == "Stand Tall":
            if caster.attacksreceived >= 1:
                caster.attack(targets, 7)
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
            b=R.randint(1,12)
            c=R.randint(1,12)
            d=R.randint(1,12)
            e = b + c + d
            caster.attack(targets, e , accuracy = 0.55)

        elif self.name == "Kick":
            a = R.randint(1,10)
            b = R.randint(1,10)
            c = a + b
            caster.attack(targets, c)
       
        elif self.name == "Punch":
            caster.attack(targets, 9)
            
        elif self.name == "Blood Drain":

            a = R.randint(1,8)
            b = R.randint(1,8)
            c = a + b
            caster.lifesteal += 1
            caster.attack(targets, c, accuracy = 0.75)
            
        elif self.name == "Headbutt":
            d = R.randint(1,100)
            if d <= 10:
                caster.conditions.append(condition("Paralyzed", caster, 1, 1))
                print(caster.name + " paralyzed himself with Headbutt")
            a = R.randint(1,12)
            b = R.randint(1,12)
            c = a + b
            caster.attack(targets, c)
                
        elif self.name == "On The Edge":
            a = 0
            b = 0
            for d in gstate.get().decisionlist:
                if d[0] == caster:
                    pass
                else:
                    if d[1].abilitytype == "Offensive":
                        a += 1
                        
                    if caster in d[2]:
                        b += 1 
            if a == b and a > 0:
                caster.attack(targets, 30)
            else:
                print("but it failed")
        
        elif self.name == "Everyone... GET IN HERE!":
            a = 0
            for d in gstate.get().decisionlist: #calcular quantos ataques te tao a dar target
                if d[0] == caster:
                    pass
                elif (caster in d[2]) and d[1].abilitytype == "Offensive":
                    a = a + 1
            n = 15 * a
            caster.attack(targets, n)        

        elif self.name == "From The Shadows":
            a = 0
            for d in gstate.get().decisionlist: #verificar quantas pessoas te deram target:
                if d[0] == caster:
                    pass
                elif caster in d[2]:
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
                caster.abilitiesinchannel.append([self.name, self.channel - 1, True, self.clone()])
                #este "True" é verdadeiro ou falso consuante esta habilidade foi usada esta ronda, visto que se a habilidade channel nao for usada uma ronda, entao o channel para.
                print(caster.name + " began channeling " + self.name + " for 4 rounds")
                 
            else: #a é o indice das habilidades que estao em channel que é o desta habilidade
                a = [i[0] == "Unleash The Power" for i in caster.abilitiesinchannel].index(True)
                if caster.abilitiesinchannel[a][1] == 1 or caster.abilitiesinchannel[a][1] == 0: #se o channel chegou ao fim, a habilidade atua
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

        elif self.name == "Rock Solid":
            caster.conditions.append(condition("Rock Solid", caster, 1, 1))

        elif self.name == "Regenerate":
            a = R.randint(1,10)
            caster.conditions.append(condition("Regenerate", caster, 1, a))
             
            print(caster.name + " will regenerate 3 HP per turn for " + str(a) + " turns")

        elif self.name == "Dodge":
            caster.dodge = (1 - ( (1 - caster.dodge) * (1 - 0.7) ))
            print(caster.name + " dodged this turn.")
            
        elif self.name == "Shocking Response":
            caster.conditions.append(condition("Shocking Response", caster, 3, 2 ))
            
        elif self.name == "Flight":
            a = R.randint(1,3)
            caster.conditions.append(condition("Flight", caster, 1, a))
            print(caster.name + " is flying for " + str(a) + " round(s)")
            
        elif self.name == "Nature's Call":
            a = R.randint(1,10)
            caster.conditions.append(condition("Nature's Call", caster, 1, a))
            print(caster.name + " will take 3 less damage for " + str(a) + " turns.")
            
        elif self.name == "Web Cacoon":
            caster.conditions.append(condition("Web Cacoon", caster, 3, 3 + 1))
            print(caster.name + " is encaised in a  Webby Cacoon for 3 rounds!")
            
        elif self.name == "High Jump":
            caster.conditions.append(condition("High Jump", caster, 3, 1 + 1))
            caster.conditions.append(condition("Immobilized", caster, 1, 1 + 1))
            caster.conditions.append(condition("Anti-Immobilized", caster, 1, 1))
            caster.conditions.append(condition("Double Damage", caster, 1, 1 + 1))
            caster.conditions.append(condition("Half Damage", caster, 1, 1))
            caster.dodge = 1
            print(caster.name + " Jumped high in the air!")
            
        elif self.name == "Fight Stance":
            a = R.randint(1,6)
            caster.conditions.append(condition("Fight Stance", caster, 1, a))
            print(caster.name + " will deal 7 more damage for " + str(a) + " turns because of Fight Stance")

        elif self.name == "Limitless":
            caster.conditions.append(condition("Limitless", caster, 1, 1))
            print(caster.name + " will deal double damage next turn because of Limitless")

        elif self.name == "Lullaby":
            for player in targets:
                if player == caster:
                    pass
                else:
                    a = R.randint(1,2)
                    if a == 1:
                        player.conditions.append(condition("Asleep", player, 3, 5))
                        print(caster.name + " put " + player.name + " to Sleep. ")

        elif self.name == "Intimidate":
            a = R.randint(1,6)
            for player in targets:
                if player == caster:
                    pass
                else:
                    player.conditions.append(condition("Intimidated", player, 1, a))
                    print(caster.name + " intimidated " + player.name + " for " + str(a) + " rounds ")
        
        elif self.name == "No Pain, No Gain":
            caster.conditions.append(condition("More Experience", caster, 1, 2, value = 2))
            
        elif self.name == "Reflective Mirror":
            for d in gstate.get().decisionlist:
                if caster in d[2] and d[1].abilitytype == "Offensive":
                    d[2].remove(caster)
                    d[2].append(d[0])
            print("every attack that targeted " + caster.name + " was rederected to the attacker!")
            
        elif self.name == "Target Enemy":
            caster.conditions.append(condition())
            
        elif self.name == "Taunt":
            for p in gstate.get().players:
                if p == caster:
                    p.conditions.append(condition("Taunt Origin", caster, 1, 1))
                else:
                    p.conditions.append(condition("Taunt", p, 1, 1))

            #______________________________________________________________________________________________________________________________________________________________________
            #_______________________________________________________________________________________________________________________________________________________--
            #________________________________________________________-----------------------____________________________________________________________________
            #fire:
            
        elif self.name == "Fire Burst":
            caster.attack(targets, 35)
            caster.orbs[0] += 1
            
        elif self.name == "Fire Shield":
            caster.conditions.append(condition("More Defense", caster, 1, 1, value = 10))
            caster.conditions.append(condition("Thorns", caster, 3, 1, value = 5))
            caster.orbs[0] += 1
            
        elif self.name == "Fire Charge":
            caster.orbs[0] += 2
            
        elif self.name == "Fire Blast":
            caster.attack(targets, 45)
            caster.orbs[0] += 1
            
        elif self.name == "The Floor Is Lava":
            for t in targets:
                t.conditions.append(condition("Take Damage", t, 1, duration = 4, value = 10, caster = caster))
            
        elif self.name == "Fire Rain":
            for t in targets:
                caster.attack([t], 60, accuracy = 0.7)
                
        elif self.name == "Lava Burst":
            for t in targets:
                a = R.random()
                if a < 0.6:
                    caster.attack([t], 60)
                    t.conditions.append(condition("Immobilized", t, 1, 1))
                    
        elif self.name == "Explosion":
            caster.attack(targets, 50)
            for t in targets:
                caster.attack([t], 50, accuracy = 0.5)
                
        elif self.name == "Living Inferno":
            if  not (self.name in [i[0] for i in caster.abilitiesinchannel]): #verificar se o player ja esta a dar channel à habilidade
                caster.abilitiesinchannel.append([self.name, self.channel - 1, True, self.clone()])
                #este "True" é verdadeiro ou falso consuante esta habilidade foi usada esta ronda, visto que se a habilidade channel nao for usada uma ronda, entao o channel para.
                print(caster.name + " began channeling " + self.name + " for 3 rounds")
                 
            else: #a é o indice das habilidades que estao em channel que é o desta habilidade
                a = [i[0] == "Living Inferno" for i in caster.abilitiesinchannel].index(True)
                if caster.abilitiesinchannel[a][1] == 1 or caster.abilitiesinchannel[a][1] == 0: #se o channel chegou ao fim, a habilidade atua
                    caster.abilitiesinchannel[a][1] -= 1
                    caster.attack(targets, 250)
                    b = R.randint(1,4) + 1
                    for t in targets:
                        t.conditions.append(condition("Take Damage", t, 1, duration = b, value = 50, caster = caster))
                else:
                    caster.abilitiesinchannel[a][1] -= 1
                    caster.abilitiesinchannel[a][2] = True
                     
                    print("Only " + str(caster.abilitiesinchannel[a][1]) + " turns left until " + caster.name + " uses " + self.name)
                    
        elif self.name == "Cold Flame":
            caster.attack(targets, 45)
            for t in targets:
                t.conditions.append(condition("Iced", t, "Afterstartnewround", 1))
        
        elif self.name == "Mystical Flame":
            caster.attack(targets, 45)
            for t in targets:
                a = R.random()
                if a < 0.6:
                    t.conditions.append(condition("Asleep", t, 3, 5))
                
        elif self.name == "Corrosive Flame":
            for t in targets:
                caster.soulattack([t], 80)
                
        elif self.name == "Flame Of Death":
            for t in targets:
                b = 2 + R.randint(1,8)
                t.conditions.append(condition("Take Soul Damage", t, 1, b, value = 50))
             
        elif self.name == "Forgetfull Combustion":
            caster.attack(targets, 60)
            for t in targets:
                t.conditions.append(condition("Forget",t, 4, 1, value = 6))
                
        elif self.name == "Fire Elemental":
            if  not (self.name in [i[0] for i in caster.abilitiesinchannel]): #verificar se o player ja esta a dar channel à habilidade
                caster.abilitiesinchannel.append([self.name, self.channel - 1, True, self.clone()])
                #este "True" é verdadeiro ou falso consuante esta habilidade foi usada esta ronda, visto que se a habilidade channel nao for usada uma ronda, entao o channel para.
                print(caster.name + " began channeling " + self.name + " for 2 rounds")
                 
            else: #a é o indice das habilidades que estao em channel que é o desta habilidade
                a = [i[0] == "Fire Elemental" for i in caster.abilitiesinchannel].index(True)
                if caster.abilitiesinchannel[a][1] == 1 or caster.abilitiesinchannel[a][1] == 0: #se o channel chegou ao fim, a habilidade atua
                    caster.abilitiesinchannel[a][1] -= 1
                    from creature import pet
                    from aicomponent import attackpet
                    a = pet(owner = caster, name = "Fire Elemental", color = (255,0,0), HP = 50, MaxHP = 50)
                    a.ai = attackpet(a)
                    a.abilities.append(ability("FireElementalAttack", 3, 1, False, 2, True, "Offensive"))
                    caster.pets.append(a)
                    gstate.get().availabletargets.append(a)
                else:
                    caster.abilitiesinchannel[a][1] -= 1
                    caster.abilitiesinchannel[a][2] = True
                     
                    print("Only " + str(caster.abilitiesinchannel[a][1]) + " turns left until " + caster.name + " uses " + self.name)
                    
        elif self.name == "FireElementalAttack":
            caster.attack(targets, 30)
            caster.owner.orbs[0] += 1
            
        elif self.name == "Wall Of Fire":
            a = R.randint(1,4)
            print("The Wall of fire will be active this and the next " + str(1+a) + " rounds")
            for t in targets:
                t.conditions.append(condition("Thorns", t, 3, 2+a, value = 15))
                t.conditions.append(condition("More Dodge", t, 1, 1+a, value = 0.3))
                t.conditions.append(condition("More Dodge", t, 3, 1, value = 0.3))
                t.conditions.append(condition("Less Accuracy", t, 1, 1+a, value = 0.5))
                t.conditions.append(condition("Less Accuracy", t, 3, 1, value = 0.5))
                
        elif self.name == "Healing Flames":
            caster.heal([caster], 30) 
            caster.orbs[0] += 1
            
        elif self.name == "Fiery Spirit":
            a = R.randint(1,8)
            caster.conditions.append(condition("Fiery Spirit", caster, 4, 2+a))
            print(caster.name + " has a fiery spirit for this and the next " + str(1+a) + " rounds")
            
        elif self.name == "Fire Jet":
            caster.conditions.append(condition("Immobilized", caster, 1, 1 + 1))
            caster.conditions.append(condition("Anti-Immobilized", caster, 1, 1))
            caster.conditions.append(condition("Get Thorns", caster, 4, 1, value = 10))
            caster.dodge = 1
            print(caster.name + " Jumped high in the air with a fire jet!")
            
            #______________________________________________________________________________________________________________________________________________________________________
            #_______________________________________________________________________________________________________________________________________________________--
            #________________________________________________________-----------------------____________________________________________________________________
            #ice:
            
        elif self.name == "Icicle Spike":
            caster.attack(targets, 25)
            for t in targets:
                a = R.randint(0,1)
                if a == 0:
                    t.freezestacks += 1
                    print(t.name + " was frozen ")
            caster.orbs[1] += 1
            
        elif self.name == "Ice Shield":
            caster.conditions.append(condition("More Defense", caster, 1, 1, value = 10))
            caster.conditions.append(condition("Ice Thorns", caster, 3, 1, value = 0.5))
            caster.orbs[1] += 1
            
        elif self.name == "Ice Charge":
            caster.orbs[1] += 2
            
            #______________________________________________________________________________________________________________________________________________________________________
            #_______________________________________________________________________________________________________________________________________________________--
            #________________________________________________________-----------------------____________________________________________________________________
            #tempest:
            
        # elif self.name == "Discharge":
            # caster.attack(targets, 25)
            # for t in targets:
                # a = R.randint(0,1)
                # if a == 0:
                    # t.freezestacks += 1
                    # print(t.name + " was frozen ")
            # caster.orbs[1] += 1
            # caster.proficiencies[1] += 1
            
        # elif self.name == "Wind Shield":
            # caster.conditions.append(condition("More Defense", caster, 1, 1, value = 10))
            # caster.conditions.append(condition("Ice Thorns", caster, 3, 1, value = 0.5))
            # caster.orbs[1] += 1
            # caster.proficiencies[1] += 1
            
        # elif self.name == "Tempest Charge":
            # caster.orbs[1] += 2
            # caster.proficiencies[1] += 1
            
            #______________________________________________________________________________________________________________________________________________________________________
            #_______________________________________________________________________________________________________________________________________________________--
            #________________________________________________________-----------------------____________________________________________________________________
            #necrotic:
            
        elif self.name == "Necrotic Wave":
            caster.soulattack(targets, 20)
            for t in targets:
                caster.heal([caster], 10)
            caster.orbs[3] += 1
            
        elif self.name == "Paralyzing Gaze":
            for t in targets:
                b = R.random()
                if b < 0.2:
                    t.conditions.append(condition("Paralyzed", t, 1, 1))
            caster.orbs[3] += 1
            
        elif self.name == "Necrotic Charge":
            caster.orbs[3] += 2
            
            #______________________________________________________________________________________________________________________________________________________________________
            #_______________________________________________________________________________________________________________________________________________________--
            #________________________________________________________-----------------------____________________________________________________________________
            #mind:
        elif self.name == "Mind Burst":
            caster.attack(targets, 25)
            for t in targets:
                a = R.random()
                if a < 0.4:
                    t.conditions.append(condition("Forget", t, 4, 1, value = 2))
            caster.orbs[4] += 1
            
        elif self.name == "Dull Mind":
            for t in targets:
                a = R.random()
                if a < 0.2:
                    t.conditions.append(condition("Asleep", t, 3, 5))
            caster.orbs[4] += 1
            
        elif self.name == "Mind Charge":
            caster.orbs[4] += 2
            
        elif self.name == "passed":
            caster.abilitylasttarget = []
            print(caster.name + " did nothing.")
        elif self.name == "Asleep":
            caster.abilitylasttarget = []
            
        #caster.abilitylastused = self.name
     
     
     
class buff():

    def __init__(self, name, bufftype1, bufftype2, text, value = 0, duration = 1): #bufftype1 é se é uma blessing ou uma curse, bufftype2 é se é instantaneo ou dá uma condiçao
        self.name = name
        self.renderables = []
        self.bufftype1 = bufftype1 
        self.bufftype2 = bufftype2
        self.text = text
        self.value = value
        self.duration = duration
        
    def draw(self,screen):
        for r in self.renderables:
            r.draw(screen)
            
    def effect(self, target):
        if self.bufftype2 == "Condition":
            if self.name == "Double Damage":
                target.conditions.append(condition("Double Damage", target, 1, self.duration))
                print(target.name + " will deal double damage for " + str(self.duration) + " turns.")
                
            elif self.name == "Lifesteal":
                target.conditions.append(condition("Lifesteal", target, 1, duration = self.duration, value = self.value))
                
            elif self.name == "Take Damage":
                target.conditions.append(condition("Take Damage", target, 2, duration = self.duration, value = self.value))
                
            elif self.name == "Damage":
                target.conditions.append(condition("Take Damage", target, 2, duration = self.duration, value = self.value))

            elif self.name == "Heal":
                target.conditions.append(condition("Take Heal", target, 2, duration = self.duration, value = self.value))
                
            elif self.name == "Less Damage":
                target.conditions.append(condition("Less Damage", target, 1, duration = self.duration, value = self.value))
                
            elif self.name == "More Damage":
                target.conditions.append(condition("More Damage", target, 1, duration = self.duration, value = self.value))
                
            elif self.name == "Heal Modifier":
                target.conditions.append(condition("Heal Modifier", target, 1, duration = self.duration, value = self.value))
                
            elif self.name == "More Experience":
                target.conditions.append(condition("More Experience", target, 1, duration = self.duration, value = self.value))
                
            elif self.name == "Become Paralyzed":
                target.conditions.append(condition("Become Paralyzed", target, 3, duration = self.duration, value = self.value))
                
        elif self.bufftype2 == "Instantaneous":
            pass
                
            
                