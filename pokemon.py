import json

from utils import effectiveness, settings

def get_all_pokemon():
    with open('pokemon.json') as f:
        data = json.load(f)
    full_list = [pokemon['speciesId'] for pokemon in data]
    return full_list

class Move:

    def __init__(self, name: str, type: str, cooldown: str, power: int):
        self.name = name
        self.type = type
        self.cooldown = cooldown
        self.power = power

class FastMove(Move):

    def __init__(self, name: str, type: str, cooldown: float, power: int, energy: int):
        super().__init__(name, type, cooldown, power)
        self.energy = energy

class ChargedMove(Move):

    def __init__(self, name: str, type: str, cooldown: float, power: int, energy_cost: int):
        super().__init__(name, type, cooldown, power)
        self.energy_cost = energy_cost

class Pokemon:

    def __init__(self, species_name: str, species_id: str, shadow: bool, attack: int, defense: int, hp: int, types: list[str], fast_move: FastMove, charged_moves: list[ChargedMove]):
        self.species_name = species_name
        self.species_id = species_id
        self.shadow = shadow
        self.attack = attack
        self.defense = defense
        self.hp = hp
        self.types = types
        self.fast_move = fast_move
        self.charged_moves = charged_moves

        self.remaining_hp = self.hp
        self.energy = 0

    def calculate_damage(self, opponent):
        mult = 1.0
        if self.fast_move.type in self.types:
            mult *= 1.2
        for opp_type in opponent.types:
            for type_info in effectiveness:
                if type_info["type"] == self.fast_move.type.lower():
                    if opp_type in type_info.get("strong", []):
                        mult *= settings["strongMult"]
                    elif opp_type in type_info.get("weak", []):
                        mult *= settings["weakMult"]
                    elif opp_type in type_info.get("immune", []):
                        mult *= settings["immuneMult"]
        if self.shadow:
            mult *= settings["shadowAtkMult"]
        if opponent.shadow:
            mult *= settings["shadowDefMult"]
        damage = (0.5 * self.fast_move.power * mult * self.attack / opponent.defense) + 1
        return damage

    def fast_attack(self, opponent):
        damage = self.calculate_damage(opponent)
        self.energy += self.fast_move.energy
        return opponent.damage(damage)
    
    def charged_attack(self, opponent, idx):
        damage = self.calculate_damage(opponent)
        self.energy -= self.charged_attack[idx].energy_cost
        return opponent.damage(damage)
    
    def can_charged_attack(self, idx):
        if self.energy >= self.charged_moves[idx].energy_cost:
            return True
        return False
    
    def damage(self, amount):
        self.remaining_hp -= amount
        print(f"{self.species_name} took {amount} damage, hp: {self.remaining_hp}/{self.hp}")
        if self.remaining_hp > 0:
            return False
        return True
        


