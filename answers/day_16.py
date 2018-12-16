import click


METHOD_NAMES = [
            'addi',
            'addr',
            'bani',
            'banr',
            'bori',
            'borr',
            'eqir',
            'eqri',
            'eqrr',
            'gtir',
            'gtri',
            'gtrr',
            'muli',
            'mulr',
            'seti',
            'setr'
]


def read_lines(lines):
    length = len(lines)
    idx = 0
    samples = []
    sample = {}
    programs = []
    while idx < length:
        line = lines[idx]
        if len(line) > 0 and line[0] == 'B':
            start = line.index('[')
            end = line.index(']')
            sample['B'] = eval(line[start:end+1])

            idx += 1
            line = lines[idx]
            sample['O'] = [int(n) for n in line.split(' ')]

            idx += 1
            line = lines[idx]
            start = line.index('[')
            end = line.index(']')
            sample['A'] = eval(line[start:end+1])

            samples.append(sample)
            sample = {}
            idx += 2
        elif len(line) == 0:
            idx += 2
        else:
            programs.append([int(n) for n in line.split(' ')])
            idx += 1

    return samples, programs


class Registers:

    def __init__(self, registers):
        self.regs = registers.copy()

    def addr(self, A, B, C):
        """adding register A and register B"""
        self.regs[C] = self.regs[A] + self.regs[B]

    def addi(self, A, B, C):
        """adding register A and value B"""
        self.regs[C] = self.regs[A] + B

    def mulr(self, A, B, C):
        """multiplying register A and register B"""
        self.regs[C] = self.regs[A]*self.regs[B]

    def muli(self, A, B, C):
        """multiplying register A and value B"""
        self.regs[C] = self.regs[A]*B

    def banr(self, A, B, C):
        """bitwise AND of register A and register B"""
        self.regs[C] = self.regs[A] & self.regs[B]

    def bani(self, A, B, C):
        """bitwise AND of register A and value B"""
        self.regs[C] = self.regs[A] & B

    def borr(self, A, B, C):
        """bitwise OR of register A and register B"""
        self.regs[C] = self.regs[A] | self.regs[B]

    def bori(self, A, B, C):
        """bitwise OR of register A and value B"""
        self.regs[C] = self.regs[A] | B

    def setr(self, A, B, C):
        """returns register A (Input B is ignored)"""
        self.regs[C] = self.regs[A]

    def seti(self, A, B, C):
        """returns value A (Input B is ignored)"""
        self.regs[C] = A

    def gtir(self, A, B, C):
        """1 if value A is greater than register B. Otherwise, 0"""
        self.regs[C] = int(A > self.regs[B])

    def gtri(self, A, B, C):
        """1 if register A is greater than value B. Otherwise,  0"""
        self.regs[C] = int(self.regs[A] > B)

    def gtrr(self, A, B, C):
        """1 if register A is greater than register B. Otherwise, 0"""
        self.regs[C] = int(self.regs[A] > self.regs[B])

    def eqir(self, A, B, C):
        """1 if value A is equal to register B. Otherwise, 0"""
        self.regs[C] = int(A == self.regs[B])

    def eqri(self, A, B, C):
        """1 if register A is equal to value B. Otherwise, 0"""
        self.regs[C] = int(self.regs[A] == B)

    def eqrr(self, A, B, C):
        """1 if register A is equal to register B. Otherwise, 0"""
        self.regs[C] = int(self.regs[A] == self.regs[B])


def get_possible_opcodes(sample):
    methods = set()
    op_num, A, B, C = sample['O']
    for method_name in METHOD_NAMES:
        reg = Registers(sample['B'])
        method = getattr(reg, method_name)
        method(A, B, C)
        if reg.regs == sample['A']:
            methods.add(method_name)
    return (op_num, methods)


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

    samples, programs = read_lines(lines)

    possibles = {i: set(METHOD_NAMES) for i in range(16)}
    ans1 = 0
    for sample in samples:
        op_num, methods = get_possible_opcodes(sample)
        if len(methods) >= 3:
            ans1 += 1
        possibles[op_num] = possibles[op_num].intersection(methods)

    print("Part 1 solution is:")
    print(ans1)
    print('-------')

    methods = set(range(16))
    op_map = {}
    while len(methods) > 0:
        to_remove = set()
        for m in methods:
            val = possibles[m]
            if len(val) == 1:
                to_remove.add(m)
                op_map[m] = list(val)[0]
                for i in range(16):
                    if i != m:
                        possibles[i] = possibles[i].difference(val)
        methods = methods.difference(to_remove)

    register = Registers([0, 0, 0, 0])
    for (op, A, B, C) in programs:
        method = getattr(register, op_map[op])
        method(A, B, C)

    ans2 = register.regs[0]
    print("Part 2 solution is:")
    print(ans2)


if __name__ == '__main__':
    main()
