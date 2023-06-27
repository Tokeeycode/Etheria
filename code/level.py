from BLACKFORGE2 import *

from CONSTANTS import *

from player import Player

class Level:
    def __init__(self, level_data, game, surface):
        self.game = game
        self.level_data = level_data
        self.surface = surface
        
        self.tile_index = {}
        self.create_tile_index()
        self.create_group(level_data)
        self.calculate_level_size()
    
    def calculate_level_size(self):
        max_right = 0
        max_bottom = 0

        for layer in self.world_layers:
            for sprite in layer:
                sprite_rect = sprite.rect
                sprite_right = sprite_rect.x + sprite_rect.width
                sprite_bottom = sprite_rect.y + sprite_rect.height

                max_right = max(max_right, sprite_right)
                max_bottom = max(max_bottom, sprite_bottom)

        self.level_width = max_right
        self.level_height = max_bottom
    
    def create_group(self, level_data):
        self.on_screen_tiles = pygame.sprite.Group()
        self.terrain = pygame.sprite.Group()
        self.decoration = pygame.sprite.Group()
        self.player_layer = pygame.sprite.GroupSingle()
        for layout_name in ['Terrain','Decoration']:
            layout = import_csv_layout(self.level_data[layout_name])
            self.create_tile_group(layout, layout_name, TILE_SIZE)
            
        Player_layout = import_csv_layout(self.level_data['Player'])
        self.player_setup(Player_layout, TILE_SIZE) 
           
        self.world_layers = [
            self.decoration,
            self.terrain,
            self.player_layer
        ]
        self.level_topleft = self.terrain.sprites()[0].rect
        self.level_bottomright = self.terrain.sprites()[len(self.terrain)-1].rect
    
    def create_tile_index(self):
        tile_list = import_cut_graphics("../assets/tileset.png", TILE_SIZE)
        for index, tile in enumerate(tile_list):
            self.tile_index[index] = tile
            
    def create_tile_group(self, level_data, tiletype, tilesize):
        for row_index, row in enumerate(level_data):
            for column_index, value in enumerate(row):
                if value != '-1':
                    x = column_index * tilesize
                    y = row_index * tilesize
                    match tiletype:
                        case 'Terrain':
                            sprite = StaticTile((x, y), [self.terrain], self.tile_index[int(value)])
                        case 'Decoration':
                            sprite = StaticTile((x, y), [self.decoration], self.tile_index[int(value)])
    
    def player_setup(self, layout, tilesize):
        for row_index, row in enumerate(layout):
            for column_index, value in enumerate(row):
                x = column_index * tilesize
                y = row_index * tilesize
                if value == '0':
                    self.player_spawn = pygame.math.Vector2(x, y)
                    self.game.player = Player(self.game, 32, (x, y), 5, [self.player_layer])

    def draw_level(self, surface):
        for layer in self.world_layers:
            for tile in layer.sprites():
                if layer == self.player_layer:
                    pass
                else:
                    surface.blit(tile.image, (tile.rect.x - self.game.camera.level_scroll.x, tile.rect.y - self.game.camera.level_scroll.y))