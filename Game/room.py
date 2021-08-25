import json
import sqlite3
import tempfile
import shutil #shell utility
from os import system, name

def get_room(id, dbfile):
    ret = None

    con    = sqlite3.connect(dbfile)
    cursor = con.cursor()
    cursor.execute("select * from rooms where id = ?", (id,))
    for row in cursor:
        ret = Room(*row)
        break

    con.close()

    return ret

def get_rooms(id, dbfile):
        ret = []
        con    = sqlite3.connect(dbfile)
        cursor = con.cursor()
        cursor.execute("select * from rooms")
        for row in cursor:
            ret.append(Room(*row))
        con.close()

        return ret

def get_items(id, dbfile):
        ret = []

        con    = sqlite3.connect(dbfile)
        cursor = con.cursor()
        cursor.execute("select * from items")
        for row in cursor:
            ret.append(Item(*row))

        con.close()

        return ret

""" This is old. It pulls the room info from json files directly each time a room is entered.
    with open("rooms/" + str(id)+".json", "r") as F:
        jsontext = F.read()
        d = json.loads(jsontext)
        d['id'] = id
        ret = Room(**d) #Return the room with that corresponding id.
    return ret
"""

class Item:
    def __init__ (self,
                  id=0,
                  name="Item",
                  location=0,
                  description="An Item"):
        self.id          = id
        self.name        = name
        self.location    = location
        self.description = description

class Room():
    def __init__ (self,
                  id=0,
                  name="A Room",
                  description= "An Empty Room",
                  neighbors=""):
       self.id          = id
       self.name        = name
       self.description = description
       self.neighbors   = json.loads(neighbors)

    def _neighbor(self, direction):
        if direction in self.neighbors:
            return self.neighbors[direction]
        else:
            return None
