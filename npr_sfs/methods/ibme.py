
"""Usage: ibme.py <input> [-h] [-o output] [--quiet]

<input>      Input image.
-h --help    Show help.
-o output    Output file.
--quiet      No GUI, [default: False]

"""
from docopt import docopt

if __name__ == '__main__':
    args = docopt(__doc__)
    print args