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
        
    ]

