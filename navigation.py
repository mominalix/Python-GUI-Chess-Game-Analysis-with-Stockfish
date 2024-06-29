import tkinter as tk


class Navigation:
    def __init__(self, parent, on_next, on_prev):
        self.frame = tk.Frame(parent)
        self.frame.grid(row=8, column=0, columnspan=2, pady=5)

        self.prev_button = tk.Button(self.frame, text="Previous Move", command=on_prev)
        self.prev_button.grid(row=0, column=0, padx=5)

        self.next_button = tk.Button(self.frame, text="Next Move", command=on_next)
        self.next_button.grid(row=0, column=1, padx=5)
