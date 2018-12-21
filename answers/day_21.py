import click


puzzle_template = """
#ip 3
seti 123 0 4
bani 4 456 4
eqri 4 72 4
addr 4 3 3
seti 0 0 3
seti 0 9 4
bori 4 65536 2
seti 6152285 4 4
bani 2 255 1
addr 4 1 4
bani 4 16777215 4
muli 4 65899 4
bani 4 16777215 4
gtir 256 2 1
addr 1 3 3
addi 3 1 3
seti 27 4 3
seti 0 3 1
addi 1 1 5
muli 5 256 5
gtrr 5 2 5
addr 5 3 3
addi 3 1 3
seti 25 9 3
addi 1 1 1
seti 17 4 3
setr 1 9 2
seti 7 4 3
eqrr 4 0 1
addr 1 3 3
seti 5 6 3
""".split('\n')[1:-1]


def read_lines(lines):
    ip = int(lines[0][-1])
    programs = []
    for line in lines[1:]:
        line_split = line.split(' ')
        row = [line_split[0]]
        row.extend([int(v) for v in line_split[1:]])
        programs.append(row)
    return ip, programs


class Registers:

    def __init__(self, registers, ip_reg):
        self.regs = registers.copy()
        self.ip_reg = ip_reg
        self.ip_val = 0

    def ip_to_reg(self):
        self.regs[self.ip_reg] = self.ip_val

    def reg_to_ip(self):
        self.ip_val = self.regs[self.ip_reg]
        self.ip_val += 1

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


def check_template(ip, programs):
    """Checks the puzzle input fits my template."""

    error_msg = "Invalid puzzle input for solver."
    ip_template, programs_template = read_lines(puzzle_template)
    permutations = {
        ip_template: ip,  # the pointers
        programs_template[0][3]: programs[0][3],  # use the 1st row
        programs_template[8][1]: programs[8][1],  # use the 8th row
        programs_template[8][3]: programs[8][3],  # use the 8th row
        programs_template[19][1]: programs[19][1],  # use the 8th row
    }
    if set(permutations.keys()) != {1, 2, 3, 4, 5}:
        raise RuntimeError(error_msg)
    if set(permutations.values()) != {1, 2, 3, 4, 5}:
        raise RuntimeError(error_msg)

    permutations[0] = 0

    for (idx, (m, A, B, C)) in enumerate(programs):
        m0, A0, B0, C0 = programs_template[idx]
        if m0 != m:
            raise RuntimeError(error_msg)
        if permutations[C0] != C:
            raise RuntimeError(error_msg)
        if m[:2] != 'eq' and m[:2] != 'gt':
            if m != 'seti' and permutations[A0] != A:
                raise RuntimeError(error_msg)
            if m[-1] == 'r' and m != 'setr' and permutations[B0] != B:
                raise RuntimeError(error_msg)
        else:
            if m[-2] == 'r' and permutations[A0] != A:
                raise RuntimeError(error_msg)
            if m[-1] == 'r' and permutations[B0] != B:
                raise RuntimeError(error_msg)
    return permutations


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

    ip, programs = read_lines(lines)

    # my solution assume that other inputs of a certain format, check this
    perm = check_template(ip, programs)

    reg = Registers([1, 0, 0, 0, 0, 0], ip)

    log = set()
    while reg.ip_val < len(programs):
        if reg.ip_val == 18:
            reg.regs[perm[1]] = reg.regs[perm[2]]//256
        m, A, B, C = programs[reg.ip_val]
        method = getattr(reg, m)
        reg.ip_to_reg()
        method(A, B, C)
        reg.reg_to_ip()
        if reg.ip_val == 28:
            tup = tuple(reg.regs)
            if len(log) == 0:
                ans1 = tup[perm[4]]
                log.add(ans1)
            elif tup[perm[4]] in log:
                break
            else:
                ans2 = tup[perm[4]]
                log.add(ans2)

    print("Part 1 solution is:")
    print(ans1)
    print('-------')

    print("Part 2 solution is:")
    print(ans2)
    print('-------')


if __name__ == '__main__':
    main()
