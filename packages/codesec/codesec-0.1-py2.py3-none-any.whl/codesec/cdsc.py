import argparse
import os
from collections import namedtuple
from configparser import ConfigParser

import pyperclip

# +--------------------------╔====================╗--------------------------+ #
# |::::::::::::::::::::::::::║ Exception Handling ║::::::::::::::::::::::::::| #
# +--------------------------╚====================╝--------------------------+ #


class Error(Exception):
    pass


class InvalidConfig(Error):
    pass


class FileDoesNotExist(InvalidConfig):
    pass


# +----------------------------╔===============╗-----------------------------+ #
# |::::::::::::::::::::::::::::║ Configuration ║:::::::::::::::::::::::::::::| #
# +----------------------------╚===============╝-----------------------------+ #

cpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini")


def load_config() -> ConfigParser:
    config = ConfigParser()
    if not os.path.isfile(cpath):
        raise InvalidConfig(f"Configuration file '{cpath}' is not a file")
    config.read(cpath)
    if not config.has_section("USER"):
        config.add_section("USER")
    return config


def reset():
    config = load_config()
    config["USER"].clear()
    config.update()
    with open(cpath, "w") as file:
        config.write(file)
    print("Reset config")


# +----------------------------╔=================╗---------------------------+ #
# |::::::::::::::::::::::::::::║ Pretty Printing ║:::::::::::::::::::::::::::| #
# +----------------------------╚=================╝---------------------------+ #


def repeat(fill: str, limit: int) -> str:
    count, remainder = divmod(limit, len(fill))
    return fill * count + fill[:remainder]


def format(title: str) -> str:
    Edges = namedtuple("Edges", "top down left right")
    Corners = namedtuple("Corners", "tl tr br bl")

    config = load_config()["USER"]

    # Parse config
    try:
        length = config.getint("length")
    except ValueError as e:
        raise InvalidConfig(e)
    try:
        oc = Corners._make(config.get("outer_corners").split(","))
        oe = Edges._make(config.get("outer_edges").split(","))
        ic = Corners._make(config.get("inner_corners").split(","))
        ie = Edges._make(config.get("inner_edges").split(","))
    except TypeError as e:
        raise InvalidConfig(e)
    center_fill = config.get("center_fill")
    if not center_fill:
        center_fill = " "
    try:
        comm = config.getboolean("comment") * "# "
    except ValueError as e:
        raise InvalidConfig(e)
    tlen = len(title)

    # Top Construction
    limit = length - (2 * len(comm) + len(oc.tl + oc.tr + ic.tl + ic.tr) + (tlen + 2))
    if len(oe.top) > limit:
        raise InvalidConfig("length set too short for title")
    top = repeat(oe.top, limit)
    div = round(len(top) / 2)
    l1 = f"{comm}{oc.tl}{top[:div]}{ic.tl}{repeat(ie.top, tlen+2)}{ic.tr}{top[div:]}{oc.tr}{comm[::-1]}"

    # Mid Construction
    limit = length - (2 * len(comm) + (tlen + 2) + 4)
    if len(center_fill) > limit:
        raise InvalidConfig("center_fill too long for given length")
    fill = repeat(center_fill, limit)
    div = round(len(fill) / 2)
    l2 = (
        f"{comm}{oe.left}{fill[:div]}{ie.left} {title} {ie.right}{fill[div:]}{oe.right}{comm[::-1]}"
    )

    # Bottom Construction
    limit = length - (2 * len(comm) + len(oc.bl + oc.br + ic.bl + ic.br) + (tlen + 2))
    if len(oe.down) > limit:
        raise InvalidConfig("length set too short for title")
    btm = repeat(oe.down, limit)
    div = round(len(btm) / 2)
    l3 = f"{comm}{oc.bl}{btm[:div]}{ic.bl}{repeat(ie.down, tlen+2)}{ic.br}{btm[div:]}{oc.br}{comm[::-1]}"

    return f"{l1}\n{l2}\n{l3}"


# +----------------------------╔===============╗-----------------------------+ #
# |::::::::::::::::::::::::::::║ Program Modes ║:::::::::::::::::::::::::::::| #
# +----------------------------╚===============╝-----------------------------+ #


def copy(title: str) -> str:
    section = format(title)
    pyperclip.copy(section)
    print("Copied:\n" + section)


def print_symbols():
    print(
        """☺ ☻ ♥ ♦ ♣ ♠ • ◘ ○ ◙ ♂ ♀ ♪ ♫ ☼ ► ◄ ↕ ‼ ¶ § ▬ ↨ ↑ ↓ → ← ∟ ↔ \
▲ ▼ ◄ ↕ ‼ ¶ § ▬ ↨ ↑ ↓ → ← ∟ ↔ ▲ ▼ Δ € ƒ „ … † ‡ ˆ ‰ Š ‹ Œ Ž ‘ ’ “ ” • \
– — ˜ ™ › ¡ ¢ £ ¤ ¥ ¦ § ¨ © ª « ¬ ® ¯ ° ± ´ ¶ · ¸ ¹ º » ø ¢ º ⌐ ¬ ¡ \
« » ░ ▒ ▓ │ ┤ ╡ ╢ ╖ ╕ ╣ ║ ╗ ╝ ╜ ╛ ┐ └ ┴ ┬ ├ ─ ┼ ╞ ╟ ╚ ╔ ╩ ╦ ╠ ═ ╬ ╧ ╨ \
╤ ╥ ╙ ╘ ╒ ╓ ╫ ╪ ┘ ┌ █ ▄ ▌ ▐ ▀ Γ π Φ Θ Ω ∞ ∩ ≡ ± ≥ ≤ ⌠ ⌡ ÷ ≈ ° ∙ · √ ■"""
    )


def set_param(setting: str) -> None:
    config = load_config()
    while True:
        print(
            f"\nDefault {setting}: {config['DEFAULT'].get(setting)}\
\nCurrent {setting}: {config['USER'].get(setting)}"
        )
        new_setting = input("Enter setting: ")
        config["USER"][setting] = new_setting
        config.update()
        with open(cpath, "w") as file:
            config.write(file)
        try:
            print("Preview:", format("Section Title"), sep="\n")
            break
        except InvalidConfig as e:
            print(f"\n{e}\nTry again: ")


# +-----------------------------╔==============╗-----------------------------+ #
# |:::::::::::::::::::::::::::::║ Command Line ║:::::::::::::::::::::::::::::| #
# +-----------------------------╚==============╝-----------------------------+ #


def cli():
    config = load_config()
    parser = argparse.ArgumentParser(
        description="Create pretty printed section title for your code"
    )
    parser.add_argument(
        "-s",
        "--set",
        choices=config.defaults().keys(),
        metavar="",
        help=f"configure settings: {', '.join(config.defaults().keys())}",
    )
    parser.add_argument(
        "--symbols", action="store_true", help="prints out common ascii symbols for decoration"
    )
    parser.add_argument("--reset", action="store_true", help="reset config")
    parser.add_argument(
        "title", type=str, default="Section Title", nargs="?", help="title of your section"
    )
    return parser.parse_args()


def main():
    args = cli()
    if args.symbols:
        print_symbols()
    elif args.reset:
        reset()
    elif setting := args.set:
        set_param(setting)
    else:
        copy(args.title)


if __name__ == "__main__":
    main()
