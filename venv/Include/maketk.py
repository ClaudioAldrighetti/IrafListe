import tkinter as tk
from tkinter import ttk

from winconfig import *


def make_Button(master, command, state=tk.NORMAL, text="",
                bg=BT_BG, fg=BT_FG, relief=BT_REL,
                highlightbackground=BT_BDC, highlightthickness=BT_BDT, activebackground=BT_ABG,
                row=0, rowspan=1, columnspan=1, column=0, height=0, padx=3, pady=3, sticky=tk.EW,
                grid_flag=True, fill=tk.NONE, expand=False):
    new_button = tk.Button(master, command=command, state=state, text=text, default=tk.ACTIVE,
                           bg=bg, fg=fg, height=height, relief=relief, activebackground=activebackground,
                           highlightbackground=highlightbackground, highlightthickness=highlightthickness)
    if grid_flag:
        new_button.grid(row=row, rowspan=rowspan, column=column, columnspan=columnspan,
                        padx=padx, pady=pady, sticky=sticky)
    else:
        new_button.pack(padx=padx, pady=pady, fill=fill, expand=expand)
    return new_button


def make_Label(master, text="", bg=LB_BG, fg=LB_FG, row=0, column=0, padx=1, pady=3, sticky=tk.E, state=tk.NORMAL):
    new_label = tk.Label(master, text=text, bg=bg, fg=fg, state=state)
    new_label.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)

    return new_label


def make_Entry(master, text="", row=0, column=0, padx=1, pady=3, width=15, sticky=tk.W, state=tk.NORMAL):
    new_entry = tk.Entry(master, width=width, bg=EN_BG, fg=EN_FG, insertbackground=EN_INS,
                         disabledbackground=EN_BG, readonlybackground=EN_BG, state=tk.NORMAL)
    new_entry.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)
    new_entry.insert(0, text)
    new_entry.configure(state=state)

    return new_entry


def make_ListBox(master, row=0, column=0, padx=1, pady=3, width=15, sticky=tk.W, selectmode=tk.SINGLE):
    new_list_box = tk.Listbox(master, width=width, bg=EN_BG, fg=EN_FG, selectmode=selectmode)
    new_list_box.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)

    return new_list_box


def clear_Entry(entry, final_state=None):
    prev_state = entry.cget("state")
    entry.configure(state=tk.NORMAL)
    entry.delete(0, "end")
    if final_state is None:
        entry.configure(state=prev_state)
    else:
        entry.configure(state=final_state)
    return


# Entry error blink function
def _change_bg(this_entry, new_color):
    this_entry.configure(bg=new_color)
    return


def entry_err_blink(this_entry):
    clear_Entry(this_entry)

    t_ms = 0
    t_step = 100
    for i in range(1):
        this_entry.after(t_ms, lambda entry=this_entry, color="Red": _change_bg(entry, color))
        this_entry.after(t_ms + t_step, lambda entry=this_entry, color="White": _change_bg(entry, color))
        this_entry.after(t_ms + t_step*2, lambda entry=this_entry, color="Black": _change_bg(entry, color))
        this_entry.after(t_ms + t_step*3, lambda entry=this_entry, color=EN_BG: _change_bg(entry, color))
        t_ms += t_step*4
    return


def make_OptionMenu(master, var_val, list_val, defaultval=None,
                    row=0, column=0, padx=1, pady=3, width=10, sticky=tk.EW, state=tk.NORMAL):
    new_optionmenu = ttk.OptionMenu(master, var_val, defaultval, *list_val)
    new_optionmenu.configure(state=state, width=width, style=OM_STYLE)
    new_optionmenu["menu"].configure(bg=OM_BG, fg=OM_FG, relief=tk.FLAT, activebackground=OM_ABG)
    new_optionmenu.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)

    return new_optionmenu


def make_Checkbutton(master, var, text="", state=tk.NORMAL, offvalue=0, onvalue=1,
                     bg=CB_BG, fg=CB_FG, selectcolor=CB_SELC, activebackground=CB_ABC, activeforeground=CB_AFC,
                     row=0, column=0, padx=1, pady=3, sticky=tk.E):
    new_checkbutton = tk.Checkbutton(master, variable=var, text=text, state=state, offvalue=offvalue, onvalue=onvalue,
                                     bg=bg, fg=fg, selectcolor=selectcolor,
                                     activebackground=activebackground, activeforeground=activeforeground)
    new_checkbutton.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)

    return new_checkbutton


def make_Separator(master, bg=SEP_BG, height=SEP_HGT,
                   padx=2, pady=3, fill=tk.X):
    new_separator = tk.Frame(master, bg=bg, height=height, bd=0)
    new_separator.pack(padx=padx, pady=pady, fill=fill)

    return new_separator
