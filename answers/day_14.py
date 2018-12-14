import click


def get_recipes_after(puzzle_input):
    recipes = {}
    elf1 = 0
    elf2 = 1
    recipes = {0: 3, 1: 7}
    length = 2
    after = int(puzzle_input)

    while length < after + 10:
        # combine score
        elf1_recipe = recipes[elf1]
        elf2_recipe = recipes[elf2]
        combined = str(elf1_recipe + elf2_recipe)
        for r in combined:
            recipes[length] = int(r)
            length += 1

        # change elf index
        elf1 += 1 + elf1_recipe
        elf1 = elf1 % length
        elf2 += 1 + elf2_recipe
        elf2 = elf2 % length

    output = ''
    for i in range(after, after+10):
        output += str(recipes[i])
    return output


def count_recipes_up_to(puzzle_input):
    recipes = {}
    elf1 = 0
    elf2 = 1
    recipes = {0: 3, 1: 7}
    length = 2
    last = '37'
    match = False
    length = 2
    p = len(puzzle_input)

    while not match:
        # combine scores
        elf1_recipe = recipes[elf1]
        elf2_recipe = recipes[elf2]
        combined = str(elf1_recipe + elf2_recipe)
        for r in combined:
            recipes[length] = int(r)
            last += r
            last = last[-p:]
            if last == puzzle_input:
                match = True
                break
            length += 1

        # change elf index
        elf1 += 1 + int(elf1_recipe)
        elf1 = elf1 % length
        elf2 += 1 + int(elf2_recipe)
        elf2 = elf2 % length

    return length - p + 1


@click.command()
@click.argument('puzzle_input', type=str)
def main(puzzle_input):

    ans1 = get_recipes_after(puzzle_input)
    print("Part 1 solution is:")
    print(ans1)
    print('-------')

    ans2 = count_recipes_up_to(puzzle_input)
    print("Part 2 solution is:")
    print(ans2)


if __name__ == '__main__':
    main()
