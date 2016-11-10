from pymongo import MongoClient

import numpy as np

def dump_glove_matrix(lang_origin,lang_target):
    client = MongoClient('localhost', 27017)
    db = client['nlprokz']
    words = sorted(db.hinglish.find({"lang":lang_target}).distinct("words"))
    count = 0
    count_update = 0
    for i in db.hinglish.find({"lang":lang_origin}):
        try:
            target_sentence = db.hinglish.find_one({"identifier":i['identifier'],"lang":lang_target})
            bulk_vec = []
            for j in i["words"]:
                vec_count = db.bilingual_glove_vec.count({"word":j.lower()})
                if vec_count > 0:
                    doc = db.bilingual_glove_vec.find_one({"word":j.lower()})
                    vec = np.array(doc["vec"])
                    norm = doc['norm_count']
                    flag = False
                    for k in xrange(len(words)):
                        if words[k] in target_sentence["words"]:
                            glove = db.glove.find_one({"gram":words[k]})
                            if glove is not None:
                                glove_vec = [ float(t) for t in glove['glove_vector']]
                                vec += np.array(glove_vec)
                                norm += 1
                                flag = True

                    if flag:
                        count_update += 1
                        db.bilingual_glove_vec.update({"word":j.lower()},{"$set":{"vec":vec.tolist(),"norm_count":norm,"lang_origin":lang_origin,"lang_target":lang_target}})

                else:
                    vec = np.zeros(300)
                    norm = 0
                    flag = False
                    for k in words:
                        if k in target_sentence["words"]:
                            glove = db.glove.find_one({"gram":k})
                            if glove is not None:
                                glove_vec = [ float(t) for t in glove['glove_vector']]
                                vec += np.array(glove_vec)
                                norm += 1
                                flag = True

                    if flag:
                        count += 1
                        db.bilingual_glove_vec.insert({"word":j.lower(),"norm_count":norm,"vec":vec.tolist(),"lang_origin":lang_origin,"lang_target":lang_target})

                    print "NEW INSERTS:"+str(count)
        except Exception as e:
            print e

def find_closest(lang_origin,lang_target):
    client = MongoClient("localhost", 27017)
    db = client["nlprokz"]
    target_words = []
    target_words_strings = []
    for i in db.bilingual_glove_vec.find({"lang_origin":lang_target}):
        target_words.append(i['vec'])
        target_words_strings.append(i['word'])

    words = sorted(db.hinglish.find({"lang":lang_target}).distinct("words"))

    target_words = np.transpose(np.array(target_words))
    target_words =  target_words/ np.linalg.norm(target_words,axis = 0)

    count = 0
    for i in db.bilingual_glove_vec.find({"lang_origin":lang_origin}):
        origin_word = 1.0*np.array([i['vec']])
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
           print "STRING %s: %s : %s" % (i['word'],target_words_strings[j],str(dot_product[0][j]))
        # max_similarity = np.argmax(dot_product[0])
        # print "STRING:"+i['word']+":"+target_words_strings[max_similarity]+":"+str(dot_product[0][max_similarity])
        count += 1
        if count > 10:
           break

if __name__ == '__main__':
    #dump_glove_matrix("eng","eng")
    find_closest("hin","eng")
