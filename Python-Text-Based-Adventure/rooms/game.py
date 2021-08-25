import cmd
from room import get_room
from room import Item
import textwrap
import shutil
import tempfile
import sqlite3

class Game(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)

        self.dbfile = tempfile.mktemp()
        shutil.copyfile("game.db", self.dbfile)

        self.loc = get_room("quarenteen", self.dbfile)
        self.inventory = []
        self.look()

    def move(self, dir):
        newroom = self.loc._neighbor(dir)
        if newroom is None:
            print("you can't go that way")
        else:
            self.loc = get_room(newroom, self.dbfile)
            self.look()

        if newroom==13:
            exit()

    def take(self, item):
        """do pickup stuff"""
        index = 0
        for itemObject in self.loc.itemlist:

            #Add the item to inventory
            if self.loc.itemlist[index].name == item:
               self.inventory.append(self.loc.itemlist[index])
               print("You just got "+self.loc.itemlist[index].name+"!\n\n")

               #Remove item from room
               self.loc.itemlist.pop(index) #This breaks the program if taking muliple items

               #Test reading a room from the database
               con = sqlite3.connect(self.dbfile)
               cur = con.cursor()
               cur.execute("select * from rooms where id = \"quarenteen\"")
               rows = cur.fetchall()

               """
               for row in rows:
                   print("Id:", row[0])
                   print("json:", row[1])"""

               #Delete the room? No! Delete the item!
               #con.execute("delete from rooms where id = ?", (self.loc.itemlist[index].name,))

               con.close()
            else:
                ("There is nothing to take.")
            index += 1

    def look(self):
        print(self.loc.name)
        print("")
        for line in textwrap.wrap(self.loc.description, 72):
            print(line)

    def do_observe(self, args):
        """Observe for any items"""
        itemlist = ''
        index = 0
        if len(self.loc.itemlist):
            print("\nAs you observe, you see some items lying around:\n")
            for item in self.loc.itemlist:
                print(self.loc.itemlist[index].name + ":\n" + self.loc.itemlist[index].extDescription + "\n\n")
                index += 1
        else:
            print("That is all you see.")

    def do_up(self, args):
        """Go up"""
        self.move('up')

    def do_down(self, args):
        """Go down"""
        self.move('down')

    def do_n(self, args):
        """Go north"""
        self.move('n')

    def do_s(self, args):
        """Go south"""
        self.move('s')

    def do_e(self, args):
        """Go east"""
        self.move('e')

    def do_w(self, args):
        """Go west"""
        self.move('w')

    def do_take(self, item):
        """Pickup an item"""
        self.take(item)

    def do_inventory(self, args):
        """Look at inventory"""
        index = 0
        for invent in self.inventory:
            print (self.inventory[index].name)
            index += 1

    def do_whereami(self, args):
        """Find the location where you are"""
        print(self.loc.name)

    def do_quit(self, args):
        """Leaves the game"""
        print('Thank you for playing.')
        return True

if __name__ == '__main__':
    g = Game()
    g.cmdloop()
