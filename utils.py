import os

# get absolute path to mids folder
def get_mids_path():
    return os.path.join(os.path.dirname(__file__), "mids")


# get absolute bath to mid file
def get_mid_path(name):
    return os.path.join(get_mids_path(), name)


# get all midi files in mids folderr
def get_midi_files():
    midies = []
    for midi in os.listdir(get_mids_path()):
        if midi.endswith(".mid"):
            midies.append(midi)

    return midies
