#!/usr/bin/python3
import re, sys

#LogFile='~/.local/share/gtimelog/timelog.txt'
LogFile='~/timelog.txt'

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
    # Return help
    if category == '?':
        return(sorted(Categories.keys()))

    if category == 'new':
        return('Arrived')
    else:
        return(category)

if __name__ == '__main__':
    try:
        if len(sys.argv) == 1:
            raise ValueError

        if len(sys.argv) == 2:
            if sys.argv[1] == '?':
                print("{}".format(show_help()));
                
            log_activity(sys.argv[1])
            sys.exit(0)

    except ValueError:
        print("Missing Argument")
        sys.exit(1)
