from game import Game


def main():
    game: Game = Game()

    game.draw()
    while True:
        input('next turn')
        game.tick()
        game.draw()


if __name__ == '__main__':
    main()
