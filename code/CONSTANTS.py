SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 800
FPS = 60
TILE_SIZE = 64
HALF_WIDTH = SCREEN_WIDTH // 2
HALF_HEIGHT = SCREEN_HEIGHT // 2
FRAME_DURATIONS = {
    'idle': 4,
    'walk': 4,
    'walk_left': 4,
    'walk_right': 4,
    'walk_up': 4,
}
CHAR_PATH = '../assets/player/'
PLAYER_ANIMATION_SPEED = 0.15
SPELLS = {
    # type         size speed
    '': [0, 0],
    'fireball': [32, 6],
}

SPELL_FRAME_DURATIONS = {
    'fireball': 2,
}
SPELL_PATH = '../assets/player/spells/' 
PLAYER_ATTACK_COOLDOWN = 25
PLAYER_IMG_SCALING = (96, 96)
PLAYER_SPEED = 4

weapon_data = {
    'sword': {'cooldown': 20, 'damage': 5, 'graphic': ''}
}