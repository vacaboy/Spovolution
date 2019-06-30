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
            target.heal([target], 3)

        elif self.name == "Fight Stance":
            self.target.attackadd = 7
            print(self.target.name + " deals 7 more damage this turn")
            # if self.target.ability.damage and self.target.ability.worked:
                # for target in self.target.target:
                    # target.HP -= 7 
                    # self.target.EXP += 7
                    # target.EXP += 7
                    # print(self.target.name + " dealt 7 more damage")

        elif self.name == "Limitless":
            self.target.attackmultiplier = 2
            print(self.target.name + " dealt double extra damage because of Limiless")
            # for i in gstate.get().log:
                # if i[0] == self.target:
                    # i[2].HP -= i[1]
                    # i[2].EXP += i[1]
                    # self.target.EXP += i[1]
                    # print(self.target.name + " dealt " + str(i[1]) + " extra damage because of Limiless")

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
            # if self.target.ability.damage and self.target.ability.worked:
                # for i in gstate.get().log:
                    # if i[0] == self.target:
                        # a = 5
                        # if i[1] < 5:
                            # a = i[i]
                        # i[2].HP += a 
                        # self.target.EXP -= a
                        # i[2].EXP -= a
                        # print(self.target.name + " dealt minus " + str(a) + " damage")
                


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


        
    # def effect(self, targets, caster):
        
        # if self.name == "Tackle":
            # caster.abilitylastused = "Tackle"
            # caster.abilitylasttarget = [player.name for player in targets]
            # caster.dealtdamage = True
            # for target in targets:
                # gstate.get().log.append([caster, 2, target])
                # caster.EXP += 2
                # target.EXP += 2
                # target.HP -= 2
                # target.damaged = True
                # target.attacksreceived += 1
                #  
                # print(caster.name + " dealt 2 damage to " + target.name + " using tackle")

        # elif self.name == "Double Edged Sword":
            # caster.abilitylastused = "Double Edged Sword"
            # caster.abilitylasttarget = [player.name for player in targets]
            # caster.dealtdamage = True
            # for target in targets:
                # gstate.get().log.append([caster, 3, target])
                # gstate.get().log.append([caster, 2, caster])
                # caster.EXP += 5
                # caster.HP -= 2
                # target.EXP += 3
                # target.HP -= 3
                # target.damaged = True
                # target.attacksreceived += 1
                #  
                # print(caster.name + " dealt 3 damage to " + target.name + " using double edged sword")
                # print(caster.name + " dealt 2 damage to " + caster.name + " because of double edged sword")

        # elif self.name == "Stand Tall":
            # caster.abilitylastused = "Stand Tall"
            # caster.abilitylasttarget = [player.name for player in targets]
            # if caster.attacksreceived >= 2:
                # for target in targets:
                    # gstate.get().log.append([caster, 8, target])
                    # caster.EXP += 8
                    # target.EXP += 8
                    # target.HP -= 8
                    #  
                    # print(caster.name + " dealt 8 damage to " + target.name + " using Stand Tall")
            
        # elif self.name == "Uncertain Footing":
            # caster.abilitylastused = "Uncertain Footing"
            # caster.abilitylasttarget = [player.name for player in targets]
            # if not caster.damaged:
                # for target in targets:
                    # gstate.get().log.append([caster, 8, target])
                    # caster.EXP += 8
                    # target.EXP += 8
                    # target.HP -= 8
                    #  
                    # print(caster.name + " dealt 8 damage to " + target.name + " using Uncertain Footing")

        # elif self.name == "QuickPoke":
            # caster.abilitylastused = "QuickPoke"
            # caster.abilitylasttarget = [p.name for p in targets]
# ##            for player in player:
# ##                if player == self.caster:
# ##                    pass
# ##                else:
# ##                    caster.abilitylasttarget.append(player.name)
            # caster.dealtdamage = True
            # for target in players:
                # if target == caster:
                    # pass
                # else:
                    # gstate.get().log.append([caster, 1, target])
                    # target.EXP += 1
                    # target.HP -= 1
                    # caster.EXP += 1
                    # target.damaged = True
                    # target.attacksreceived += 1
                    #  
                    # print(caster.name + " dealt 1 damage to " + target.name + " using QuickPoke")
                
        # elif self.name == "chill":
            # caster.abilitylastused = "chill"
            # caster.abilitylasttarget = [player.name for player in targets]
            # caster.HP += 3
            #  
            # print(caster.name + " regained 3 damage using Chill")

        # elif self.name == "Spear Throw":
            # caster.abilitylastused = "Spear Trhow"
            # caster.abilitylasttarget = [player.name for player in targets]
            # a = R.randint(1, 100)
            # if a > 55:
                # print(caster.name + " missed the Spear Throw")
            # else:
                # caster.dealtdamage = True
                # b=R.randint(1,12)
                # c=R.randint(1,12)
                # d=R.randint(1,12)
                # e = b + c + d
                # for target in targets:
                    # gstate.get().log.append([caster, e, target])
                    # caster.EXP += e
                    # target.HP -= e
                    # target.EXP += e
                    # target.damaged = True
                    # target.attacksreceived += 1
                    #  
                    # print(caster.name + " dealt " + str(e) +" damage to " + target.name + " using Spear Throw")

        # elif self.name == "Kick":
            # caster.abilitylastused = "Kick"
            # caster.abilitylasttarget = [player.name for player in targets]
            # caster.dealtdamage = True
            # a = R.randint(1,10)
            # b = R.randint(1,10)
            # c = a + b
            # for target in targets:
                # gstate.get().log.append([caster, c, target])
                # caster.EXP += c
                # target.EXP += c
                # target.HP -= c
                # target.damaged = True
                # target.attacksreceived += 1
                #  
                # print(caster.name + " dealt " + str(c) +" damage to " + target.name + " using Kick")

        # elif self.name == "Punch":
            # caster.abilitylastused = "Punch"
            # caster.abilitylasttarget = [player.name for player in targets]
            # caster.dealtdamage = True
            # for target in targets:
                # gstate.get().log.append([caster, 9, target])
                # caster.EXP += 9
                # target.EXP += 9
                # target.HP -= 9
                # target.damaged = True
                # target.attacksreceived += 1
                #  
                # print(caster.name + " dealt 9 damage to " + target.name + " using Punch")

        # elif self.name == "Blood Drain":
            # caster.abilitylastused = "Blood Drain"
            # caster.abilitylasttarget = [player.name for player in targets]
            # d = R.randint(1,100)
            # if d <= 75:
                # caster.dealtdamage = True
                # a = R.randint(1,8)
                # b = R.randint(1,8)
                # c = a + b
                # for target in targets:
                    # gstate.get().log.append([caster, c, target])
                    # caster.EXP += c
                    # target.EXP += c
                    # target.HP -= c
                    # caster.HP += c
                    # target.damaged = True
                    # target.attacksreceived += 1
                    #  
                    # print(caster.name + " dealt " + str(c) +" damage to " + target.name + " using Blood Drain")
            # else:
                # print(caster.name + " missed Blood Drain")

        # elif self.name == "Headbutt":
            # caster.abilitylastused = "Headbutt"
            # caster.abilitylasttarget = [player.name for player in targets]
            # caster.dealtdamage = True
            # d = R.randint(1,100)
            # if d <= 10:
                # caster.conditions.append(condition("Paralyzed", caster, "chooseability", 1))
                # print(caster.name + " paralyzed himself with Headbutt")
            # for target in targets:
                # a = R.randint(1,12)
                # b = R.randint(1,12)
                # c = a + b
                # gstate.get().log.append([caster, c, target])
                # caster.EXP += c
                # target.EXP += c
                # target.HP -= c
                # target.damaged = True
                # target.attacksreceived += 1
                #  
                # print(caster.name + " dealt " + str(c) + " damage to " + target.name + " using Headbutt. d = " + str(d))
                
        # elif self.name == "On The Edge":
            # caster.abilitylastused = "On The Edge"
            # caster.abilitylasttarget = [player.name for player in targets]
            # a = 0
            # b = 0
            # for player in players:
                # if player == caster:
                    # pass
                # else:
                    # if player.ability.abilitytype == "Offensive":
                        # a += 1
                    # if caster in player.target:
                        # b += 1
            
            # if a == b and a > 0:
                # for target in targets:
                    # gstate.get().log.append([caster, 30, target])
                    # caster.EXP += 30
                    # target.EXP += 30
                    # target.HP -= 30
                    #  
                    # target.damaged = True
                    # target.attacksreceived += 1
                    # print(caster.name + " dealt 30 damage to " + target.name + " using On The Edge")

        
        # elif self.name == "Everyone... GET IN HERE!":
            # caster.abilitylastused = "Everyone... GET IN HERE!"
            # caster.abilitylasttarget = [player.name for player in targets]
            # a = 0
            # for p in players: #calcular quantos ataques te tao a dar target
                # if p == caster:
                    # pass
                # elif (caster in p.target) and p.ability.abilitytype == "Offensive":
                    # a = a + 1
                    
            # for target in targets:
                # n = 0
                # for i in range(a):
                    # b = R.randint(1,15)
                    # n = n + b
                # gstate.get().log.append([caster, n, target])
                # caster.EXP += n
                # target.EXP += n
                # target.HP -= n
                #  
                # target.damaged = True
                # target.attacksreceived += 1
                # print(caster.name + " dealt " + str(n) + " damage to " + target.name + " using Everyone... GET IN HERE!")

        # elif self.name == "From The Shadows":
            # caster.abilitylastused = "From The Shadows"
            # caster.abilitylasttarget = [player.name for player in targets]
            # a = 0
            # for p in players: #verificar quantas pessoas te deram target:
                # if p == caster:
                    # pass
                # elif caster in p.target:
                    # a = a + 1
            # if a == 0:
                # for target in targets:
                    # n = 0
                    # for i in range(6):
                        # b = R.randint(1,6)
                        # n = n + b
                    # gstate.get().log.append([caster, n, target])
                    # caster.EXP += n
                    # target.EXP += n
                    # target.HP -= n
                    #  
                    # target.damaged = True
                    # target.attacksreceived += 1
                    # print(caster.name + " dealt " + str(n) + " damage to " + target.name + " using From The Shadows")

        # elif self.name == "Unleash The Power":
            # caster.abilitylastused = "Unleash The Power"
            # caster.abilitylasttarget = [player.name for player in targets]
            # if  not (self.name in [i[0] for i in caster.abilitiesinchannel]): #verificar se o player ja esta a dar channel à habilidade
                # caster.abilitiesinchannel.append([self.name, self.channel - 1, True])
                # #este "True" é verdadeiro ou falso consuante esta habilidade foi usada esta ronda, visto que se a habilidade channel nao for usada uma ronda, entao o channel para.
                # print(caster.name + " began channeling " + self.name + " for 4 rounds")
                #  
            # else: #a é o indice das habilidades que estao em channel que é o desta habilidade
                # a = [i[0] == "Unleash The Power" for i in caster.abilitiesinchannel].index(True)
                # if caster.abilitiesinchannel[a][1] == 1: #se o channel chegou ao fim, a habilidade atua
                    # caster.abilitiesinchannel[a][1] -= 1
                    # b = R.randint(1,14)
                    # c = R.randint(1,14)
                    # d = R.randint(1,14)
                    # e = R.randint(1,14)
                    # f = b + c + d + e
                    # caster.abilitiesincooldown.append(["Unleash The Power", 3 + 1])
                    # for t in targets:
                        # t.EXP += f
                        # t.HP -= f
                        # caster.EXP += f
                        #  
                        # t.damaged = True
                        # t.attacksreceived += 1
                        # gstate.get().log.append([caster, f, t])
                        # print(caster.name + " dealt " + str(f) + " damage to " + t.name + " using Unleash The Power")
                # else:
                    # caster.abilitiesinchannel[a][1] -= 1
                    # caster.abilitiesinchannel[a][2] = True
                    #  
                    # print("Only " + str(caster.abilitiesinchannel[a][1]) + " turns left until " + caster.name + " Unleashes The Power")
                    
        # elif self.name == "Refreshing Waters":
            # caster.abilitylastused = "Refreshing Waters"
            # caster.abilitylasttarget = [player.name for player in targets]
            # caster.HP += 12
            #  
            # print(caster.name + " regained 12 damage using Refreshing Waters")

        # elif self.name == "Rock Solid":
            # caster.abilitylastused = "Rock Solid"
            # caster.abilitylasttarget = [player.name for player in targets]
            # caster.conditions.append(condition("Rock Solid", caster, "chooseability", 1))
            #  
            # caster.abilitiesincooldown.append(["Rock Solid", 5 + 1])

        # elif self.name == "Regenerate":
            # caster.abilitylasttarget = [player.name for player in targets]
            # a = R.randint(1,10)
            # caster.conditions.append(condition("Regenerate", caster, 1, a))
            #  
            # print(caster.name + " will regenerate 3 HP per turn for " + str(a) + " turns")

        # elif self.name == "Fight Stance":
            # caster.abilitylasttarget = [player.name for player in targets]
            # a = R.randint(1,6)
            # caster.conditions.append(condition("Fight Stance", caster, "chooseability", a + 1))
            #  
            # print(caster.name + " will deal 7 more damage for " + str(a) + " turns because of Fight Stance")

        # elif self.name == "Limitless":
            # caster.abilitylasttarget = [player.name for player in targets]
            # caster.conditions.append(condition("Limitless", caster, "chooseability", 1 + 1))
            #  
            # caster.abilitiesincooldown.append(["Limitless", 999])
            # #self.cooldown = 999
            # print(caster.name + " will deal double damage next turn because of Limitless")

        # elif self.name == "Lullaby":
            # caster.abilitylasttarget = [player.name for player in targets]
            # print(caster.name + " sang a Lullaby")
            # caster.abilitiesincooldown.append(["Lullaby", 5 + 1])
            # #self.cooldown = 5 + 1
            # for player in players:
                # if player == caster:
                    # pass
                # else:
                    # a = R.randint(1,2)
                    # if a == 1:
                        # player.conditions.append(condition("Asleep", player, "chooseability", 5))
                        # print(caster.name + " put " + player.name + " to Sleep. ")

        # elif self.name == "Intimidate":
            # caster.abilitylasttarget = [player.name for player in targets]
            # caster.abilitiesincooldown.append(["Intimidate", 1 + 1])
            # a = R.randint(1,6)
            # for player in players:
                # if player == caster:
                    # pass
                # else:
                    # player.conditions.append(condition("Intimidated", player, "chooseability", a + 1))
                    # print(caster.name + " intimidated " + player.name + " for " + str(a) + " rounds ")
            
        # elif self.name == "teste":
            # caster.abilitylasttarget = [player.name for player in targets]
            # caster.conditions.append(condition("teste", caster, 3, 4))


        # elif self.name == "teste2":
            # caster.abilitylasttarget = [player.name for player in targets]
            # for target in targets:
                # target.conditions.append(condition("Paralyzed", target, "chooseability", 1))
                    
        # elif self.name == "passed":
            # caster.abilitylasttarget = []
            #  
            # print(caster.name + " did nothing.")
            # pass
        # caster.abilitylastused = self.name
        
        
        
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
            for player in players:
                if player == caster:
                    pass
                else:
                    if player.ability.abilitytype == "Offensive":
                        a += 1
                    if caster in player.target:
                        b += 1    
            if a == b and a > 0:
                caster.attack(targets, 30)


        
        elif self.name == "Everyone... GET IN HERE!":
            a = 0
            for p in players: #calcular quantos ataques te tao a dar target
                if p == caster:
                    pass
                elif (caster in p.target) and p.ability.abilitytype == "Offensive":
                    a = a + 1
            n = 0
            for i in range(a):
                b = R.randint(1,15)
                n = n + b
            caster.attack(targets, n)        

        elif self.name == "From The Shadows":
            a = 0
            for p in players: #verificar quantas pessoas te deram target:
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
            for player in players:
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
            for player in players:
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