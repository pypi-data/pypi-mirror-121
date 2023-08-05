import os


def get_version():
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "VERSION")
    if os.path.isfile(path):
        with open(path) as f:
            return f.read().strip()
    return '0.0.0'


__version__ = get_version()
