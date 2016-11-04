from pymongo import MongoClient
import glob
import os
import re

if __name__ == '__main__':
    client = MongoClient('localhost', 27017)
    db = client['nlprokz']
    glove = db.hinglish
    count = 0
    for root, dirs, files in os.walk('Corpus/Hindi_English/'):
        for basename in files:
            filename = os.path.join(root, basename)
            bulk_grams = []
            for line in open(filename):
                grams = re.split(r'\s',line.strip().replace("\\"," "))
                id = grams[0]
                sentence = grams[1:]
                words = sentence[::2]
                pos_tags = sentence[1::2]
                bulk_grams.append({"identifier":id,"words":words,"pos_tags":pos_tags})

            count += len(bulk_grams)
            print 'Inserted '+str(count)
            glove.insert_many(bulk_grams)
