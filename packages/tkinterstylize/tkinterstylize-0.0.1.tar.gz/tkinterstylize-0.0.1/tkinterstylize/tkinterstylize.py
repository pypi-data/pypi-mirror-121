from tkinter import Button,Label
from functools import partial
def _button(root, text="", command=None):
    # Customise Here
    # fg=text color
    # bg=backgeound colour
    # relief=button shape and all...see net..
    # valathum venki ankane...
    # u can bind it to give hover
    def _on_enter(event="", but=None):

        but.config(bg="Pink")
        but.config(fg="Purple")

    def _on_leave(event="", but=None):
        but.config(fg="Pink")
        but.config(bg="Purple")

    b = Button(root, text=text, fg="pink", bg="purple", command=command, relief='flat')
    b.bind("<Enter>", partial(_on_enter, but=b))
    b.bind("<Leave>", partial(_on_leave, but=b))
    return b


def _label(root: object, text: str = "") -> object:
    # Customise Here
    # fg=text color
    # bg=backgeound colour
    # valathum venki ankane...

    return Label(root, text=text, fg="green")
