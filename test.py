import random
import time
from stun_feature import check_stun, stun_attack

class Character:
    def __init__(self, name, hp, pp, attack, defense):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.pp = pp
        self.max_pp = pp
        self.attack = attack
        self.defense = defense
        self.is_stunned = False
        self.stun_duration = 0

    def take_damage(self, damage, is_smash=False):
        if is_smash:
            actual_damage = damage  # SMASH! ignores defense
        else:
            actual_damage = max(damage - self.defense, 0)

        if random.random() < 0.1:  # 10% chance of mortal damage
            actual_damage *= 2
            print("Mortal damage! Double damage dealt!")

        self.hp = max(self.hp - actual_damage, 0)
        print(f"{self.name} took {actual_damage} damage!")

    def is_alive(self):
        return self.hp > 0

    def use_psi(self, psi_name, target):
        if psi_name == "PSI Fire":
            if self.pp >= 5:
                self.pp -= 5
                damage = random.randint(20, 30)
                print(f"{self.name} uses PSI Fire!")
                target.take_damage(damage)
            else:
                print("Not enough PP!")
        elif psi_name == "PSI Heal":
            if self.pp >= 10:
                self.pp -= 10
                heal = random.randint(30, 50)
                self.hp = min(self.hp + heal, self.max_hp)
                print(f"{self.name} uses PSI Heal and recovers {heal} HP!")
            else:
                print("Not enough PP!")

def battle_text(text):
    print(text)
    time.sleep(1)

def ultra_smash(attacker, defender):
    print(f"{attacker.name} unleashes an ULTRA SMASH!!!")
    damage = attacker.attack * 5  # deals 5x normal attack
    defender.take_damage(damage, is_smash=True)
    print(f"{defender.name} takes a devastating {damage} damage!")

def get_player_action(player, enemy, team):
    print(f"\n{player.name}'s turn to choose an action:")
    print("1. Attack")
    print("2. Defend")
    print("3. PSI Fire")
    print("4. PSI Heal")
    print("5. Stun Attack")
    print("6. ULTRA SMASH")
    choice = input("Choose an action: ")

    if choice == "1":
        return ("attack", enemy)
    elif choice == "2":
        return ("defend", None)
    elif choice == "3":
        return ("psi_fire", enemy)
    elif choice == "4":
        return ("psi_heal", player)
    elif choice == "5":
        return ("stun", enemy)
    elif choice == "6":
        return ("ultra_smash", enemy)
    else:
        print("Invalid choice. Defaulting to Attack")
        return ("attack", enemy)

def get_enemy_action(enemy, team):
    alive_team = [char for char in team if char.is_alive()]
    target = random.choice(alive_team)

    if isinstance(enemy, Boss):
        if random.random() < 0.2:
            return ("stun", target)
        elif random.random() < 0.1:
            return ("ultra_smash", target)
        else:
            return ("attack", target)
    else:
        if random.random() < 0.1:
            return ("smash", target)
        else:
            return ("attack", target)

def execute_action(actor, action):
    action_type, target = action
    
    if check_stun(actor):
        print(f"{actor.name} is stunned and cannot act!")
        return

    if action_type == "attack":
        damage = random.randint(actor.attack - 2, actor.attack + 2)
        print(f"{actor.name} attacks {target.name}!")
        target.take_damage(damage)
    elif action_type == "defend":
        actor.defense += 5
        print(f"{actor.name} is defending. Defense increased by 5!")
    elif action_type == "psi_fire":
        actor.use_psi("PSI Fire", target)
    elif action_type == "psi_heal":
        actor.use_psi("PSI Heal", actor)  # Corrected: target should be actor for self-heal
    elif action_type == "stun":
        stun_attack(actor, target)
    elif action_type == "ultra_smash":
        if random.random() < 0.0005:  # Increased chance to succeed
            ultra_smash(actor, target)
        else:
            print(f"{actor.name}'s ULTRA SMASH failed!")
    elif action_type == "smash":
        damage = actor.attack * 3
        print(f"SMASHHH! {actor.name} hits {target.name} hard!")
        target.take_damage(damage, is_smash=True)

def battle(team, enemy):
    print(f"A wild {enemy.name} appears!")

    while any(char.is_alive() for char in team) and enemy.is_alive():
        actions = []
        print("\nTeam status:")
        for char in team:
            print(f"{char.name}: HP {char.hp}/{char.max_hp} | PP {char.pp}/{char.max_pp}")
        print(f"{enemy.name}: HP {enemy.hp}/{enemy.max_hp}")

        actions.clear()
        # Collect actions for characters
        for char in team: 
            if char.is_alive():
                action = get_player_action(char, enemy, team)
                actions.append((char, action))
       

        enemy_action = get_enemy_action(enemy, team)
        actions.append((enemy, enemy_action))

        # Randomize order of actions
        random.shuffle(actions)

        # Execute actions
        for actor, action in actions:
            #print(f"Executing action for {actor.name}: {action}")  # Debugging line
            if actor.is_alive():  # Ensure actor is still alive
                if action[0] != 'defend':  # Only extract target if not defending
                    execute_action(actor, action)
                else:
                     execute_action(actor,action) #pass both defend
            if not enemy.is_alive() or not any(char.is_alive() for char in team):
                break
        time.sleep(1)

        if not enemy.is_alive():
            print(f"\nYou defeated {enemy.name}!")
            return True 
        elif not any(char.is_alive() for char in team):
            print(f"\nYour team has been defeated...")
            return False 
def switch_character(team):
    print("\nChoose a character to switch to:")
    for i, char in enumerate(team):
        print(f"{i+1}. {char.name} (HP: {char.hp}/{char.max_hp}, PP: {char.pp}/{char.max_pp})")
    choice = int(input("Enter the number of the character: ")) - 1
    return team[choice]

def ultra_smash(attacker, defender):
    print(f"{attacker.name} unleashes an ULTRA SMASH!!!")
    damage = attacker.attack * 5 # deals 5x normal attack
    defender.take_damage(damage, is_smash=True)
    print(f"{defender.name} takes a devastating {damage} damage!")

#def execute_action(actor, action, target):
def get_enemy_action(enemy, team):
    alive_team = [char for char in team if char.is_alive()]
    if not alive_team:
        return None, None #return Nonetype
    target = random.choice(alive_team)

    if isinstance(enemy, Boss):
        if random.random() < 0.2:
            return ("stun", target)
        elif random.random() < 0.1:
            return ("ultra_smash", target)
        else:
            return ("attack", target)
    else:
        if random.random() < 0.1:
            return ("smash", target)
        else:
            return ("attack", target)

class Boss(Character):
    def __init__(self, name, hp, pp, attack, defense):
        super().__init__(name, hp, pp, attack, defense)
        self.special_cooldown = 0

    def psi_rock(self, target):
        if self.pp >= 20 and self.special_cooldown == 0:
            self.pp -= 20
            damage = random.randint(30,50)
            print(f"The Ground shakes in terror as {self.name} uses PSI Rock on {target.name}!")
            target.take_damage(damage)
            self.special_cooldown = 3

            return True 
        return False

# Main game
pythonie = Character("Pythonie", hp=100, pp=50, attack=15, defense=5)
javacript = Character("Javacript", hp=90, pp=60, attack=12, defense=4)
rustacean = Character("Rustacean", hp=120, pp=30, attack=18, defense=8)
golanger = Character("Golanger", hp=110, pp=40, attack=14, defense=6)

team = [pythonie, javacript, rustacean, golanger]

monster = Character("Monster", hp=50, pp=20, attack=10, defense=3)
boss = Boss("MegaByte", hp=400, pp=150, attack=30, defense=20)

