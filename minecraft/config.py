import random


class Config:
    SEED = random.randint(0, 100000)
    CHUNK_SIZE = 8
    RENDER_DISTANCE = 3

    BLOCK_ASSETS = [
        'grass.png',
        'stone.png',
        'dirt.png',
        'water.png',
        'sand.png',
        'white_cube',
        'leaf.png',
        'oaklog.png',
        None
    ]
    HOTBAR_COUNT = 9
    HOTBAR_X_START = -0.32
    HOTBAR_X_STEP = 0.08
    HOTBAR_Y = -0.42
    HOTBAR_SCALE = 0.08

    THICKNESS = 0.0048
    LENGTH = 0.04

    HAND_POSITION = (0.5, -0.3, 0.8)
    HAND_SCALE = 0.2

    PLAYER_GRAVITY = 0.5
    PLAYER_SPEED = 7
    RUN_SPEED = 11
    CROUCH_SPEED = 3
    PLAYER_START_Y = 10
    CAMERA_NORMAL_Y = 1.9
    CAMERA_CROUCH_Y = 1.5

    JUMP_BLOCK_CHECK_DISTANCE = 0.5
    RESPAWN_Y = -10
    MAX_PLACE_Y = -5
