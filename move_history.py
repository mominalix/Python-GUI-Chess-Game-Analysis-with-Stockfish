import tkinter as tk


class MoveHistory:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)
        self.frame.grid(row=0, column=2, rowspan=8, padx=10, pady=5)
        self.history_area = tk.Listbox(self.frame, width=30)
        self.history_area.pack(fill=tk.BOTH, expand=True)

    def update(self, move_stack):
        self.history_area.delete(0, tk.END)
        for move in move_stack:
            self.history_area.insert(tk.END, move.uci())
