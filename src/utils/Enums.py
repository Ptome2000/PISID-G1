from enum import Enum

class AlertType(Enum):
    SOUND_EXCEEDS_90_PERCENT = ("Sound over 90%", "Sound exceeds 90% of the maximum limit")
    SOUND_BELOW_90_PERCENT = ("Sound under 90%", "Sound dropped below 90% of the maximum limit")
    SOUND_TOO_CLOSE_TO_NORMAL = ("No Movement detected", "The sound is too close to normal noise, no movements detected")
    SOUND_EXCEEDS_MAX_LIMIT = ("Sound Limit Exceeded", "The sound produced exceeds the maximum limit (Game Over)")

    def __init__(self, code, message):
        self.code = code
        self.message = message


class GameActions:
    SCORE = 1
    OPEN_DOOR = 2
    CLOSE_DOOR = 3
    CLOSE_ALL_DOOR = 4
    OPEN_ALL_DOOR = 5
