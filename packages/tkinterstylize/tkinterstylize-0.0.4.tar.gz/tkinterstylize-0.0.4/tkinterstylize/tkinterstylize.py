from functools import partial
from tkinter import Button, Label

fg = "pink"
bg = "purple"


def colours(fg1, bg1):
    global fg, bg
    fg, bg = fg1, bg1


def _button(root, text="", command=None):
    # Customise Here
    # fg=text color
    # bg=backgeound colour
    # relief=button shape and all...see net..
    # valathum venki ankane...
    # u can bind it to give hover
    def _on_enter(event="", but=None):
        but.config(bg=fg)
        but.config(fg=bg)

    def _on_leave(event="", but=None):
        but.config(fg=fg)
        but.config(bg=bg)

    b = Button(root, text=text, fg=fg, bg=bg, command=command, relief='flat')
    b.bind("<Enter>", partial(_on_enter, but=b))
    b.bind("<Leave>", partial(_on_leave, but=b))
    return b


def _label(root: object, text: str = "") -> object:
    # Customise Here
    # fg=text color
    # bg=backgeound colour
    # valathum venki ankane...

    return Label(root, text=text, fg="green")
