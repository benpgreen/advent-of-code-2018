import click
import numpy as np


def check_power_level(x, y, serial_num):
    rack_id = x + 10
    power = rack_id*y + serial_num
    power *= rack_id
    power = str(power)
    if len(power) < 3:
        power = 0
    else:
        power = int(power[-3])
    power -= 5
    return power


def get_power_levels(serial_num):
    power_levels = []
    for x in range(1, 301):
        row = []
        for y in range(1, 301):
            row.append(check_power_level(x, y, serial_num))
        power_levels.append(row)
    return np.array(power_levels)


@click.command()
@click.argument('serial_number', type=int)
def main(serial_number):

    power_levels = get_power_levels(serial_number)

    max_score = -np.inf
    ans1 = None
    for y in range(1, 298):
        for x in range(1, 298):
            new_power = power_levels[x-1:x+2, y-1:y+2].sum()
            if new_power > max_score:
                ans1 = (x, y)
                max_score = new_power

    print("Part 1 solution is:")
    print(ans1)

    max_score = -np.inf
    ans2 = None
    msg = 'Calculating answer for part 2'
    with click.progressbar(range(1, 301), label=msg) as Y:
        for y in Y:
            for x in range(1, 301):
                k = 0
                while x+k <= 300 and y+k <= 300:
                    new_power = power_levels[x-1:x+k, y-1:y+k].sum()
                    if new_power > max_score:
                        ans2 = (x, y, k+1)
                        max_score = new_power
                    k += 1

    print("Part 2 solution is:")
    print(ans2)


if __name__ == '__main__':
    main()
