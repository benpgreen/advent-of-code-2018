import click
import networkx as nx


def convert_input(lines):
    array = [[l for l in line] for line in lines]
    return array


def manhatten(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def arena_to_graph(arena):
    G = nx.Graph()
    for (i, row) in enumerate(arena):
        for (j, entry) in enumerate(row):
            if entry == '.':
                G.add_node((i, j))
                neighbours = get_neighbours((i, j), arena)
                for (i0, j0) in neighbours:
                    G.add_node((i0, j0))
                    G.add_edge((i, j), (i0, j0))

    return G


def distance(pos1, pos2, arena):
    G = arena_to_graph(arena)
    try:
        path = nx.shortest_path(G, pos1, pos2)
        length = len(path) - 1
    except nx.NetworkXNoPath:
        length = None
    return length


def get_neighbours(pos, arena):
    i, j = pos
    out = []
    neighbours = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
    for neighbour in neighbours:
        i0, j0 = neighbour
        try:
            n_char = arena[i0][j0]
            if n_char == '.':
                out.append(neighbour)
        except IndexError:
            pass
    return out


class Creature:

    def __init__(self, character, pos, attack_power=3):
        if character != 'E' and character != 'G':
            raise ValueError('Invalid character: {}'.format(character))
        else:
            self.char = character
        self.hp = 200
        self.pos = pos
        if character == 'E':
            self.ap = attack_power
        else:
            self.ap = 3

    def move(self, positions, arena):
        possibles = []
        for (i, j) in positions:
            if arena[i][j].char != self.char:
                # found opponent
                if manhatten((i, j), self.pos) == 1:
                    possibles = []
                    break
                else:
                    # get neigbourhood spaces
                    opp_neighbours = get_neighbours((i, j), arena)
                    char_neighbours = get_neighbours(self.pos, arena)
                    for char_n in char_neighbours:
                        for opp_n in opp_neighbours:
                            dist = distance(char_n, opp_n, arena)
                            if dist is not None:
                                tup = (
                                    dist,
                                    opp_n[0], opp_n[1],
                                    char_n[0], char_n[1]
                                    )
                                possibles.append(tup)

        possibles = sorted(possibles)
        if len(possibles) > 0:
            move = (possibles[0][-2], possibles[0][-1])
        else:
            move = self.pos
        return move

    def attack(self, positions, arena):
        possibles = []
        for (i, j) in positions:
            if (manhatten((i, j), self.pos) == 1
               and arena[i][j].char != self.char):
                opp = arena[i][j]
                possibles.append((opp.hp, i, j))
        possibles = sorted(possibles)
        if len(possibles) > 0:
            hit = possibles[0]
        else:
            hit = None
        return hit


class ElvesvsGoblins:

    def __init__(self, arena, elf_save=False, elf_ap=3):
        self.round = 0
        new_arena = []
        positions = []
        counts = {'E': 0, 'G': 0}
        for (i, row) in enumerate(arena):
            new_row = []
            for (j, entry) in enumerate(row):
                if entry == 'E' or entry == 'G':
                    e = Creature(entry, (i, j), attack_power=elf_ap)
                    positions.append((i, j))
                    counts[entry] += 1
                else:
                    e = entry
                new_row.append(e)
            new_arena.append(new_row)
        self.arena = new_arena
        self.positions = positions
        self.counts = counts
        self.victory = False
        self.elf_save = elf_save
        self.elf_dead = False

    def next_round(self):
        idx = 0
        length = len(self.positions)
        while idx < length and not self.victory:
            i, j = self.positions[idx]
            character = self.arena[i][j]
            character.pos = character.move(self.positions, self.arena)
            if character.pos == (i, j):
                self.arena[i][j] = character
            else:
                self.arena[character.pos[0]][character.pos[1]] = character
                self.positions[idx] = character.pos
                self.arena[i][j] = '.'

            hit = character.attack(self.positions, self.arena)
            if hit is not None:
                hp, i, j = hit
                hp += -character.ap
                if hp > 0:
                    self.arena[i][j].hp = hp
                else:
                    # opp is dead
                    opp = self.arena[i][j].char
                    if opp == 'E':
                        self.elf_dead = True
                        if self.elf_save:
                            break
                    self.arena[i][j] = '.'
                    opp_idx = self.positions.index((i, j))
                    if idx > opp_idx:
                        idx += -1
                    length += -1
                    self.counts[opp] += -1
                    del self.positions[opp_idx]

                    if self.counts[opp] == 0:
                        self.victory = True
                        idx += 1
                        break

            idx += 1

        if not self.victory or idx == length:
            self.round += 1
            self.positions = sorted(self.positions)

    def viz(self):
        for (i, row) in enumerate(self.arena):
            viz_row = ''
            for (j, entry) in enumerate(row):
                if isinstance(entry, str):
                    e = entry
                else:
                    e = entry.char
                viz_row += e
            print(viz_row)

    def score(self):
        assert self.victory
        hp_sum = 0
        for (i, j) in self.positions:
            hp_sum += self.arena[i][j].hp
        return self.round*hp_sum


@click.command()
@click.argument('puzzle_input', type=click.Path(exists=True))
@click.option('--dark', is_flag=True)
def main(puzzle_input, dark):

    with open(puzzle_input, 'r') as f:
        file = f.read()

    lines = file.split('\n')
    if lines[0] == '':
        lines = lines[1:]
    if lines[-1] == '':
        lines = lines[:-1]

    arena = convert_input(lines)
    game = ElvesvsGoblins(arena)
    if not dark:
        print('Computing answer for part 1...')
        print('---------------------')
        print('Initial layout:')
        print('---------------------')
        game.viz()
        print('---------------------')

    while not game.victory:
        game.next_round()
        if not dark:
            round = game.round
            if round == 1:
                print('After 1 round:')
            else:
                print('After {} rounds:'.format(game.round))
            print('---------------------')
            game.viz()
            print('---------------------')

    ans1 = game.score()
    print("Part 1 solution is:")
    print(ans1)
    print('-------')

    if not dark:
        print('Computing answer for part 2...')

    if game.elf_dead:
        minimum = 3
        maximum = 200
    else:
        minimum = 0
        maximum = 3
    ap = (maximum-minimum)//2
    ans_dict = {}
    while True:
        game = ElvesvsGoblins(arena, elf_save=True, elf_ap=ap)
        if not dark:
            print('Try elf attack power of {}'.format(ap))
        while not game.victory and not game.elf_dead:
            game.next_round()
        if game.elf_dead:
            minimum = ap
            if not dark:
                print('Increase attack power')
                print('-------')
            ap = max((maximum+ap)//2, ap+1)
        else:
            maximum = ap
            ans_dict[ap] = game.score()
            if not dark:
                print('Decrease attack power')
                print('-------')
            ap = min((minimum+ap)//2, ap-1)
        if maximum - minimum == 1:
            ans2 = ans_dict[maximum]
            if not dark:
                print('Elf attack power {} is required'.format(maximum))
                print('-------')
            break

    print("Part 2 solution is:")
    print(ans2)
    print('-------')


if __name__ == '__main__':
    main()
