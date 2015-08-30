#!/usr/bin/env python3
from dictionary.dict_db_handler_error import DictDBHandlerError
import sqlite3
import os

class DictionaryDBHandler(object):
    def __init__(self, db_path="dictionary.db"):
        try:
            # code to check if file exists or not here
            self.database = sqlite3.connect(db_path)
        except Exception:
            raise DictDBHandlerError("dataabase not exist")
    
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

    def insert_unigram(self, nepali_unigram, english):
        # here english is tuple
        cursor = self.database.cursor()
        raw_res = cursor.execute("""
                    SELECT ID FROM unigram_nepali WHERE unigram='{}'
                """.format(nepali_unigram)
        )
        result = raw_res.fetchall()
        if len(result) > 0:
            nep_id = int(result[0][0])
        elif len(result) == 0:
            # first insert the new nepali into database
            cursor.execute("INSERT INTO unigram_nepali(unigram) VALUES(?)", [nepali_unigram])
            self.database.commit()
            # now get the id of the recently added row
            nep_id = int(cursor.lastrowid)
        else: return

        # now insert meanings
        if type(nep_id) is int:
            for word in english:
                try:
                    res = cursor.execute("""
                                INSERT INTO unigram_meanings(nepali_unigram, english) 
                                VALUES(?, ?)""", [nep_id, word]
                        )
                except sqlite3.IntegrityError as e:
                    if 'UNIQUE constraint failed' in repr(e): 
                        pass
                    else:
                        print(e)
            self.database.commit()

    def get_english1(self, nepali):
        length = len(nepali.split())
        if length==1:
            table = "nepali_unigram"
            field = 'unigram'
        elif length==2:
            table = "nepali_bigram"
            field = 'bigram'
        elif length==3:
            table = "nepali_trigram"
            field = 'trigram'
        elif length==4:
            table = "nepali_quadgram"
            field = 'quadgram'
        else:
            raise DictDBHandlerError("no table for "+str(length)+"-grams")

        cursor = self.database.cursor() 
        results = cursor.execute("""
                        SELECT ID FROM {} WHERE {}='{}'
                        """.format(table, field, nepali)
        )
        nep_id = results.fetchall()[0][0]
        meaning_table = table.split('_')[1]+'_'+'meanings'
        raw_results = cursor.execute('''
                            SELECT english FROM {} WHERE {}={}
                            '''.format(meaning_table,table ,nep_id)
        )
        return [x[0] for x in raw_results.fetchall()]

def main():
    print("This is dictionary dababase handler.. ")

if __name__=="__main__":
    main()
