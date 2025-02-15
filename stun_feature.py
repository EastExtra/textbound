import random 

def apply_stun(target):
    target.is_stunned = True 
    target.stun_duration = random.randint(1,2)
    print(f"{target.name} has been stunned for {target.stun_duration} turns!")

def check_stun(character):
    if hasattr(character, 'is_stunned') and character.is_stunned:
        character.stun_duration -= 1 
        if character.stun_duration <= 0: 
            character.is_stunned = False 
            print(f"{character.name} is no longer stunned!")
            return False 
        else:
            print(f"{character.name} is stunned and cannot act!")
            return True 
        return False 
    
def stun_attack(attacker, defender):
    if random.random() < 0.3: # 30% chance to stun 
        apply_stun(defender)
    else:
        print(f"{attacker.name}'s stun attack missed!")