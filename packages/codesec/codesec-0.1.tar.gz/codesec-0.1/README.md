# codesec

## Installation
```
$ pip install codesec
```
### Dependencies
Python dependencies included during pip install:
- `pyperclip`

No other dependencies on Windows and Mac OS.

Other systems may need to install `xclip` or `xsel` packages

## Usage
``` 
usage: codesec [-h] [-s] [--symbols] [--reset] [title]

Create pretty printed section title for your code

positional arguments:
  title        title of your section

optional arguments:
  -h, --help   show this help message and exit
  -s , --set   configure settings: length, outer_corners, inner_corners,
               outer_edges, inner_edges, center_fill, comment
  --symbols    prints out common ascii symbols for decoration
  --reset      reset config
```

### Example:

```bash
$ codesec --set length

Default length: 80
Current length: 80
Enter setting: 50
Preview:
# +--------------╔===============╗-------------+ #
# |::::::::::::::║ Section Title ║:::::::::::::| #
# +--------------╚===============╝-------------+ #

$ codesec --set inner_edges

Default inner_edges: =,=,║,║
Current inner_edges: =,=,║,║
Enter setting: ≡+,≡+,►,◄
Preview:
# +--------------╔≡+≡+≡+≡+≡+≡+≡+≡╗-------------+ #
# |::::::::::::::► Section Title ◄:::::::::::::| #
# +--------------╚≡+≡+≡+≡+≡+≡+≡+≡╝-------------+ #

$ codesec "My Section"

Copied:
# +---------------╔≡+≡+≡+≡+≡+≡+╗---------------+ #
# |:::::::::::::::► My Section ◄:::::::::::::::| #
# +---------------╚≡+≡+≡+≡+≡+≡+╝---------------+ #
```