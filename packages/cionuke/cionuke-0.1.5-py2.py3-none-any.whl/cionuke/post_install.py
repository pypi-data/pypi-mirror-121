"""
Set up Nuke so it can see the Conductor installation.

Companion calls this module automatically after installation.

It writes stuff into the files menu.py and init.py
"""
import os
import sys
import errno

# /users/me/Conductor/cionuke
PKG_DIR = os.path.dirname(os.path.abspath(__file__))
# /users/me/Conductor/cionuke/conductor_menu.py
CIO_MENU = os.path.join(PKG_DIR, "conductor_menu.py")
CIO_DIR = os.path.dirname(PKG_DIR)  # /users/me/Conductor
PKGNAME = os.path.basename(PKG_DIR)  # cionuke
NUKE_HOME_PATH = os.path.expanduser("~/.nuke/")  # /Users/me/.nuke/
SUFFIX = "# Added by Conductor\n"


def main():
    """
    Write Conductor stuff to Nuke's init.py and menu.py.
    """
    menu_file = os.path.join(NUKE_HOME_PATH, "menu.py")
    init_file = os.path.join(NUKE_HOME_PATH, "init.py")

    init_file_lines = [
        "import sys",
        "sys.path.append(\"{}\")".format(CIO_DIR)
    ]
    menu_file_lines = [
        "import sys",
        "try:",
        "\twith open(\"{}\") as infile:".format(CIO_MENU),
        "\t\texec(infile.read())",
        "except IOError:",
        "\tsys.stderr.write(\"Cant load Conductor Menu file {}\")".format(
            CIO_MENU)
    ]

    ensure_directory(NUKE_HOME_PATH)

    replace_conductor_lines(init_file, init_file_lines)
    replace_conductor_lines(menu_file, menu_file_lines)

    sys.stdout.write("Added conductor setup commands to \"{}\" and \"{}\"!\n".format(
        menu_file, init_file))

    sys.stdout.write("Completed Nuke setup!\n")


def replace_conductor_lines(filename, new_lines):
    """
    Replace previous Conductor lines with new Conductor lines.

    Conductor lines are identified by the suffix: # Added by Conductor
    """
    try:
        with open(filename, "r") as f:
            lines = [line for line in f.readlines() if line.strip() and not line.endswith(SUFFIX)]
    except IOError:
        lines = []

    with open(filename, "w") as f:
        for line in lines:
            f.write(line)
        f.write("\n\n")
        for line in new_lines:
            f.write("{} {}".format(line, SUFFIX))


def ensure_directory(directory):
    try:
        os.makedirs(directory)
    except OSError as ex:
        if ex.errno == errno.EEXIST and os.path.isdir(directory):
            pass
        else:
            raise


if __name__ == '__main__':
    main()
