# Imports
import random


# Character Class
class Character:

    def __init__(self, isplayer: bool, name: str, hp: int, ac: int, damagedice: tuple, equipment: list, isalive: bool):
        self.isplayer = isplayer
        self.name = name
        self.hp = hp
        self.ac = ac
        # is attack more accurate?
        self.damagedice = damagedice
        self.equipment = equipment
        self.isalive = isalive
        self.damageModifier = 0

    # Hit function
    def ac_check(self, target):
        # D20 dice
        d20 = random.randint(1, 20)

        if d20 >= target.ac:
            """ Debug code need to remove or comment out so player doesnt see.
            print(f"{self.name} rolled {d20} to hit")
            print(f"Target's AC was {target.ac}")
             end debug code """
            return True
        else:
            return False

    # Attack function
    def attack(self, target):
        if self.isalive:
            if self.ac_check(target):

                # Check how many dice to roll
                numberOfDice = self.damagedice[0]
                sizeOfDice = self.damagedice[1]

                diceOutput = []

                # Roll all damage dice
                for i in range(numberOfDice):
                    diceOutput.append(random.randint(1, sizeOfDice))

                # Add all dice together, then apply modifier
                damage = sum(diceOutput) + self.damageModifier
                print(
                    f"{self.name} attacked {target.name}!\n"
                    f"{self.name} dealt {damage} damage to {target.name}!"
                )
                target.takeDamage(damage)
                return damage
            else:
                print(f"{self.name} attacked {target.name}")
                print("The attack missed!")
                return 0

    # Damage tracking
    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.isalive = False
            if self.isplayer:
                print(
                    "Oh No!\n"
                    "You have been defeated!\n"
                    "Please try again young hero!\n"
                    "You can do it.")
            else:
                print(f"You have defeated {self.name}.")
        else:
            if self.isplayer:
                print(f"You have {self.hp} HP left.")
            else:
                print(f"{self.name} has {self.hp} HP left.")

    # Item effects
    def modify_stats(self, item, target=None):
        # Modifier target
        if item["target"] == "self":
            target = self

        # Apply the modifier
        if item["stat"] == "ac":
            target.ac += item["modifier"]

        elif item["stat"] == "damage":
            target.damageModifier += item["modifier"]

    # "Equip" items
    def apply_equipment(self):
        modified = []

        for item in self.equipment:
            if item not in modified:
                self.modify_stats(item)
                modified.append(item)

        print(self.ac)
        print(", ".join(item["name"] for item in modified))

