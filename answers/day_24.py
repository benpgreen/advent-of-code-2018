import click


class Group:

    def __init__(self, units, hp, attack_power, attack_type, initiative,
                 weaknesses=None, immunities=None):
        self.units = units
        self.hp = hp
        self.attack_power = attack_power
        self.attack_type = attack_type
        self.initiative = initiative
        if weaknesses is None:
            self.weaknesses = set()
        else:
            self.weaknesses = set(weaknesses)
        if immunities is None:
            self.immunities = set()
        else:
            self.immunities = set(immunities)

    def damage_calc(self, opp):
        if self.attack_type in opp.immunities:
            out = 0
        elif self.attack_type in opp.weaknesses:
            out = 2*(self.units*self.attack_power)
        else:
            out = self.units*self.attack_power
        return out

    def attack(self, opp, verbose=False):
        if self.attack_type in opp.immunities:
            damage = 0
        elif self.attack_type in opp.weaknesses:
            damage = 2*(self.units*self.attack_power)
        else:
            damage = self.units*self.attack_power

        killed = min(damage//opp.hp, opp.units)
        if verbose:
            print('{} units killed'.format(killed))
        opp.units -= killed
        return killed


def read_lines(lines):
    if 'Immune' in lines[0]:
        name = 'immune'
    else:
        name = 'infec'
    out_dict = {name: []}
    line = lines[1]
    ldx = 1
    while line != '':
        line_split = line.split(' ')
        units = int(line_split[0])
        hp = int(line_split[4])

        weaknesses = []
        immunities = []
        if '(' in line:
            left = line.index('(')
            right = line.index(')')
            modifiers = line[left+1:right].replace(',', '').replace(';', '')
            modifiers = modifiers.split(' ')
            if modifiers[0] == 'weak':
                idx = 2
                while idx < len(modifiers) and modifiers[idx] != 'immune':
                    weaknesses.append(modifiers[idx])
                    idx += 1
                idx += 2
                while idx < len(modifiers):
                    immunities.append(modifiers[idx])
                    idx += 1
            elif modifiers[0] == 'immune':
                idx = 2
                while idx < len(modifiers) and modifiers[idx] != 'weak':
                    immunities.append(modifiers[idx])
                    idx += 1
                idx += 2
                while idx < len(modifiers):
                    weaknesses.append(modifiers[idx])
                    idx += 1

        rest = line_split[line_split.index('does')+1:]
        attack_power = int(rest[0])
        attack_type = rest[1]
        initiative = int(rest[-1])
        if len(immunities) == 0:
            immunities = None
        if len(weaknesses) == 0:
            weaknesses = None

        group = Group(units, hp, attack_power, attack_type, initiative,
                      weaknesses=weaknesses, immunities=immunities)
        out_dict[name].append(group)
        ldx += 1
        line = lines[ldx]

    ldx += 1
    if 'Immune' in lines[ldx]:
        name = 'immune'
    else:
        name = 'infec'
    out_dict[name] = []
    ldx += 1
    while ldx < len(lines) and lines[ldx] != '':
        line = lines[ldx]
        line_split = line.split(' ')
        units = int(line_split[0])
        hp = int(line_split[4])

        weaknesses = []
        immunities = []
        if '(' in line:
            left = line.index('(')
            right = line.index(')')
            modifiers = line[left+1:right].replace(',', '').replace(';', '')
            modifiers = modifiers.split(' ')
            if modifiers[0] == 'weak':
                idx = 2
                while idx < len(modifiers) and modifiers[idx] != 'immune':
                    weaknesses.append(modifiers[idx])
                    idx += 1
                idx += 2
                while idx < len(modifiers):
                    immunities.append(modifiers[idx])
                    idx += 1
            elif modifiers[0] == 'immune':
                idx = 2
                while idx < len(modifiers) and modifiers[idx] != 'weak':
                    immunities.append(modifiers[idx])
                    idx += 1
                idx += 2
                while idx < len(modifiers):
                    weaknesses.append(modifiers[idx])
                    idx += 1

        rest = line_split[line_split.index('does')+1:]
        attack_power = int(rest[0])
        attack_type = rest[1]
        initiative = int(rest[-1])
        if len(immunities) == 0:
            immunities = None
        if len(weaknesses) == 0:
            weaknesses = None

        group = Group(units, hp, attack_power, attack_type, initiative,
                      weaknesses=weaknesses, immunities=immunities)
        out_dict[name].append(group)
        ldx += 1
    immunes = out_dict['immune']
    infections = out_dict['infec']
    return immunes, infections


def choose_target(attacker, opponents, chosen):
    damages = []
    for (idx, opp) in enumerate(opponents):
        damage = attacker.damage_calc(opp)
        effective_power = opp.units*opp.attack_power
        damages.append((damage, effective_power, opp.initiative, idx))
    damages = sorted(damages, reverse=True)
    out = None
    for d in damages:
        if d[-1] not in chosen and d[0] > 0:
            out = d[-1]
            break
    return out


def fight(immunes, infections):
    master = [(i.units*i.attack_power, i.initiative, 0, idx)
              for (idx, i) in enumerate(immunes)]
    master += [(i.units*i.attack_power, i.initiative, 1, idx)
               for (idx, i) in enumerate(infections)]
    master = sorted(master, reverse=True)

    attacks = []
    chosens = {0: set(), 1: set()}
    for (_, i, t, idx) in master:
        if t == 0:
            attacker = immunes[idx]
            opponents = infections
        elif t == 1:
            attacker = infections[idx]
            opponents = immunes
        opp_idx = choose_target(attacker, opponents, chosens[t])
        if opp_idx is not None:
            chosens[t].add(opp_idx)
            attacks.append((i, t, idx, opp_idx))

    attacks = sorted(attacks, reverse=True)
    killed_one = False
    for (_, t, idx, opp_idx) in attacks:
        if t == 0:
            attacker = immunes[idx]
            opp = infections[opp_idx]
        elif t == 1:
            attacker = infections[idx]
            opp = immunes[opp_idx]
        killed = attacker.attack(opp, verbose=False)
        if killed > 0:
            killed_one = True

    new_immunes = []
    new_infections = []
    for i in immunes:
        if i.units > 0:
            immunes = []
            new_immunes.append(i)
    for i in infections:
        if i.units > 0:
            new_infections.append(i)
    return new_immunes, new_infections, killed_one


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

    immunes, infections = read_lines(lines)

    while len(immunes) > 0 and len(infections) > 0:
        immunes, infections, _ = fight(immunes, infections)

    if len(immunes) == 0:
        ans1 = sum([i.units for i in infections])
    elif len(infections) == 0:
        ans1 = sum([i.units for i in immunes])
    else:
        raise RuntimeError('Part 1 answer failed to complete.')

    print("Part 1 solution is:")
    print(ans1)
    print('-------')

    boost = 1
    while True:
        immunes_orig, infections = read_lines(lines)
        immunes = []
        for i in immunes_orig:
            i.attack_power += boost
            immunes.append(i)

        killed_one = True

        while len(immunes) > 0 and len(infections) > 0 and killed_one:
            immunes, infections, killed_one = fight(immunes, infections)

        if len(immunes) == 0 or not killed_one:
            boost += 1
        else:
            ans2 = sum([i.units for i in immunes])
            break

    print("Part 2 solution is:")
    print(ans2)


if __name__ == '__main__':
    main()
