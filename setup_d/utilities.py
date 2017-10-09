# File: setup_d/utilities.py

import os
import shutil

from books.src.config import DEFAULTS as D

file_name = os.path.join(D["home"], D["last_entity"])
# the file containing the name of the last used or default entity.

def restore_virgin_data_directory():
    """
    Deletes all local data and restores the data directory
    to a 'virginal' state.  Depends on the presence of a default
    chart of accounts in a location specified by config.DEFAULTS.
    """
    try:
        shutil.rmtree(D["home"])
    except OSError:
        print("Directory '{}' wasn't there to delete."
            .format(D["home"]))
    os.mkdir(D["home"])
    shutil.copy(os.path.join(D["virgin_home"], D["cofa_template"]),
        D["home"])
    with open(file_name, 'w') as f_obj:
        f_obj.write('')


def save_local_data():
    """
    Used to save local data and create a fresh data directory
    for testing.  After testing use restore_local_data().
    """
    os.rename(D["home"], D["temp_home"])
    os.mkdir(D["home"])
    with open(file_name, 'w') as f_obj:
        f_obj.write('')
    shutil.copy(
        os.path.join(D['virgin_home'], D['cofa_template']),
        D['home'])

def restore_local_data():
    """
    Used to return things as they were before testing.
    Returns things to what they were before save_local_data() is
    called.
    """
    shutil.rmtree(D["home"])
    os.rename(D["temp_home"], D["home"])
