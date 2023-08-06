from functools import partial
from tkinter import Button, Label

fg = "pink"
bg = "purple"


def colours(fg1, bg1):
    global fg, bg
    fg, bg = fg1, bg1


def _button(root, text="", command=None, font="Comic Sans MS", size=15,relief='ridge',fg1=None,bg1=None):
    # Customise Here
    # fg=text color
    # bg=backgeound colour
    # relief=button shape and all...see net..
    # valathum venki ankane...
    # u can bind it to give hover
    if fg1 is None:
        fg1 = fg
    if bg1 is None:
        bg1 = bg



    def _on_enter(event="", but=None):
        but.config(bg=fg1)
        but.config(fg=bg1)

    def _on_leave(event="", but=None):
        but.config(fg=fg1)
        but.config(bg=bg1)

    b = Button(root, text=text, fg=fg1, bg=bg1, command=command, relief=relief)
    b.bind("<Enter>", partial(_on_enter, but=b))
    b.bind("<Leave>", partial(_on_leave, but=b))
    b.config(font=(font, size))
    return b


def _label(root: object, text: str = "", font="Comic Sans MS", size=15,fg1=None,bg1=None) -> object:
    # Customise Here
    # fg=text color
    # bg=backgeound colour
    # valathum venki ankane...
    if fg1 is None:
        fg1=fg
    if bg1 is None:
        bg1=bg

    l = Label(root, text=text, fg=fg1,bg=bg1)
    l.config(font=(font, size))
    return l
