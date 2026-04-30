import argparse
import sys
import io
import chess

import chess.pgn


def pgn_to_fens(pgn_text):
    game = chess.pgn.read_game(io.StringIO(pgn_text))
    if game is None:
        raise ValueError("No game found in PGN input")

    board = game.board()
    fens = [board.fen()]

    for move in game.mainline_moves():
        board.push(move)
        fens.append(board.fen())

    return fens


def parse_args():
    parser = argparse.ArgumentParser(
        description="Convert a PGN game into FEN strings for each position."
    )
    parser.add_argument(
        "pgn_file",
        nargs="?",
        help="PGN input file path. If omitted, reads from stdin.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if args.pgn_file:
        with open(args.pgn_file, "r", encoding="utf-8") as f:
            pgn_text = f.read()
    else:
        pgn_text = sys.stdin.read()

    try:
        fens = pgn_to_fens(pgn_text)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    for index, fen in enumerate(fens):
        print(f"{index}: {fen}")


if __name__ == "__main__":
    main()