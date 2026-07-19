from ursina import Entity, raycast, mouse, destroy, held_keys, lerp, color
from ursina.prefabs.first_person_controller import FirstPersonController
from config import Config


class PlayerController:
    def __init__(self, world_manager, ui_manager):
        self.world_manager = world_manager
        self.ui_manager = ui_manager
        self.player = FirstPersonController(gravity=Config.PLAYER_GRAVITY, speed=Config.PLAYER_SPEED)
        self.player.y = Config.PLAYER_START_Y

    def handle_input(self, key):
        if key in [str(i) for i in range(1, 10)]:
            self.ui_manager.selected_index = int(key) - 1
        elif key == 'scroll up':
            self.ui_manager.selected_index = (self.ui_manager.selected_index - 1) % 9
        elif key == 'scroll down':
            self.ui_manager.selected_index = (self.ui_manager.selected_index + 1) % 9

        self.ui_manager.set_selected_texture()

        if key in [str(i) for i in range(1, 10)]:
            self.ui_manager.selected_index = int(key) - 1
            self.ui_manager.set_selected_texture()

        if key == 'left mouse down' and mouse.hovered_entity:
            target = mouse.hovered_entity
            pos = (round(target.x), round(target.y), round(target.z))
            is_player_placed = getattr(target, 'is_player_placed', False)
            is_brown = (target.color == color.brown)
            is_grass = hasattr(target, 'has_dirt') and target.has_dirt
            self.world_manager.mined_positions.add(pos)
            if pos in self.world_manager.runtime_blocks:
                del self.world_manager.runtime_blocks[pos]
            destroy(target)
            if not is_player_placed:
                if is_grass:
                    self.world_manager.spawn_dirt(pos[0], pos[1] - 1, pos[2])
                if target.color == color.gray:
                    self.world_manager.spawn_dirt(pos[0], pos[1] - 1, pos[2])
                if is_brown:
                    self.world_manager.spawn_dirt(pos[0] + 1, pos[1], pos[2])
                    self.world_manager.spawn_dirt(pos[0] - 1, pos[1], pos[2])
                    self.world_manager.spawn_dirt(pos[0], pos[1], pos[2] + 1)
                    self.world_manager.spawn_dirt(pos[0], pos[1], pos[2] - 1)
            self.ui_manager.swing_hand()

        if key == 'right mouse down' and mouse.hovered_entity and self.ui_manager.selected_texture is not None:
            pos = (round(mouse.hovered_entity.x + mouse.normal.x),
                   round(mouse.hovered_entity.y + mouse.normal.y),
                   round(mouse.hovered_entity.z + mouse.normal.z))
            if pos[1] > Config.MAX_PLACE_Y:
                if pos in self.world_manager.mined_positions:
                    self.world_manager.mined_positions.remove(pos)
                new_b = Entity(model='cube', color=color.white, position=pos, collider='box', texture=self.ui_manager.selected_texture)
                new_b.is_player_placed = True
                if self.ui_manager.selected_texture == 'grass.png':
                    new_b.has_dirt = True
                cx, cz = pos[0] // self.world_manager.CHUNK_SIZE, pos[2] // self.world_manager.CHUNK_SIZE
                if (cx, cz) in self.world_manager.loaded_chunks:
                    new_b.parent = self.world_manager.loaded_chunks[(cx, cz)]
                self.world_manager.runtime_blocks[pos] = {
                    'texture': self.ui_manager.selected_texture,
                    'is_player_placed': True,
                    'has_dirt': self.ui_manager.selected_texture == 'grass.png'
                }
                self.ui_manager.swing_hand()

    def update(self):
        head_check = raycast(self.player.position + (0, 1.8, 0), direction=(0, 1, 0), distance=Config.JUMP_BLOCK_CHECK_DISTANCE)

        if head_check.hit:
            self.player.jump_height = 0
        else:
            self.player.jump_height = 1

        if held_keys['left control']:
            self.player.speed = Config.RUN_SPEED
            self.player.camera_pivot.y = lerp(self.player.camera_pivot.y, Config.CAMERA_NORMAL_Y, 0.15)
        elif held_keys['left shift']:
            self.player.speed = Config.CROUCH_SPEED
            self.player.camera_pivot.y = lerp(self.player.camera_pivot.y, Config.CAMERA_CROUCH_Y, 0.15)
        else:
            self.player.speed = Config.PLAYER_SPEED
            self.player.camera_pivot.y = lerp(self.player.camera_pivot.y, Config.CAMERA_NORMAL_Y, 0.15)

        if self.player.y < Config.RESPAWN_Y:
            self.player.position = (0, Config.PLAYER_START_Y, 0)

        p_cx, p_cz = int(self.player.x // self.world_manager.CHUNK_SIZE), int(self.player.z // self.world_manager.CHUNK_SIZE)
        for x in range(p_cx - self.world_manager.RENDER_DISTANCE, p_cx + self.world_manager.RENDER_DISTANCE + 1):
            for z in range(p_cz - self.world_manager.RENDER_DISTANCE, p_cz + self.world_manager.RENDER_DISTANCE + 1):
                if (x, z) not in self.world_manager.loaded_chunks:
                    self.world_manager.loaded_chunks[(x, z)] = self.world_manager.create_chunk(x, z)
        for (cx, cz), parent_ent in list(self.world_manager.loaded_chunks.items()):
            if abs(cx - p_cx) > self.world_manager.RENDER_DISTANCE or abs(cz - p_cz) > self.world_manager.RENDER_DISTANCE:
                destroy(parent_ent)
                del self.world_manager.loaded_chunks[(cx, cz)]
