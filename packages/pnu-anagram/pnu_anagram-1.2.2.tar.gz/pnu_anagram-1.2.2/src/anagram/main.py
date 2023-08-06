#!/usr/bin/env python
""" anagram - rearrange letters to form new words
License: 3-clause BSD (see https://opensource.org/licenses/BSD-3-Clause)
Author: Hubert Tournier
"""

import getopt
import logging
import os
import sys
import time

# Version string used by the what(1) and ident(1) commands:
ID = "@(#) $Id: anagram - rearrange letters to form new words v1.2.2 (September 26, 2021) by Hubert Tournier $"

# Default parameters. Can be overcome by environment variables, then command line options
parameters = {
    "Path": [],
    "Dictionary": "",
    "Length": [],
}


################################################################################
def _initialize_debugging(program_name):
    """Debugging set up"""
    console_log_format = program_name + ": %(levelname)s: %(message)s"
    logging.basicConfig(format=console_log_format, level=logging.DEBUG)
    logging.disable(logging.INFO)


################################################################################
def _display_help():
    """Displays usage and help"""
    print("usage: anagram [--debug] [--help|-?] [--version]", file=sys.stderr)
    print("       [-d|--dictionary PATH] [-f|--files] [-l|--length NUMBERS]", file=sys.stderr)
    print("       [--] [LETTERS]", file=sys.stderr)
    print(
        "  --------------------  ---------------------------------------------------",
        file=sys.stderr
    )
    print(
        "  -d|--dictionary PATH  Dictionary's pathname if you don't want the default",
        file=sys.stderr
    )
    print(
        "  -f|--files            Print possible dictionary files in the DICTPATH",
        file=sys.stderr
    )
    print(
        "  -l|--length NUMBERS   Requested anagrams lengths if you want intermediate",
        file=sys.stderr
    )
    print(
        "                        sizes. NUMBERS is a number or a comma separated",
        file=sys.stderr
    )
    print(
        "                        list of numbers or dash separated number intervals",
        file=sys.stderr
    )
    print("  --debug               Enable debug mode", file=sys.stderr)
    print("  --help|-?             Print usage and this help message and exit", file=sys.stderr)
    print("  --version             Print version and exit", file=sys.stderr)
    print("  --                    Options processing terminator", file=sys.stderr)
    print(
        "  LETTERS               The letters allowed, taken from the command line or",
        file=sys.stderr
    )
    print("                        standard input if missing", file=sys.stderr)
    print(file=sys.stderr)


################################################################################
def _process_environment_variables():
    """Process environment variables"""
    if "ANAGRAM_DEBUG" in os.environ.keys():
        logging.disable(logging.NOTSET)

    if "DICTPATH" in os.environ.keys():
        for directory in os.environ["DICTPATH"].split(os.pathsep):
            if os.path.isdir(directory):
                parameters["Path"].append(directory)
            else:
                logging.warning('DICTPATH directory "%s" not found', directory)
        if len(parameters["Path"]) == 0:
            logging.critical("None of the directories specified in DICTPATH found")
            sys.exit(1)
    else:
        if os.name == "posix":
            if os.path.isdir("/usr/share/dict"):
                parameters["Path"].append("/usr/share/dict")
            if os.path.isdir("/usr/local/share/dict"):
                parameters["Path"].append("/usr/local/share/dict")
            if "HOME" in os.environ.keys():
                home = os.environ["HOME"]
                if os.path.isdir(home + os.sep + ".local/share/dict"):
                    parameters["Path"].append(home + os.sep + ".local/share/dict")

        elif os.name == "nt":
            appdata_path = os.sep + "appdata" + os.sep + "roaming"
            pnu_dictpath = os.sep + "python" + os.sep + "share" + os.sep + "dict"
            if os.environ["APPDATA"]:
                pnu_dictpath = os.environ["APPDATA"] + pnu_dictpath
            elif os.environ["HOMEPATH"]:
                pnu_dictpath = os.environ["HOMEPATH"] + appdata_path + pnu_dictpath
            elif os.environ["USERPROFILE"]:
                pnu_dictpath = os.environ["USERPROFILE"] + appdata_path + pnu_dictpath
            if os.path.isdir(pnu_dictpath):
                parameters["Path"].append(pnu_dictpath)

            pnu_dictpath2 = sys.base_prefix + os.sep + "share" + os.sep + "dict"
            if os.path.isdir(pnu_dictpath2):
                parameters["Path"].append(pnu_dictpath2)

    # Setting the default dictionary, if any:
    # (the first one named words)
    for directory in parameters["Path"]:
        if os.path.isfile(directory + os.sep + "words"):
            parameters["Dictionary"] = directory + os.sep + "words"
            break

    if "ANAGRAM_DICT" in os.environ.keys():
        if os.path.isfile(os.environ["ANAGRAM_DICT"]):
            parameters["Dictionary"] = os.environ["ANAGRAM_DICT"]
        else:
            logging.critical("Dictionary pathname doesn't exist: %s", os.environ["ANAGRAM_DICT"])
            sys.exit(1)


################################################################################
def _list_dictionaries():
    """Print the list of files in the DICTPATH"""
    print("Possible dictionaries in these directories / files:", file=sys.stderr)
    for directory in parameters["Path"]:
        print("    " + directory + os.sep, file=sys.stderr)
        for item in os.listdir(directory):
            if os.path.isfile(directory + os.sep + item):
                print("        " + item, file=sys.stderr)


################################################################################
def _get_number(length):
    """Read a number in the lengths specification"""
    try:
        value = int(length)
    except ValueError:
        logging.critical("Lengths list is invalid")
        sys.exit(1)

    if value < 1:
        logging.critical("Length value must be strictly positive: %d", value)
        sys.exit(1)

    return value


################################################################################
def _parse_numbers_list(lengths):
    """Expands the lengths specification to a list of numbers"""
    numbers_list = []

    for item in lengths.split(","):
        if "-" in item:
            subitems = item.split("-")

            if len(subitems) != 2:
                logging.critical("Lengths interval is invalid: %s", item)
                sys.exit(1)

            value1 = _get_number(subitems[0])
            value2 = _get_number(subitems[1])
            if value1 >= value2:
                logging.critical("Lengths interval values must be strictly ascending: %s", item)
                sys.exit(1)

            for value in range(value1, value2 + 1):
                if value not in numbers_list:
                    numbers_list.append(value)

        else:
            value = _get_number(item)
            if value not in numbers_list:
                numbers_list.append(value)

    return sorted(numbers_list)


################################################################################
def _process_command_line():
    """Process command line options"""
    # pylint: disable=C0103
    global parameters
    # pylint: enable=C0103

    # option letters followed by : expect an argument
    # same for option strings followed by =
    character_options = "d:fl:?"
    string_options = [
        "debug",
        "dictionary=",
        "files",
        "help",
        "length=",
        "version",
    ]

    try:
        options, remaining_arguments = getopt.getopt(
            sys.argv[1:], character_options, string_options
        )
    except getopt.GetoptError as error:
        logging.critical("Syntax error: %s", error)
        _display_help()
        sys.exit(1)

    for option, argument in options:

        if option == "--debug":
            logging.disable(logging.NOTSET)

        elif option in ("-d", "--dictionary"):
            if os.path.isfile(argument):
                parameters["Dictionary"] = argument
            else:
                logging.critical("Dictionary pathname doesn't exist: %s", argument)
                sys.exit(1)

        elif option in ("-f", "--files"):
            _list_dictionaries()
            sys.exit(0)

        elif option in ("--help", "-?"):
            _display_help()
            sys.exit(0)

        elif option in ("-l", "--length"):
            parameters["Length"] = _parse_numbers_list(argument)

        elif option == "--version":
            print(ID.replace("@(" + "#)" + " $" + "Id" + ": ", "").replace(" $", ""))
            sys.exit(0)

    logging.debug("_process_command_line(): parameters:")
    logging.debug(parameters)
    logging.debug("_process_command_line(): remaining_arguments:")
    logging.debug(remaining_arguments)

    return remaining_arguments


################################################################################
def _load_dictionary(dictionary, lengths):
    """Load the words of the required lengths from the chosen dictionary"""
    time_start = time.time()
    words = {}
    for length in lengths:
        words[length] = []

    with open(dictionary, "r", encoding='utf-8') as file:
        for word in file.readlines():
            word = word.strip()
            length = len(word)
            if length in lengths:
                # We don't care about dupes. It's way more quicker!
                words[length].append(word)

    time_stop = time.time()
    logging.debug("_load_dictionary() time: %f", time_stop - time_start)

    return words


################################################################################
def _search_anagrams(letters, lengths, words):
    """Search anagrams of the required lengths and letters from the loaded words"""
    time_start = time.time()
    anagrams = []
    for length in lengths:
        for word in words[length]:
            match = True
            allowed_letters = list(letters)
            for letter in word:
                if letter not in allowed_letters:
                    match = False
                    break
                allowed_letters.remove(letter)
            if match:
                if word not in anagrams:
                    anagrams.append(word)

    time_stop = time.time()
    logging.debug("_search_anagrams() time: %f", time_stop - time_start)

    return anagrams


################################################################################
def anagram(letters, lengths, dictionary):
    """Return a list of anagrams of required lengths and letters from a dictionary"""
    if not letters \
    or not dictionary:
        return []

    if not lengths:
        lengths = [len(letters)]
    words = _load_dictionary(dictionary, lengths)

    return _search_anagrams(letters, lengths, words)


################################################################################
def main():
    """The program's main entry point"""
    program_name = os.path.basename(sys.argv[0])

    _initialize_debugging(program_name)
    _process_environment_variables()
    arguments = _process_command_line()

    if arguments:
        letters = arguments[0]
    else:
        letters = input("Letters: ")

    if len(letters) == 0:
        logging.critical("No letters, no anagram...")
        sys.exit(1)

    if not parameters["Dictionary"]:
        logging.critical("No dictionary found!")
        _list_dictionaries()
        print("Then either select one:", file=sys.stderr)
        print("- with the -d option", file=sys.stderr)
        print("- or with the ANAGRAM_DICT environment variable", file=sys.stderr)
        sys.exit(1)

    length = 0
    for word in anagram(letters, parameters["Length"], parameters["Dictionary"]):
        if len(word) != length:
            if length:
                print()
            length = len(word)
            print(str(length) + " letters words: ", end="")
        print(word + " ", end="")
    print()

    sys.exit(0)


if __name__ == "__main__":
    main()
