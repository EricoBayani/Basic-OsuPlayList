# File OsuPlaylist.py
# This is a python program that's going to read the collections.db in an Osu Folder
# and then use it to extract the songs from the songs folder, copying each mp3 into
# another folder so as to have only the mp3s in a folder ready to be put into a
# music player.

import os
import re
import shutil


# createNewFolder() is a function that creates a new directory for the songs to go in
# when it is called. The default name is "Songs from playlist". It takes a string
# as an argument.

def createNewFolder(dirName = "Songs_from_playlist"):
    # Create target Directory if it doesn't exist
    if not os.path.exists(dirName):
        os.mkdir(dirName)
        print("Directory " , dirName ,  " Created ")
    else:    
        print("Directory " , dirName ,  " already exists")


# findOsuHash will go through every song in OsuSongs folder and look through each .osu
# file, matches the hash with the argument, and if they do match, return the name of the
# directory. If the function doesn't find the hash, that means the song isn't in the folder
# and will return a string saying "not found"


def findPreviousLine(fileobject):
    while fileobject.read(1) != "\n":
        fileobject.seek(fileobject.tell() - 2, os.SEEK_SET)
    return fileobject.tell()

def findSongFolderName(fileobject):
    name = re.search(r'[0-9]+\b [\w\-()\\\/!? \.,`~@#$%^&*\[\]{}\|\'\"]+ - [\w\-()\\\/!? \.,`~@#$%^&*\[\]{}\|\'\"]+\B\w', fileobject.readline())
    while not name:
        findPreviousLine(fileobject)
        name = re.search(r'[0-9]+\b [\w\-()\\\/!? \.,`~@#$%^&*\[\]{}\|\'\"]+ - [\w\-()\\\/!? \.,`~@#$%^&*\[\]{}\|\'\"]+\B\w', fileobject.readline())
    return name.group(0)

def findOsuHash(code):

    # this treats a .db binary file as a text file for parsing
    osudb = open('osu!.db', 'rt', encoding = 'latin-1')

    
    position = re.search(code, osudb.read())  # This returns a match object, not a string

    osudb.seek(position.start())

    foldername = findSongFolderName(osudb)

    osudb.close()

    return foldername


# parseCollection will take in the collection fileobject as input, and output a list of the hashes from the collection
def parseCollection(fileobject):
    hashList = []

    collectionString = fileobject.readline()

    hashList = re.findall(r'[a-z,0-9]{32}',collectionString)

    return hashList


# copyMusic takes in the sourceName as an argument, uses it to match to the correct folder name, copies the mp3 into another folder, 
# the name of which is another argument destName, renames the mp3 to the song name, which is another argument 
def copyMusic(songName, artistName, sourceName, destName):
    
    os.chdir(sourceName)
    for file in os.listdir(sourceName):
        if file.endswith(".mp3"):
            filepath = shutil.copy2(file, destName)
            break
    
    return filepath

def main():
    print("Welcome to Erico's OsuPlayList")
    print("This program creates a directory containing mp3s of the songs I enjoy from Osu!")
    print("For now, the program only works properly if there is only one collection of songs I enjoy\n\n")

    createNewFolder()
    dirName = "Songs from playlist"

    collectionFile = open("collection.db", 'rt', encoding = 'latin-1')
    collectionList = []
    collectionList = parseCollection(collectionFile)

    folderNames = []

    for i in range(len(collectionList)):
        folderNames.append(findOsuHash(collectionList[i]))

    smallNames = []

    for i in range(len(folderNames)):
        smallNames.append(re.search(r' [\w\-()\\\/!? \.,`~@#$%^&*\[\]{}\|\'\"]+ - [\w\-()\\\/!? \.,`~@#$%^&*\[\]{}\|\'\"]{3}',folderNames[i]).group(0))


    collectionFile.close()

    # Relevant information for names acquired, now doing the mp3 copying and renaming

    # First, match the names with their respective directories, and separate the song names and song artists

    songNames = []
    songArtists = []

    allSongFolderNames = os.listdir('Songs')
    collectionSongFolderNames = []
    for i in range(len(smallNames)):
        for j in range(len(allSongFolderNames)):
            if re.search(smallNames[i], allSongFolderNames[j]) is not None:
                folder = allSongFolderNames[j]
                collectionSongFolderNames.append(allSongFolderNames[j])
                noNumber = folder.split(' ',1)
                brokenName = noNumber[1].split(' - ')

                songArtists.append(brokenName[0])
                songNames.append(brokenName[1])

                break


    for i in range(len(collectionSongFolderNames)):
        sourceName = "C:\\Programming_Stuff\\Python Programs\\Songs\\" + collectionSongFolderNames[i]
        fullDest = "C:\\Programming_Stuff\\Python Programs\\Songs from playlist\\" + songNames[i] + " by " + songArtists[i] + ".mp3"
        filepath = copyMusic(songNames[i], songArtists[i], sourceName, fullDest)
        print(filepath)


main()

# *NOTES ABOUT PROJECT*
# This script only works when put in an isolated folder containing the necessary files
# from the game. 
# 
# It needs to later take in the necessary directory paths to work anywhere. 
# When using my collection in Osu, there was 1 misinterpretted song, meaning there must be 
# parsing problem.
# 
# The script doesn't work with multiple collections: the way it is right now, the collection 
# reader function will parse through the entire collection file, essentially combining
# multiple collections together. This can be fixed by creating a more robust
# parsing function to start at a certain collection name and stop once it hits another collection
# name


# This script is intended to only work in a terminal using command line arguments. 





