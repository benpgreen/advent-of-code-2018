import click


def manhatten(p, q):
    return abs(p[0] - q[0]) + abs(p[1] - q[1])


def get_boundary_points(puzzle):
    point0 = puzzle[0]
    x_min = point0[0]
    x_max = x_min
    y_min = point0[1]
    y_max = y_min
    memory = {
        "x_min": [point0],
        "y_min": [point0],
        "x_max": [point0],
        "y_max": [point0],
    }
    for (x, y) in puzzle[1:]:
        if x == x_min:
            memory["x_min"].append((x, y))
        elif x < x_min:
            memory["x_min"] = [(x, y)]
            x_min = x

        if x == x_max:
            memory["x_max"].append((x, y))
        elif x > x_max:
            memory["x_max"] = [(x, y)]
            x_max = x

        if y == y_min:
            memory["y_min"].append((x, y))
        elif y < y_min:
            memory["y_min"] = [(x, y)]
            y_min = y

        if y == y_max:
            memory["y_max"].append((x, y))
        elif y > y_max:
            memory["y_max"] = [(x, y)]
            y_max = y

    X_sort = sorted(puzzle)
    Y_sort = sorted(puzzle, key=lambda x: x[1])

    # x_min
    for (x, y) in X_sort:
        add = True
        current = memory["x_min"]
        for (b0, b1) in current:
            if x - b0 >= abs(y - b1):
                add = False
                break
        if add:
            memory["x_min"].append((x, y))

    # y_min
    for (x, y) in Y_sort:
        add = True
        current = memory["y_min"]
        for (b0, b1) in current:
            if y - b1 >= abs(x - b0):
                add = False
                break
        if add:
            memory["y_min"].append((x, y))

    # x_max
    for (x, y) in X_sort[::-1]:
        add = True
        current = memory["x_max"]
        for (b0, b1) in current:
            if b0 - x >= abs(y - b1):
                add = False
                break
        if add:
            memory["x_max"].append((x, y))

    # y_max
    for (x, y) in Y_sort[::-1]:
        add = True
        current = memory["y_max"]
        for (b0, b1) in current:
            if b1 - y >= abs(x - b0):
                add = False
                break
        if add:
            memory["x_min"].append((x, y))

    output = set()
    for val in memory.values():
        output.update(set(val))

    return output


def get_max_area(puzzle, inf_points=None):
    if inf_points is not None:
        remove = set(inf_points)
    else:
        remove = set()
    point_dict = {p: 0 for p in puzzle if p not in remove}

    X = []
    Y = []
    for (x, y) in puzzle:
        X.append(x)
        Y.append(y)
    x_min = min(X)
    x_max = max(X)
    y_min = min(Y)
    y_max = max(Y)

    for i in range(x_min, x_max + 1):
        for j in range(y_min, y_max + 1):
            best_dist = manhatten(puzzle[0], (i, j))
            best_point = puzzle[0]
            for p in puzzle[1:]:
                new_dist = manhatten(p, (i, j))
                if new_dist < best_dist:
                    best_dist = new_dist
                    best_point = p
                elif new_dist == best_dist:
                    best_point = None
            if best_point is not None and best_point not in remove:
                point_dict[best_point] += 1
    return max(point_dict.values())


def check_distance(point, puzzle, cut=10000):
    i = 0
    total = 0
    n = len(puzzle)
    while i < n and total < cut:
        total += manhatten(puzzle[i], point)
        i += 1
    if total < cut:
        out = 1
    else:
        out = 0
    return out


def get_distance(point, puzzle):
    i = 0
    total = 0
    n = len(puzzle)
    while i < n:
        total += manhatten(puzzle[i], point)
        i += 1
    return total


def adjust_end(dist, cut, length):
    out = 0
    d = dist
    while d < cut:
        out += 1
        d += length
    return out


def count_close_points(puzzle, cut=10000):

    X = []
    Y = []
    for (x, y) in puzzle:
        X.append(x)
        Y.append(y)
    x_min = min(X)
    x_max = max(X)
    y_min = min(Y)
    y_max = max(Y)

    # initialisation
    xl_dist = get_distance((x_min, y_max), puzzle)
    xh_dist = get_distance((x_max, y_max), puzzle)
    for y in range(y_min, y_max):
        l_new = get_distance((x_min, y), puzzle)
        h_new = get_distance((x_max, y), puzzle)
        if l_new < xl_dist:
            xl_dist = l_new
        if h_new < xh_dist:
            xh_dist = h_new

    yl_dist = get_distance((x_max, y_min), puzzle)
    yh_dist = get_distance((x_max, y_max), puzzle)
    for x in range(x_min, x_max):
        l_new = get_distance((x, y_min), puzzle)
        h_new = get_distance((x, y_max), puzzle)
        if l_new < yl_dist:
            yl_dist = l_new
        if h_new < yh_dist:
            yh_dist = h_new

    p_len = len(puzzle)
    x_min -= adjust_end(xl_dist, cut, p_len)
    y_min -= adjust_end(yl_dist, cut, p_len)
    x_max += adjust_end(xh_dist, cut, p_len)
    y_max += adjust_end(xh_dist, cut, p_len)

    total = 0
    for i in range(x_min, x_max + 1):
        for j in range(y_min, y_max + 1):
            point = (i, j)
            total += check_distance(point, puzzle, cut=cut)
    return total


@click.command()
@click.argument("puzzle_input", type=click.Path(exists=True))
def main(puzzle_input):

    with open(puzzle_input, "r") as f:
        file = f.read()

    lines = file.split("\n")
    if lines[0] == "":
        lines = lines[1:]
    if lines[-1] == "":
        lines = lines[:-1]

    puzzle = []
    for line in lines:
        x, y = line.split(",")
        x = int(x)
        y = int(y)
        puzzle.append((x, y))

    puzzle_boundary = get_boundary_points(puzzle)
    ans1 = get_max_area(puzzle, inf_points=puzzle_boundary)

    print("Part 1 solution is:")
    print(ans1)
    print("-------")

    ans2 = count_close_points(puzzle)
    print("Part 2 solution is:")
    print(ans2)


if __name__ == "__main__":
    main()
