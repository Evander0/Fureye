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
    "Layer": {
        "eyeball": 1
    }
}
files: dict = {}
layer: dict = {}
screen_width = 0
screen_height = 0


def __init__():
    global files, layer, screen_width, screen_height, path, canvas
    config = Config("display", default)
    conf = config.read()
    path = conf["Path"]
    file = conf["Layer"]

    dynamic['eyes'] = {}
    root = Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.overrideredirect(True)
    root.config(cursor="none")
    root.geometry(f'{screen_width}x{screen_height}')
    canvas = Canvas(root, width=screen_width, height=screen_height)
    if static["SYS_INFO"] == "Windows":
        root.state('zoom')
    else:
        root.state('normal')
        root.attributes("-fullscreen", True)

    sys.path.append(path)
    for f in file.keys():
        load(f, file[f])
    canvas.place(x=0, y=0, width=screen_width, height=screen_height)
    static["running"]["eye_display"] = True
    while static["running"]["eye_display"]:
        for i in file.keys():
            if dynamic['eyes'][i]["enabled"]:
                x = int(dynamic['eyes'][i]["x"] * screen_width / 2 + screen_width / 2 - files[i][
                    dynamic['eyes'][i]["selected"]].width() / 2)
                y = int(dynamic['eyes'][i]["y"] * screen_height / 2 + screen_height / 2 - files[i][
                    dynamic['eyes'][i]["selected"]].height() / 2)
                dynamic['eyes'][i]["nx"] = (int(
                    canvas.coords(layer[i][dynamic['eyes'][i]["selected"]])[0]) - screen_width / 2 + files[i][
                                                dynamic['eyes'][i]["selected"]].width() / 2) / screen_width * 2
                dynamic['eyes'][i]["ny"] = (int(
                    canvas.coords(layer[i][dynamic['eyes'][i]["selected"]])[1]) - screen_height / 2 + files[i][
                                                dynamic['eyes'][i]["selected"]].height() / 2) / screen_height * 2
                if len(layer[i]) > 1:
                    for j in layer[i]:
                        canvas.moveto(j, screen_width, screen_height)
                canvas.moveto(layer[i][dynamic['eyes'][i]["selected"]], x, y)
            else:
                print(layer[i])
                for j in layer[i]:
                    canvas.moveto(j, screen_width, screen_height)
        sleep(0.02)
        root.update()
    canvas.delete("all")
    canvas.destroy()
    root.destroy()
    return


def load(name, size):
    global files, layer
    try:
        file = pathlib.Path(list(glob.glob(f'{path}/{name}.*'))[0])
    except IndexError:
        print(f"File {name} not found")
        return -1

    dynamic['eyes'][name] = {}
    dynamic['eyes'][name]["x"] = 0
    dynamic['eyes'][name]["y"] = 0
    dynamic['eyes'][name]["nx"] = 0
    dynamic['eyes'][name]["ny"] = 0
    dynamic['eyes'][name]["selected"] = 0
    dynamic['eyes'][name]["enabled"] = False
    scale = int(float(size)*screen_height)

    match file.suffix:
        case ".png" | ".jpg":
            layer[name] = []
            files[name] = []
            img = Image.open(file)
            img = img.resize((int(img.size[0] * scale / img.size[1]), scale))
            files[name].append(ImageTk.PhotoImage(img))
            layer[name].append(canvas.create_image(0, 0, image=files[name][0], anchor=NW))
            canvas.moveto(layer[name][0], screen_width / 2 - files[name][0].width() / 2,
                          screen_height / 2 - files[name][0].height() / 2)
        case ".gif":
            img = Image.open(file)
            files[name] = []
            layer[name] = []
            for i in range(img.n_frames):
                img.seek(i)
                frame = img.resize((int(img.size[0] * scale / img.size[1]), scale))
                files[name].append(ImageTk.PhotoImage(frame))
                layer[name].append(canvas.create_image(0, 0, image=files[name][i], anchor=NW))
                canvas.moveto(layer[name][i], screen_width / 2 - files[name][i].width() / 2,
                              screen_height / 2 - files[name][i].height() / 2)
        case _:
            print(f"Not supported file type: {file.suffix}")
