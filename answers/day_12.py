import click

from collections import defaultdict


def string_to_bool(string):
    if string == '#':
        out = True
    elif string == '.':
        out = False
    else:
        raise ValueError('Invalid input: {}'.format(string))
    return out


def read_puzzle(puzzle):
    plants = defaultdict(bool)
    rules = defaultdict(bool)
    init = puzzle[0].split(' ')[-1]
    for (idx, entry) in enumerate(init):
        plants[idx] = string_to_bool(entry)

    lines = puzzle[2:]
    for line in lines:
        pattern, _, new = line.split(' ')
        new = string_to_bool(new)
        pattern = tuple([string_to_bool(p) for p in pattern])
        rules[pattern] = new

    return plants, rules


class Plants:

    def __init__(self, init_plants, rules):
        self.plants = init_plants
        if rules[(False, False, False, False, False)]:
            msg = "(..... => #) cannot be in puzzle rules"
            raise ValueError(msg)
        else:
            self.rules = rules
        self.min = min(init_plants.keys())
        self.max = max(init_plants.keys())
        self.generation = 0

    def next_gen(self):
        updates = {}
        for k in range(self.min-2, self.max+3):
            pattern = tuple([self.plants[i] for i in range(k-2, k+3)])
            new = self.rules[pattern]
            updates[k] = new
        for key, val in updates.items():
            self.plants[key] = val
        self.min -= 2
        self.max += 2
        self.generation += 1

    def plant_sum(self):
        out = 0
        for key, val in self.plants.items():
            if val:
                out += key
        return out


@click.command()
@click.argument('puzzle_input', type=click.Path(exists=True))
@click.option(
    '--wait_tol', type=int, default=1000,
    help='How long to look for convergence for before stopping'
    )
@click.option(
    '--convergence_tol', type=int, default=25,
    help='How may differences must be the same to count as converged'
    )
def main(puzzle_input, wait_tol, convergence_tol):

    with open(puzzle_input, 'r') as f:
        file = f.read()

    lines = file.split('\n')
    if lines[0] == '':
        lines = lines[1:]
    if lines[-1] == '':
        lines = lines[:-1]

    plants = Plants(*read_puzzle(lines))
    for _ in range(20):
        plants.next_gen()
    ans1 = plants.plant_sum()

    print("Part 1 solution is:")
    print(ans1)
    print('-------')

    plants = Plants(*read_puzzle(lines))
    prev_sum = plants.plant_sum()
    prev_diff = None
    counter = 0
    diff_match = 0
    while counter < wait_tol and diff_match < convergence_tol:
        plants.next_gen()
        new_sum = plants.plant_sum()
        diff = new_sum - prev_sum
        if diff == prev_diff:
            diff_match += 1
        else:
            diff_match = 0
            prev_diff = diff
        prev_sum = new_sum
        counter += 1

    if diff_match == convergence_tol:
        ans2 = prev_sum + (50000000000-counter)*prev_diff
        print("Possible part 2 solution is:")
        print(ans2)
        print('If not your answer, try increasing --convergence_tol')
    else:
        raise RuntimeError('No convergence: try increasing --wait_tol')


if __name__ == '__main__':
    main()
