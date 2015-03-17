#!/usr/bin/python3
# Add a new task to the gtimelog log file.
# Propose a list of task if only the category is supplied
#
# Copyright (c) 2006 Canonical Ltd.
# Author: Louis Bouchard <louis.bouchard@ubuntu.com>
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.  See http://www.gnu.org/copyleft/gpl.html for
# the full text of the license.

import re, sys, time

LogFile='~/.local/share/gtimelog/timelog.txt'

Categories = {
    'ua': 'L3 / L3 support',
    'up': 'Upstream',
    'ubu': 'Upstream Ubuntu',
    'meet': 'Internal meetings',
    'pers': 'Personal management',
    'skill': 'Skills building',
    'know': 'Knowledge transfer',
    'team': 'Team support'
    }


def show_help():
    return("Categories : {}".format(sorted(list(Categories.keys()))))

def select_ua_tasks():
    cases = []
    regex = re.compile(r'L3 / L3 support')
    with open(LogFile, 'r') as timelog:
        for line in timelog:
            if regex.findall(line):
                case = regex.split(line)[-1].strip()
                if case.lstrip(": ") not in cases:
                    cases.append(case.lstrip(": "))
    for I in cases:
        print("{}) {}".format(cases.index(I)+1,I))

def log_activity(category, task=None):

    now = time.localtime()
    shortlogformat = '{:04d}-{:02d}-{:02d} {:02d}:{:02d}: {}\n'
    longlogformat = '{:04d}-{:02d}-{:02d} {:02d}:{:02d}: {} : {}\n'

    with open(LogFile, 'a') as timelog:
        if task is None:
            timelog.write(shortlogformat.format(
                now.tm_year, now.tm_mon, now.tm_mday,
                now.tm_hour, now.tm_min, category))
        else:
            task_string = " ".join(task)
            if category in Categories.keys():
                timelog.write(longlogformat.format(
                    now.tm_year, now.tm_mon, now.tm_mday,
                    now.tm_hour, now.tm_min, Categories[category],
                    task_string))
            else:
                timelog.write(longlogformat.format(
                    now.tm_year, now.tm_mon, now.tm_mday,
                    now.tm_hour, now.tm_min, category, task_string))
    return(0)

if __name__ == '__main__':
    try:
        if len(sys.argv) == 1:
            raise ValueError

        if len(sys.argv) == 2:
            if sys.argv[1] == '?':
                print("{}".format(show_help()))
                sys.exit(0)
            elif sys.argv[1] == 'new':
                log_activity('new', 'Arrived')
            elif sys.argv[1] == 'ua':
                select_ua_tasks()
                sys.exit(0)
            else:
                log_activity(sys.argv[1])
        else:

            log_activity(sys.argv[1], sys.argv[3:])
        sys.exit(0)

    except ValueError:
        print("Missing Argument")
        sys.exit(1)
