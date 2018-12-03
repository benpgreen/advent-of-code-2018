import click


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

    freq_list = []
    ans1 = 0
    for line in lines:
        num = int(line)
        ans1 += num
        freq_list.append(num)

    memory = set([0])
    i = 0
    current = 0

    while True:
        current += freq_list[i]
        if current in memory:
            ans2 = current
            break
        else:
            memory.add(current)
        if i < len(freq_list) - 1:
            i += 1
        elif i == len(freq_list) - 1:
            i = 0

    print("Part 1 solution is:")
    print(ans1)
    print('-------')
    print("Part 2 solution is:")
    print(ans2)


if __name__ == '__main__':
    main()
