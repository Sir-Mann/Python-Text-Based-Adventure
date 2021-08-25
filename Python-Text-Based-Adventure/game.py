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
        data = []

        '''open json file'''
        file = open('rooms.json', 'r')

        '''attempt to load in json file
           python should see it as a list[of dictionaries{}]'''
        try:
            dataList = json.loads(file.read())
            index = 0
            for data in dataList:
                print(data.get('name'))
                index += 1
        except Exception as e:
            print("***** Start Error *****")
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(e).__name__, e.args)
            print(message)
            print(e)
            print("***** End Error *****")


    def do_quit(self, args):
        """Leaves the game"""
        print('Thank you for playing.')
        return True

if __name__ == '__main__':
    g = Game()
    g.cmdloop()
