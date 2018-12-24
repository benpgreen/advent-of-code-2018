import click
import numpy as np


def read_positions(lines):
    positions = []
    radii = []
    for line in lines:
        left = line.index('<')
        right = line.index('>')
        position = eval('(' + line[left+1:right] + ')')
        radius = int(line.split('=')[-1])
        positions.append(position)
        radii.append(radius)
    return positions, radii


def manhatten(a, b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])+abs(a[2]-b[2])


def get_strongest(positions, radii):
    r = np.argmax(radii)
    radius = radii[r]
    pos0 = positions[r]
    count = 0
    for pos in positions:
        if manhatten(pos, pos0) <= radius:
            count += 1
    return count


def check_point(v, positions, radii):
    sub_sum = np.absolute(positions - v).sum(axis=1)
    return (sub_sum <= radii).sum()


def get_new_vector(v, pos, positions, radii):

    n = v.copy()
    best = check_point(n, positions, radii)
    new = best
    while new >= best:
        best = new
        for p in pos:
            n[p] += -1
        new = check_point(n, positions, radii)
    for p in pos:
        n[p] += 1
    new_vector = (n, best)

    n = v.copy()
    best = check_point(n, positions, radii)
    new = best
    while new >= best:
        best = new
        for p in pos:
            n[p] += 1
        new = check_point(n, positions, radii)
    for p in pos:
        n[p] += -1
    if best > new_vector[1]:
        new_vector = (n, best)
    return new_vector


def optimize(positions, radii):
    v = np.median(positions, axis=0)
    v = np.array([int(v0) for v0 in v])
    poss = [(0, ), (1, ), (2, ), (0, 1), (0, 2), (1, 2), (0, 1, 2)]
    new_vectors = []
    while True:
        for pos in poss:
            n = get_new_vector(v, pos, positions, radii)
            new_vectors.append(n)
        new_vectors = sorted(new_vectors, key=lambda x: x[1], reverse=True)
        n = new_vectors[0][0]
        if (n == v).all():
            break
        else:
            v = n

    return np.absolute(v).sum()


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

    positions, radii = read_positions(lines)

    ans1 = get_strongest(positions, radii)

    positions = np.array(positions)
    radii = np.array(radii)

    print("Part 1 solution is:")
    print(ans1)
    print('-------')

    ans2 = optimize(positions, radii)
    print("Part 2 solution is:")
    print(ans2)


if __name__ == '__main__':
    main()
