#!/usr/bin/env python3
#from exceptions import DBHandlerError
import sqlite3
import os

class DictionaryDBHandler(object):
    def __init__(self, db_path="dictionary.db"):
        try:
            # code to check if file exists or not here
            self.database = sqlite3.connect(db_path)
        except Exception:
            print("dataabase not exist")
    
    def close(self):
        self.database.close()

    def get_english(self, nepali):
        cursor = self.database.cursor()
        result_tuples = cursor.execute("""
                SELECT English FROM Dictionary 
                WHERE Nepali='{}'
                """.format(nepali)).fetchall()
        return [x[0] for x in result_tuples]

    # here we insert nepali word and its equivalent english words
    def insert(self, nepali, *english):
        cursor = self.database.cursor()
        for word in english:
            cursor.execute("""
                    INSERT INTO Dictionary(Nepali, English) 
                    VALUES('{}','{}')""".format(nepali, word))
            self.database.commit()
    
    def delete(self, nepali):
        cursor = self.database.cursor()
        cursor.execute("""
                DELETE FROM Dictionary
                WHERE Nepali='{}'""".format(nepali))
        self.database.commit()
    


def main():
    dicthandler = DictionaryDBHandler()
    res = dicthandler.get_english('म')
    for x in res: print(x)
    dicthandler.close()

if __name__=="__main__":
    main()
