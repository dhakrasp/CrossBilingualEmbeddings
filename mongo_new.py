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

if __name__ == '__main__':
    dump_glove_matrix("eng","eng")
