#!/usr/bin/env python
import threading
import atexit
from swpag_client import *
from prettytable import PrettyTable

TEAM_TOKEN = ""

GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

team = Team("http://api.ictf2019.net/", TEAM_TOKEN)

try:
    TEAM_ID = team.get_team_status()["team_id"]
except RuntimeError:
    print("could not fetch team status")
    exit()

i = 0

def set_interval(f, time):
    def wrapper():
        set_interval(f, time)
        f()
    t = threading.Timer(time, wrapper)
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
    pwned_states = status["exploited_services"]

    table = PrettyTable()
    table.add_column("", ["status", "pwned"])

    should_beep = False
    for service_id in service_states.keys():
        state = service_states[service_id]["service_state"]
        pwned = any(lambda x: x["team_id"] == TEAM_ID, pwned_states[service_id]["teams"])

        if state == "up":
            color = GREEN
        elif state == "down":
            color = RED
            should_beep = True
        else:
            color = RESET

        value = "{}{}{}".format(color, state, RESET)
        pwned_value = "{}{}{}".format(RED if pwned else GREEN, "yes" if pwned else "no", RESET)
        table.add_column(service["service_name"], [value, pwned_value])

    print(table)

    if "tick" in status:
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
