from lib.lib import *
from lib.config import Config
import time
import random

default = {
    "Limit": [-0.05, 0.05],
    "Time": [0.5, 1]
}


def __init__():
    global limit, wtime

    config = Config("display_pos", default)
    conf = config.read()
    limit = conf["Limit"]
    wtime = conf["Time"]

    while not static["running"]["eye_display"]:
        continue
    mdata = dynamic["eyes"]["eyeball"]
    static["running"]["move_eye"] = True
    dynamic['eyes']["eyeball"]["enabled"] = True
    while static["running"]["move_eye"]:
        x = random.uniform(limit[0], limit[1])
        y = random.uniform(limit[0], limit[1])
        schedule = time.time() + random.uniform(wtime[0], wtime[1])
        while time.time() <= schedule:
            mdata["x"] += (x - mdata["nx"]) / 20
            mdata["y"] += (y - mdata["ny"]) / 20
            time.sleep(0.01)
    return
