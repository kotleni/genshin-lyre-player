import json, os, sys
from utils import *
from player.LyrePlayer import *

def generate_config():
    print('Generating config')
    files = get_midi_files()
    songs = []
    i = 0
    for file in files:
        songs.append({"key": f'{i + 1}', "file": get_mid_path(file)})
        i += 1
    config = { "WARNING!":"DON'T EDIT THIS FILE, IT'S GENERATE AUTO AFTER RESTART", "songs": songs }
    hjson = json.dumps(config, indent=4)
    with open(DEFAULT_CONFIG_FILE_PATH, 'w') as f:
        f.write(hjson)


if __name__ == "__main__":
    if not os.path.exists("mids"):
        os.mkdir("mids")
        print("Mids folder created. Place .mid files in ./mids and restart.")
        sys.exit(0)
    generate_config()
    LyrePlayer(DEFAULT_CONFIG_FILE_PATH).start()
