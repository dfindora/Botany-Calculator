import re
import tkinter as tk
from tkinter import ttk
from functools import partial

import tkentryautocomplete as tkac
import botany

curr_pigments = []


def main():
    pigments = botany.get_pigments()
    pigment_names = to_readable(pigments.keys())
    pigment_to_readable = {pigment_names[i]: list(pigments.keys())[i] for i in range(len(pigment_names))}
    readable_to_pigment = {list(pigments.keys())[i]: pigment_names[i] for i in range(len(pigment_names))}
    window = tk.Tk()
    window.title("Botany 1.7.10 calculator")
    lbl_pigments = tk.Label(window, text="pigments")
    lbl_pigments.pack()
    cb_pigments = tkac.AutocompleteCombobox(window, values=pigment_names)
    cb_pigments.set_completion_list(pigment_names)
    cb_pigments.pack()
    btn_add_pigment = tk.Button(window, text="+", command=partial(add_to_pigments, cb_pigments, pigment_to_readable))
    btn_add_pigment.pack()
    btn_debug = tk.Button(window, text="debug", command=partial(print, curr_pigments))
    btn_debug.pack()
    lbl_target = tk.Label(window, text="target")
    lbl_target.pack()
    cb_target = tkac.AutocompleteCombobox(window, values=pigment_names)
    cb_target.set_completion_list(pigment_names)
    cb_target.pack()
    tv_mutations = ttk.Treeview(window, columns=(1, 2, 3), show='headings', height=8)
    tv_mutations.heading(1, text="First Pigment")
    tv_mutations.heading(2, text="Second Pigment")
    tv_mutations.heading(3, text="Result")
    btn_get_mutations = tk.Button(window, text="Get Mutations", command=partial(get_mutations, pigment_to_readable,
                                                                                readable_to_pigment, cb_target,
                                                                                pigments, tv_mutations))
    btn_get_mutations.pack()
    tv_mutations.pack()

    window.mainloop()


def to_readable(vals):
    new_vals = []
    for val in vals:
        new_vals.append(re.sub(r'(\w+)_(\w+)', botany.title_case, val) if '_' in val
                        else re.sub(r'(\w+)', botany.title_case, val))
    return new_vals


def add_to_pigments(cb_pigments, pigment_dict):
    curr_pigments.append(pigment_dict.get(cb_pigments.get()))


def get_mutations(pigment_to_readable, readable_to_pigment, cb_target, pigments, tv_mutations):
    path = botany.find_path(curr_pigments, pigment_to_readable.get(cb_target.get()), pigments)
    print(path.to_list())
    for i, step in enumerate(path.to_list()):
        tv_mutations.insert(parent='', index=i, iid=i, values=tuple([readable_to_pigment[item] for item in step]))
    tv_mutations.pack()



if __name__ == "__main__":
    main()
