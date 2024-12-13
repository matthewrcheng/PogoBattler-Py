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
        self.cooldown_timer = 0
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
        self.image = f"C:/Users/mchen/OneDrive/Desktop/Pokemon Essentials v20.1 2022-06-20/Pokemon Essentials v20.1 2022-06-20/Graphics/Pokemon/Front/{self.species_name.upper()}.png"

    def calculate_damage(self, move_type, power, opponent):
        mult = 1.0
        for opp_type in opponent.types:
            for type_info in effectiveness:
                if type_info["type"] == move_type.lower():
                    if opp_type in type_info.get("strong", []):
                        mult *= settings["strongMult"]
                    elif opp_type in type_info.get("weak", []):
                        mult *= settings["weakMult"]
                    elif opp_type in type_info.get("immune", []):
                        mult *= settings["immuneMult"]
        if mult > 1.0:
            print("It's super effective!")
        elif mult < 1.0:
            print("It's not very effective...")
        if move_type in self.types:
            mult *= 1.2
        if self.shadow:
            mult *= settings["shadowAtkMult"]
        if opponent.shadow:
            mult *= settings["shadowDefMult"]
        damage = (0.5 * power * mult * self.attack / opponent.defense) + 1
        return damage

    def fast_attack(self, opponent):
        if self.fast_move.cooldown_timer <= 0:
            print(f"{self.species_name} used {self.fast_move.name}")
            damage = self.calculate_damage(self.fast_move.type, self.fast_move.power, opponent)
            self.energy += self.fast_move.energy
            self.energy = min(100, self.energy)
            self.fast_move.cooldown_timer = self.fast_move.cooldown
            return opponent.damage(damage)
        else:
            self.fast_move.cooldown_timer -= 0.5
            return False
    
    def charged_attack(self, opponent, idx):
        print(f"{self.species_name} used {self.charged_moves[idx].name}")
        damage = self.calculate_damage(self.charged_moves[idx].type, self.charged_moves[idx].power, opponent)
        self.energy -= self.charged_moves[idx].energy_cost
        self.energy = max(0, self.energy)
        return opponent.damage(damage)
    
    def get_better_charged_attack(self, opponent):
        # calculate the charged attack that does the most damage
        highest = 0
        best_idx = 0
        for idx, move in enumerate(self.charged_moves):
            damage = self.calculate_damage(move.type, move.power, opponent)
            if damage > highest:
                highest = damage
                best_idx = idx
        return best_idx

    
    def can_charged_attack(self, idx):
        if self.energy >= self.charged_moves[idx].energy_cost:
            return True
        return False
    
    def damage(self, amount):
        self.remaining_hp -= amount
        print(f"It dealt {amount} damage!")
        if self.remaining_hp > 0:
            return False
        return True
        


