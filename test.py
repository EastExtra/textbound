import random
import time
import ctypes
from stun_feature import check_stun, stun_attack

lib = ctypes.CDLL('./difficulty_adjuster.dylib')

lib.calculate_difficulty.argtypes = [ctypes.Structure]
lib.calculate_difficulty.restype = ctypes.c_float
lib.adjust_enemy_stats.argtypes = [ctypes.c_float, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]

class GameStats(ctypes.Structure):
    __fields__ = [
        ("player_health", ctypes.c_int),
        ("enemies_defeated", ctypes.c_int)
        ("turns_taken", ctypes.c_int)

    ]

class Character:
    def __init__(self, name, hp, pp, attack, defense):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.pp = pp
        self.max_pp = pp
        self.attack = attack
        self.defense = defense
        self.status = {'stunned': False, 'stun_duration': 0}

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage, is_smash=False):
        actual_damage = damage if is_smash else max(damage - self.defense,0)
        actual_damage *= 2 if random.random() < 0.1 else 1
        self.hp = max(self.hp - actual_damage,0)
        print(f"{self.name} took {actual_damage} damage!")

    def use_psi(self,psi_type,target):
        psi_cost = {'Fire':5,'Heal':10}.get(psi_type,0)
        if psi_cost == 0 or self.pp >= psi_cost:
            if psi_type == 'Fire':
                damage = random.randint(20,30)
                target.take_damage(damage)
                self.pp -= 5
            elif psi_type == 'Heal':
                heal = random.randint(30,50)
                self.hp = min(self.hp + heal, self.max_hp)
                self.pp -= 10

            else:
                print("Not enough PP!")

    def get_action_input(actor,options):
        print(f"\n{actor.name}'s turn to choose an action:")
        for idx, option in emumerate(options, 1):
            print(f"{idx}.{option}")
        choice = int(input("Choose an action:")) - 1
        return choice

    def execute_action(actor, action, target=None):
        if check_stun(actor):
            print(f"{actor.name} is stunned and cannot act!")
            return

        action_type = action[0]
        if action_type == 'attack':
            damage = random.randint(actor.attack -2, actor.attack + 2)
            execute_attack(actor,damage,target)
        elif action_type == 'psi':
            psi_type = action[1]
            actor.use_psi(psi_type, target)
        elif action_type == 'stun':
            stun_attack(actor, target)
        elif action_type == 'ultra':
            ultra_smash(actor, target)
        elif action_type == 'defend':
            actor.defense += 5
            print(f"{actor.name} is defending. Defense increased by 5!")
        elif action_type == 'switch':
            switch_character(actor.team)

        def ultra_smash(attacker, defender):
            damage = attacker.attack * 5
            defender.take_damage(damage, True)
            print(f"{attacker.name} unleashes an ULTRA SMASH!!!!{defender.name} takes {damage} damage!")

        def create_enemy(player_stats):
            stats = GameStats(player_stats.hp, player_stats.enemies_defeated, player_stats.turns_taken)
            difficulty = lib.calculate_difficulty(stats)

            hp = ctypes.c_int(50)
            attack = ctypes.c_int(0)
            lib.adjust_enemy_stats(difficulty, ctypes.byref(hp), ctypes.byref(attack))

            return Character("Monster", hp.value, 20, attack.value, 3)

        class Boss(Character):
            def __init__(self,name,hp,pp,attack,defense):
                super().__init__(name,hp,pp,attack,defense)
                self.special_cooldown = 0

            def psi_rock(self, target):
                if self.pp >= 20 and self.special_cooldown == 0:
                    self.pp -= 20
                    damage = random.randint(30,50)
                    target.take_damage(damage)
                    self.special_cooldown = 3
