
from akl import alogging


def on_module_import():
    alogging.default_setup('akl')


on_module_import()
