from keymaps import keymaps


class NoteKeyMap:
    KEY_STEPS = keymaps['456789']

    def __init__(self, root_note):
        self.map = {}
        for key_step in self.KEY_STEPS:
            self.map[root_note + key_step[0]] = key_step[1]

    def get_key(self, note):
        return self.map.get(note)
