import enum

STYLE_SHEET = "background-color: rgb({},{},{})"
KEY_STRING = "COLOR_{}"


class CellsColors(enum.Enum):
    COLOR_0 = (204, 192, 179)
    COLOR_2 = (238, 228, 218)
    COLOR_4 = (237, 224, 200)
    COLOR_8 = (242, 177, 121)
    COLOR_16 = (245, 149, 99)
    COLOR_32 = (246, 124, 95)
    COLOR_64 = (246, 94, 59)
    COLOR_128 = (237, 207, 114)
    COLOR_256 = (237, 204, 97)
    COLOR_512 = (237, 200, 80)
    COLOR_1024 = (237, 197, 63)
    COLOR_2048 = (237, 194, 46)
    COLOR_OTHER = (0, 0, 0)
    COLOR_GAME_OVER = (238, 228, 218, 0.73)
    COLOR_GAME = (187, 173, 160)


class FakeCallable:
    def __call__(self, *args, **kwargs):
        pass
