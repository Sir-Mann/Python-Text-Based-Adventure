"""
sequence:
1. Files loaded into the database. The file names are the IDs that are loaded in.
2. ID comes from the neighbor where you are going into.
                    ---------
                    | Table |
        --------------------------------
        |ID         | jsontext         |
        --------------------------------
        |quarenteen | info text (including ID of neighbors)|
        |tunnel     | info text (including ID of neighbors)|
        --------------------------------
        exc.


"""

import sys
import sqlite3
import os
import os.path
import json
from room import Room

def main(dbname):
    con = sqlite3.connect(dbname)

    """Clear the previous rooms and recreate them"""
    con.execute("DROP TABLE IF EXISTS rooms")
    con.execute("DROP TABLE IF EXISTS items")
    con.execute("CREATE TABLE IF NOT EXISTS rooms(id TEXT PRIMARY KEY, json TEXT NOT NULL)")
    #con.execute("CREATE TABLE IF NOT EXISTS items(id TEXT PRIMARY KEY, name TEXT NOT NULL, movable BOOL, extDescription TEXT)")
    con.commit()

    for filename in os.listdir():
        base, extension = os.path.splitext(filename)
        if extension == '.json':
            with open(filename, 'r') as f:

                #Read the file
                filecontent = f.read()

                #Print that a room is inserted
                print("Inserting room {0}".format(base))

                #Insert room information
                con.execute("INSERT OR REPLACE INTO rooms(id, json) VALUES(?, ?);",
                            (str(base), filecontent))

                #Load in text as jsontext
                jsontext = json.loads(filecontent)

                #Create Rooms
                ret = room.Room(**d)

                con.commit()

    con.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Usage: {0} <database name>'.format(sys.argv[0]))
    else:
        main(sys.argv[1])
