import glob
import os
import re
import numpy as np
from pymongo import MongoClient
from pymongo import UpdateOne
from sklearn.metrics import pairwise_distances

def dump_sentences():
    client = MongoClient('localhost', 27017)
    db = client['nlprokz']
    hinglish = db.hinglish
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
            hinglish.insert_many(bulk_grams)
    hinglish.remove({"identifier":"ID"})

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
            vec_count = db.bilingualvec.count({"word":j.lower()})
            if vec_count > 0:
                doc = db.bilingualvec.find_one({"word":j.lower()})
                vec = doc["vec"]
                for k in xrange(len(words)):
                    if words[k] in hindi_sentence["words"]:
                        vec[k] += 1
                count_update += 1
                #print "INSERTS:"+str(count_update)
                db.bilingualvec.update({"word":j.lower()},{"$set":{"vec":vec,"lang_origin":lang_origin,"lang_target":lang_target}})
            else:
                vec = []
                for k in words:
                    if k in hindi_sentence["words"]:
                        vec.append(1)
                    else:
                        vec.append(0)
                count += 1
                db.bilingualvec.insert({"word":j.lower(),"vec":vec,"lang_origin":lang_origin,"lang_target":lang_target})
                print "NEW INSERTS:"+str(count)

def translate_word(word,lang_target):
    client = MongoClient("localhost", 27017)
    db = client["nlprokz"]
    elem = db.bilingualvec.find_one({"word":word})
    elem_vec = np.array(elem["vec"])
    max_index = elem_vec.argsort()[-5:][::-1]
    for i in max_index:
        words = sorted(db.hinglish.find({"lang":lang_target}).distinct("words"))
        print words[i]


def find_closest(lang_origin,lang_target):
    client = MongoClient("localhost", 27017)
    db = client["nlprokz"]
    target_words = []
    target_words_strings = []
    for i in db.bilingualvec.find({"lang_origin":lang_target}):
        target_words.append(i['vec'])
        target_words_strings.append(i['word'])

    target_words = np.transpose(np.array(target_words))
    target_words =  target_words/ np.linalg.norm(target_words)

    for i in db.bilingualvec.find({"lang_origin":lang_origin}):
        origin_word = np.array([i['vec']])/np.linalg.norm([i['vec']])
        dot_product = np.dot(origin_word,target_words)
        max_similarity = np.argmax(dot_product[0])
        print "STRING:"+i['word']+":"+target_words_strings[max_similarity]



if __name__ == '__main__':
    find_closest("eng","hin")
    #translate_word("pitamah","hin")
    #dump_matrix("hin","hin")
    #dump_sentences()
