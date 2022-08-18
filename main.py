from board import Board


if __name__ == "__main__":
    b = Board(128, 128)
    while True:
        b.tick()