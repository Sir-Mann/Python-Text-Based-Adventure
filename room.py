import json
import sqlite3

def get_room(id):
    ret = None
    with open("rooms/" + str(id)+".json", "r") as F:
        jsontext = F.read()
        d = json.loads(jsontext)
        d['id'] = id
        ret = Room(**d) #Return the room with that corresponding id.
    return ret

class Item:
  def __init__(self,specifics:list):
    self.description = specifics[0]
    if specifics[1] == "True":
        self.movable = True
    else:
        self.movable = False
    self.extDescription = specifics[2]

class Room():
    def __init__ (self,
                  id=0,
                  name="A Room",
                  description= "An Empty Room",
                  neighbors={},
                  itemlist=[]):
       self.id = id
       self.name = name
       self.description = description
       self.neighbors = neighbors
       self.itemObjects = []
       """Create item objects from the list of items in the json files"""
       for item in itemlist:
          self.itemObjects.append(Item(item))

    def _neighbor(self, direction):
        if direction in self.neighbors:
            return self.neighbors[direction]
        else:
            return None

    def _items(self, item):
        if item in self.items:
            """remove item from room"""
            return self.items[item]
        else:
            return None
