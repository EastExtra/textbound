#include <stdio.h>

typedef struct {
    int player_health;
    int enemies_defeated;
    int turns_taken;
} GameStats;

float calculate_difficulty(GameStats stats) {
    float difficulty = 1.0;
    
    if (stats.enemies_defeated > 5 && stats.player_health > 50) {
        difficulty += 0.2;
    }
    
    if (stats.turns_taken > 20 && stats.enemies_defeated < 3) {
        difficulty -= 0.1;
    }
    
    if (difficulty < 0.5) difficulty = 0.5;
    if (difficulty > 2.0) difficulty = 2.0;
    
    return difficulty;
}

void adjust_enemy_stats(float difficulty, int* enemy_hp, int* enemy_attack) {
    *enemy_hp = (int)(*enemy_hp * difficulty);
    *enemy_attack = (int)(*enemy_attack * difficulty);
}
