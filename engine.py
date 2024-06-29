import chess.engine


class ChessEngine:
    def __init__(self, stockfish_path):
        self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)

    def analyze(self, board):
        info = self.engine.analyse(board, chess.engine.Limit(time=0.1))
        return {
            "score": info["score"].relative.score(mate_score=10000),
            "pv": info.get("pv"),
        }

    def quit(self):
        self.engine.quit()
