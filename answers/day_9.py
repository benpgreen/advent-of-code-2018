import click


def score_game(players, last_marble):
    scores = {p: 0 for p in range(1, players+1)}
    if last_marble == 0:
        out = 0
    elif last_marble >= 1:
        # store what is to the "left and right" of the key
        circle = {0: [1, 1], 1: [0, 0]}
        current_val = 1
        for turn in range(2, last_marble+1):

            player = ((turn-1) % players)+1

            if turn % 23 != 0:

                left = circle[current_val][1]
                right = circle[left][1]
                circle[turn] = [left, right]
                circle[left][1] = turn
                circle[right][0] = turn
                current_val = turn

            else:

                counter = 0
                left = current_val
                while counter < 7:
                    left = circle[left][0]
                    counter += 1
                scores[player] += turn + left
                new_left, current_val = circle[left]
                del circle[left]
                circle[current_val][0] = new_left
                circle[new_left][1] = current_val

        out = max(scores.values())

    return out


@click.command()
@click.argument('num_players', type=int)
@click.argument('last_marble', type=int)
def main(num_players, last_marble):
    """
    num_players: int
        The number of players in the marble game, should be a positive integer.
    last_marble: int
        The value of the last marble, should be a positive integer.

    """

    score = score_game(num_players, last_marble)
    msg = '{0} players; last marble is worth {1} points: high score is {2}.'
    print(msg.format(num_players, last_marble, score))


if __name__ == '__main__':
    main()
