import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk
import chess
import chess.engine

STOCKFISH_PATH = "stockfish/stockfish-windows-x86-64-avx2.exe"


class ChessBot:
    def __init__(self, root):
        self.root = root
        self.board = chess.Board()
        self.engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
        self.images = self.load_images()
        self.setup_ui()
        self.selected_square = None
        self.drag_data = {"piece": None, "start_square": None}
        self.flip = False

        self.update_ui()

    def load_images(self):
        pieces = [
            "wp",
            "bp",
            "wn",
            "bn",
            "wb",
            "bb",
            "wr",
            "br",
            "wq",
            "bq",
            "wk",
            "bk",
        ]
        images = {}
        for piece in pieces:
            img = Image.open(f"assets/piece_images/{piece}.png")
            img = img.resize((60, 60), Image.Resampling.LANCZOS)
            images[piece] = ImageTk.PhotoImage(img)
        return images

    def setup_ui(self):
        self.canvas = tk.Canvas(self.root, width=480, height=480)
        self.canvas.pack(side=tk.LEFT)
        self.sidebar = tk.Frame(self.root, width=200)
        self.sidebar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_drop)

        flip_button = tk.Button(
            self.sidebar, text="Flip Board", command=self.flip_board
        )
        flip_button.pack()

    def draw_board(self):
        self.canvas.delete("square")
        colors = ["#f0d9b5", "#b58863"]
        for i in range(8):
            for j in range(8):
                color = colors[(i + j) % 2]
                x0 = i * 60
                y0 = j * 60
                x1 = (i + 1) * 60
                y1 = (j + 1) * 60
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, tags="square")

        self.draw_labels()
        self.draw_pieces()

    def draw_labels(self):
        for i in range(8):
            x = i * 60 + 30
            y = 8 * 60 + 15
            rank = str(8 - i) if self.flip else str(i + 1)
            file = chr(ord("a") + i) if not self.flip else chr(ord("h") - i)

            self.canvas.create_text(10, y - 60, text=rank, anchor="w")
            self.canvas.create_text(x, 485, text=file)

    def draw_pieces(self):
        self.canvas.delete("piece")
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                piece_str = f"{'w' if piece.color else 'b'}{piece.symbol().lower()}"
                x = (square % 8) * 60
                y = (7 - square // 8) * 60
                if self.flip:
                    x = 420 - x
                    y = 420 - y
                img = self.images[piece_str]
                self.canvas.create_image(x, y, anchor="nw", image=img, tags="piece")

    def on_click(self, event):
        x, y = event.x // 60, event.y // 60
        if self.flip:
            x, y = 7 - x, 7 - y
        square = chess.square(x, 7 - y)
        piece = self.board.piece_at(square)
        if piece and piece.color == self.board.turn:
            self.drag_data["piece"] = piece
            self.drag_data["start_square"] = square

    def on_drag(self, event):
        if self.drag_data["piece"]:
            self.canvas.delete("drag_piece")
            img = self.images[
                f"{'w' if self.drag_data['piece'].color else 'b'}{self.drag_data['piece'].symbol().lower()}"
            ]
            self.canvas.create_image(
                event.x - 30, event.y - 30, anchor="nw", image=img, tags="drag_piece"
            )

    def on_drop(self, event):
        if self.drag_data["piece"]:
            x, y = event.x // 60, event.y // 60
            if self.flip:
                x, y = 7 - x, 7 - y
            end_square = chess.square(x, 7 - y)
            move = chess.Move(self.drag_data["start_square"], end_square)
            if self.board.is_legal(move):
                self.board.push(move)
                self.drag_data["piece"] = None
                self.canvas.delete("drag_piece")
                self.update_ui()

    def show_top_moves(self):
        for widget in self.sidebar.winfo_children():
            if widget.winfo_class() != "Button":
                widget.destroy()

        info = self.engine.analyse(self.board, chess.engine.Limit(time=2.0), multipv=4)
        moves = [entry["pv"][0] for entry in info]
        move_strings = [self.board.san(move) for move in moves]

        tk.Label(self.sidebar, text="Top Moves:").pack()
        for move in move_strings:
            tk.Label(self.sidebar, text=move).pack()

    def flip_board(self):
        self.flip = not self.flip
        self.update_ui()

    def update_ui(self):
        self.draw_board()
        self.show_top_moves()

    def close(self):
        self.engine.quit()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Chess Bot")
    bot = ChessBot(root)
    root.protocol("WM_DELETE_WINDOW", bot.close)
    root.mainloop()
s
