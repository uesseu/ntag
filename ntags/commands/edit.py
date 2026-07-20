from subprocess import run
from os import environ
from subprocess import run
from ..lib.dbclass import check_tagjson, find_tagdb_inparents
from ..lib.defaults import DEFAULT_TAGJSON_FNAME, DEFAULT_TAGDB_FNAME


def edit_command():
    run([environ['EDITOR'], check_tagjson(DEFAULT_TAGDB_FNAME, '')])
