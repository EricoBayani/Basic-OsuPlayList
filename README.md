# Basic-OsuPlayList
A simple program to extract only the music files according to a collection from the Osu! rhythm game. 

This program was intented as Python practice, and I thought it would be a fairly simple and quick bodge 
to get a functionality I've always wanted. 

This ended up being harsh and grueling lesson in underestimation, as this simple project ended up causing quite a lot
of headache with the amount of problems springing up. 

I ended up gaining a deeper appreciation for MD5 hashes, character encodings, and Regular Expressions, along with 
a dip into file I/O with Python, my intended goal. 

# How It Works
The script creates a directory for the music files to go into. It then uses three things from Osu! to get those music files: 

the osu!.db file that contains all the information of each beatmap in the game
the collection.db file that contains all the MD5 hashes of the beatmaps in your collections, and the name of that collection
the "Songs" folder that contains all the beatmaps themselves; the beatmaps are folders that contain a .mp3, pictures and/or
sound effects, and .osu files that contain the postions and timing of circles to click, the beatmap itself. 

The script first creates a list of hashes from the collection.db folder using a regular expression. 

Then it opens the osu!.db folder using latin-1 encoding so that the file can properly be intrepreted as text. 

A list of song folder names get created by matching the MD5 hash to the corresponding area the name and artist would be in the
binary. From here, a regex corresponding to the size of the beatmap, the artist, and the song name returns the relevant 
information, and that information gets put in a list. 

After all the hashes get matched, the script then loops through the folder names and searches and copies the mp3s into
the directory at the beginning, and exits.

# Issues and Plans
This program is intended to run on a terminal using a command line. I don't plan on adding a GUI.

Osu! stores its relevant beatmap data in a database file, and collections in a separate database file. Initally, 
I had problems trying to open the .db file in a viewer, and with SQLite in Python to open it. I imagine it would conceptually
be ten times simpler and faster to be able to cross-reference databases together, and that was my intention. Unfortunately, 
I felt that working wit the raw binary file would be faster, since it contained to relevant information anyway, so I did. 


Currently, this script only works on my personal computer, since the directory path used to find the necessary files
for operation only refer to my computer. I plan on going through the finer range of the os library functions to make this script
able to run anywhere. 

As a consequence of using complex regexes to parse a binary not meant to be interpreted as text, the script runs remarkably slow.

The program right now can't support multiple collections; it'll combine multiple collections together. I intend to fix this as a
check using an inline argument would be a simple addition. 
