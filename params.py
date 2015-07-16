import pickle

default = {
    'CAPTION': 'snake',

    'WIN_SIZE': (800, 800),
    'TILE_SIZE': 40,
    'TILE_COUNT': 20,

    'START_POS': (10, 10),
    'START_SIZE': 7,

    'FPS': 20,
    'STEP_TIME': 200,

    'MAP_FOLDER': 'maps',
    'DEFAULT_MAP': 'map3.txt',

    'PIC_FOLDER': 'pics',
    'PAUSE_PIC': 'pause.jpg',
    'GAME_OVER_PIC': 'game over.jpg',
    'BG_PIC': 'snake.jpg',
    'ICON': 'ksnake.png',

    'FRUIT_PICS': ['apple.png', 'cherry.png', 'lemon.png', 'strawberry.png'],
    'FRUIT_WEIGHTS': [1, 2, 3, 4],

    'BG_COLOR': (55, 55, 55),
    'TEXT_COLOR': (255, 160, 40),
    'SCORE_COLOR': (204, 204, 0),
    'HEAD_COLOR': (46, 166, 42),
    'BODY_COLOR': (37, 60, 213),
    'GRID_COLOR': (100, 100, 100),
    'OBSTACLE_COLOR': (102, 0, 0),
    'FRUIT_COLOR': (204, 0, 204),

    'FONT': 'optima',
    'GAME_OVER_TEXT': 'Game Over, press any key to restart',
    'GAME_PAUSED_TEXT': 'Pause, press any key to continue',

    'HIGH_SCORE': 0
}

PARAM_PAM_PAM = "params.pickle"
params = default


def load_params():
    global params
    try:
        with open(PARAM_PAM_PAM, mode='rb') as f:
            params = pickle.load(f)
    except IOError:
        pass


def save_params():
    with open(PARAM_PAM_PAM, mode='wb') as f:
        pickle.dump(params, f)


load_params()
