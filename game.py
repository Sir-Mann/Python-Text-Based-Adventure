import cmd
from room import get_room
import textwrap
import shutil
import tempfile

class Game(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)

        self.loc = get_room("quarenteen")
        self.inventory = []
        self.look()

    def move(self, dir):
        newroom = self.loc._neighbor(dir)
        if newroom is None:
            print("you can't go that way")
        else:
            self.loc = get_room(newroom)
            self.look()

        if newroom==13:
            exit()

    def take(self, item):
        """do pickup stuff"""
        item = self.loc._items(item)
        if item is None:
            print("There is nothing to take.")
        else:
            self.inventory.append(item)
            print("You just got "+item+"!")

    def look(self):
        print(self.loc.name)
        print("")
        for line in textwrap.wrap(self.loc.description, 72):
            print(line)

    def do_observe(self, args):
        """Observe for any items"""
        itemlist = ''
        index = 0
        if len(self.loc.itemObjects):
            print("\n you observe you see some items lying around:\n")
            for item in self.loc.itemObjects:
                print(self.loc.itemObjects[index].description + ":\n" + self.loc.itemObjects[index].extDescription + "\n\n")
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
        print(*self.inventory)

    def do_whereami(self, args):
        """Find the location where you are"""
        print(self.loc[id])

    def do_quit(self, args):
        """Leaves the game"""
        print('Thank you for playing.')
        return True

if __name__ == '__main__':
    g = Game()
    g.cmdloop()
