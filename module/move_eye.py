from lib.lib import *
from lib.config import Config
import time
import random

default = {
    "Limit": [-0.05, 0.05],
    "Time": [0.5, 1]
}


def __init__():
    config = Config("display_pos", default)
    try:
        conf = config.read()
        limit = conf["Limit"]
        wtime = conf["Time"]
    except KeyError:
        config.update()
        conf = config.read()
        limit = conf["Limit"]
        wtime = conf["Time"]

    while not static["running"]["fureyev1"]:
        continue
    mdata1 = dynamic["eyes"][0]["eyeball"]
    mdata2 = dynamic["eyes"][1]["eyeball"]
    static["running"]["move_eye"] = True
    mdata1["enabled"] = True
    mdata2["enabled"] = True
    while static["running"]["move_eye"]:
        x = random.uniform(limit[0], limit[1])
        y = random.uniform(limit[0], limit[1])
        schedule = time.time() + random.uniform(wtime[0], wtime[1])
        while time.time() <= schedule:
            mdata1["x"] += (x - mdata1["nx"]) / 20
            mdata1["y"] += (y - mdata1["ny"]) / 20
            mdata2["x"] += (x - mdata2["nx"]) / 20
            mdata2["y"] += (y - mdata2["ny"]) / 20
            time.sleep(0.01)
    return
