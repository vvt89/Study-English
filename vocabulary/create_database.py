import random
import re
import sqlite3


def add_new_word(database_file, word):
    conn = sqlite3.connect(database_file)
    cur = conn.cursor()

    wordiscorrect = False
    words_match = True
    list_of_rows = []
    last_number = 0

    word = word.strip()  # Delete spaces on both sides
    word = word.lower()
    match = []
    match0 = (re.match("^[ '\-abcdefghijklmnopqrstuvwxyz]*$", word))  # Check if string consists only letters
    match.append(re.search("^'\S", word))  # Check if word starts from '
    match.append(re.search("^\S+'$", word))  # Check if word ends by '
    match.append(re.search("^\S+'+'", word))  # Check if word consists ''
    match.append(re.search("^-\S", word))  # Check if word starts from -
    match.append(re.search("^\S+-$", word))  # Check if word ends by -
    match.append(re.search("^\S+-+-", word))  # Check if word consists --
    match_flag = False
    # print(match0, match)
    if match0 is None:
        match_flag = True
    for m in match:
        if m is not None:
            match_flag = True
    if match_flag is False:
        words = word.split()  # Delete redundant spaces
        new_word = ""
        for w in words:
            if len(w)>0:
                new_word += w
                new_word += " "
        new_word = new_word.strip()  # Delete spaces on both sides
        wordiscorrect = True
    else:
        wordiscorrect = False
        #print("Uncorrect word")

    if len(word) == 0:
        wordiscorrect = False

    # Check the length of a word. The longest known word is pseudopseudohypoparathyroidism, which contains 30 letters.
    if len(word) > 30:
        wordiscorrect = False

    if wordiscorrect:
        cur.execute('SELECT * FROM Words')
        counter = 0

        words_match = False
        for row in cur:  # How large is our vocabulary?
            counter += 1
            last_number = row[0]  # It is used for next id calculation
            #print(row)
            if new_word == row[1]:
                words_match = True
        #print("length of the base: ", counter)

        if words_match is False:  # Add new word
            params = (last_number+1, new_word)
            cur.execute('INSERT INTO Words (id, word) VALUES(?,?)', params)
            conn.commit()
        else:
            pass
            #print("this word is already exists in vocabulary")

        cur.execute('SELECT * FROM Words')
        list_of_rows = cur.fetchall()

    cur.close()
    return wordiscorrect, words_match, list_of_rows, last_number,


def delete_word(database_file, input_word):
    conn = sqlite3.connect(database_file)
    cur = conn.cursor()
    cur.execute('DELETE FROM Words WHERE word = "' + input_word + '"')
    conn.commit()
    cur.execute('SELECT * FROM Words')
    list_of_rows = cur.fetchall()
    cur.close()
    return list_of_rows


def delete_id(database_file, index):
    conn = sqlite3.connect(database_file)
    cur = conn.cursor()
    cur.execute('DELETE FROM Words WHERE id = ' + str(index))
    conn.commit()
    cur.execute('SELECT * FROM Words')
    list_of_rows = cur.fetchall()
    cur.close()
    return list_of_rows


def get_random_word(database_file):
    word = None
    conn = sqlite3.connect(database_file)
    cur = conn.cursor()
    cur.execute('SELECT * FROM Words')
    counter = len(cur.fetchall())
    last_number = random.randint(1, counter)
    cur.execute('SELECT * FROM Words')
    counter = 0
    for i in cur:
        counter += 1
        if counter == last_number:
            word = i[1]
    return word


def get_random_word_from_the_last(database_file, first_num):
    word = None
    conn = sqlite3.connect(database_file)
    cur = conn.cursor()
    cur.execute('SELECT * FROM Words')
    counter = len(cur.fetchall())
    first_num = min(first_num, counter)
    last_number = random.randint(first_num, counter)
    cur.execute('SELECT * FROM Words')
    counter = 0
    for i in cur:
        counter += 1
        if counter == last_number:
            word = i[1]
    return word


# main routine:
if __name__ == "__main__":
    file_name = 'english_vocabulary.sqlite'
    new_word = "derivative"
    res = add_new_word(file_name, new_word)
    if res[0] is False:
        print("Incorrect word")
    else:
        if res[1] is True:
            print("This word is already exists in vocabulary")
    for row in res[2]:
        print(row)
    print("The last number is: ", res[3])
    random_word = get_random_word_from_the_last(file_name, 1)
    print("random word: ", random_word)
    # delete_word(file_name, "wast")
    # Irregular Verbs located from 1033 to 1277
    # Do not uncomment if database already created:
    # cur.execute('DROP TABLE IF EXISTS Words')
    # cur.execute('CREATE TABLE Words (id INTEGER, word TEXT)')
    # cur.execute('DELETE FROM Words WHERE id = 617')
    # cur.execute('INSERT INTO Words (id, word) VALUES(?,?)', (181, "grandmother"))
    # conn.commit()
