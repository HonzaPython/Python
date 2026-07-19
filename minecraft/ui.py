from ursina import Entity, Button, Text, camera, color, invoke, time
from config import Config


class UIManager:
    def __init__(self):
        self.block_assets = Config.BLOCK_ASSETS
        self.selected_index = 0
        self.selected_texture = self.block_assets[self.selected_index]
        self.thickness = Config.THICKNESS
        self.length = Config.LENGTH

        self.crosshair_h = Entity(parent=camera.ui, model='quad', color=color.white, scale=(self.length, self.thickness), position=(0, 0))
        self.crosshair_v = Entity(parent=camera.ui, model='quad', color=color.white, scale=(self.thickness, self.length), position=(0, 0))

        self.hotbar = []
        for i in range(Config.HOTBAR_COUNT):
            box = Button(
                parent=camera.ui,
                model='quad',
                scale=Config.HOTBAR_SCALE,
                position=(Config.HOTBAR_X_START + (i * Config.HOTBAR_X_STEP), Config.HOTBAR_Y),
                color=color.dark_gray
            )
            if i < len(self.block_assets) and self.block_assets[i]:
                Entity(parent=box, model='quad', scale=0.8, texture=self.block_assets[i], color=color.white)
            self.hotbar.append(box)

        self.hand = Entity(parent=camera, model='cube', position=Config.HAND_POSITION, scale=Config.HAND_SCALE, texture=self.selected_texture, color=color.white)
        self.info_text = Text(text='', position=(-0.85, 0.45), background=True)
        self.fps_value = 0
        self.update_fps()

    def swing_hand(self):
        self.hand.animate_rotation((30, 0, 0), duration=0.1)
        self.hand.animate_rotation((0, 0, 0), duration=0.1, delay=0.1)

    def set_selected_texture(self):
        self.selected_texture = self.block_assets[self.selected_index]
        self.hand.texture = self.selected_texture
        self.hand.color = color.white
        self.hand.visible = (self.selected_texture is not None)

    def update_fps(self):
        self.fps_value = int(1 / time.dt) if time.dt > 0 else 0
        invoke(self.update_fps, delay=1)

    def update_info(self, player):
        self.info_text.text = f'FPS: {self.fps_value}\nPos: ({round(player.x, 1)}, {round(player.y, 1)}, {round(player.z, 1)})'
