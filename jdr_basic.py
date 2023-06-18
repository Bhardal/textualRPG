from random import randint
from time import sleep
from math import floor

class Creature:
    def __init__(self, name = "Monster", weapon = 1, ring = 2, level = 1, toughness = 0, agility = 0, magic = 0, stealth = 0, force = 0, intelligence = 0, luck = 0, stamina = 0):
        self.inFight = 0
        self.hp = self.maxHp = 400
        self.nbpots = self.nbpotsmax = 5
        self.armor = randint(10, 20)
        self.armorUpgrade = 1
        self.weapon = weapon
        self.weaponUpgrade = 1
        self.ring = ring
        self.ringUpgrade = 1
        self.name = name
        self.money =  0
        self.mana = 100
        self.level = level
        self.xp = 0
        self.toughness = toughness
        self.agility = agility
        self.magic = magic
        self.stealth = stealth
        self.force = force
        self.intelligence = intelligence
        self.luck = luck
        self.stamina = stamina
        self.points = randint(40, 60)
        

    def attack(self, enemy, game):
        damage = self.agility*5+self.force*10 + self.weapon
        damage = damage - enemy.toughness - enemy.armor 
        if randint(0, 100) <= (self.luck/30)*100:
            print(f"Critical Hit on {enemy.name} !")
            damage *= 2
        elif randint(0, 100) <= (enemy.agility/40)*100:
            print(f"{self.name} missed !")
            damage = 0
        if damage < 0:
            damage = 0
        enemy.hp -= damage
        if enemy.hp <= 0:
            enemy.Death(self, game)
        self.inFight = 1
        self.levelUp()
        self.levelUp()
        self.levelUp()


    def attackSpell(self, enemy, game):
        if self.mana - 20 >= 0:
            damage = self.intelligence * 7.5 + self.magic *15 + self.ring
            damage = damage - enemy.toughness - enemy.armor 
            if randint(0, 100) <= (self.luck/30)*100:
                print(f"Critical Hit on {enemy.name}  !")
                damage *= 2
            elif randint(0, 100) <= (enemy.agility/40)*100:
                print(f"{self.name} missed")
                damage = 0
            if damage < 0:
                damage = 0
            enemy.hp -= damage
            self.mana -= 20
        if enemy.hp <= 0:
            enemy.Death(self, game)
        self.inFight = 1
        self.levelUp()
        self.levelUp()
        self.levelUp()


    def flee(self, enemy, game):
        if randint(0, 100) <= (self.luck/30)*100:
            print("You managed to fled the fight. The opponent's health has been restored")
            enemy.hp = enemy.maxHp
            enemy.mana = 100
            self.inFight = 0
            game.Village()
        else:
            print("You failed to escape the fight.")
            self.inFight = 1
            

    
    def avoidFight(self, enemy, game):
        if randint(0, 100) <= (self.stealth/40)*100 + (self.luck/80)*100:
            print("You avoided this fight.")
            del game.mobs[0]
            self.inFight = 0
        else:
            print("You didn't manage to avoid the fight. The enemy is attacking !")
            self.inFight = 1


    def usePot(self):
        if self.nbpots > 0:
            self.nbpots -= 1
            if self.hp + 500 <= self.maxHp:
                self.hp += 500
            else:
                self.hp = self.maxHp
    

    def healSpell(self):
        if self.mana > 19:
            self.hp = self.maxHp
            self.mana -= 20


    def buyPot(self):
        if self.money > 119:
            if self.nbpots +1 <= self.nbpotsmax + self.stamina/5:
                self.nbpots += 1
                self.money -= 120
                print(f"You bought a new potion. You now have {self.nbpots} potions")
            else:
                print("You cannot store more potions. It would be too heavy for you.")
        else:
            print("You don't have enough money to buy a new potion. A potion costs 120.")
    
    def buyArmor(self):
        if self.money >= 150*self.armorUpgrade:
            self.money -= 150*self.armorUpgrade
            self.armorUpgrade += 1
            self.armor += self.armorUpgrade*10
            print(f"Your armor was reforged and you gained an additional {self.armorUpgrade*10} defense")
        else:
            print(f"You don't have enough money to upgrade your armor. The upgrade costs {150*self.armorUpgrade}")
    

    def buyWeapon(self):
        if self.money >= 150*self.weaponUpgrade:
            self.money -= 150*self.weaponUpgrade
            self.weaponUpgrade += 1
            self.weapon += self.weaponUpgrade*10
            print(f"Your weapon was reforged and you gained an additional {self.weaponUpgrade*10} melee damage.")
        else:
            print(f"You don't have enough money to upgrade your weapon. The upgrade costs {150*self.weaponUpgrade}")

    
    def buyRing(self):
        if self.money >= 175*self.ringUpgrade:
            self.money -= 175*self.ringUpgrade
            self.ringUpgrade += 1
            self.ring += self.ringUpgrade*15
            print(f"You bought a new ring. You can now deal {self.ringUpgrade*15} more magic damage.")
        else:
            print(f"You don't have enough money to buy a new ring. A new one will cost {175*self.ringUpgrade}")
    

    def levelUp(self):
        if self.xp >= (self.level**2)*10:
            self.xp -= (self.level**2)*10
            self.level += 1
            self.points += 5
            print("You leveled up ! You earned 5 skill points")
            print(f"You have {self.points} unused skill points")
    

    def Toughness(self):
        if self.points > 0 and self.toughness < 20:
            self.toughness += 1
            self.points -= 1
            print("You feel more resistant")
            if self.toughness == 20:
                print("Your skin is as hard as rock ! (+20 toughness)")
                self.toughness += 20
    

    def Agility(self):
        if self.points > 0 and self.agility < 20:
            self.agility += 1
            self.points -= 1
            print("You feel faster")
            if self.agility == 20:
                print("You are now as fast as wind ! (agility + 10)")
                self.agility += 10
    

    def Magic(self):
        if self.points > 0 and self.magic < 20:
            self.magic += 1
            self.points -= 1
            print("Your connection with magic deepens")
            if self.magic == 20:
                print("You feel magic flowing through your body ! (magic +10)")
                self.magic += 10
    

    def Stealth(self):
        if self.points > 0 and self.stealth < 20:
            self.stealth += 1
            self.points -= 1
            print("You feel stealthier")
            if self.stealth == 20:
                print("You feel invisible ! (stealh + 10)")
                self.stealth += 10
    

    def Force(self):
        if self.points > 0 and self.force < 20:
            self.force += 1
            self.points -= 1
            print("You feel stronger")
            if self.force == 20:
                print("You now have the strengh of ten men ! (force + 10)")
                self.force += 10
    

    def Intelligence(self):
        if self.points > 0 and self.intelligence < 20:
            self.intelligence += 1
            self.points -= 1
            print("You feel smarter")
            if self.intelligence == 20:
                print("It's as if you've read all Alexandry's library ! (intelligence +10)")
                self.intelligence += 10
    

    def Luck(self):
        if self.points > 0 and self.luck < 20:
            self.luck += 1
            self.points -= 1
            print("You feel lucky")
            if self.luck == 20:
                print("You are as lucky as a leprechaun ! (luck + 10)")
                self.luck += 10
    

    def Stamina(self):
        if self.points > 0 and self.stamina < 20:
            self.stamina += 1
            self.points -= 1
            self.hp += self.stamina**2
            self.maxHp += self.stamina**2
            print(f"You feel better and your health increased by {self.stamina**2}")
            if self.stamina == 20:
                print("You feel immortal ! (stamina + 10)")
                for _ in range (10):
                    self.stamina += 1
                    self.hp += self.stamina**2
                    self.maxHp += self.stamina**2


    def Death(self, enemy, game):
        print("You Died")
        sleep(5)
        a = input("Press enter to exit : ")
        exit()
    

class Monster(Creature):
    def __init__(self, name, weapon, ring, level, toughness, agility, magic, stealth, force, intelligence, luck, stamina):
        self.inFight = 1
        self.hp = self.maxHp = int(floor(level**2)*15)
        self.nbpots = self.nbpotsmax = 0
        self.armor = int(floor(randint(10, 20)*(0.10*level)))
        self.armorUpgrade = 1
        self.weapon = weapon
        self.weaponUpgrade = 1
        self.ring = ring
        self.ringUpgrade = 1
        self.name = name
        self.money =  int(randint(10, 100)*level)
        self.mana = 100
        self.level = level
        self.xp = int(floor(self.level**2*2))
        self.toughness = toughness
        self.agility = agility
        self.magic = magic
        self.stealth = stealth
        self.force = force
        self.intelligence = intelligence
        self.luck = luck
        self.stamina = stamina


    def fight(self, player, game):
        if randint(0,1) == 0:
            self.attack(player, game)
        else:
            self.attackSpell(player, game)

    
    def Death(self, player, game):
        player.money += int(self.money*(1+player.luck/20))
        player.mana += 25
        if  player.mana > 100:
            player.mana = 100
        player.xp += self.xp
        del game.mobs[0]
        game.nbMobs -= 1
        if game.mobs == []:
            player.inFight = 0

    
    def levelUp(self):
        self.xp = self.xp


class Game:
    def __init__(self, p1, difficulty = 1, p2=None, p3=None, p4=None):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.difficulty = difficulty + 10
        self.area = 0
        self.nbPersos = 1
        if self.p2 != None:
            self.nbPersos += 1
        if self.p3 != None:
            self.nbPersos += 1
        if self.p4 != None:
            self.nbPersos +=1 
        self.nbMobs = 0
        self.mobLevel = 0
        self.mobs = []
        self.names = ["Zyneste l'indomptable", "Dasuke le rebelle", "Synestra l'elfe noire", "Goultard l'abruti", "Ada la stupide", "Voker le gardien", "Mage Nothar", "Mage Witfar","Eli le prophète", "Randarcos le barbare", "Zilka la stranguleuse", "Uhmar le guerrier", "Prisane l'aquatique", "Nathon le malformé", "l'archère Fayenia", "Sathe le sournois", "Wyeth le drogué", "Urda la demeurée", "Zytan le gitan", "Lox l'horloger fou", "le magnifique Migorn", "Gamud l'irresponsable", "Samondrag le chevaucheur de wyvern", "Teresa la télépathe", "Vacon l'agile", "Migorn le nain sans richesse", "Elthen le forgeron démoniaque", "Laki la succube", "Mercy l'ange déchue", "Io la déesse oubliée", "Lya la corrompue", "le démon Bodial", "Aslan l'animal", "Senic le rapide", "Dakmon l'Aorz", "Zary l'artiste décadent", "Zakya la Russe", "Ive le désespéré", "l'ombre de Touckthol", "   l'invaincu", "Tok l'additif", "Atlin le sans-âme", "Chino la sanguinaire", "Linwang le dresseur de morts", "Haddock l'insaisissable", "Randar le maniaque", "IbfistXithyl l'imcompris", "Aldaren l'invocatrice", "Shillenieli l'elfe perdue", "Bedic le soigneur", "Staph l'idiote", "Azazel l'ange perverse", "Kib l'avaleur", "Sidaravalot démon noir", "Gilby le mal-aimé", "Vora l'apocalypse", "Zhang le ninja renégat", "Corvis le mage sans sceptre", "AidoKoDon", ]



    def printNew(self, x):
        for _ in range(x):
            print("")


    def Loading(self):
        print("Loading, please wait.")
        sleep(0.5)
        print("Loading, please wait..")
        sleep(0.5)
        print("Loading, please wait...")
        sleep(0.5)

        
    def place(self):
        if self.mobs == []:
            self.area += 1
            self.difficulty += 1
            self.printNew(50)
            print("Area cleared !")
            self.printNew(10)
            sleep(2)
        elif self.p1.inFight == 0:
            self.Village()
        else:
            self.Fight() 

    
    def Village(self):
        ok = 1
        while ok:
            input("press enter to continue : ")
            self.printNew(50)
            if self.p1.points > 0:
                print(f"You have {self.p1.points} skill points to use")
            choice = str(input("You can rest (1), go to fight (2), enter the shop (3), level up (4), switch character (5), \nKill yourself (9) : "))
            try:
                if 1 <= int(choice) <= 6:
                    ok = 0
                elif int(choice) == 9:
                    ok = 0
            except:
                ok = 1
            if choice == "cheatcode":
                ok = 0

        if choice == "1":
            self.printNew(3)
            print("You rested. Your hps and mana are restored.")
            self.p1.hp = self.p1.maxHp
            if self.p2 != None:
                self.p2.hp = self.p2.maxHp
            if self.p3 != None:
                self.p3.hp = self.p3.maxHp
            if self.p4 != None:
                self.p4.hp = self.p4.maxHp
        elif choice == "2":
            self.printNew(3)
            print("You chose to fight !")
            self.printNew(3)
            self.Loading()
            self.newFight()
        elif choice == "3":
            self.printNew(3)
            print("You're entering the shop.")
            self.printNew(3)
            self.Loading()
            self.Shop()
        elif choice == "4":
            choice = "done"
            self.LevelUp()
        elif choice == "5":
            choice = "done"
            self.Switch()
            self.place()
        elif choice == "cheatcode":
            print("You were granted 50 skill points")
            self.p1.points += 50
            self.Village()
        elif choice == "9":
            self.p1.Death(self.mobs, self)


    def Shop(self):
        ok = 1
        while ok:
            input("press enter to continue : ")
            self.printNew(50)
            print(f"You have {self.p1.money} coins.")
            print(f"A potion costs 120 coins. Upgrading your weapon costs {150*self.p1.weaponUpgrade} coins. Upgrading your armor costs {150*self.p1.armorUpgrade} coins. A new ring will cost {self.p1.ringUpgrade*175}")
            choice = str(input("Buy potion (1), Upgrade your weapon (2), Upgrade your armor (3), Buy a new magic ring (4), \nLeave the shop (9),show help (10) : "))
            if choice == "1":
                self.printNew(3)
                self.p1.buyPot()
            elif choice == "2":
                self.printNew(3)
                self.p1.buyWeapon()
            elif choice == "3":
                self.printNew(3)
                self.p1.buyArmor()
            elif choice == "4":
                self.printNew(3)
                self.p1.buyRing()
            elif choice == "9":
                ok = 0
            elif choice == "10":
                self.printNew(50)
                print("In the shop you can use your coins to improve your stuff.")
                print("Every upgrade will cost more and more, but will add even more power.")
                print("For example, upgrading a weapon for the first time is 150 coins and increases the attack by 20")
                print("And upgrading it for the second time costs 300 coins and add 30 to the attack increase")
        self.printNew(3)
        self.Loading()
        self.Village()
    

    def LevelUp(self):
        ok = 1
        while ok:
            input("press enter to continue : ")
            self.printNew(50)
            print(f"You have {self.p1.toughness} toughness, {self.p1.agility} agility, {self.p1.magic} magic, {self.p1.stealth} stealth, {self.p1.force} force, {self.p1.intelligence} intelligence, {self.p1.luck} luck and {self.p1.stamina} stamina")
            print(f"You have {self.p1.points} skill points to use")
            self.printNew(3)
            choice = str(input("assign five skill points (0), toughness (1), agility (2), magic (3), stealth (4), force (5), intelligence (6), luck (7), stamina (8),\ngo back to village (9), show help (10) : "))
            if choice == "0":
                ok2 = 1
                while ok2:
                    input("press enter to continue : ")
                    self.printNew(50)
                    print(f"You have {self.p1.toughness} toughness, {self.p1.agility} agility, {self.p1.magic} magic, {self.p1.stealth} stealth, {self.p1.force} force, {self.p1.intelligence} intelligence, {self.p1.luck} luck and {self.p1.stamina} stamina")
                    print(f"You have {self.p1.points} skill points to use")
                    self.printNew(3)
                    choice = str(input("toughness (1), agility (2), magic (3), stealth (4), force (5), intelligence (6), luck (7), stamina (8),\ngo back to assign one point (9), show help (10) : "))
                    if choice == "1":
                        self.printNew(3)
                        for _ in range(5):
                            self.p1.Toughness()
                    elif choice == "2":
                        self.printNew(3)
                        for _ in range(5):
                            self.p1.Agility()
                    elif choice == "3":
                        self.printNew(3)
                        for _ in range(5):
                            self.p1.Magic()
                    elif choice == "4":
                        self.printNew(3)
                        for _ in range(5):
                            self.p1.Stealth()
                    elif choice == "5":
                        self.printNew(3)
                        for _ in range(5):
                            self.p1.Force()
                    elif choice == "6":
                        self.printNew(3)
                        for _ in range(5):
                            self.p1.Intelligence()
                    elif choice == "7":
                        self.printNew(3)
                        for _ in range(5):
                            self.p1.Luck()
                    elif choice == "8":
                        self.printNew(3)
                        for _ in range(5):
                            self.p1.Stamina()
                    elif choice == "9":
                        ok2 = 0
                    elif choice == "10":
                        self.printNew(50)
                        print("You can increase your stats up to 20 points each.")
                        print("Once a stat is maxed, you get a bonus.")
                        print("")
                        input("press enter to show more : ")
                        print("")
                        print("Toughness reduces the damages you take")
                        print("Agility increases your dodge rate and gives you some additional damages")
                        print("Magic greatly increases your magic damages")
                        print("Stealth greatly increases the chance to skip a figth")
                        print("Force greatly increases your sword damages")
                        print("Intelligence increases your magic damages")
                        print("Luck increases the amount of coins you get, your crit rate, the chance to skip or flee a fight")
                        print("Stamina increases the number of potions you can carry and increases greatly your hps")
            elif choice == "1":
                self.printNew(3)
                self.p1.Toughness()
            elif choice == "2":
                self.printNew(3)
                self.p1.Agility()
            elif choice == "3":
                self.printNew(3)
                self.p1.Magic()
            elif choice == "4":
                self.printNew(3)
                self.p1.Stealth()
            elif choice == "5":
                self.printNew(3)
                self.p1.Force()
            elif choice == "6":
                self.printNew(3)
                self.p1.Intelligence()
            elif choice == "7":
                self.printNew(3)
                self.p1.Luck()
            elif choice == "8":
                self.printNew(3)
                self.p1.Stamina()
            elif choice == "9":
                ok = 0
            elif choice == "10":
                self.printNew(50)
                print("You can increase your stats up to 20 points each.")
                print("Once a stat is maxed, you get a bonus.")
                print("")
                input("press enter to show more : ")
                print("")
                print("Toughness reduces the damages you take")
                print("Agility increases your dodge rate and gives you some additional damages")
                print("Magic greatly increases your magic damages")
                print("Stealth greatly increases the chance to skip a figth")
                print("Force greatly increases your sword damages")
                print("Intelligence increases your magic damages")
                print("Luck increases the amount of coins you get, your crit rate, the chance to skip or flee a fight")
                print("Stamina increases the number of potions you can carry and increases greatly your hps")

        self.Village()

        
    def Switch(self):
        ok = 1
        while ok:
            input("press enter to continue : ")
            self.printNew(50)
            choice = str(input("Which character do you want to make player 1 ? (number in the party) : "))
            if choice == "1":
                ok = 0
            elif choice == "2":
                self.printNew(3)
                if self.p2 != None:
                    self.p1, self.p2 = self.p2, self.p1
                    print(f"{self.p1.name} is the new party leader")
                    if self.p1.inFight == 1:
                        self.mobs[0].fight(self.p1, self)
                    ok = 0
                else:
                    print("Player n°2 does not exist !")
            elif choice == "3":
                self.printNew(3)
                if self.p3 != None:
                    self.p1, self.p3 = self.p3, self.p1
                    print(f"{self.p1.name} is the new party leader")
                    if self.p1.inFight == 1:
                        self.mobs[0].fight(self.p1, self)
                    ok = 0
                else:
                    print("Player n°3 does not exist !")
            elif choice == "4":
                self.printNew(3)
                if self.p4 != None:
                    self.p1, self.p4 = self.p4, self.p1
                    print(f"{self.p1.name} is the new party leader")
                    if self.p1.inFight == 1:
                        self.mobs[0].fight(self.p1, self)
                    ok = 0
                else:
                    print("Player n°4 does not exist !")


    def Area(self):
        tmp = ((self.nbPersos+1)//2)*self.difficulty
        self.nbMobs = randint(1, tmp)
        self.mobLevel = int(floor(tmp/self.nbMobs))
        if self.mobLevel < self.p1.level:
            self.mobLevel = (self.mobLevel*2)+1 
        if self.mobLevel*2 < self.p1.level:
            self.mobLevel = self.mobLevel*2+1
        if self.mobLevel*2 < self.p1.level:
            self.mobLevel = self.mobLevel*2+1
        self.mobs = [Monster(self.names[randint(0, 58)], int(floor(self.mobLevel*2)), int(floor(self.mobLevel*2)), int(floor(self.mobLevel)), self.mobLevel, self.mobLevel, self.mobLevel, self.mobLevel, self.mobLevel, self.mobLevel, self.mobLevel, self.mobLevel) for i in range(self.nbMobs)]
        self.Village()


    def printFightSword(self):
        if self.mobs != []:
            msgName = ""
            for _ in range(13-(len(self.p1.name)//2)):
                msgName += " "
            msgName += self.p1.name
            for _ in range (25-(len(self.mobs[0].name)//2)):
                msgName += " "
            msgName += self.mobs[0].name
            msgHp = ""
            for _ in range(11-(len(str(self.p1.hp))//2)):
                msgHp += " "
            msgHp += str(self.p1.hp)
            for _ in range (27-(len(str(self.mobs[0].hp))//2)):
                msgHp += " "
            msgHp += str(self.mobs[0].hp)
            print(msgName)
            print(f"            o   /                      \   x         ")
            print(f"          -- --/                        \-- --       ")
            print(f"            |                              |         ")
            print(f"           / \                            / \        ")
            print(msgHp)
            self.printNew(3)

    
    def printFightDodge(self):
        if self.mobs != []:
            msgName = ""
            for _ in range (43-(len(self.mobs[0].name)//2)):
                msgName += " "
            msgName += self.mobs[0].name
            msgHp = ""
            for _ in range (41-(len(str(self.mobs[0].hp))//2)):
                msgHp += " "
            msgHp += str(self.mobs[0].hp)
            print(msgName)
            print(f"                                       \   x         ")
            print(f"                                        \-- --       ")
            print(f"                                           |         ")
            print(f"                                          / \        ")
            print(msgHp)
            sleep(0.5)
            self.printNew(50)
            msgName = ""
            for _ in range (38-(len(self.mobs[0].name)//2)):
                msgName += " "
            msgName += self.mobs[0].name
            msgHp = ""
            for _ in range (36-(len(str(self.mobs[0].hp))//2)):
                msgHp += " "
            msgHp += str(self.mobs[0].hp)
            print(msgName)
            print(f"                                  \   x         ")
            print(f"                                   \-- --       ")
            print(f"                                      |         ")
            print(f"                                     / \        ")
            print(msgHp)
            sleep(0.5)
            self.printNew(50)
            msgName = ""
            for _ in range (33-(len(self.mobs[0].name)//2)):
                msgName += " "
            msgName += self.mobs[0].name
            msgHp = ""
            for _ in range (31-(len(str(self.mobs[0].hp))//2)):
                msgHp += " "
            msgHp += str(self.mobs[0].hp)
            print(msgName)
            print(f"                             \   x         ")
            print(f"                              \-- --       ")
            print(f"                                 |         ")
            print(f"                                / \        ")
            print(msgHp)
            sleep(0.5)
            self.printNew(50)
            msgName = ""
            for _ in range (23-(len(self.mobs[0].name)//2)):
                msgName += " "
            msgName += self.mobs[0].name
            msgHp = ""
            for _ in range (21-(len(str(self.mobs[0].hp))//2)):
                msgHp += " "
            msgHp += str(self.mobs[0].hp)
            print(msgName)
            print(f"                   \   x         ")
            print(f"                    \-- --       ")
            print(f"                       |         ")
            print(f"                      / \        ")
            print(msgHp)
            sleep(0.5)
            self.printNew(50)
            msgName = ""
            for _ in range (13-(len(self.mobs[0].name)//2)):
                msgName += " "
            msgName += self.mobs[0].name
            msgHp = ""
            for _ in range (11-(len(str(self.mobs[0].hp))//2)):
                msgHp += " "
            msgHp += str(self.mobs[0].hp)
            print(msgName)
            print(f"         \   x         ")
            print(f"          \-- --       ")
            print(f"             |         ")
            print(f"            / \        ")
            print(msgHp)
            sleep(0.5)
            self.printNew(3)

    
    def printFightSpell(self):
        if self.mobs != []:
            msgName = ""
            for _ in range(13-(len(self.p1.name)//2)):
                msgName += " "
            msgName += self.p1.name
            for _ in range (25-(len(self.mobs[0].name)//2)):
                msgName += " "
            msgName += self.mobs[0].name
            msgHp = ""
            for _ in range(11-(len(str(self.p1.hp))//2)):
                msgHp += " "
            msgHp += str(self.p1.hp)
            for _ in range (27-(len(str(self.mobs[0].hp))//2)):
                msgHp += " "
            msgHp += str(self.mobs[0].hp)
            print(msgName)
            print(f"            o                          \   x         ")
            print(f"          -- --@ -_*                    \-- --       ")
            print(f"            |                              |         ")
            print(f"           / \                            / \        ")
            print(msgHp)
            sleep(0.5)
            self.printNew(50)
            print(msgName)
            print(f"            o                          \   x         ")
            print(f"          -- --@ -__- -*                \-- --       ")
            print(f"            |                              |         ")
            print(f"           / \                            / \        ")
            print(msgHp)
            sleep(0.5)
            self.printNew(50)
            print(msgName)
            print(f"            o                          \   x         ")
            print(f"          -- --@ -__- - - _ *           \-- --       ")
            print(f"            |                              |         ")
            print(f"           / \                            / \        ")
            print(msgHp)
            sleep(0.5)
            self.printNew(50)
            print(msgName)
            print(f"            o                          \   x         ")
            print(f"          -- --@ -__- - - _ _ - '-*     \-- --       ")
            print(f"            |                              |         ")
            print(f"           / \                            / \        ")
            print(msgHp)
            sleep(0.5)
            self.printNew(50)
            print(msgName)
            print(f"            o                          \   x         ")
            print(f"          -- --@ -__- - - _ _ - '- _ -* \-- --       ")
            print(f"            |                              |         ")
            print(f"           / \                            / \        ")
            print(msgHp)
            sleep(0.5)
            self.printNew(50)
            print(msgName)
            print(f"            o                          \   x         ")
            print(f"          -- --@                        \-- --       ")
            print(f"            |                              |         ")
            print(f"           / \                            / \        ")
            print(msgHp)
            sleep(0.5)
            self.printNew(3)

    
    def Fight(self):
        ok = 1
        while ok:
            print("")
            input("press enter to continue : ")
            self.printNew(50)
            self.printFightSword()
            print(f"There are {self.nbMobs} enemies left")
            print(f"You have {self.p1.mana} mana and {self.p1.nbpots} potions")
            choice = str(input("Escape fight (1), attack (2), heal (3), Switch characters (4) : "))
            try:
                if 1 <= int(choice) <= 4:
                    ok = 0
            except:
                ok = 1
        
        if choice == "1":
            self.printNew(3)
            self.p1.flee(self.mobs[0], self)
            if self.p1.inFight == 1:
                self.mobs[0].fight(self.p1, self)
        elif choice == "2":
            ok2 = 1
            while ok2:
                self.printNew(50)
                self.printFightSword()
                print(f"You have {self.p1.mana} mana")
                choice2 = str(input("Slash (1), Fireball (2) : "))
                try:
                    if 1 <= int(choice2) <= 2:
                        ok2 = 0
                except:
                    ok2 = 1 

            if choice2 == "1": 
                self.printFightSword()
                self.p1.attack(self.mobs[0], self)
                if self.mobs == []:
                    self.p1.inFight = 0
                elif self.p1.inFight == 1:
                    self.mobs[0].fight(self.p1, self)
            elif choice2 == "2":
                if self.p1.mana >= 20:
                    self.printFightSpell()
                    self.p1.attackSpell(self.mobs[0], self)
                    if self.mobs == []:
                        self.p1.inFight = 0
                    if self.p1.inFight == 1:
                        self.mobs[0].fight(self.p1, self)
                else:
                    print("You don't have enough mana to do that. A spell costs 20 mana")
        elif choice == "3":
            ok2 = 1
            while ok2:
                self.printNew(50)
                self.printFightSword()
                print(f"You have {self.p1.mana} mana and {self.p1.nbpots} potions")
                print("A potion heals you for 500hp, and a spell fully heals you")
                choice2 = str(input("potion (1), heal spell (2) : "))
                try:
                    if 1 <= int(choice2) <= 2:
                        ok2 = 0
                except:
                    ok2 = 1 
                
            if choice2 == "1":
                if self.p1.nbpots > 0:
                    self.printFightSword()
                    self.p1.usePot()
                    if self.p1.inFight == 1:
                        self.mobs[0].fight(self.p1, self)
                else:
                    print("You don't have any potions")
            elif choice2 == "2":
                if self.p1.mana > 20:
                    self.printFightSword()
                    self.p1.healSpell()
                    if self.p1.inFight == 1:
                        self.mobs[0].fight(self.p1, self)
                else:
                    print("You don't have enough mana to do that")
        elif choice == "4":
            self.Switch()
        
        self.place()

    
    def newFight(self):
        ok = 1
        while ok:
            input("press enter to continue : ")
            self.printNew(50)
            print(f"In this area, there are {self.nbMobs} enemies, and they are level {self.mobLevel}")
            print("If you manage to avoid a fight, it will kill the enemy, but you won't get any xp or coins.")
            choice = str(input("Avoid fight (1), attack (2) : "))
            try:
                if 1 <= int(choice) <= 2:
                    ok = 0
            except:
                ok = 1 

        if choice == "1":
            self.printFightDodge()
            self.p1.avoidFight(self.mobs[0], self)
            if self.p1.inFight == 1:
                self.mobs[0].fight(self.p1, self)
            self.place()
        elif choice == "2":
            self.Fight()

    
    def Start(self):
        self.printNew(50)
        print(f"-{self.p1.name}...")
        sleep(1)
        print(f"-{self.p1.name}...")
        sleep(1)
        print(f"-{self.p1.name} !")
        sleep(1)
        print("-Wake up !")
        sleep(1)
        print("-You must free this world from the tyran's wrath !")
        print("")
        input("press enter to continue : ")
        print("")
        self.printNew(50)
        print("-I, the great goddess Dragonix, saved you from a certain death when your village was invaded.")
        sleep(1)
        print("-You are now the last of your kind... The last of the Ska-a Drins.")
        sleep(1)
        print("-It is now your duty to save the Mlear continent from Arcxeo, the Evil Corrupted.")
        sleep(1)
        print("-I shall now send you to a safe village, in the center of Mlear.")
        sleep(1)
        print("-I wish you good luck, my hero.")
        print("")
        input("press enter to continue : ")
        print("")
        self.printNew(50)
        print("Oh. I nearly forgot, but my power has been bestowed upon you.")
        print("")
        sleep(1)
        if self.nbPersos > 1:
            print("And you won't be alone on this dangerous quest.")
            sleep(1)
            print("Your companions are waiting for you in town.")
            sleep(1)
        print("Then, goodbye, my hero.")
        print("")
        input("press enter to continue : ")
        print("")
        self.printNew(50)
        print("You are waking up in a village, near a campfire.")
        sleep(1)
        print("You pack your possessions (a wooden sword gifted by your father a long time ago, and a magic ring made of your umbilical cord) and look around.")
        sleep(1)
        if self.nbPersos > 1:
            print("You cannot explain how but you kown at first glance who are your companions, and their names.")
            sleep(1)
            print("You quickly join what will be your adventure party, and explore some more the town.")
        print("You can see a blacksmith shop, a wizardry shop and a potion merchant.")
        sleep(1)
        print("You can feel a new power flowing in your body. Maybe, if you said Level up...")
        sleep(1)
        self.Area()

    def NewArea(self):
        if self.area == 11:
            sleep(1)
            self.printNew(50)
            print("BOSS FIGHT")
            self.printNew(10)
            sleep(2.5)
            self.nbMobs = 1
            self.mobLevel = 50
            self.mobs = [Monster(f"Arcxeo, The Evil Corrupted", int(floor(self.mobLevel*2)), int(floor(self.mobLevel*2)), int(floor(self.mobLevel)), self.mobLevel, self.mobLevel, self.mobLevel, self.mobLevel, self.mobLevel, self.mobLevel, self.mobLevel, self.mobLevel) for i in range(self.nbMobs)]
            self.Village()
        elif self.area > 11:
            sleep(1)
            self.printNew(50)
            print("-And thus, your duty on this world was fulfilled")
            sleep(2)
            self.printNew(50)
            print("You Won")
            self.printNew(10)
            sleep(10)
            input("Press enter to exit : ")
            exit()
        else:
            self.Area()


# difficulty = input("In which difficulty do you wish to play ? : ")
# try:
#     difficulty = int(difficulty)
# except:
#     difficulty = 1

# nb = input("How many will you be in this adventure ? (up to 4) : ")
# try:
#     nb = int(nb)
# except:
#     nb = 1

# players = [None, None, None, None]
# playernames = [None, None, None, None]
# for i in range(nb):
#     playernames[i] = input("The character's name : ")
#     players[i] = Creature(playernames[i])



# game = Game(players[0], difficulty, players[1], players[2], players[3])

# game.Start()
# for _ in range(12):
#     game.NewArea()