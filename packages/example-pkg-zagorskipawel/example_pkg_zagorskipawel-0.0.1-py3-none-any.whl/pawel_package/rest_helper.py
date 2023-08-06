""" This is a helper program that lists the requests urls in rows, where n equal to amount of them.
You might need to install the following packages:
(pip install) configparser
(pip install) docopt (Python 2 users might need sudo apt install python3-docopt instead)

Usage:
    rest_helper.py [-n] <int> [-c] <filename>
    rest_helper.py -h | --help

Options:
    -h --help     Show this screen
    -n --num      Define number of rows, must be greater than 0
    -c --config   Define the config file
"""

import sys
from configparser import ConfigParser

from docopt import docopt

if sys.version_info[0] == 3:
    from urllib.parse import urlparse
else:
    from urlparse import urlparse


def load_config_file():
    if args['--config']:
        file = args['<filename>']
        config = ConfigParser()
        config.read(file)
        if not config.has_section('Data' or 'Urls'):
            print("Given config file has no required Data or/and Urls section!")
            print("Please make sure that you provided the right file and that it exists!")
            sys.exit()
        return config


def list_addresses():
    config_file = load_config_file()
    uri_prefix = '://'
    at_sign = '@'
    keys_and_values = list(config_file.items('Urls'))
    username = config_file['Data']['username']
    urlpath = config_file['Data']['urlpath']
    if args['--num']:
        # Checking if given positional argument is an integer
        try:
            # Converting the positional argument num from string to int
            num_rows = int(args['<int>'])
        except ValueError:
            print("-n | --num value has to be a positive integer!")
            sys.exit()
        try:
            # Printing merged strings as final addresses
            for i in range(num_rows):
                link = urlparse(keys_and_values[i][1])
                print("{}{}{}{}{}{}".format(link.scheme, uri_prefix, username, at_sign, link.netloc, urlpath))
        # Informing the user whether the number of desired rows is exceeding existing ones
        except IndexError:
            print("Already printed all of the possible positions!")
            print("-n | --num value is out of range! Max amount of rows is: {}!".format(len(keys_and_values)))


if __name__ == "__main__":
    args = docopt(__doc__)
    list_addresses()
