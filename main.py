import pygame

from game import game_loop
from pokemon import *

# basic game logic:
# determine first action given first legal input (fast attack if clicked, charged attack if clicked and enough energy, otherwise do nothing)
# after 0.5 seconds, make the first action that was determined in the previous step
# repeat every 0.5 seconds, ignoring other inputs after the action has been determined

if __name__ == "__main__":
    # testing
    snarl = FastMove("Snarl", "Dark", 1, 10, 10)
    dark_pulse = ChargedMove("Dark Pulse", "Dark", 3, 90, 50)
    mandibuzz = Pokemon("Mandibuzz", "mandibuzz", False, 100, 100, 100, ["Dark", "Flying"], snarl, [dark_pulse])

    tackle = FastMove("Tackle", "Normal", 1, 5, 5)
    string_shot = ChargedMove("String Shot", "Bug", 3, 30, 30)
    caterpie = Pokemon("Caterpie", "caterpie", True, 40, 40, 40, ["Bug"], tackle, [string_shot])
 

    game_loop(mandibuzz, caterpie)