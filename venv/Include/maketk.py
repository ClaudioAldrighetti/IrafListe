import tkinter as tk

from winconfig import *

def make_Button(master, command, state=tk.NORMAL, text="",
                bg=BT_BG, fg=BT_FG, highlightbackground=BT_BDC, highlightthickness=BT_BDT, activebackground=BT_ABG,
                row=0, column=0, height=0, padx=3, pady=3, sticky=tk.EW,
                grid_flag=True, fill="none", expand=False):
    new_button = tk.Button(master, command=command, state=state, text=text, default="active",
                            bg=bg, fg=fg, height=height, relief=BT_REL, activebackground=activebackground,
                            highlightbackground=highlightbackground, highlightthickness=highlightthickness)
    if grid_flag:
        new_button.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)
    else:
        new_button.pack(padx=padx, pady=pady, fill=fill, expand=expand)
    return new_button

def make_Label(master, text="", row=0, column=0, padx=1, pady=3, sticky=tk.E, state=tk.NORMAL):
    new_label = tk.Label(master, text=text, bg=LB_BG, fg=LB_FG, state=state)
    new_label.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)

    return new_label

def make_Entry(master, text="", row=0, column=0, padx=1, pady=3, width=15, sticky=tk.W, state=tk.NORMAL):
    new_entry = tk.Entry(master, width=width, bg=EN_BG, fg=EN_FG, insertbackground=EN_INS,
                         disabledbackground=EN_BG, readonlybackground=EN_BG, state=tk.NORMAL)
    new_entry.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)
    new_entry.insert(0, text)
    new_entry.configure(state=state)

    return new_entry

def clear_Entry(entry, final_state=None):
    prev_state = entry.cget("state")
    entry.configure(state=tk.NORMAL)
    entry.delete(0, "end")
    if final_state is None:
        entry.configure(state=prev_state)
    else:
        entry.configure(state=final_state)
    return

def make_OptionMenu(master, var_val, list_val, defaultval=None, row=0, column=0, padx=1, pady=3, width=10, sticky=tk.EW, state=tk.NORMAL):
    new_optionmenu = ttk.OptionMenu(master, var_val, defaultval, *list_val)
    new_optionmenu.configure(state=state, width=width, style=OM_STYLE)
    new_optionmenu["menu"].configure(bg=OM_BG, fg=OM_FG, relief=tk.FLAT, activebackground=OM_ABG)
    new_optionmenu.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)

    return new_optionmenu
