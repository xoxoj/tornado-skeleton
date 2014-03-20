#!/usr/bin/env python3
import optparse
import task
from termcolor import colored
import tornado.util

def main():
    p = optparse.OptionParser()
    options, arguments = p.parse_args()
    try:
        cmd = tornado.util.import_object('task.' + arguments[0])
        return cmd.execute(options, arguments)
    except ImportError:
        print(colored('Command not found', 'red'))
    except IndexError:
        print(colored('Missing command argument', 'yellow'))
        print('Available command: ')
        print(task.available())
  
if __name__ == '__main__':
    exit_code = main()
    if exit_code:
        sys.exit(exit_code)