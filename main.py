# Imports
from character import Character
from items import items
import map
import pygame
import utils
import sys

player = Character(True, "You", 15, 11, (2, 6), [], True)
nightmare = Character(False, "Nightmare", 50, 15, (1, 12), [], True)
goblin = Character(False, "The Goblin", 20, 10, (2, 10), [], True)
beast = Character(False, "Artemis", 15, 15, (2, 8), None, True)

def try_moving(current_room, rooms, direction):
    room = rooms[current_room]

    # Check if that direction exists
    if direction not in room["exits"]:
        return current_room, "You can't travel in that direction."

    # Check if that exit is locked
    if direction in room["locked exits"]:
        return current_room, "That way is locked."

    # Move to the new room
    current_room = room["exits"][direction]

    description = rooms[current_room]["description"]

    return current_room, description


test = Character(True, "test", 5, 5, (0, 0), [items["socks"], items["tunic"]], True)


def game_loop():
    current_room = "Entrance"
    running = True

    while running:
        room = map.rooms[current_room]

        print()
        print(current_room)
        print(room["description"])
        # Check for an unsolved puzzle
        if room["puzzle"] is not None and not room["solved"]:
            solved = room["puzzle"]()

            if solved:
                room["solved"] = True
                room["locked exits"].clear()
            else:
                print("The puzzle remains unsolved.")
        print("Exits:", ", ".join(room["exits"].keys()))

        command = input("> ").lower().strip()

        if command == "quit":
            running = False

        elif command in ["north", "south", "east", "west", "up", "down"]:
            current_room, description = try_moving(
                current_room,
                map.rooms,
                command
            )

            print(description)

        else:
            print("I don't understand that command.")


"""
# pygame setup
pygame.init()

screen = pygame.display.set_mode((utils.WIDTH, utils.HEIGHT))
clock = pygame.time.Clock()
running = True

while running:
    # Poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill screen
    screen.fill("Black")

    # RENDER YOUR GAME HERE

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
"""

if __name__ == "__main__":
    game_loop()
