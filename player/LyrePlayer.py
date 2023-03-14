import asyncio
import json
import os
import time
import mido
import pynput.keyboard
from typing import List
from player.NoteKeyMap import NoteKeyMap
from player.SongConfig import SongConfig
from utils import *

START_COMBO_KEY = [pynput.keyboard.Key.tab]
STOP_KEY_COMBO = [pynput.keyboard.Key.space]
RELOAD_CONFIG_KEY = pynput.keyboard.KeyCode.from_char('`')  # todo: remove
DEFAULT_CONFIG_FILE_PATH = "midi_config.json"

def default_if_invalid(config, name, type_check, default):
    return config[name] if name in config and isinstance(config[name], type_check) else default

class LyrePlayer:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.always_reload = False
        self.song_key_dict = None

        self.load_config()

        self.playing_event_loop = asyncio.get_event_loop()
        self.cur_pressed_keys = set()
        self.play_task_active = False

    def load_config(self):
        with open(self.config_path) as config_file:
            config_json = json.load(config_file)

        self.always_reload = False

        self.song_key_dict = dict()
        for song_config in config_json["songs"]:
            if "key" in song_config and type(song_config["key"]) == str and len(song_config["key"]) == 1 and "file" in song_config:
                if os.path.exists(song_config["file"]):
                    self.song_key_dict[pynput.keyboard.KeyCode.from_char(song_config["key"])] = SongConfig(song_config)
                    print(f"{song_config['key']} - {os.path.basename(song_config['file'])}")
                else:
                    print(f'Midi file {os.path.basename(song_config["file"])} is not loaded')

        print(f"loaded {len(self.song_key_dict)} songs from config!")

    @staticmethod
    def auto_root_key_map(mid: mido.midifiles.midifiles.MidiFile, channels: List[int], tracks: List[int],
                          lowest: int, highest: int, use_count: bool):
        # collect notes
        note_count = {}
        for i, track in enumerate(mid.tracks):
            if len(tracks) == 0 or i in tracks:
                for msg in track:
                    if msg.type == "note_on" and (len(channels) == 0 or msg.channel in channels):
                        if msg.note not in note_count:
                            note_count[msg.note] = 1
                        else:
                            note_count[msg.note] += 1

        if not note_count:
            print("0 notes found! did you forget to change the filters?")
            return NoteKeyMap(0)

        # count notes
        notes = sorted(note_count.keys())
        best_key_map = None
        best_root = None
        best_hits = -1
        total = 0
        for cur_root in range(max(notes[0] - 24, 0), min(notes[-1] + 25, 128)):
            cur_key_map = NoteKeyMap(cur_root)
            cur_note_hits = 0
            cur_total = 0
            for note, count in note_count.items():
                if lowest <= note < highest:
                    if cur_key_map.get_key(note):
                        cur_note_hits += count if use_count else 1
                    cur_total += count if use_count else 1

            if cur_note_hits > best_hits:
                best_hits = cur_note_hits
                total = cur_total
                best_key_map = cur_key_map
                best_root = cur_root

        print(f"auto root found root at {best_root} with {best_hits}/{total} ({best_hits / total})")
        return best_key_map

    async def play(self, song_config: SongConfig):
        keyboard = pynput.keyboard.Controller()

        # load mid file and get key map
        print(f"loading {os.path.basename(song_config.file_path)}")
        mid = mido.MidiFile(song_config.file_path)
        if song_config.use_auto_root:
            note_key_map = self.auto_root_key_map(mid, song_config.auto_root_channels, song_config.auto_root_tracks,
                                                  song_config.auto_root_lowest, song_config.auto_root_highest,
                                                  song_config.auto_root_use_count)
        else:
            note_key_map = NoteKeyMap(song_config.root_note)

        # reset all keys
        for note, key in note_key_map.KEY_STEPS:
            keyboard.press(key)
            await asyncio.sleep(0.03)
            keyboard.release(key)

        # play
        print('start playing')
        fast_forward_time = song_config.skip_start_time
        last_clock = time.time()
        for msg in mid:
            # check for stop
            if not self.play_task_active:
                print("stop playing")
                for key in self.cur_pressed_keys.copy():
                    keyboard.release(key)
                return

            if fast_forward_time > 0:  # skip if fast forward
                fast_forward_time -= msg.time
                continue
            elif msg.time > 0:
                # sleep msg.time based on time.time()
                await asyncio.sleep(msg.time - (time.time() - last_clock))
                last_clock += msg.time

            # press keys
            if msg.type == "note_on" \
               and (len(song_config.channel_filter) == 0 or msg.channel in song_config.channel_filter):
                if key := note_key_map.get_key(msg.note):
                    keyboard.press(key)
                    if song_config.no_hold:
                        note_time = song_config.key_press_duration
                        await asyncio.sleep(note_time)
                        keyboard.release(key)

            elif not song_config.no_hold and msg.type == "note_off" \
                 and (len(song_config.channel_filter) == 0 or msg.channel in song_config.channel_filter):
                if key := note_key_map.get_key(msg.note):
                    keyboard.release(key)

        self.play_task_active = False
        print("finished playing")

    def on_press(self, key):
        self.cur_pressed_keys.add(key)

        if not self.play_task_active and all(key in self.cur_pressed_keys for key in START_COMBO_KEY):
            # check reload config
            if RELOAD_CONFIG_KEY in self.cur_pressed_keys:
                self.load_config()

            else:
                # check song key
                for key in self.song_key_dict:
                    if key in self.cur_pressed_keys:
                        if self.always_reload:
                            self.load_config()
                        # play song
                        self.play_task_active = True
                        self.playing_event_loop.call_soon_threadsafe(
                            lambda: self.playing_event_loop.create_task(self.play(self.song_key_dict[key])))
                        break
        # stop
        elif all(key in self.cur_pressed_keys for key in STOP_KEY_COMBO):
            self.play_task_active = False

    def on_release(self, key):
        self.cur_pressed_keys.discard(key)

    def start(self):
        pynput.keyboard.Listener(on_press=self.on_press, on_release=self.on_release).start()
        self.playing_event_loop.run_forever()
