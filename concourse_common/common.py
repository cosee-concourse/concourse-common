import json
import os
import sys
import tempfile

from jsonschema import Draft4Validator
from colorama import Fore


def check_system_argument_number():
    if len(sys.argv) < 2:
        log_error("Wrong number of arguments!")
        return False
    return True


def join_paths(*paths):
    return os.path.join(*paths)

def log(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def log_error(message):
    log(Fore.RED + str(message))


def log_warning(message):
    log(Fore.YELLOW + str(message))
    log(Fore.RED)


def log_info(message):
    log(Fore.WHITE + str(message))
    log(Fore.RED)


def validate_path(file_path):
    try:
        file_stream = open(file_path, 'r')
        file_stream.close()
        return True
    except IOError:
        return False