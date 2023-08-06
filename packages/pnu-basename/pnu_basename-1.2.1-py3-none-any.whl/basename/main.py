#!/usr/bin/env python
""" basename, dirname - return filename or directory portion of pathname
License: 3-clause BSD (see https://opensource.org/licenses/BSD-3-Clause)
Author: Hubert Tournier
"""

import getopt
import logging
import re
import os
import sys

# Version string used by the what(1) and ident(1) commands:
ID = "@(#) $Id: basename, dirname - return filename or directory portion of pathname v1.2.1 (September 26, 2021) by Hubert Tournier $"

# Default parameters. Can be superseded by environment variables, then command line options
parameters = {
    "Dirname": False,
    "Multiple": False,
    "Posix": False,
    "Suffix": "",
    "Zero": False,
}


################################################################################
def initialize_debugging(program_name):
    """Debugging set up"""
    console_log_format = program_name + ": %(levelname)s: %(message)s"
    logging.basicConfig(format=console_log_format, level=logging.DEBUG)
    logging.disable(logging.INFO)


################################################################################
def display_help():
    """Displays usage and help"""
    if parameters["Dirname"]:
        print("usage: dirname string", end="", file=sys.stderr)
        if parameters["Posix"]:
            print(file=sys.stderr)
        else:
            print(" [...]", file=sys.stderr)
            print("       dirname [-z|--zero] string [...]", file=sys.stderr)
            print(
                "       dirname [--debug] [--help|-?] [--version] [--]", file=sys.stderr
            )
            print(
                "  ------------------   ---------------------------------------------------",
                file=sys.stderr,
            )
            print(
                "  -z|--zero            End each output line with NUL, not newline",
                file=sys.stderr,
            )
            print("  --debug              Enable debug mode", file=sys.stderr)
            print(
                "  --help|-?            Print usage and this help message and exit",
                file=sys.stderr,
            )
            print("  --version            Print version and exit", file=sys.stderr)
            print(
                "  --                   Options processing terminator", file=sys.stderr
            )
            print(file=sys.stderr)
    else:
        print("usage: basename string [suffix]", file=sys.stderr)
        if not parameters["Posix"]:
            print(
                "       basename [-a|--multiple] [-s|--suffix suffix] [-z|--zero] string [...]",
                file=sys.stderr,
            )
            print(
                "       basename [-d|--dirname] [-a|--multiple] [-z|--zero] string [...]",
                file=sys.stderr,
            )
            print(
                "       basename [--debug] [--help|-?] [--version] [--]",
                file=sys.stderr,
            )
            print(
                "  ------------------   ---------------------------------------------------",
                file=sys.stderr,
            )
            print(
                "  -a|--multiple        Support multiple arguments and treat each as a name",
                file=sys.stderr,
            )
            print(
                "  -d|--dirname         Print the directory component", file=sys.stderr
            )
            print(
                "  -s|--suffix SUFFIX   Remove trailing SUFFIX. Implies -a",
                file=sys.stderr,
            )
            print(
                "  -z|--zero            End each output line with NUL, not newline",
                file=sys.stderr,
            )
            print("  --debug              Enable debug mode", file=sys.stderr)
            print(
                "  --help|-?            Print usage and this help message and exit",
                file=sys.stderr,
            )
            print("  --version            Print version and exit", file=sys.stderr)
            print(
                "  --                   Options processing terminator", file=sys.stderr
            )
            print(file=sys.stderr)


################################################################################
def process_environment_variables():
    """Process environment variables"""
    # pylint: disable=C0103
    global parameters
    # pylint: enable=C0103

    # From "man environ":
    # POSIXLY_CORRECT
    # When set to any value, this environment variable
    # modifies the behaviour of certain commands to (mostly)
    # execute in a strictly POSIX-compliant manner.
    if "POSIXLY_CORRECT" in os.environ.keys():
        parameters["Posix"] = True


################################################################################
def process_command_line():
    """Process command line options"""
    # pylint: disable=C0103
    global parameters
    # pylint: enable=C0103

    # option letters followed by : expect an argument
    # same for option strings followed by =
    character_options = ""
    string_options = []
    if parameters["Posix"]:
        character_options = "?"
        string_options = ["debug", "help", "version"]
    elif parameters["Dirname"]:
        character_options = "z?"
        string_options = ["debug", "help", "version", "zero"]
    else:
        character_options = "ads:z?"
        string_options = [
            "debug",
            "dirname",
            "help",
            "multiple=",
            "suffix=",
            "version",
            "zero",
        ]

    try:
        options, remaining_arguments = getopt.getopt(
            sys.argv[1:], character_options, string_options
        )
    except getopt.GetoptError as error:
        logging.critical(error)
        display_help()
        sys.exit(1)

    for option, argument in options:

        if option in ("-a", "--multiple"):
            parameters["Multiple"] = True

        elif option in ("-d", "--dirname"):
            parameters["Dirname"] = True

        elif option in ("-s", "--suffix"):
            parameters["Suffix"] = argument

        elif option in ("-z", "--zero"):
            parameters["Zero"] = True

        elif option == "--debug":
            logging.disable(logging.NOTSET)

        elif option in ("--help", "-?"):
            display_help()
            sys.exit(0)

        elif option == "--version":
            print(ID.replace("@(" + "#)" + " $" + "Id" + ": ", "").replace(" $", ""))
            sys.exit(0)

    logging.debug("process_command_line(): parameters:")
    logging.debug(parameters)
    logging.debug("process_command_line(): remaining_arguments:")
    logging.debug(remaining_arguments)

    return remaining_arguments


################################################################################
def basename(pathname):
    """Do basename processing on a pathname"""

    # First stripping trailing slashes:
    # Regular Expression means slash character, 0 to N times (*), at the end of the string ($)
    pathname = re.sub(re.escape(os.sep) + "*$", "", pathname)

    # If string consists entirely of slash characters, string shall be set to a single slash
    # character:
    if not pathname:
        return os.sep

    # Delete any prefix ending with the last slash character present in string:
    # Regular Expression means any character (.), 0 to N times (*), till a slash character
    pathname = re.sub(".*" + re.escape(os.sep), "", pathname)

    # Delete the suffix unless if it is identical to the remaining characters in string:
    if pathname != parameters["Suffix"]:
        # A non-existent suffix is ignored.
        # Regular Expression means the suffix string, at the end of the string ($)
        pathname = re.sub(re.escape(parameters["Suffix"]) + "$", "", pathname)

    return pathname


################################################################################
def dirname(pathname):
    """Do dirname processing on a pathname"""

    # Step 1: If string is //, skip steps 2 to 5:
    if pathname != os.sep + os.sep:
        # Step 2: If string consists entirely of <slash> characters, string shall be set to a
        # single <slash> character:
        # Regular Expression means from the beginning (^), slash character, 1 to N times (+),
        # till the end of the string ($)
        pathname = re.sub("^" + re.escape(os.sep) + "+$", os.sep, pathname)
        if pathname == os.sep:
            return pathname

        # Step 3: If there are any trailing <slash> characters in string, they shall be removed
        # Regular Expression means slash character, 0 to N times (*), at the end of the string ($)
        pathname = re.sub(re.escape(os.sep) + "*$", "", pathname)

        # Step 4: If there are no <slash> characters remaining in string, string shall be set to
        # single <period> character:
        if os.sep not in pathname:
            return os.curdir

        # Step 5: If there are any trailing non- <slash> characters in string, they shall be
        # removed:
        # Regular Expression means non slash character 0 to N times ([^/]), at the end of the
        # string ($)
        pathname = re.sub("[^" + re.escape(os.sep) + "]*$", "", pathname)

    # Step 6: If there are any trailing <slash> characters in string, they shall be removed
    # (same as step 3):
    pathname = re.sub(re.escape(os.sep) + "*$", "", pathname)

    # Step 7: If the remaining string is empty, string shall be set to a single <slash> character:
    if not pathname:
        return os.sep

    return pathname


################################################################################
def print_pathname(pathname):
    """print() wrapper to handle the zero option"""
    if parameters["Zero"]:
        sys.stdout.buffer.write(bytes(pathname, encoding="utf8"))
        sys.stdout.buffer.write(bytes([0x00]))
    else:
        print(pathname)


################################################################################
def main():
    """The program's main entry point"""
    program_name = os.path.basename(sys.argv[0])
    if program_name == "dirname":
        parameters["Dirname"] = True

    initialize_debugging(program_name)
    process_environment_variables()
    arguments = process_command_line()

    if len(arguments) == 0:
        display_help()
        sys.exit(1)

    if parameters["Dirname"] and parameters["Posix"] and len(arguments) > 1:
        logging.critical("POSIX compatibility requires a single argument")
        display_help()
        sys.exit(1)

    # If -a is specified, then every argument is treated as a string as if basename were invoked
    # with just one argument. If -s is specified, then the suffix is taken as its argument, and all
    # other arguments are treated as a string
    if (
        len(arguments) == 2
        and not parameters["Multiple"]
        and parameters["Suffix"] == ""
        and not parameters["Dirname"]
    ):
        parameters["Suffix"] = arguments[1]
        print_pathname(basename(arguments[0]))
    elif parameters["Dirname"]:
        for argument in arguments:
            print_pathname(dirname(argument))
    else:
        for argument in arguments:
            print_pathname(basename(argument))

    sys.exit(0)


if __name__ == "__main__":
    main()
