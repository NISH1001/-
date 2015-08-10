#!/usr/bin/env python3

import sqlite3

class NgramDB(object):
    def __init__(self, db_name="../data/ngrams/ngrams.db"):
        self.db_name = db_name
        self.db = sqlite3.connect(db_name)
        self.list_str = ['unigrams', 'bigrams', 'trigrams', 'quadgrams']
        #self.db = sqlite3.connect(":memory:")

    def close(self):
        self.db.close()

    def create_table_all(self):
        self.create_table(n=2)
        self.create_table(n=3)
        self.create_table(n=4)

    """create the table for ngram"""
    def create_table(self, n=2):
        print("creating {}grams table... :D".format(n))
        cursor = self.db.cursor()
        if n==2:
            cursor.execute("""
                    CREATE TABLE bigrams
                    (
                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
                        word1 TEXT,
                        word2 TEXT, 
                        count INTEGER
                    )
                """)
        if n==3:
            cursor.execute("""
                    CREATE TABLE trigrams
                    (
                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
                        word1 TEXT,
                        word2 TEXT, 
                        word3 TEXT,
                        count INTEGER
                    )
                """)
        if n==4:
            cursor.execute("""
                    CREATE TABLE quadgrams
                    (
                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
                        word1 TEXT,
                        word2 TEXT, 
                        word3 TEXT,
                        word4 TEXT,
                        count INTEGER
                    )
                """)
        self.db.commit()    # save the changes
    
    """ insert the word sequence and occurence count """
    def insert(self, word_seq, count):
        n = len(word_seq)
        data = list(word_seq)
        data.append(count)
        data = tuple(data)
        cursor = self.db.cursor()
    
        if n==2:
            cursor.execute("""
                    INSERT INTO bigrams(word1, word2, count)
                    VALUES(?,?,?)""", data
                )
        elif n==3:
            cursor.execute("""
                    INSERT INTO trigrams(word1, word2, word3, count)
                    VALUES(?,?,?,?)""", data
                )
        else:
            cursor.execute("""
                    INSERT INTO qudgrams(word1, word2, word3, word4, count)
                    VALUES(?,?,?,?,?)""", data
                )
        self.db.commit()

    def insert_many(self, data, n=2):
        cursor = self.db.cursor()
    
        if n==2:
            cursor.executemany("""
                    INSERT INTO bigrams(word1, word2, count)
                    VALUES(?,?,?)""", data
                )
        elif n==3:
            cursor.executemany("""
                    INSERT INTO trigrams(word1, word2, word3, count)
                    VALUES(?,?,?,?)""", data
                )
        else:
            cursor.executemany("""
                    INSERT INTO quadgrams(word1, word2, word3, word4, count)
                    VALUES(?,?,?,?,?)""", data
                )
        self.db.commit()
    
    """ return the count query -> list of tuples it is
        if total=True -> total ngram count is returned instead of 
            just a specifirc ngram
    """
    def count(self, word_seq, total=False):
        n = len(word_seq)
        cursor = self.db.cursor()

        if total:
            cnt = tuple(['count_'+self.list_str[n-1]])
            return cursor.execute("""
                    SELECT value FROM aggregate
                    WHERE name=?
                """, cnt )
    
        if n==2:
            return cursor.execute("""
                    SELECT count FROM bigrams
                    WHERE word1=? and word2=?
                """, word_seq)
        elif n==3:
            return cursor.execute("""
                    SELECT count FROM trigrams
                    WHERE word1=? and word2=? and word3=?
                """, word_seq)
        else:
            return cursor.execute("""
                    SELECT count FROM quadgrams
                    WHERE word1=? and word2=? and word3=? and word4=?
                """, word_seq)


def main():
    ngramdb = NgramDB("../data/ngrams/ngrams.db")

    ngramdb.create_table(n=2)
    ngramdb.create_table(n=3)
    ngramdb.create_table(n=4)

    #ngramdb.insert( ("i", "am", "nishan"), 444)

    ngramdb.close()

if __name__=="__main__":
    main()

