from cowsay import cowsay


class Coord:
    def __init__(self, x=0, y=0):
        self.x: int = x
        self.y: int = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Field:
    def __init__(self):
        self.field = [[None for _ in range(10)] for _ in range(10)]

    def add_mob(self, coord: Coord, msg: str):
        tmp = self.field[coord.x][coord.y]
        self.field[coord.x][coord.y] = Mob(msg)
        print(f"Added monster to {str(coord)} saying {msg}")
        if tmp:
            print(f"Replaced the old monster")


class Mob:
    def __init__(self, msg: str):
        self.msg: str = msg

    def say(self):
        print(cowsay(self.msg))


class Player:
    def __init__(self):
        self.coord = Coord()

    def move(self, direction: str):
        match direction:
            case "up":
                self.coord = Coord(self.coord.x, (self.coord.y - 1) % 10)
            case "down":
                self.coord = Coord(self.coord.x, (self.coord.y + 1) % 10)
            case "left":
                self.coord = Coord((self.coord.x - 1) % 10, self.coord.y)
            case "right":
                self.coord = Coord((self.coord.x + 1) % 10, self.coord.y)
        print(f"Moved to {self.coord}")


class Game:
    def __init__(self):
        self.player = Player()
        self.field = Field()

    def add_mob(self, coord: Coord, msg: str):
        self.field.add_mob(coord, msg)

    def encounter(self):
        x = self.player.coord.x
        y = self.player.coord.y
        if self.field.field[x][y] is not None:
            self.field.field[x][y].say()

    def move_player(self, direction: str):
        self.player.move(direction)
        self.encounter()


def main():
    game = Game()
    while line := input():
        cmd, *args = line.split()
        match cmd:
            case "up" | "down" | "left" | "right" as direction:
                game.move_player(direction)
            case "addmon":
                if len(args) != 3:
                    print("Invalid arguements")
                else:
                    x, y, msg = args
                    game.add_mob(Coord(int(x), int(y)), msg)
            case _:
                print("Invalid command")


if __name__ == "__main__":
    main()
