import click
import numpy as np


def read_lines(lines):
    output = []
    for line in lines:
        output.append(eval('[' + line + ']'))
    return np.array(output)


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

    puzzle = read_lines(lines)
    ans = 0
    constellation = puzzle[0].reshape(1, -1)
    puzzle = puzzle[1:]

    while len(puzzle) > 0:
        p = 0
        while p < len(constellation):
            point = constellation[p]
            dist = np.absolute(puzzle-point).sum(axis=1)
            to_add = puzzle[dist <= 3]
            if len(to_add) > 0:
                constellation = np.concatenate([constellation, to_add])
                puzzle = puzzle[dist > 3]
            p += 1
        ans += 1
        if len(puzzle) > 1:
            constellation = puzzle[0].reshape(1, -1)
            puzzle = puzzle[1:]
        elif len(puzzle) == 1:
            ans += 1
            break
        p = 0

    print("Part 1 solution is:")
    print(ans)
    print('-------')


if __name__ == '__main__':
    main()
