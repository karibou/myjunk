#!/usr/bin/python3
import re, sys, time

# LogFile='~/.local/share/gtimelog/timelog.txt'
LogFile = './timelog.txt'

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
            else:
                log_activity(sys.argv[1])
        else:
            log_activity(sys.argv[1], sys.argv[3:])
        sys.exit(0)

    except ValueError:
        print("Missing Argument")
        sys.exit(1)
