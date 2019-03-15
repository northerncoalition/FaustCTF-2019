#!/usr/bin/env python
import threading
import atexit
from swpag_client import *
from prettytable import PrettyTable

TEAM_TOKEN = ""
TEAM_ID = ""

GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

team = Team("http://api.ictf2019.net/", TEAM_TOKEN)

i = 0

def set_interval(f, time):
    def wrapper():
        set_interval(f, time)
        f()
    t = threading.Timer(time, wrapper)
    t.deamon = True
    t.start()

def print_status():
    global i
    i = (i + 1) % 10
    print("iCTF Status Dashboard [{}]".format(i))

    try:
        status = team.get_game_status()

    except RuntimeError, e:
        print(e)
        print("\x13\033[3A")
        return

    service_states = status["service_states"][TEAM_ID]

    table = PrettyTable()
    table.add_column("", ["status"])

    should_beep = False
    for service in service_states.values():
        state = service["service_state"]

        if state == "up":
            color = GREEN
        elif state == "down":
            color = RED
            should_beep = True
        else:
            color = RESET

        value = "{}{}{}".format(color, state, RESET)
        table.add_column(service["service_name"], [value])

    print(table)

    tick = status["tick"]
    print("Round time remaining: {}".format(tick["approximate_seconds_left"]))
    
    if should_beep:
        print("\7\033[1A") # COMMENT THIS LINE TO SHUT THE ALARM DOWN LOL

    print("\x13\033[8A")

print("\033[?25l")
print_status()
set_interval(print_status, 1)

def show_cursor():
    print("\033[?25h")

atexit.register(show_cursor)
