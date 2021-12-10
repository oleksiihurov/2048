"""
https://2048game.com
"""


# Project imports
from demo import Demo


# --- Main Program ------------------------------------------------------------

def main():
    demo = Demo()
    while demo.loop_handler():
        demo.events_handler()
        demo.actions_handler()
        demo.graphics_handler()


if __name__ == '__main__':
    main()
