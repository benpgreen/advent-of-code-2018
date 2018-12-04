import click
import numpy as np
import pandas as pd

from collections import defaultdict


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

    df_dict = {'guard_id': [], 'action': []}
    times = []

    for line in lines:
        rb_idx = line.index(']')

        dt_time = line[1:rb_idx]
        date, time = dt_time.split(' ')
        year, month, day = date.split('-')
        hour, minute = time.split(':')
        times.append(pd.datetime(
                        int(year), int(month), int(day),
                        int(hour), int(minute)
                                ))

        remaining = line[rb_idx+2:].split(' ')
        action = remaining[0]
        if action == 'Guard':
            guard_id = int(remaining[1][1:])
            act = 'C'
        elif action == 'wakes':
            guard_id = None
            act = 'W'
        else:
            guard_id = None
            act = 'S'

        df_dict['guard_id'].append(guard_id)
        df_dict['action'].append(act)

    df = pd.DataFrame(df_dict, index=times).sort_index()
    df['guard_id'] = df['guard_id'].fillna(method='ffill')

    guards = []
    asleep_times = []
    asleep_minutes = []
    asleep_minute_counts = []

    for guard_id, group in df.groupby('guard_id'):
        counts = defaultdict(int)
        sleeps = group[group['action'] == 'S'].index.values
        wakes = group[group['action'] == 'W'].index.values
        time_asleep = (wakes-sleeps).sum()
        for (i, sl) in enumerate(sleeps):
            sl_min = sl.minute
            wk_min = wakes[i].minute
            for j in range(sl_min, wk_min):
                counts[j] += 1

        guards.append(guard_id)
        max_count = 0
        for key, val in counts.items():
            if val > max_count:
                most_slept_min = key
                max_count = val
        asleep_minutes.append(most_slept_min)
        asleep_minute_counts.append(max_count)
        if not isinstance(time_asleep, (int, float)):
            time_asleep = time_asleep.days*24*60+time_asleep.seconds//60
        asleep_times.append(time_asleep)

    ai1 = np.argmax(asleep_times)
    ans1 = int(asleep_minutes[ai1]*guards[ai1])

    ai2 = np.argmax(asleep_minute_counts)
    ans2 = int(asleep_minutes[ai2]*guards[ai2])

    print("Part 1 solution is:")
    print(ans1)
    print('-------')
    print("Part 2 solution is:")
    print(ans2)


if __name__ == '__main__':
    main()
