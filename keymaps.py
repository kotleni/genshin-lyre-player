import pynput

keymaps = {
    # 'qwerty' : [ # default keymap for pc genshin
    #     (0, pynput.keyboard.KeyCode.from_vk(0x5A)),  # z
    #     (2, pynput.keyboard.KeyCode.from_vk(0x58)),  # x
    #     (4, pynput.keyboard.KeyCode.from_vk(0x43)),  # c
    #     (5, pynput.keyboard.KeyCode.from_vk(0x56)),  # v
    #     (7, pynput.keyboard.KeyCode.from_vk(0x42)),  # b
    #     (9, pynput.keyboard.KeyCode.from_vk(0x4E)),  # n
    #     (11, pynput.keyboard.KeyCode.from_vk(0x4D)),  # m
    #     (12, pynput.keyboard.KeyCode.from_vk(0x41)),  # a
    #     (14, pynput.keyboard.KeyCode.from_vk(0x53)),  # s
    #     (16, pynput.keyboard.KeyCode.from_vk(0x44)),  # d
    #     (17, pynput.keyboard.KeyCode.from_vk(0x46)),  # f
    #     (19, pynput.keyboard.KeyCode.from_vk(0x47)),  # g
    #     (21, pynput.keyboard.KeyCode.from_vk(0x48)),  # h
    #     (23, pynput.keyboard.KeyCode.from_vk(0x4A)),  # j
    #     (24, pynput.keyboard.KeyCode.from_vk(0x51)),  # q
    #     (26, pynput.keyboard.KeyCode.from_vk(0x57)),  # w
    #     (28, pynput.keyboard.KeyCode.from_vk(0x45)),  # e
    #     (29, pynput.keyboard.KeyCode.from_vk(0x52)),  # r
    #     (31, pynput.keyboard.KeyCode.from_vk(0x54)),  # t
    #     (33, pynput.keyboard.KeyCode.from_vk(0x59)),  # y
    #     (35, pynput.keyboard.KeyCode.from_vk(0x55)),  # u
    # ],
    '456789' : [ # special keymap for playcover
        (0, pynput.keyboard.KeyCode.from_vk(9)),  # v
        (2, pynput.keyboard.KeyCode.from_vk(11)),  # b
        (4, pynput.keyboard.KeyCode.from_vk(45)),  # n
        (5, pynput.keyboard.KeyCode.from_vk(46)),  # m
        (7, pynput.keyboard.KeyCode.from_vk(43)),  # ,
        (9, pynput.keyboard.KeyCode.from_vk(47)),  # .
        (11, pynput.keyboard.KeyCode.from_vk(44)),  # /
        (12, pynput.keyboard.KeyCode.from_vk(3)),  # f
        (14, pynput.keyboard.KeyCode.from_vk(5)),  # g
        (16, pynput.keyboard.KeyCode.from_vk(4)),  # h
        (17, pynput.keyboard.KeyCode.from_vk(38)),  # j
        (19, pynput.keyboard.KeyCode.from_vk(40)),  # k
        (21, pynput.keyboard.KeyCode.from_vk(37)),  # l
        (23, pynput.keyboard.KeyCode.from_vk(41)),  # ;
        (24, pynput.keyboard.KeyCode.from_vk(21)),  # 4
        (26, pynput.keyboard.KeyCode.from_vk(23)),  # 5
        (28, pynput.keyboard.KeyCode.from_vk(22)),  # 6
        (29, pynput.keyboard.KeyCode.from_vk(26)),  # 7
        (31, pynput.keyboard.KeyCode.from_vk(28)),  # 8
        (33, pynput.keyboard.KeyCode.from_vk(29)),  # 9
        (35, pynput.keyboard.KeyCode.from_vk(25)),  # 0
    ]
}