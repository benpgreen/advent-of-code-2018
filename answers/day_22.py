import click
import networkx as nx


def get_risk_scores(depth, target, additional=100):
    X_max, Y_max = target
    geo_indexes = {(0, 0): 0, target: 0}
    for x in range(1, X_max+1+additional):
        if (x, 0) != target:
            geo_indexes[(x, 0)] = x*16807 % 20183
    for y in range(1, Y_max+1+additional):
        if (x, 0) != target:
            geo_indexes[(0, y)] = y*48271 % 20183

    for x in range(1, X_max+1+additional):
        for y in range(1, Y_max+1+additional):
            if (x, y) != target:
                num = ((geo_indexes[(x-1, y)]+depth) *
                       (depth+geo_indexes[(x, y-1)]))
                geo_indexes[(x, y)] = num % 20183
    geo_indexes[target] = 0

    total_score = 0
    scores = {}
    for key, value in geo_indexes.items():
        e_level = (value + depth) % 20183
        score = (e_level % 3)
        if key[0] <= target[0] and key[1] <= target[1]:
            total_score += score
        scores[key] = score
    return total_score, scores


def get_graph(scores, target, additional=100):
    G = nx.Graph()
    x_targ, y_targ = target

    for y in range(y_targ+1+additional):
        for x in range(x_targ+1+additional):
            current_score = scores[(x, y)]
            if current_score == 0:
                G.add_edge((x, y, 'T'), (x, y, 'C'), weight=7)
            elif current_score == 1:
                G.add_edge((x, y, 'N'), (x, y, 'C'), weight=7)
            elif current_score == 2:
                G.add_edge((x, y, 'T'), (x, y, 'N'), weight=7)
            else:
                raise RuntimeError('')
            if x < x_targ+additional:
                next_score = scores[(x+1, y)]
                x0, y0 = x+1, y
                if current_score == 0 and next_score == 0:
                    G.add_edge((x, y, 'T'), (x0, y0, 'T'), weight=1)
                    G.add_edge((x, y, 'C'), (x0, y0, 'C'), weight=1)
                elif current_score == 0 and next_score == 1:
                    G.add_edge((x, y, 'C'), (x0, y0, 'C'), weight=1)
                elif current_score == 0 and next_score == 2:
                    G.add_edge((x, y, 'T'), (x0, y0, 'T'), weight=1)
                elif current_score == 1 and next_score == 0:
                    G.add_edge((x, y, 'C'), (x0, y0, 'C'), weight=1)
                elif current_score == 1 and next_score == 1:
                    G.add_edge((x, y, 'N'), (x0, y0, 'N'), weight=1)
                    G.add_edge((x, y, 'C'), (x0, y0, 'C'), weight=1)
                elif current_score == 1 and next_score == 2:
                    G.add_edge((x, y, 'N'), (x0, y0, 'N'), weight=1)
                elif current_score == 2 and next_score == 0:
                    G.add_edge((x, y, 'T'), (x0, y0, 'T'), weight=1)
                elif current_score == 2 and next_score == 1:
                    G.add_edge((x, y, 'N'), (x0, y0, 'N'), weight=1)
                elif current_score == 2 and next_score == 2:
                    G.add_edge((x, y, 'T'), (x0, y0, 'T'), weight=1)
                    G.add_edge((x, y, 'N'), (x0, y0, 'N'), weight=1)
            if x > 0:
                next_score = scores[(x-1, y)]
                x0, y0 = x-1, y
                if current_score == 0 and next_score == 0:
                    G.add_edge((x, y, 'T'), (x0, y0, 'T'), weight=1)
                    G.add_edge((x, y, 'C'), (x0, y0, 'C'), weight=1)
                elif current_score == 0 and next_score == 1:
                    G.add_edge((x, y, 'C'), (x0, y0, 'C'), weight=1)
                elif current_score == 0 and next_score == 2:
                    G.add_edge((x, y, 'T'), (x0, y0, 'T'), weight=1)
                elif current_score == 1 and next_score == 0:
                    G.add_edge((x, y, 'C'), (x0, y0, 'C'), weight=1)
                elif current_score == 1 and next_score == 1:
                    G.add_edge((x, y, 'N'), (x0, y0, 'N'), weight=1)
                    G.add_edge((x, y, 'C'), (x0, y0, 'C'), weight=1)
                elif current_score == 1 and next_score == 2:
                    G.add_edge((x, y, 'N'), (x0, y0, 'N'), weight=1)
                elif current_score == 2 and next_score == 0:
                    G.add_edge((x, y, 'T'), (x0, y0, 'T'), weight=1)
                elif current_score == 2 and next_score == 1:
                    G.add_edge((x, y, 'N'), (x0, y0, 'N'), weight=1)
                elif current_score == 2 and next_score == 2:
                    G.add_edge((x, y, 'T'), (x0, y0, 'T'), weight=1)
                    G.add_edge((x, y, 'N'), (x0, y0, 'N'), weight=1)
            if y < y_targ + additional:
                next_score = scores[(x, y+1)]
                x0, y0 = x, y+1
                if current_score == 0 and next_score == 0:
                    G.add_edge((x, y, 'T'), (x0, y0, 'T'), weight=1)
                    G.add_edge((x, y, 'C'), (x0, y0, 'C'), weight=1)
                elif current_score == 0 and next_score == 1:
                    G.add_edge((x, y, 'C'), (x0, y0, 'C'), weight=1)
                elif current_score == 0 and next_score == 2:
                    G.add_edge((x, y, 'T'), (x0, y0, 'T'), weight=1)
                elif current_score == 1 and next_score == 0:
                    G.add_edge((x, y, 'C'), (x0, y0, 'C'), weight=1)
                elif current_score == 1 and next_score == 1:
                    G.add_edge((x, y, 'N'), (x0, y0, 'N'), weight=1)
                    G.add_edge((x, y, 'C'), (x0, y0, 'C'), weight=1)
                elif current_score == 1 and next_score == 2:
                    G.add_edge((x, y, 'N'), (x0, y0, 'N'), weight=1)
                elif current_score == 2 and next_score == 0:
                    G.add_edge((x, y, 'T'), (x0, y0, 'T'), weight=1)
                elif current_score == 2 and next_score == 1:
                    G.add_edge((x, y, 'N'), (x0, y0, 'N'), weight=1)
                elif current_score == 2 and next_score == 2:
                    G.add_edge((x, y, 'T'), (x0, y0, 'T'), weight=1)
                    G.add_edge((x, y, 'N'), (x0, y0, 'N'), weight=1)
            if y > 0:
                next_score = scores[(x, y-1)]
                x0, y0 = x, y-1
                if current_score == 0 and next_score == 0:
                    G.add_edge((x, y, 'T'), (x0, y0, 'T'), weight=1)
                    G.add_edge((x, y, 'C'), (x0, y0, 'C'), weight=1)
                elif current_score == 0 and next_score == 1:
                    G.add_edge((x, y, 'C'), (x0, y0, 'C'), weight=1)
                elif current_score == 0 and next_score == 2:
                    G.add_edge((x, y, 'T'), (x0, y0, 'T'), weight=1)
                elif current_score == 1 and next_score == 0:
                    G.add_edge((x, y, 'C'), (x0, y0, 'C'), weight=1)
                elif current_score == 1 and next_score == 1:
                    G.add_edge((x, y, 'N'), (x0, y0, 'N'), weight=1)
                    G.add_edge((x, y, 'C'), (x0, y0, 'C'), weight=1)
                elif current_score == 1 and next_score == 2:
                    G.add_edge((x, y, 'N'), (x0, y0, 'N'), weight=1)
                elif current_score == 2 and next_score == 0:
                    G.add_edge((x, y, 'T'), (x0, y0, 'T'), weight=1)
                elif current_score == 2 and next_score == 1:
                    G.add_edge((x, y, 'N'), (x0, y0, 'N'), weight=1)
                elif current_score == 2 and next_score == 2:
                    G.add_edge((x, y, 'T'), (x0, y0, 'T'), weight=1)
                    G.add_edge((x, y, 'N'), (x0, y0, 'N'), weight=1)
    return G


@click.command()
@click.argument('depth', type=int)
@click.argument('x_target', type=int)
@click.argument('y_target', type=int)
@click.option(
        '--additional', type=int, default=100,
        help='The additional range to explore to make the graph.'
        )
def main(depth, x_target, y_target, additional):

    ans1, scores = get_risk_scores(depth, (x_target, y_target),
                                   additional=additional)

    print("Part 1 solution is:")
    print(ans1)
    print('-------')

    G = get_graph(scores, (x_target, y_target), additional=additional)
    ans2 = nx.dijkstra_path_length(G, (0, 0, 'T'), (x_target, y_target, 'T'))
    print("Part 2 solution is:")
    print(ans2)


if __name__ == '__main__':
    main()
