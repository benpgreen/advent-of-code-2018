import click


class Land:

    def __init__(self, land_array):
        self.land = land_array
        self.minute = 0

    def _find_next_value(self, c, i, j):
        neighbours = [
                (i+1, j), (i+1, j+1), (i+1, j-1),
                (i-1, j), (i-1, j+1), (i-1, j-1),
                (i, j+1), (i, j-1)
        ]
        neighbours = [(i, j) for (i, j) in neighbours
                      if i >= 0 and j >= 0]
        if c == '.':
            count = 0
            for (i_n, j_n) in neighbours:
                try:
                    n = self.land[i_n][j_n]
                except IndexError:
                    continue
                if n == '|':
                    count += 1
                    if count >= 3:
                        break
            if count >= 3:
                new_c = '|'
            else:
                new_c = '.'
        elif c == '|':
            count = 0
            for (i_n, j_n) in neighbours:
                try:
                    n = self.land[i_n][j_n]
                except IndexError:
                    continue
                if n == '#':
                    count += 1
                    if count >= 3:
                        break
            if count >= 3:
                new_c = '#'
            else:
                new_c = '|'
        elif c == '#':
            counts = {'.': 0, '#': 0, '|': 0}
            for (i_n, j_n) in neighbours:
                try:
                    n = self.land[i_n][j_n]
                except IndexError:
                    continue
                counts[n] += 1
                if counts['|'] >= 1 and counts['#'] >= 1:
                    break
            if counts['|'] >= 1 and counts['#'] >= 1:
                new_c = '#'
            else:
                new_c = '.'
        else:
            msg = 'Invalid land input: {0} at {1}'.format(c, (i, j))
            raise ValueError(msg)
        return new_c

    def next_min(self):
        new_land = []
        for (i, row) in enumerate(self.land):
            new_row = []
            for (j, c) in enumerate(row):
                new_c = self._find_next_value(c, i, j)
                new_row.append(new_c)
            new_land.append(new_row)
        self.minute += 1
        if self.land == new_land:
            print('Converged')
        self.land = new_land

    def score(self):
        counts = {'.': 0, '#': 0, '|': 0}
        for row in self.land:
            for c in row:
                counts[c] += 1
        return counts['|']*counts['#']


@click.command()
@click.argument('puzzle_input', type=click.Path(exists=True))
@click.option(
    '--wait_tol', type=int, default=1000,
    help='The number of minutes to wait until check for convergence.'
    )
def main(puzzle_input, wait_tol):

    with open(puzzle_input, 'r') as f:
        file = f.read()

    lines = file.split('\n')
    if lines[0] == '':
        lines = lines[1:]
    if lines[-1] == '':
        lines = lines[:-1]

    array = []
    for line in lines:
        row = [c for c in line]
        array.append(row)

    land = Land(array)
    for _ in range(10):
        land.next_min()

    ans1 = land.score()

    print("Part 1 solution is:")
    print(ans1)
    print('-------')

    land = Land(array)
    scores = [land.score()]
    for _ in range(wait_tol):
        land.next_min()
        scores.append(land.score())

    last = scores[-1]
    i = len(scores)-2
    while i >= 0 and scores[i] != last:
        i -= 1

    if i < 0 or len(scores)-1-i > len(scores[:i]):
        msg = 'Sequence failed to converge, try increasing --wait_tol'
        raise RuntimeError(msg)
    else:
        period = scores[i:-1]
        p = len(period)
        second_period = scores[i-p:i]
        if period != second_period:
            msg = 'Sequence failed to converge, try increasing --wait_tol'
            raise RuntimeError(msg)

    ans2 = period[(1000000000-wait_tol) % p]
    print("Part 2 solution is:")
    print(ans2)


if __name__ == '__main__':
    main()
