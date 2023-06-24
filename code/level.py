from BLACKFORGE2 import *

from CONSTANTS import *

class Level:
    def __init__(self, level_data, game, surface):
        self.game = game
        self.level_data = level_data
        self.surface = surface
        
        self.tile_index = {}
        self.create_tile_index()
        self.create_group(level_data)

    def create_group(self, level_data):
        self.on_screen_tiles = pygame.sprite.Group()
        self.terrain = pygame.sprite.Group()
        self.decoration = pygame.sprite.Group()
        for layout_name in ['Terrain','Decoration']:
            layout = import_csv_layout(self.level_data[layout_name])
            self.create_tile_group(layout, layout_name, TILE_SIZE)
            
        self.world_layers = [
            self.terrain,
            self.decoration
        ]
    
    def create_tile_index(self):
        tile_list = import_cut_graphics("../assests/tileset.png", TILE_SIZE)
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
                if value != '-1':
                    x = column_index * tilesize
                    y = row_index * tilesize
                    match value:
                        case '0':
                            self.player_spawn = pygame.math.Vector2(x, y)
                            # self.game.player = Player()

    def draw_level(self, surface):
        for layer in self.world_layers:
            for tile in layer.sprites():
                surface.blit(tile.image, (tile.rect.x - self.game.camera.level_scroll.x, tile.rect.y - self.game.camera.level_scroll.y))