import click
import string
import copy

from collections import defaultdict


def run(reqs, letters, workers=5, base_time=60):
    times = {
        letter: string.ascii_uppercase.index(letter) + 1 + base_time
        for letter in letters
    }
    t = 0
    remaining = letters.copy()
    req = copy.deepcopy(reqs)
    running = {}
    worker_count = workers
    finished = set()

    while len(finished) < len(letters):
        queue = []
        for letter in remaining:
            if len(req[letter]) == 0:
                queue.append(letter)

        while worker_count > 0 and len(queue) > 0:
            letter = queue[0]
            running[letter] = times[letter]
            worker_count -= 1
            remaining.remove(letter)
            queue = queue[1:]

        to_remove = []
        for key in running.keys():
            running[key] -= 1
            if running[key] == 0:
                finished.add(key)
                worker_count += 1
                to_remove.append(key)
        for letter in to_remove:
            del running[letter]
            for key in req.keys():
                if letter in req[key]:
                    req[key].remove(letter)

        t += 1
    return t


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

    reqs = defaultdict(set)
    letters = set()
    for line in lines:
        split_line = line.split(" ")
        letters.update({split_line[1], split_line[7]})
        reqs[split_line[7]].add(split_line[1])
    letters = sorted(list(letters))

    remaining = letters.copy()
    reqs_copy = copy.deepcopy(reqs)
    ans1 = ""
    while len(remaining) > 0:

        for letter in remaining:
            if len(reqs_copy[letter]) == 0:
                ans1 += letter
                for key in reqs_copy.keys():
                    if letter in reqs_copy[key]:
                        reqs_copy[key].remove(letter)
                break
        remaining.remove(letter)

    print("Part 1 solution is:")
    print(ans1)
    print("-------")

    ans2 = run(reqs, letters)
    print("Part 2 solution is:")
    print(ans2)


if __name__ == "__main__":
    main()
