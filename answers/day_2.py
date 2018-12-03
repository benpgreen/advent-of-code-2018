import click
import numpy as np

from collections import Counter


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

    twos = 0
    threes = 0
    np_arrays = []

    for id0 in lines:

        np_arrays.append(np.array([l for l in id0]))

        counter = Counter(id0)
        two_found = False
        three_found = False
        for value in counter.values():
            if value == 2 and not two_found:
                twos += 1
                two_found = True
            elif value == 3 and not three_found:
                threes += 1
                three_found = True

    ans1 = twos*threes
    stop = False

    for (idx, array1) in enumerate(np_arrays):
        for array2 in np_arrays[idx+1:]:
            if (array1 != array2).sum() == 1:
                rels = array1[array1 == array2]
                ans2 = ''.join(a for a in rels)
                stop = True
                break
        if stop:
            break

    print("Part 1 solution is:")
    print(ans1)
    print('-------')
    print("Part 2 solution is:")
    print(ans2)


if __name__ == '__main__':
    main()
