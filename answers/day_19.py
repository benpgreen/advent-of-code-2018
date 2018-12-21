import click


puzzle_template = """
#ip 3
addi 3 16 3
seti 1 5 1
seti 1 4 4
mulr 1 4 5
eqrr 5 2 5
addr 5 3 3
addi 3 1 3
addr 1 0 0
addi 4 1 4
gtrr 4 2 5
addr 3 5 3
seti 2 6 3
addi 1 1 1
gtrr 1 2 5
addr 5 3 3
seti 1 1 3
mulr 3 3 3
addi 2 2 2
mulr 2 2 2
mulr 3 2 2
muli 2 11 2
addi 5 3 5
mulr 5 3 5
addi 5 3 5
addr 2 5 2
addr 3 0 3
seti 0 6 3
setr 3 8 5
mulr 5 3 5
addr 3 5 5
mulr 3 5 5
muli 5 14 5
mulr 5 3 5
addr 2 5 2
seti 0 2 0
seti 0 2 3
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


def divisor_sum(n):
    s = 0
    for i in range(1, int(n**(1/2)+1)):
        if n % i == 0:
            s += i + n//i
    if n**(1/2) % 1 == 0.0:
        s -= int(n**(1/2))
    return s


def check_part2_template(ip, programs):
    """Checks the puzzle input fits my template."""

    error_msg = "Invalid puzzle input for part 2 solver."
    ip_template, programs_template = read_lines(puzzle_template)
    permutations = {
        ip: ip_template,  # the pointers
        programs[4][1]: programs_template[4][1],  # use the 4th row
        programs[4][2]: programs_template[4][2],
        programs[7][1]: programs_template[7][1],  # use the 7th row
        programs[9][1]: programs_template[9][1],  # use the 9th row
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
        if C0 != permutations[C]:
            raise RuntimeError(error_msg)
        if m[:2] != 'eq' and m[:2] != 'gt':
            if m != 'seti' and A0 != permutations[A]:
                raise RuntimeError(error_msg)
            if m[-1] == 'r' and m != 'setr' and B0 != permutations[B]:
                raise RuntimeError(error_msg)
        else:
            if m[-2] == 'r' and A0 != permutations[A]:
                raise RuntimeError(error_msg)
            if m[-1] == 'r' and B0 != permutations[B]:
                raise RuntimeError(error_msg)


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
    reg = Registers([0, 0, 0, 0, 0, 0], ip)

    while reg.ip_val < len(programs):
        m, A, B, C = programs[reg.ip_val]
        method = getattr(reg, m)
        reg.ip_to_reg()
        method(A, B, C)
        reg.reg_to_ip()

    ans1 = reg.regs[0]
    print("Part 1 solution is:")
    print(ans1)
    print('-------')

    # my solution assume that other inputs of a certain format, check this
    check_part2_template(ip, programs)

    reg = Registers([1, 0, 0, 0, 0, 0], ip)
    while reg.ip_val != 4:
        m, A, B, C = programs[reg.ip_val]
        method = getattr(reg, m)
        reg.ip_to_reg()
        method(A, B, C)
        reg.reg_to_ip()
    d = reg.regs[programs[4][2]]
    ans2 = divisor_sum(d)

    print("Part 2 solution is:")
    print(ans2)
    print('-------')


if __name__ == '__main__':
    main()
