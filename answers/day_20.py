import click
import networkx as nx

from collections import defaultdict


class Tree:

    def __init__(self, string):
        self.string = string
        self.current_node = 0
        self.max_id = 0
        self.tree = {0: {'points': [(0, 0)], 'branches': []}}
        self.parents = {}
        self.coords = defaultdict(lambda: '#')
        self.coords[(0, 0)] = 'X'

    def create_tree(self):
        for s in self.string:
            if s == '(':  # create a branch
                self.max_id += 1
                self.tree[self.current_node]['branches'].append(self.max_id)
                parent_points = self.tree[self.current_node]['points']
                self.parents[self.max_id] = self.current_node
                self.current_node = self.max_id
                self.tree[self.current_node] = {
                                'points': parent_points,
                                'branches': []
                                }
            elif s == ')':  # move back up the tree
                self.current_node = self.parents[self.current_node]
                points = []
                for branch in self.tree[self.current_node]['branches']:
                    points.extend(self.tree[branch]['points'])
            elif s == '|':  # create a new branch on the same parent
                self.max_id += 1
                parent_id = self.parents[self.current_node]
                parent_points = self.tree[parent_id]['points']
                self.tree[parent_id]['branches'].append(self.max_id)
                self.parents[self.max_id] = parent_id
                self.current_node = self.max_id
                self.tree[self.current_node] = {
                                'points': parent_points,
                                'branches': []
                                }
            else:
                new_points = []
                for point in self.tree[self.current_node]['points']:
                    new_point = self.walk_path(s, point)
                    new_points.append(new_point)
                self.tree[self.current_node]['points'] = new_points
        # in case this has been overwritten
        self.coords[(0, 0)] = 'X'

    def walk_path(self, s, pos):
        x, y = pos
        if s == 'N':
            self.coords[(x-1, y)] = '-'
            self.coords[(x-2, y)] = '.'
            x += -2
        elif s == 'S':
            self.coords[(x+1, y)] = '-'
            self.coords[(x+2, y)] = '.'
            x += 2
        elif s == 'E':
            self.coords[(x, y+1)] = '|'
            self.coords[(x, y+2)] = '.'
            y += 2
        elif s == 'W':
            self.coords[(x, y-1)] = '|'
            self.coords[(x, y-2)] = '.'
            y += -2
        else:
            raise ValueError('Invalid input: {}'.format(s))
        return (x, y)

    def visualize(self):
        X = [x for x, _ in self.coords.keys()]
        Y = [y for _, y in self.coords.keys()]

        x_min = min(X)
        x_max = max(X)
        y_min = min(Y)
        y_max = max(Y)

        array = []
        for x in range(x_min-1, x_max+2):
            row = []
            for y in range(y_min-1, y_max+2):
                row.append(self.coords[(x, y)])
            array.append(row)
        return array


def get_graph(array):
    G = nx.Graph()
    for (i, row) in enumerate(array[1:-1]):
        i = i + 1
        for (j, entry) in enumerate(row[1:-1]):
            j = j + 1
            if entry == '.' or entry == 'X':
                G.add_node((i, j))
                if entry == 'X':
                    start = (i, j)
                if array[i+1][j] == '-':
                    G.add_edge((i, j), (i+2, j))
                if array[i-1][j] == '-':
                    G.add_edge((i, j), (i-2, j))
                if array[i][j+1] == '|':
                    G.add_edge((i, j), (i, j+2))
                if array[i][j-1] == '|':
                    G.add_edge((i, j), (i, j-2))
    return G, start


@click.command()
@click.argument('puzzle_input', type=click.Path(exists=True))
def main(puzzle_input):

    with open(puzzle_input, 'r') as f:
        puzzle = f.read()

    puzzle = puzzle.replace('\n', '')
    puzzle = puzzle.replace(' ', '')
    puzzle = puzzle[1:-1]

    tree = Tree(puzzle)
    tree.create_tree()
    array = tree.visualize()
    G, start = get_graph(array)

    ans1 = nx.eccentricity(G, start)

    print("Part 1 solution is:")
    print(ans1)
    print('-------')

    ans2 = len(G.nodes()) - len(nx.ego_graph(G, start, radius=999).nodes())
    print("Part 2 solution is:")
    print(ans2)


if __name__ == '__main__':
    main()
