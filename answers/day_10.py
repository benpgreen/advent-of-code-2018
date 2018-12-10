import click
import string
import numpy as np


def get_ranges(vector):
    h_max, v_max = vector.max(axis=0)
    h_min, v_min = vector.min(axis=0)
    h_range = h_max - h_min
    v_range = v_max - v_min
    return v_range, h_range


def print_msg(vector):
    set_v = [tuple(v) for v in vector]
    h_max, v_max = vector.max(axis=0)
    h_min, v_min = vector.min(axis=0)
    for y in range(v_min, v_max+1):
        row = ''
        for x in range(h_min, h_max+1):
            if (x, y) in set_v:
                row += '#'
            else:
                row += ' '
        print(row)


def find_possible_messages(positions, velocities, v_tol=10, h_tol=100,
                           wait_tol=100000):

    pos = positions.copy()
    v_range, h_range = get_ranges(pos)
    seconds = 0

    # wait until positions close enough
    while (v_range > v_tol or h_range > h_tol) and seconds <= wait_tol:
        pos += velocities
        v_range, h_range = get_ranges(pos)
        seconds += 1

    # now print until they are apart
    while v_range <= v_tol and h_range <= h_tol:
        print('Possible message:')
        print_msg(pos)
        print("Appears in {} seconds".format(seconds))
        print('--------------------')
        pos += velocities
        v_range, h_range = get_ranges(pos)
        seconds += 1


@click.command()
@click.argument('puzzle_input', type=click.Path(exists=True))
@click.option(
    '--v_tol', type=int, default=10,
    help='The vertical range: msgs must be within this height to be printed'
    )
@click.option(
    '--h_tol', type=int, default=100,
    help='The horizontal range: msgs must be within this length to be printed'
    )
@click.option(
    '--wait_tol', type=int, default=100000,
    help='The number of seconds to wait at the start before giving up'
    )
def main(puzzle_input, v_tol, h_tol, wait_tol):
    """Will print possible messages, you will then need to decide which is
    your answer in the case of mutliple messages.

    If you aren't getting any messages then try tuning `v_tol` and `h_tol`;
    the former in the first instance.

    """

    with open(puzzle_input, 'r') as f:
        file = f.read()

    lines = file.split('\n')
    if lines[0] == '':
        lines = lines[1:]
    if lines[-1] == '':
        lines = lines[:-1]

    to_remove = string.ascii_lowercase + '=< '
    positions = []
    velos = []
    for line in lines:
        c_line = ''.join(l for l in line if l not in to_remove)
        c_line = '[' + c_line[:-1].replace('>', ',') + ']'
        c_line = eval(c_line)
        positions.append(c_line[:2])
        velos.append(c_line[2:])
    positions = np.array(positions)
    velos = np.array(velos)

    find_possible_messages(positions, velos, v_tol=v_tol, h_tol=h_tol,
                           wait_tol=wait_tol)


if __name__ == '__main__':
    main()
