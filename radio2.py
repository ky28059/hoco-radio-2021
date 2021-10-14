import time
import json
from datetime import datetime
from os import walk
from random import randrange
from pygame import mixer

is_passing = False
with open('hoco_schedule.json') as f:
    schedule = json.load(f)

(_, _, filenames) = next(walk('./music'))
queue = []  # An array of filenames that houses the remaining songs to play
curr = None  # The filename of the currently playing song, so that it doesn't get played twice
mixer.init()


# Load and play a song from the remaining songs in the queue
def play_random_song_from_queue():
    # Add all files except currently playing song back to queue when it becomes empty
    if len(queue) == 0:
        queue.extend(filter(lambda x: x != curr, filenames))
    index = randrange(len(queue))

    print(f"Playing {queue[index]}: position {index + 1} of {len(queue)}")
    mixer.music.load('./music/' + queue[index])
    mixer.music.play()

    global curr
    curr = queue[index]
    queue.pop(index)  # Remove the song from queue so it doesn't get replayed


warn_message_sent = False

# Tick every 1/2 second
while True:
    # Get current schedule
    now = datetime.now()
    is_passing = True  # Whether it is passing period or before/after school

    try:
        curr_schedule = schedule[now.strftime('%m-%d')]

        # Flatten, parse
        # Sort values because the pi is not on python 3.6+
        flattened = sorted([[p['s'], p['e']] for p in curr_schedule.values()], key=lambda x: x[0])
        curr_minutes = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds() / 60

        # Don't play if more than 45 minutes before school or 15 minutes after
        if flattened[0][0] - curr_minutes >= 45 or curr_minutes - flattened[-1][1] > 15:
            if mixer.music.get_busy():
                mixer.music.fadeout(7500)  # Fade out over 7.5 seconds
            time.sleep(0.5)
            continue

        for [s, e] in flattened:
            if s <= curr_minutes <= e:
                is_passing = False
                break
    except KeyError:
        if not warn_message_sent:  # Perhaps a better approach for only sending these logs once exists, but this works
            print('[WARN] KeyError - Function most likely invoked on non-hoco day')
            print('[WARN] Fallback will play music at max volume')
            warn_message_sent = True

    # Music logic
    if not mixer.music.get_busy():  # If the music player is idle, queue another track
        play_random_song_from_queue()
    # Adjust right float as needed to determine how quiet it should be during class
    mixer.music.set_volume(1.0 if is_passing else 0.1)

    time.sleep(0.5)
