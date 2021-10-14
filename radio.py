# NOTE: This iteration of radio used timeouts, which was vetoed by Liang.
# This file therefore does not contain any logic for playing music and exists only for archival purposes.
# DO NOT USE THIS FILE.

import time
import json
from datetime import datetime


started = False
schedule = json.load(open('hoco_schedule.json'))


# Return seconds to next toggle time if current time < last time stop, None otherwise
def time_to_next_period():
    # Get current schedule
    now = datetime.now()
    try:
        curr_schedule = schedule[now.strftime('%m-%d')]
    except KeyError:
        return print('KeyError - Function most likely invoked on non-hoco day')

    # Flatten and parse schedule
    flattened = [p[k] for p in curr_schedule.values() for k in ['s', 'e']]
    flattened.insert(0, flattened[0] - 60)  # Start playing 1 hour before school
    flattened.append(flattened[-1] + 60)  # Stop playing 1 hour after school

    # Get next period via brainwoke for loop
    curr_seconds = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
    for j in range(len(flattened)):
        arr_seconds = flattened[j] * 60
        if curr_seconds < arr_seconds:
            break
    diff = arr_seconds - curr_seconds
    # print(f'System time is {now}. Next timestop is {flattened[j]} in {diff} seconds')  # Uncomment for debug

    if diff < 0:  # Curr time is after last time stop
        return None
    return diff


def toggle_radio():
    global started
    started = not started
    # Do some logic with the radio thing to volume

    sleep_until_next_toggle()


def sleep_until_next_toggle():
    t = time_to_next_period()
    if t is None:
        return  # Returns if after school, replace with some fancy date switching logic later
    print(f'Next toggle in {t} seconds')
    time.sleep(t)
    toggle_radio()


sleep_until_next_toggle()
