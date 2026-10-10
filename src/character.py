# Imports
import random


# Character Class
class Character:

    def __init__(self, is_player: bool, name: str, hp: int, ac: int, damage_dice: tuple, equipment: list,
                 is_alive: bool):
        self.is_player = is_player
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.ac = ac
        self.damage_dice = damage_dice
        self.equipment = equipment
        self.is_alive = is_alive
        self.damage_modifier = 0

    # Hit function
    def ac_check(self, target):
        target_ac = target.ac

        if self.is_player:
            for item in self.equipment:
                if item["target"] == "target" and item["stat"] == "ac":
                    target_ac += item["modifier"]

        d20 = random.randint(1, 20)

        if d20 >= target_ac:
            return True
        else:
            return False

    # Attack function
    def attack(self, target):
        if self.is_alive:
            if self.ac_check(target):

                # Check how many dice to roll
                number_of_dice = self.damage_dice[0]
                size_of_dice = self.damage_dice[1]

                dice_output = []

                # Roll all damage dice
                for i in range(number_of_dice):
                    dice_output.append(random.randint(1, size_of_dice))

                # Add all dice together, then apply modifier
                damage = sum(dice_output) + self.damage_modifier
                print(
                    f"{self.name} attacked {target.name}!\n"
                    f"{self.name} dealt {damage} damage to {target.name}!"
                )
                target.take_damage(damage)
                return damage
            else:
                print(f"{self.name} attacked {target.name}")
                print("The attack missed!")
                return 0

    # Damage tracking
    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.is_alive = False
            if self.is_player:
                print(
                    "Oh No!\n"
                    "You have been defeated!\n"
                    "Please try again young hero!\n"
                    "You can do it.")
            else:
                print(f"You have defeated {self.name}.")
        else:
            if self.is_player:
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
            target.damage_modifier += item["modifier"]

    # Display equipment
    def display_equipment(self):
        if not self.equipment:
            print("You have no equipment.")
            return

        print("\n=== Equipment ===")

        for item in self.equipment:
            print(f"\n{item['name']}")
            print(f"  {item['description']}")

            if item["modifier"] is not None:
                stat = item["stat"].upper()
                modifier = item["modifier"]
                target = item["target"]

                if target == "self":
                    print(f"  Effect: {stat} {modifier:+}")
                else:
                    print(f"  Enemy effect: {stat} {modifier:+}")

            elif item.get("character"):
                print("  Effect: Companion joins you in combat.")