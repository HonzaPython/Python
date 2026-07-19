from ursina import Ursina, Audio, Sky
from world_manager import WorldManager
from ui import UIManager
from player import PlayerController


app = Ursina()

music = Audio(
    'music.mp3',
    loop=True,
    autoplay=True,
    volume=1
)

world_manager = WorldManager()
ui_manager = UIManager()
player_controller = PlayerController(world_manager, ui_manager)


def input(key):
    player_controller.handle_input(key)


def update():
    player_controller.update()
    ui_manager.update_info(player_controller.player)


Sky()
app.run()