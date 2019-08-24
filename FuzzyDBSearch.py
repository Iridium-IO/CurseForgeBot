
###############################################################
#Approximate string matching using FuzzyWuzzy
#Runs slow as hell on Raspberry Pi, so it only gets called last
###############################################################

import sqlite3
import time
from fuzzywuzzy import process

def GetMatch(inputStr):
    print('Fuzzy Searching')
    conn = sqlite3.connect('CurseForgeMods.db')
    c = conn.cursor()

    modNames = [mod[0] for mod in c.execute('SELECT name FROM Mods')]

    highest = process.extractOne(inputStr, modNames, score_cutoff= 80)
    c.execute('SELECT * FROM Mods WHERE name = ?', [highest[0]])
    return c.fetchone()

if __name__ == '__main__':
    start_time = time.time()
    print(GetMatch('worl edit'))
    print("--- %s seconds ---" % (time.time() - start_time))


