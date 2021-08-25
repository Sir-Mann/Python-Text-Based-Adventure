import cmd
from room import get_room
from room import get_items
from room import get_rooms
from room import Item
import textwrap
import shutil
import tempfile
import sqlite3
from os import system, name

class Game(cmd.Cmd):
    def __init__(self):
        #initialize program
        cmd.Cmd.__init__(self)
        self.dbfile = tempfile.mktemp()
        shutil.copyfile("database/quarenteendb.db", self.dbfile)
        self.loc       = get_room (1, self.dbfile)
        self.gameItems = get_items(1, self.dbfile)
        self.gameRooms = get_rooms(1, self.dbfile)
        self.inventory = []
        self.PrintIntro()

    def move(self, dir):
        newroom = self.loc._neighbor(dir)
        if newroom is None or newroom == 0:
            print("You can't go that way.")
            self.PrintSpace()
        else:
            self.loc = get_room(newroom, self.dbfile)
            self.look()

        if newroom==13:
            exit()

    def take(self, chosenItem):
        """do pickup stuff"""
        self.clear()
        itemFound = False
        for item in self.gameItems:
            if item.name == chosenItem:  # If the user selected an item in the list
                if item.location == self.loc.id: # If the item is in the room
                    itemFound = True
                    item.location = 0 # Items with location of 0 are in your inventory
                    print("You just got " + item.name + "!")

        if itemFound == False:
            print("There is no " + chosenItem + " here.")

        self.PrintSpace()

    def PrintIntro(self):
        self.clear()
        introText  = "You are at the Wilds camp as a counselor. "
        introText += "Many people are getting right with God. "
        introText += "Then suddenly, everthing changes. "
        for line in textwrap.wrap(introText, 72):
            print(line)
        for line2 in textwrap.wrap(self.loc.description, 72):
            print(line2)
        self.PrintSpace()

    def look(self):
        self.clear()
        for line in textwrap.wrap(self.loc.description, 72):
            print(line)

        self.PrintSpace()
        return

    def do_observe(self, args):
        """Observe for any items"""
        itemlist = ''
        index = 0
        self.clear()
        print("You observe...")
        for item in self.gameItems:
            if item.location == self.loc.id:
                index += 1
        if index > 0:
            for item in self.gameItems:
                if item.location == self.loc.id:
                    print("and see some items:\n" + item.name + ":\n" + item.description + "\n\n")
        else:
            print("but see no items around anywhere.")

        print("\nThe directions you can go are.")
        for neighbor in self.loc.neighbors:
            if len(neighbor) > 1:
                print(neighbor[0] + neighbor[1])
            else:
                print(neighbor[0])

        self.PrintSpace()

    def do_n(self, args):
        """Go north"""
        self.clear()
        print("You went north.")
        self.move('n')

    def do_nw(self, args):
        """Go north"""
        self.clear()
        print("You went northwest.")
        self.move('nw')

    def do_ne(self, args):
        """Go north"""
        self.clear()
        print("You went northeast.")
        self.move('ne')

    def do_s(self, args):
        """Go south"""
        self.clear()
        print("You went south.")
        self.move('s')

    def do_sw(self, args):
        """Go north"""
        self.clear()
        print("You went southwest.")
        self.move('sw')

    def do_se(self, args):
        """Go north"""
        self.clear()
        print("You went southeast.")
        self.move('se')

    def do_e(self, args):
        """Go east"""
        self.clear()
        print("You went east.")
        self.move('e')

    def do_w(self, args):
        """Go west"""
        self.clear()
        print("You went west.")
        self.move('w')

    def do_take(self, item):
        """Pickup an item"""
        self.take(item)

    def do_inventory(self, args):
        """Look at inventory"""
        self.clear()
        print ("You have in your inventory:")
        index = 0
        for item in self.gameItems:
            if  item.location == 0:
                index += 1
                print ("  - "  + item.name)
        if index == 0:
            print("Nothing")

        self.PrintSpace()

    def do_database(self, args):
        """Look at room database info"""
        con = sqlite3.connect(self.dbfile)
        cur = con.cursor()
        cur.execute("select * from rooms where id = " + self.loc.id)
        rows = cur.fetchall()
        print("\n\n\n")
        for row in rows:
            print("Id:", row[0])
            print("json:", row[1])

    def do_whereami(self, args):
        """Find the location where you are"""
        self.clear()
        print(self.loc.name)
        self.PrintSpace()

    def do_quit(self, args):
        """Leaves the game"""
        print('Thank you for playing.')
        return True

    # define our clear function
    def clear(self):

        # for windows
        if name == 'nt':
            _ = system('cls')

        # for mac and linux(here, os.name is 'posix')
        else:
            _ = system('clear')

    def PrintSpace(self):
        # Print seven returns
        print("\n\n\n\n\n\n\n")

if __name__ == '__main__':
    g = Game()
    g.cmdloop()
