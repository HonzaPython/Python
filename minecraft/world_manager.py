from ursina import Entity, color, scene
import math
import random
from config import Config


class WorldManager:
    def __init__(self):
        self.SEED = Config.SEED
        self.CHUNK_SIZE = Config.CHUNK_SIZE
        self.RENDER_DISTANCE = Config.RENDER_DISTANCE
        self.loaded_chunks = {}
        self.mined_positions = set()
        self.runtime_blocks = {}

    def get_world_height(self, x, z):
        y = 0
        amplitude, frequency = 4.0, 0.05
        for i in range(3):
            y += amplitude * math.sin(x * frequency + self.SEED) * math.cos(z * frequency + self.SEED)
            amplitude *= 0.5; frequency *= 2.0
        return int(y)

    def spawn_dirt(self, x, y, z):
        pos = (round(x), round(y), round(z))
        cx, cz = pos[0] // self.CHUNK_SIZE, pos[2] // self.CHUNK_SIZE
        if (cx, cz) not in self.loaded_chunks:
            return
        if pos in self.mined_positions:
            return
        for e in scene.entities:
            if isinstance(e, Entity) and e.model == 'cube' and (round(e.x), round(e.y), round(e.z)) == pos:
                return
        new_dirt = Entity(model='cube', color=color.white, position=pos, collider='box', texture='dirt.png')
        new_dirt.is_player_placed = False
        new_dirt.parent = self.loaded_chunks[(cx, cz)]

    def spawn_tree(self, x, y, z, parent):
        for i in range(1, 4):
            Entity(model='cube', position=(x, y + i, z), texture='oaklog.png', color=color.white, collider='box', parent=parent)

        for i in range(3, 5):
            for dx in range(-2, 3):
                for dz in range(-2, 3):
                    is_corner = (abs(dx) == 2 and abs(dz) == 2)
                    if not is_corner:
                        Entity(model='cube', position=(x + dx, y + i, z + dz), texture='leaf.png', color=color.white, collider='box', parent=parent)

        i = 5
        Entity(model='cube', position=(x, y + i, z), texture='leaf.png', color=color.white, collider='box', parent=parent)
        Entity(model='cube', position=(x + 1, y + i, z), texture='leaf.png', color=color.white, collider='box', parent=parent)
        Entity(model='cube', position=(x - 1, y + i, z), texture='leaf.png', color=color.white, collider='box', parent=parent)
        Entity(model='cube', position=(x, y + i, z + 1), texture='leaf.png', color=color.white, collider='box', parent=parent)
        Entity(model='cube', position=(x, y + i, z - 1), texture='leaf.png', color=color.white, collider='box', parent=parent)

        Entity(model='cube', position=(x, y + 6, z), texture='leaf.png', color=color.white, collider='box', parent=parent)

    def create_chunk(self, chunk_x, chunk_z):
        chunk_parent = Entity()
        h_map = {}
        for x in range(chunk_x * self.CHUNK_SIZE - 3, (chunk_x + 1) * self.CHUNK_SIZE + 3):
            for z in range(chunk_z * self.CHUNK_SIZE - 3, (chunk_z + 1) * self.CHUNK_SIZE + 3):
                h_map[(x, z)] = self.get_world_height(x, z)

        texture_map = {
            color.green: 'grass.png',
            color.gray: 'stone.png',
            color.brown: 'dirt.png',
            color.blue: 'water.png',
            color.yellow: 'sand.png'
        }

        for x in range(chunk_x * self.CHUNK_SIZE, (chunk_x + 1) * self.CHUNK_SIZE):
            for z in range(chunk_z * self.CHUNK_SIZE, (chunk_z + 1) * self.CHUNK_SIZE):
                y = h_map[(x, z)]
                pos = (x, y, z)
                if pos in self.mined_positions:
                    continue

                is_near_water = False
                for dx in range(-2, 3):
                    for dz in range(-2, 3):
                        if h_map.get((x + dx, z + dz), 0) <= -2:
                            is_near_water = True
                            break
                    if is_near_water:
                        break

                if y <= -2:
                    col = color.blue
                elif is_near_water and -1 <= y <= 1:
                    col = color.yellow
                elif y > 3:
                    col = color.gray
                else:
                    col = color.green

                tex = texture_map.get(col, 'white_cube')
                b = Entity(model='cube', color=color.white, position=pos, collider='box', texture=tex, parent=chunk_parent)
                b.has_dirt = (col == color.green)
                b.is_player_placed = False
            if col == color.green and random.random() < 0.05:
                self.spawn_tree(x, y, z, chunk_parent)

        for pos, info in self.runtime_blocks.items():
            if pos[0] // self.CHUNK_SIZE == chunk_x and pos[2] // self.CHUNK_SIZE == chunk_z:
                block = Entity(
                    model='cube',
                    color=color.white,
                    position=pos,
                    collider='box',
                    texture=info['texture'],
                    parent=chunk_parent
                )
                block.is_player_placed = info['is_player_placed']
                if info.get('has_dirt'):
                    block.has_dirt = True
        return chunk_parent
