import click


def get_puzzle_info(puzzle):
    track = []
    carts = []
    for (i, line) in enumerate(puzzle):
        row = ''
        for (j, ch) in enumerate(line):
            if ch in ["<", ">"]:
                carts.append((i, j, ch, 0))
                row += "-"
            elif ch in ["v", "^"]:
                carts.append((i, j, ch, 0))
                row += "|"
            else:
                row += ch
        track.append(row)
    return track, carts


class CartTrack:

    def __init__(self, track, carts):
        self.track = track
        self.carts = carts

    def _is_free(self, new_loc):
        out = None
        for (idx, (x, y, d, num)) in enumerate(self.carts):
            if new_loc[0] == x and new_loc[1] == y:
                out = idx
                break
        return out

    def _change_dir(self, d, ints):
        directions = ["<", "^", ">", "v"]
        idx = directions.index(d)
        if ints % 3 == 1:
            new_d = d
        elif ints % 3 == 0:
            new_dirs = directions[:idx] + directions[idx+1:]
            new_d = new_dirs[idx-1 % 3]
        elif ints % 3 == 2:
            new_dirs = directions[:idx] + directions[idx+1:]
            new_d = new_dirs[idx % 3]
        else:
            raise ValueError("Invalid ints: {}".format(ints))
        return new_d

    def next_tick(self, remove_crashed=False):
        out = None
        idx = 0
        if len(self.carts) == 1:
            idx = 1
            out = (self.carts[0][1], self.carts[0][0])
        length = len(self.carts)
        while idx < length:
            x, y, d, num = self.carts[idx]
            current_pos = self.track[x][y]
            if current_pos == '-':
                if d == "<":
                    new_loc = (x, y-1, d, num)
                elif d == ">":
                    new_loc = (x, y+1, d, num)
                else:
                    msg = "Error: {0}, {1}".format(current_pos, d)
                    raise RuntimeError(msg)
            elif current_pos == '|':
                if d == "^":
                    new_loc = (x-1, y, d, num)
                elif d == "v":
                    new_loc = (x+1, y, d, num)
                else:
                    msg = "Error: {0}, {1}".format(current_pos, d)
                    raise RuntimeError(msg)
            elif current_pos == "/":
                if d == ">":
                    new_loc = (x-1, y, "^", num)
                elif d == "v":
                    new_loc = (x, y-1, "<", num)
                elif d == "<":
                    new_loc = (x+1, y, "v", num)
                elif d == "^":
                    new_loc = (x, y+1, ">", num)
                else:
                    msg = "Error: {0}, {1}".format(current_pos, d)
                    raise RuntimeError(msg)
            elif current_pos == "]":  # \
                if d == ">":
                    new_loc = (x+1, y, "v", num)
                elif d == "v":
                    new_loc = (x, y+1, ">", num)
                elif d == "<":
                    new_loc = (x-1, y, "^", num)
                elif d == "^":
                    new_loc = (x, y-1, "<", num)
                else:
                    msg = "Error: {0}, {1}".format(current_pos, d)
                    raise RuntimeError(msg)
            elif current_pos == "+":
                new_d = self._change_dir(d, num)
                if new_d == ">":
                    new_loc = (x, y+1, new_d, num+1)
                elif new_d == "v":
                    new_loc = (x+1, y, new_d, num+1)
                elif new_d == "<":
                    new_loc = (x, y-1, new_d, num+1)
                else:  # ^
                    new_loc = (x-1, y, new_d, num+1)
            else:
                msg = "Error: invalid entry {0} at coord ({1},{2})"
                raise RuntimeError(msg.format(current_pos, x, y))

            clash = self._is_free(new_loc)
            if clash is None:
                self.carts[idx] = new_loc
            elif remove_crashed:
                if clash < idx:
                    del self.carts[idx]
                    del self.carts[clash]
                    idx += -2
                elif clash > idx:
                    del self.carts[clash]
                    del self.carts[idx]
                    idx += -1
                else:
                    raise RuntimeError("Error")
                length += -2
            else:
                out = (new_loc[1], new_loc[0])
                break
            idx += 1
        self.carts = sorted(self.carts)
        return out


@click.command()
@click.argument('puzzle_input', type=click.Path(exists=True))
def main(puzzle_input):
    """Warning: be very careful putting your puzzle_input in a .txt file if
    copy and pasting. If you get an error when running this script check your
    input is right.

    """

    with open(puzzle_input, 'r') as f:
        lines = f.readlines()

    lines = [line.replace("\\", "]") for line in lines]
    if lines[0] == '':
        lines = lines[1:]
    if lines[-1] == '':
        lines = lines[:-1]

    cart_track = CartTrack(*get_puzzle_info(lines))
    ans1 = None
    while ans1 is None:
        ans1 = cart_track.next_tick(remove_crashed=False)

    print("Part 1 solution is:")
    print(ans1)
    print('-------')

    cart_track = CartTrack(*get_puzzle_info(lines))
    ans2 = None
    while ans2 is None:
        ans2 = cart_track.next_tick(remove_crashed=True)
    print("Part 2 solution is:")
    print(ans2)


if __name__ == '__main__':
    main()
