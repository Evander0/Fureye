import glob
import sys
import pathlib
from time import sleep
from tkinter import *
from lib.lib import *
from lib.config import Config
from PIL import Image, ImageTk

default = {
    "Path": "src",
    "num_display": 1,
    "Layer": {
        "eyeball": 1
    },
    "addon": {}
}
files: dict = {}
layer: list = []
d_window: list = []
canvas: list = []
screen_width = 0
screen_height = 0
num_display = 1
path = None


def __init__():
    global files, layer, screen_width, screen_height, path, canvas, num_display
    config = Config("display", default)
    conf = config.read()
    try:
        path = conf["Path"]
        file = conf["Layer"]
        addon = conf["addon"]
        num_display = conf["num_display"]
    except KeyError:
        config.update()
        conf = config.read()
        path = conf["Path"]
        file = conf["Layer"]
        addon = conf["addon"]
        num_display = conf["num_display"]

    dynamic['eyes'] = []
    root = Tk()
    root.state('iconic')
    for d in range(num_display):
        dynamic['eyes'].insert(d, {})
        d_window.insert(d, Toplevel())
        screen_width = d_window[d].winfo_screenwidth()
        screen_height = d_window[d].winfo_screenheight()
        d_window[d].overrideredirect(True)
        d_window[d].config(cursor="none")
        d_window[d].geometry(f'{screen_width}x{screen_height}+{screen_width * d}+0')
        canvas.insert(d, Canvas(d_window[d], width=screen_width * num_display, height=screen_height))
        if static["SYS_INFO"] == "Windows":
            d_window[d].state('zoom')
        else:
            d_window[d].state('normal')
            d_window[d].attributes("-fullscreen", True)
        canvas[d].place(x=0, y=0, width=screen_width, height=screen_height)

    sys.path.append(path)
    for f in file.keys():
        load(f, file[f])
    for f in addon.keys():
        for d in addon[f][1]:
            try:
                load(f, addon[f][0], d, addon[f][2])
            except IndexError:
                load(f, addon[f][0], d)
    static["running"]["fureyev1"] = True
    while static["running"]["fureyev1"]:
        for d in range(num_display):
            for i in layer[d].keys():
                if dynamic['eyes'][d][i]["enabled"]:
                    x = int(dynamic['eyes'][d][i]["x"] * screen_width / 2 + screen_width / 2 - files[i][
                        dynamic['eyes'][d][i]["selected"]].width() / 2)
                    y = int(dynamic['eyes'][d][i]["y"] * screen_height / 2 + screen_height / 2 - files[i][
                        dynamic['eyes'][d][i]["selected"]].height() / 2)
                    dynamic['eyes'][d][i]["nx"] = (int(
                        canvas[d].coords(layer[d][i][dynamic['eyes'][d][i]["selected"]])[0]) - screen_width / 2 +
                                                   files[i][
                                                       dynamic['eyes'][d][i][
                                                           "selected"]].width() / 2) / screen_width * 2
                    dynamic['eyes'][d][i]["ny"] = (int(
                        canvas[d].coords(layer[d][i][dynamic['eyes'][d][i]["selected"]])[1]) - screen_height / 2 +
                                                   files[i][
                                                       dynamic['eyes'][d][i][
                                                           "selected"]].height() / 2) / screen_height * 2
                    if len(layer[d][i]) > 1:
                        for j in layer[d][i]:
                            canvas[d].moveto(j, screen_width, screen_height)
                    canvas[d].moveto(layer[d][i][dynamic['eyes'][d][i]["selected"]], x, y)
                else:
                    for j in layer[d][i]:
                        canvas[d].moveto(j, screen_width, screen_height)
            d_window[d].update()
        sleep(0.02)
    for d in range(num_display):
        canvas[d].delete("all")
        canvas[d].destroy()
        d_window[d].destroy()
    return


def load(name, size, on_display=-1, as_f=""):
    global files, layer
    try:
        file = pathlib.Path(list(glob.glob(f'{path}/{name}.*'))[0])
    except IndexError:
        print(f"File {name} not found")
        return -1
    f_name = name
    if as_f != "":
        name = as_f
    if on_display == -1:
        for d in range(num_display):
            dynamic['eyes'][d][name] = {}
            dynamic['eyes'][d][name]["x"] = 0
            dynamic['eyes'][d][name]["y"] = 0
            dynamic['eyes'][d][name]["nx"] = 0
            dynamic['eyes'][d][name]["ny"] = 0
            dynamic['eyes'][d][name]["selected"] = 0
            dynamic['eyes'][d][name]["enabled"] = False
    else:
        dynamic['eyes'][on_display][name] = {}
        dynamic['eyes'][on_display][name]["x"] = 0
        dynamic['eyes'][on_display][name]["y"] = 0
        dynamic['eyes'][on_display][name]["nx"] = 0
        dynamic['eyes'][on_display][name]["ny"] = 0
        dynamic['eyes'][on_display][name]["selected"] = 0
        dynamic['eyes'][on_display][name]["enabled"] = False
    scale = int(float(size) * screen_height)
    try:
        if name in list(layer[on_display].keys()):
            for i in range(len(layer[on_display][name])):
                if on_display == -1:
                    for d in range(num_display):
                        canvas[d].delete(layer[d][name][i])
                else:
                    canvas[on_display].delete(layer[on_display][name][i])
    except IndexError:
        pass

    match file.suffix:
        case ".png" | ".jpg":
            files[f_name] = []
            if on_display == -1:
                for d in range(num_display):
                    try:
                        layer[d][name] = []
                    except IndexError:
                        layer.insert(d, {})
                        layer[d][name] = []
            else:
                try:
                    layer[on_display][name] = []
                except IndexError:
                    layer.insert(on_display, {})
                    layer[on_display][name] = []
            img = Image.open(file)
            img = img.resize((int(img.size[0] * scale / img.size[1]), scale))
            files[f_name].insert(0, ImageTk.PhotoImage(img))
            if on_display == -1:
                for d in range(num_display):
                    layer[d][name].insert(0, canvas[d].create_image(0, 0, image=files[f_name][0], anchor=NW))
                    canvas[d].moveto(layer[d][name][0], screen_width / 2 - files[f_name][0].width() / 2,
                                     screen_height / 2 - files[f_name][0].height() / 2)
            else:
                layer[on_display][name].insert(0,
                                               canvas[on_display].create_image(0, 0, image=files[f_name][0], anchor=NW))
                canvas[on_display].moveto(layer[on_display][name][0], screen_width / 2 - files[f_name][0].width() / 2,
                                          screen_height / 2 - files[f_name][0].height() / 2)
        case ".gif":
            img = Image.open(file)
            files[f_name] = []
            if on_display == -1:
                for d in range(num_display):
                    try:
                        layer[d][name] = []
                    except IndexError:
                        layer.insert(d, {})
                        layer[d][name] = []
            else:
                try:
                    layer[on_display][name] = []
                except IndexError:
                    layer.insert(on_display, {})
                    layer[on_display][name] = []
            for i in range(img.n_frames):
                img.seek(i)
                frame = img.resize((int(img.size[0] * scale / img.size[1]), scale))
                files[f_name].insert(i, ImageTk.PhotoImage(frame))
                if on_display == -1:
                    for d in range(num_display):
                        layer[d][name].insert(i, canvas[d].create_image(0, 0, image=files[f_name][i], anchor=NW))
                        canvas[d].moveto(layer[d][name][i], screen_width / 2 - files[f_name][i].width() / 2,
                                         screen_height / 2 - files[f_name][i].height() / 2)
                else:
                    layer[on_display][name].insert(i, canvas[on_display].create_image(0, 0, image=files[f_name][i],
                                                                                      anchor=NW))
                    canvas[on_display].moveto(layer[on_display][name][i], screen_width / 2 - files[f_name][i].width() / 2,
                                              screen_height / 2 - files[f_name][i].height() / 2)
        case _:
            print(f"Not supported file type: {file.suffix}")
