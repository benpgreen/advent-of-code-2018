import click


def get_tree(puzzle):
    memory = {}
    memory[0] = [0, puzzle[0], puzzle[1], 0]
    tree = {0: {'children': [1]}}

    t = 1
    i = 2
    old_id = 0
    node_id = 1
    new_level = True
    while i < len(puzzle):

        if new_level:
            level_idx = 0
            child_num = puzzle[i]
            meta_num = puzzle[i+1]
            memory[t] = [level_idx, child_num, meta_num, node_id]
            tree[node_id] = {'children': []}
            i += 2
            old_id = node_id
        else:
            level_idx, child_num, meta_num, old_id = memory[t]
            level_idx += 1
            memory[t][0] += 1

        if level_idx < child_num:
            new_level = True
            node_id += 1
            tree[old_id]['children'].append(node_id)
            t += 1
        else:
            tree[old_id]['meta'] = puzzle[i: i+meta_num]
            new_level = False
            t -= 1
            i += meta_num

    return tree


@click.command()
@click.argument('puzzle_input', type=click.Path(exists=True))
def main(puzzle_input):

    with open(puzzle_input, 'r') as f:
        raw_puzzle = f.read().replace('\n', '')

    puzzle = [int(p) for p in raw_puzzle.split(' ')]
    tree = get_tree(puzzle)

    ans1 = 0
    for val in tree.values():
        ans1 += sum(val['meta'])

    print("Part 1 solution is:")
    print(ans1)
    print('-------')

    values_dict = {}
    remaining = set(tree.keys())
    while len(remaining) > 0:
        to_remove = set()
        for key in remaining:
            value = tree[key]
            if len(value['children']) == 0:
                values_dict[key] = sum(value['meta'])
                to_remove.add(key)
            elif len(set(value['children']).intersection(remaining)) == 0:
                meta = value['meta']
                children = value['children']
                score = 0
                for m in meta:
                    if m - 1 < len(children):
                        score += values_dict[children[m-1]]
                values_dict[key] = score
                to_remove.add(key)
        remaining = remaining.difference(to_remove)

    ans2 = values_dict[0]

    print("Part 2 solution is:")
    print(ans2)


if __name__ == '__main__':
    main()
