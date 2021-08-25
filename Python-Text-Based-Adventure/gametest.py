import cmd
import textwrap
import shutil
import tempfile
import sqlite3
import json
from room import roomDecoder

class Game(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        file = open('rooms.json', 'r')
        data = []
        try:
            for jsonObj in file:
                roomObj = json.load(file, object_hook=roomDecoder)
        except Exception as e:
            print("***** Start Error *****")
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(e).__name__, e.args)
            print(message)
            print(e)
            print("***** End Error *****")

        print(roomObj.name)

    def do_quit(self, args):
        """Leaves the game"""
        print('Thank you for playing.')
        return True

if __name__ == '__main__':
    g = Game()
    g.cmdloop()
