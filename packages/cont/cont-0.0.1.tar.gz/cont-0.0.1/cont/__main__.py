"""Naval Fate.

Usage:
    cont (-h | --help)
    cont --version
    cont download <image_url>
    cont (run|start) <image_url>
    cont info
    cont setup [--force]

Options:
    -h --help     Show this screen.
    --version     Show version.

"""
from docopt import docopt
from .version import version
from .info import print_info
from .setup import Setup

if __name__ == "__main__":
    arguments = docopt(__doc__, version=version)
    if arguments["info"]:
        print_info()
    if arguments["setup"]:
        Setup().setup()
