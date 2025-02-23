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
    config_t = Config("display")
    conf_t = config_t.read()
    num_display = conf_t["num_display"]
    mdata = []
    for i in range(num_display):
        mdata.append(dynamic["eyes"][i]["eyeball"])
        mdata[i]["enabled"] = True
    static["running"]["move_eye"] = True
    while static["running"]["move_eye"]:
        x = random.uniform(limit[0], limit[1])
        y = random.uniform(limit[0], limit[1])
        schedule = time.time() + random.uniform(wtime[0], wtime[1])
        while time.time() <= schedule:
            for i in range(num_display):
                mdata[i]["x"] += (x - mdata[i]["nx"]) / 20
                mdata[i]["y"] += (y - mdata[i]["ny"]) / 20
            time.sleep(0.01)
    return
