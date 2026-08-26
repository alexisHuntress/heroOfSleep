# Imports
import random


# Character Class
class Character:

    def __init__(self, isplayer: bool, name: str, hp: int, ac: int, damage: tuple, equipment: list):
        self.isplayer = isplayer
        self.name = name
        self.hp = hp
        self.ac = ac
        self.damage = damage
        self.equipment = equipment

    # Hit function
    def ac_check(self, target):
        # D20 dice
        d20 = random.randint(1, 20)

        if d20 >= target.ac:
            """ Debug code need to remove or comment out so player doesnt see.
            print(f"rolled {d20} to hit")
            print(f"Target's AC was {target.ac}")
             end debug code """
            return True
        else:
            return False

    # Attack function
    def attack(self, target):
        if self.ac_check(target):

            # Check how many dice to roll
            numberOfDice = self.damage[0]
            sizeOfDice = self.damage[1]

            diceOutput = []

            for i in range(numberOfDice):
                diceOutput.append(random.randint(1, sizeOfDice))

            damage = sum(diceOutput)
            print(f"{self.name} dealt {damage} damage to {target.name}!")
            target.takeDamage(damage)
            return damage
        else:
            print(f"{self.name} attcked {target.name}")
            print("The attack missed!")
            return 0

    def takeDamage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            if self.isplayer:
                print(f"You have been defeated.")
            else:
                print(f"You have defeated {self.name}.")
        else:
            if self.isplayer:
                print(f"{self.name} have {self.hp} HP left.")
            else:
                print(f"{self.name} has {self.hp} HP left.")



