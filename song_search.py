
from hash_table import HashTable


def build_hash_table(filename):
    """
    build_hash_table function -- builds a hashtable containing the word that is used as a key to get the list
    of songs that contain that word
    Parameters:
        filename: represents the file containing all the songs
    Returns:
        the hash table that contains all the songs and words that we can look for
    """
    print("Building hash table using data in", filename)
    file = open(filename, 'r')
    hash_table = HashTable()
    for line in file:
        line = line.strip()
        grab_id = line.split(' ')
        id_song = grab_id[0]
        grab_id.remove(grab_id[0])
        temp_string = ''
        for words in grab_id:
            temp_string = temp_string + ' ' + words
        temp_string = temp_string[1:]
        song, creator = temp_string.split('::')
        creator = creator[1:]
        song = song[:-1]
        tup = (int(id_song), song, creator)
        words = song.split(' ')
        for w in words:
            hash_table.store(w, tup)
    h = hash_table
    file.close()
    f = open('logfile.txt', 'a')
    f.write('\n End reading songs from file songs.txt')
    f.write('\n HashTable details: ' + str(hash_table.size) + ' slots, ' + str(hash_table.occupied) + ' occupied, '
            + 'load factor = ' + str(hash_table.load_factor))
    f.write('\n Number of unique keys inserted into HashTable = ' + str(hash_table.occupied))
    f.write('\n Number of key conflicts encountered = ' + str(hash_table.conflicts))
    f.close()
    return h


def find_words(hash_table, filename):
    """
    find_words function -- given a file with words that we want to look for and looks through the Hash Table for the
    word and returns a list of songs that contain that word
    Parameters:
        hash_table: represents the Hash Table that we are going to look through for the key (word)
        filename: represents the that contains the words that we will look for in the Hash Table
    Returns:
        prints a list of songs that contain the words in the file
    """
    print("Searching for words listed in", filename)
    f = open('logfile.txt', 'a')
    f.write('\n Now Starting Search For Words In Songs')
    file = open(filename, 'r')
    for line in file:
        line = line.strip()
        list_songs = hash_table.get(line)
        print(str(len(list_songs) - 1) + ' Songs Contain The Word ' + '"' + list_songs[0] + '"' + ' In Their Title.')
        list_songs = list_songs[1:]
        counter = 0
        print(' ')
        for tup in list_songs:
            counter += 1
            print('    ' + str(counter) + '. ' + str(tup[0]) + ', ' + str(tup[1]) + ', ' + str(tup[2]))
        print(' ')
        print('This Search Examined ' + str(hash_table.hash_function(line, hash_table.size))
              + ' Slots In The Hash Table')
        print(' ')
        f.close()


def find_phrases(hash_table, filename):
    """
    find_phrases function -- given file that has phrases and find the songs that contain those phrases in the
    hash table
    Parameters:
        hash_table: represents the hash table that we are looking through for the song
        filename: represents the file that contains the phrases we are looking for
    Returns:
        All the songs that contains the phrases in the file
    """
    print("Searching for phrases listed in", filename)
    f = open('logfile.txt', 'a')
    f.write('\n Now starting search of phrases')
    file = open(filename, 'r')
    for line in file:
        song_list = []
        line = line.strip()
        line_words = line.split(' ')
        total = 0
        for words in range(0, len(line_words)):
            list_songs = hash_table.get(line_words[words])
            list_songs = list_songs[1:]
            for tup in list_songs:
                name = tup[1].lower()
                slot_nums = hash_table.hash_function(name, len(hash_table.slots))
                if total < slot_nums:
                    total = slot_nums
                if line in name:
                    if tup in song_list:
                        pass
                    else:
                        song_list.append(tup)
        print(' ')
        print(str(len(song_list)) + ' Songs Contain The Phrase "' + str(line) + '" In Their Title')
        counter = 0
        print(' ')
        for songs in song_list:
            counter += 1
            print('    ' + str(counter) + '. ' + str(songs[0]) + ', ' + str(songs[1]) + ', ' + str(songs[2]))
        print(' ')
        print('This Search Examined ' + str(total) + ' Slots In The Hash Table')
        f.close()


def main():
    """
    main function -- contains all the calls for the above functions
    Returns:
         Nothing
    """
    hash_table = build_hash_table("Resources/songs.txt")

    find_words(hash_table, "Resources/words.txt")

    find_phrases(hash_table, "Resources/phrases.txt")


main()
