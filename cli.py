# encoding: utf-8
"""
CLI for the 'video_logging' module.
"""

import os
import sys
import argparse
try:
    import video_logging as log
except ImportError:
    print("---X This command line tool is an interface to a python module called video_logging. In order to use this tool you must first make sure that this module is available (it currently isn't). The recommended way to do this is to grab the source code video_logging.py and put it in the same directory as this cli.py file. The source code for video_logging is available freely on GitHub at https://github.com/theodumont/video_logging-python.")
    sys.exit(1)


class CLI(object):
    """docstring for CLI."""

    def __init__(self):
        # List of all parameters accepted to trigger the different modes.
        self.change_list = ["change", "cd"]
        self.folder_list = ["folder"]
        self.trash_list = ["trash"]
        self.date_list = ["time", "date"]
        self.help_list = ["help", "h", "?"]
        self.exit_list = ["exit", "e", "leave", "l", "quit", "q"]
        # folder to clean
        self.folder = os.getcwd()

    def read_command(self, command):
        # cursor is used to keep track of how many argument we read from the users command.
        cursor = 0
        split_command = str.split(command)
        if len(split_command) == 0:
            # Empty line, we can just ignore it
            return
        # else ...
        instruction = split_command[0]
        cursor += 1

        if instruction.lower() in self.change_list:
            return self.process_change_dir(split_command, cursor)

        elif instruction.lower() in self.folder_list:
            return self.process_folder()

        elif instruction.lower() in self.trash_list:
            return self.process_trash(split_command, cursor)

        elif instruction.lower() in self.date_list:
            return self.process_date()

        elif instruction.lower() in self.help_list:
            return self.process_help(split_command, cursor)

        elif instruction.lower() in self.exit_list:
            return self.exit()
        else:
            log.bprint(f"The input command {command} could not be parsed, because the tool did not understand the term '{instruction}'. If you wish to you can use :\n'>> help'\nThat instruction will bring a list of the available instruction and their use cases.", 2)
            return

    def exit(self):
        # Used to leave the tool.
        log.bprint("Leaving the tool...")
        sys.exit(0)

    def process_ls(self):
        os.system('dir')

    def process_change_dir(self, split_command, cursor):
        if len(split_command) == cursor:
            # i.e. we have no more arguments available
            log.bprint(f"What folder do you want to clean?", 1)
            log.bprint(f"The syntax to change directory is:\n'>> cd <directory>'")
        else:
            directory = split_command[cursor]
            cursor += 1
            try:
                str_directory = str(directory)
                os.chdir(str_directory)
                self.folder = os.getcwd()
                # display(self)
            except ValueError as e:
                log.bprint(f"The tool could not parse {directory} as a string. The correct syntax to change the directory is :\n'>> cd <directory>'", 2)
                return
            except FileNotFoundError as e:
                log.bprint(f"The tool could not find the {directory} directory. The correct syntax to change the directory is :\n'>> cd <directory>'", 2)
                return

    def process_folder(self):
        log.folder_sort(self.folder)

    def process_trash(self, split_command, cursor):
        if len(split_command) == cursor:
            # i.e. we have no more arguments available
            log.bprint(f"What time limit do you want to impose?", 1)
            log.bprint(f"The syntax to choose the time limit is:\n'>> trash <time limit>'\nTime limit has to be a positive int value.")
        else:
            time_limit = split_command[cursor]
            cursor += 1
            try:
                int_time_limit = int(time_limit)
                if int_time_limit <= 0:
                    log.bprint(f"You asked the tool to take {time_limit} as a time limit, but negative (zero included) values are not valid in that context. Please input a positive integer.", 2)
                    return
                else:
                    log.trash_videos(self.folder, int_time_limit)
            except ValueError as e:
                log.bprint(f"The value of the time_limit has to be a positive int, but the tool could not parse {time_limit} as an int. The correct syntax to choose the time limit is :\n'>> trash <time limit>'", 2)
                return

    def process_date(self):
        log.sort_by_date(self.folder)

    def process_help(self, split_command, cursor):
        if len(split_command) == cursor:
            # i.e. no more arguments to read, just printing command list.
            command_help = (
            "All possible input commands are :\n\n"
            " - change : Changes the current directory. For more information about change, please use 'help change'.\n"
            " - folder : Sorts the current directory files in folders. For more information folder, please use 'help folder'.\n"
            " - trash : \n"
            " - date : \n"
            " - help : Brings out various help message, including this one.\n"
            " - exit : Leaves this tool. If your are using a keyboard you can also use EOF shortcut (Ctrl + D on Linux for instance).\n"
            )
            log.bprint(command_help)
            return
        else:
            topic = split_command[cursor]
            cursor += 1
            if topic in self.exit_list:
                log.bprint("The exit command leaves this tool. If your are using a keyboard you can also use EOF shortcut (Ctrl + D on Linux for instance).")
                return
            elif topic in self.change_list:
                log.bprint("the change command changes the current directory. The syntax to change directory is:\n'>> cd <directory>'")
                return
            elif topic in self.folder_list:
                log.bprint("folder help")
                return
            elif topic in self.trash_list:
                log.bprint("trash help")
                return
            elif topic in self.date_list:
                log.bprint("date help")
                return
            elif topic in self.help_list:
                log.bprint("Why are you here?")
                return


def display(cli):
    header = (
    "\n"
    "##############################################################################\n"
    "  This tool was designed by Théo Dumont and all the source code is available  \n"
    "   at https://github.com/theodumont/video-logging under the GPL 3 License.    \n"
    "##############################################################################\n"
             )
    os.system('cls')
    print(header)


if __name__ == '__main__':
    os.system('cls')
    cli = CLI()

    display(cli)

    while True:
        try:
            log.bprint("", 3)
            log.bprint(cli.folder, 4)
            command = input(">> ")
            cli.read_command(command)
        except EOFError:
            print("exit")  # In order to avoid ugly output
            cli.exit()
            break
