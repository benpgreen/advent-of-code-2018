import click

from collections import defaultdict


def label_points(split_line):
    coords = split_line[2]
    dims = split_line[3]
    y, x = coords.split(',')
    y = int(y)
    x = int(x[:-1])
    n, m = dims.split('x')
    n = int(n)
    m = int(m)

    out = []
    for i in range(n):
        for j in range(m):
            out.append((x+j, y+i))
    return out


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

    points = defaultdict(set)

    for line in lines:
        split_line = line.split(' ')
        out = label_points(split_line)
        for point in out:
            points[point].add(int(split_line[0][1:]))

    max_id = int(lines[-1].split(' ')[0][1:])
    master = set(range(1, 1+max_id))
    ans1 = 0

    for value in points.values():
        if len(value) > 1:
            master = master.difference(value)
            ans1 += 1

    if len(master) != 1:
        raise RuntimeError("Invalid puzzle input...")
    else:
        ans2 = list(master)[0]

    print("Part 1 solution is:")
    print(ans1)
    print('-------')
    print("Part 2 solution is:")
    print(ans2)


if __name__ == '__main__':
    main()
