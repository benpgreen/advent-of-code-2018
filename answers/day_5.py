import click
import string


def reduce_str(puzzle):
    output = ''
    i = 0
    while i < len(puzzle):
        entry = puzzle[i]
        if (i == len(puzzle)-1 or entry == puzzle[i+1] or
           entry.lower() != puzzle[i+1].lower()):
            output += entry
            i += 1
        else:
            i += 2
    return output


def fully_reduce_str(puzzle):
    further_reduce = True

    out = puzzle
    old_length = len(out)

    while further_reduce:
        out = reduce_str(out)
        if len(out) < old_length:
            old_length = len(out)
        else:
            further_reduce = False
    return out


def remove_letter(puzzle, letter):
    lower = letter.lower()
    upper = letter.upper()
    return puzzle.replace(lower, '').replace(upper, '')


@click.command()
@click.argument('puzzle_input', type=click.Path(exists=True))
def main(puzzle_input):

    with open(puzzle_input, 'r') as f:
        puzzle = f.read().replace('\n', '')

    r_puzzle = fully_reduce_str(puzzle)
    ans1 = len(r_puzzle)
    print("Part 1 solution is:")
    print(ans1)
    print('-------')

    ans2 = ans1
    for letter in string.ascii_lowercase:
        if letter in r_puzzle:
            removed = remove_letter(r_puzzle, letter)
            new_ans = len(fully_reduce_str(removed))
            if new_ans < ans2:
                ans2 = new_ans

    print("Part 2 solution is:")
    print(ans2)


if __name__ == '__main__':
    main()
