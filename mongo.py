from pymongo import MongoClient
from pymongo import UpdateOne
import glob
import os
import re

def dump_sentences():
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
                if "eng" in filename:
                    lang = "eng"
                else:
                    lang = "hin"
                bulk_grams.append({"identifier":id,"lang":lang,"words":words,"pos_tags":pos_tags})

            count += len(bulk_grams)
            print 'Inserted '+str(count)
            glove.insert_many(bulk_grams)

def dump_matrix(lang_origin,lang_target):
    client = MongoClient('localhost', 27017)
    db = client['nlprokz']
    words = sorted(db.hinglish.find({"lang":lang_target}).distinct("words"))
    count = 0
    count_update = 0
    for i in db.hinglish.find({"lang":lang_origin}):
        hindi_sentence = db.hinglish.find_one({"identifier":i['identifier'],"lang":lang_target})
        bulk_vec = []
        for j in i["words"]:
            vec_count = db.bilingualvec.count({"word":j})
            if vec_count > 0:
                doc = db.bilingualvec.find_one({"word":j})
                vec = doc["vec"]
                for k in xrange(len(words)):
                    if words[k] in hindi_sentence["words"]:
                        vec[k] += 1
                count_update += 1
                print "INSERTS:"+str(count_update)
                db.bilingualvec.update({"word":j},{"$set":{"vec":vec,"lang_origin":lang_origin,"lang_target":lang_target}})
            else:
                vec = []
                for k in words:
                    if k in hindi_sentence["words"]:
                        vec.append(1)
                    else:
                        vec.append(0)
                count += 1
                db.bilingualvec.insert({"word":j,"vec":vec,"lang_origin":lang_origin,"lang_target":lang_target})
                print "NEW INSERTS:"+str(count)



if __name__ == '__main__':
    dump_matrix("eng","hin")
