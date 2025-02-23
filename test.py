import random
import time
import ctypes
from stun_feature import check_stun, stun_attack

lib = ctypes.CDLL('./difficulty_adjuster.dylib')

class GameStats(ctypes.Structure):
    _fields_ = [("player_health", ctypes.c_int),
                ("enemies_defeated", ctypes.c_int),
                ("turns_taken", ctypes.c_int)]

lib.calculate_difficulty.arg_types = [GameStats]
lib.calculate_difficulty.restype = ctypes.c_float 

lib.adjust_enemy_stats.argtypes = [ctypes.c_float, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]

class Character: 
    def __init__(self,name: str, hp: int, pp:int, attack: int, defense: int):
        self.name = name
        self.hp = hp 
        self.max_hp = hp 
        self.pp = pp
        self.max_pp = pp
        self.attack = attack
        self.defense = defense 
        self.is_stunned = False 
        self.stun_duration = 0 

    def take_damage(self, damage: int, is_smash = bool = False) -> None:
        if is_smash: 
            actual_damage = damage
        else:
            actual_damage = max(damage - self.defense, 0)

        if random.random() < 0.1:
            actual_damage *= 2 
            print("Mortal damage! Double damage dealt!")
            
        self.hp = max(self.hp - actual_damage, 0)
        print(f"{self.name} took {actual_damage} damage!")

    def is_alive(self) -> bool:
        return self.hp > 0

    def use_psi(self, psi_name: str, target: 'Character') -> None:
        if psi_name == "PSI Fire":
            if self.pp >= 5:
                self.pp -= 5
                damage = random.randint(20,30)
                print(f"{self.name} uses PSI Fire!")
                target.take_damage(damage)
            else:
                print("Not enough PP!")
        elif psi_name == "PSI Heal":
            if self.pp >= 10:
                self.pp -= 10
                heal = random.randint(20,30)
                print(f"{self.name} uses PSI Heal!")
                self.hp = min(self.hp + heal, self.max_hp)
            else:
                print("Not enough PP!")

    def battle_text(text: str) -> None:
        print(text)
        time.sleep(1)

    def ultra_smash(attacker: Character, defender: Character) -> None:
        print(f"{attacker.name} unleashes an ULTRA SMASH!!!!")
        damage = attacker.attack * 5 
        defender.take_damage(damage, is_smash = True)
        print(f"{defender.name} takes a devastating {damage} damage!")

    def get_player_action(player: Character, enemy: Character, team: list) -> tuple:
        print(f"\n{player.name}'s turn to choose an action:")
        actions_menu = {
        "1": ("Attack", "attack", enemy),
        "2": ("Defend", "defend", None),
        "3": ("PSI Fire", "psi_fire", enemy),
        "4": ("PSI Heal", "psi_heal", player),
        "5": ("Stun Attack", "stun", enemy),
        "6": ("ULTRA SMASH", "ultra_smash", enemy)
    }

        choice = input("Choose an action: ")
        action = actions_menu.get(choice,("Attack", "attack", enemy))
        return (action[1], action[2])

    

