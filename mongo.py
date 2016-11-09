import glob
import os
import re
import numpy as np
from pymongo import MongoClient
from pymongo import UpdateOne
from sklearn.metrics import pairwise_distances
from ranking import *

def dump_sentences():
    client = MongoClient('localhost', 27017)
    db = client['nlprokz']
    hinglish = db.hinglish
    count = 0
#    for root, dirs, files in os.walk('Corpus/Hindi_English/'):
    for root, dirs, files in os.walk('Corpus/small/'):
        for basename in files:
            filename = os.path.join(root, basename)
            print(filename)
            bulk_grams = []
            flag = False
            for line in open(filename):
                if not flag:
                    flag = True
                    continue
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
                db.bilingualvec.update_one({"word":j.lower()},{"$set":{"vec":vec,"lang_origin":lang_origin,"lang_target":lang_target}})
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

    target_words = []
    for i in db.bilingualvec.find({"lang_origin":lang_target}):
        target_words.append(i['vec'])

    target_words = np.array(target_words)
    norm_vector = 1.0*np.sum(target_words,axis=0)    
    
    elem = db.bilingualvec.find_one({"word":word})
    elem_vec = np.array(elem["vec"])/norm_vector
    max_index = elem_vec.argsort()[-10:][::-1]
    words = sorted(db.hinglish.find({"lang":lang_target}).distinct("words"))
    print(max_index)
    for i in max_index:
        print(words[i] + " " + str(i) + " " + str(elem_vec[i]))


def find_closest(lang_origin,lang_target):
    client = MongoClient("localhost", 27017)
    db = client["nlprokz"]
    target_words = []
    target_words_strings = []
    for i in db.bilingualvec.find({"lang_origin":lang_target}):
        target_words.append(i['vec'])
        target_words_strings.append(i['word'])

    words = sorted(db.hinglish.find({"lang":lang_target}).distinct("words"))

    norm_vector = 1.0*np.sum(target_words,axis=0)
    target_words =  target_words/(norm_vector)
    target_words =  target_words/(norm_vector)
    target_words =  target_words/ np.linalg.norm(target_words)
    target_words = np.transpose(np.array(target_words))

    count = 0
    for i in db.bilingualvec.find({"lang_origin":lang_origin}):
        origin_word = 1.0*np.array([i['vec']])
        origin_word = origin_word/np.sum(origin_word)
        origin_word = origin_word/norm_vector
        origin_word = origin_word/np.linalg.norm([i['vec']])

        # dist = []
        # for word_vec in target_words:
        #     word_vec = np.transpose(word_vec)
        #     dist.append(euclidean(origin_word, word_vec))
        # max_similarity = np.argmax(dist[0])
        # print "STRING:"+i['word']+":"+target_words_strings[max_similarity]
        # count += 1
        # if count > 10:
        #    break

        dot_product = np.dot(origin_word,target_words)
        max_index = dot_product.argsort()[-1:][::-1]
        for j in max_index[0][-10:]:
           print "STRING:"+i['word']+":"+target_words_strings[j]+":"+str(dot_product[0][j])
        # max_similarity = np.argmax(dot_product[0])
        # print "STRING:"+i['word']+":"+target_words_strings[max_similarity]+":"+str(dot_product[0][max_similarity])
        count += 1
        if count > 10:
           break
if __name__ == '__main__':
    # dump_sentences()
    # dump_matrix("eng","hin")
    # dump_matrix("hin","hin")
    # find_closest("eng","hin")
    translate_word("prays","hin")
