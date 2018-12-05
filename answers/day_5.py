import click
import string


def reduce_str(puzzle):
    output = puzzle
    i = 0
    while True:
        entry = output[i]
        if i == len(output)-1:
            # we are done
            break
        elif entry == output[i+1] or entry.lower() != output[i+1].lower():
            i += 1
        else:
            # delete entry and entry+1
            output = output[:i] + output[i+2:]
            i += -1
    return output


def remove_letter(puzzle, letter):
    lower = letter.lower()
    upper = letter.upper()
    return puzzle.replace(lower, '').replace(upper, '')


@click.command()
@click.argument('puzzle_input', type=click.Path(exists=True))
def main(puzzle_input):

    with open(puzzle_input, 'r') as f:
        puzzle = f.read().replace('\n', '')

    r_puzzle = reduce_str(puzzle)
    ans1 = len(r_puzzle)
    print("Part 1 solution is:")
    print(ans1)
    print('-------')

    ans2 = ans1
    for letter in string.ascii_lowercase:
        if letter in r_puzzle:
            removed = remove_letter(r_puzzle, letter)
            new_ans = len(reduce_str(removed))
            if new_ans < ans2:
                ans2 = new_ans

    print("Part 2 solution is:")
    print(ans2)


if __name__ == '__main__':
    main()
