class SongConfig:
    def __init__(self, song_config: dict):
        self.file_path = song_config["file"]
        self.channel_filter = []
        self.track_filter = []
        self.no_hold = True
        self.key_press_duration = 0.01
        self.skip_start_time = 0
        self.root_note = None
        self.use_auto_root = self.root_note is None
        if self.use_auto_root:
            self.auto_root_lowest = 48
            self.auto_root_highest = 84
            self.auto_root_use_count = True
            self.auto_root_channels = self.channel_filter
            self.auto_root_tracks = self.track_filter
            