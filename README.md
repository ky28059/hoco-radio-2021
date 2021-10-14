# hoco radio 2021
Python script for the radio in the Junior float.

Populate the `./music` directory with 2 or more .wav files and run `radio2.py`.
On the Raspberry Pi, replace the relative paths with absolute paths when running it
at boot via `.bashrc`. The fstring on line 25 may also need to be altered (python 3.5 seems to
throw strange syntax errors when attempting to run it).

`hoco_schedule.json` is an altered WATT alternates JSON with 0th and 8th periods removed
to keep the school start and end times at their expected values. The script begins playing music
45 minutes before school, sets volume to 10% during class time, and stops playing music 15 minutes
after school.
