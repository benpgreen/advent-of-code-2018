import click

from collections import defaultdict


def read_lines(lines):
    ground = defaultdict(lambda: '.')
    ground[(500, 0)] = '+'
    min_y = 100000000
    max_y = 0

    for line in lines:
        i, j = line.split(',')
        # coord 1
        label_i, num_i = i.split('=')
        num_i = int(num_i)
        # coord 2
        label_j, nums_j = j[1:].split('=')
        min_j, max_j = nums_j.split('..')
        min_j = int(min_j)
        max_j = int(max_j)
        if label_i == 'x' and label_j == 'y':
            for num_j in range(min_j, max_j+1):
                if num_j > max_y:
                    max_y = num_j
                if num_j < min_y:
                    min_y = num_j
                ground[(num_i, num_j)] = '#'
        elif label_i == 'y' and label_j == 'x':
            for num_j in range(min_j, max_j+1):
                if num_i > max_y:
                    max_y = num_i
                if num_i < min_y:
                    min_y = num_i
                ground[(num_j, num_i)] = '#'
        else:
            raise RuntimeError("{0}, {1}".format(label_i, label_j))
    return ground, min_y, max_y


class WaterDrop:

    def __init__(self, id, direction, pos, pair_id=None):
        self.id = id
        self.direction = direction
        self.pair_id = pair_id
        self.pos = pos
        self.split_pos = None
        self.stopped = False
        self.active = True

    def right_copy(self, next_id):
        right_copy = WaterDrop(next_id, 'R', self.pos, pair_id=self.id)
        right_copy.split_pos = self.pos
        return right_copy

    def move(self, ground, drops):

        i, j = self.pos
        if self.direction == 'D':
            if ground[(i, j+1)] == '.':
                self.pos = (i, j+1)
                ground[(i, j+1)] = '|'
                drops[self.id] = self
            elif ground[(i, j+1)] == '-':
                # check horizontals
                breaks = 0
                broke = False
                r = i+1
                skip = False
                while ground[(r, j+1)] != '#':
                    if ground[(r, j+1)] == '|':
                        broke = True
                        break
                    elif ground[(r, j+1)] == '.':
                        skip = True
                        break
                    r += 1
                if not broke:
                    breaks += 1
                r = i-1
                broke = False
                while ground[(r, j+1)] != '#':
                    if ground[(r, j+1)] == '|':
                        broke = True
                        break
                    elif ground[(r, j+1)] == '.':
                        skip = True
                        break
                    r += -1
                if not broke:
                    breaks += 1

                if breaks < 2 and not skip:
                    self.active = False
                    drops[self.id] = self
                elif not skip:  # split
                    self.direction = 'L'
                    ground[self.pos] = '-'
                    new_id = max(drops.keys()) + 1
                    drops[new_id] = self.right_copy(new_id)
                    self.split_pos = self.pos
                    self.pair_id = new_id
                    drops[self.id] = self

            else:  # split
                self.direction = 'L'
                ground[self.pos] = '-'
                new_id = max(drops.keys()) + 1
                drops[new_id] = self.right_copy(new_id)
                self.split_pos = self.pos
                self.pair_id = new_id
                drops[self.id] = self
        elif self.direction == 'L' and not self.stopped:
            if ground[(i, j+1)] == '.':
                self.direction = 'D'
                ground[(i, j)] = '|'
                try:
                    drops[self.pair_id].pair_id = None
                except KeyError:
                    pass
                drops[self.id] = self
            elif ground[(i-1, j)] == '.' or ground[(i-1, j)] == '|':
                self.pos = (i-1, j)
                ground[(i-1, j)] = '-'
                drops[self.id] = self
            else:
                ground[(i, j)] = '-'
                try:
                    pair = drops[self.pair_id]
                except KeyError:
                    self.active = False
                if self.active and pair.stopped:
                    # move back to split_pos
                    i0, j0 = self.split_pos
                    j0 += -1
                    self.pos = (i0, j0)
                    self.stopped = False
                    self.direction = 'D'
                    pair.active = False
                    drops[self.pair_id] = pair
                else:
                    self.stopped = True
                drops[self.id] = self
        elif self.direction == 'R' and not self.stopped:
            if ground[(i, j+1)] == '.':
                self.direction = 'D'
                ground[(i, j)] = '|'
                try:
                    drops[self.pair_id].pair_id = None
                except KeyError:
                    pass
                drops[self.id] = self
            elif ground[(i+1, j)] == '.' or ground[(i+1, j)] == '|':
                self.pos = (i+1, j)
                ground[(i, j)] = '-'
                drops[self.id] = self
            else:
                ground[(i, j)] = '-'
                try:
                    pair = drops[self.pair_id]
                except KeyError:
                    self.active = False

                if self.active and pair.stopped:
                    # move back to split_pos
                    i0, j0 = self.split_pos
                    j0 += -1
                    self.stopped = False
                    self.pos = (i0, j0)
                    self.direction = 'D'
                    pair.active = False
                    drops[self.pair_id] = pair
                else:
                    self.stopped = True
                drops[self.id] = self

        if (self.stopped and
           (self.pair_id is None or drops[self.pair_id].direction == 'D')):
            self.active = False

        return ground, drops


class GroundWater:

    def __init__(self, ground, y_range):
        self.ground = ground
        self.drops = {0: WaterDrop(0, 'D', (500, 0))}
        self.y_range = y_range
        self.highest_drop = 0

    def flow(self):
        ys = []
        current_drops = list(self.drops.keys())
        for drop_id in current_drops:
            drop = self.drops[drop_id]
            ground, drops = drop.move(self.ground, self.drops)
            if not drop.active:
                del self.drops[drop.id]
            else:
                ys.append(drop.pos[1])
            self.ground = ground
            self.drops = drops
        if len(ys) > 0:
            self.highest_drop = min(ys)
        else:
            self.highest_drop = self.y_range[1]+1

    def ans1(self):
        score = 0
        for (i, j), val in self.ground.items():
            if j >= self.y_range[0] and j <= self.y_range[1]:
                if val == '|' or val == '-':
                    score += 1
        return score

    def ans2(self):
        score = 0
        for (i, j), val in self.ground.items():
            if j >= self.y_range[0] and j <= self.y_range[1]:
                if val == '-':
                    # check horizontals
                    breaks = 0
                    broke = False
                    r = i+1
                    while self.ground[(r, j)] != '#':
                        if self.ground[(r, j)] == '|':
                            broke = True
                            break
                        else:
                            r += 1
                    if not broke:
                        breaks += 1
                    r = i-1
                    broke = False
                    while self.ground[(r, j)] != '#':
                        if self.ground[(r, j)] == '|':
                            broke = True
                            break
                        else:
                            r += -1
                    if not broke:
                        breaks += 1
                    if breaks == 2:
                        score += 1
        return score

    def viz(self):
        Xs = []
        Ys = []
        for key, val in self.ground.items():
            if val != '.' and val != '#':
                Xs.append(key[0])
                Ys.append(key[1])
        x_min = min(Xs) - 5
        x_max = max(Xs) + 5
        y_max = max(Ys) + 5
        for i in range(max(0, y_max-40), y_max+1):
            row = ''
            for j in range(x_min, x_max):
                if (j, i) in self.ground.keys():
                    row += self.ground[(j, i)]
                else:
                    row += '.'
            print(row)
        print('*'*(x_max-x_min))


@click.command()
@click.argument('puzzle_input', type=click.Path(exists=True))
def main(puzzle_input):

    with open(puzzle_input, 'r') as f:
        file = f.read()

    lines = file.split('\n')
    if lines[0] == '':
        lines = lines[1:]
    if lines[-1] == '':
        lines = lines[:-1]

    ground, y_min, y_max = read_lines(lines)

    GW = GroundWater(ground, (y_min, y_max))
    hd = GW.highest_drop
    while hd <= y_max:
        GW.flow()
        hd = GW.highest_drop

    ans1 = GW.ans1()
    print("Part 1 solution is:")
    print(ans1)
    print('-------')

    ans2 = GW.ans2()
    print("Part 2 solution is:")
    print(ans2)


if __name__ == '__main__':
    main()
