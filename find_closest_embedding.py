from common import *
from sklearn.metrics import pairwise_distances
from ranking import *

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
    target_words = np.transpose(np.array(target_words))
    target_words =  target_words/ np.linalg.norm(target_words, axis=0)
    
    count = 0
    for i in db.bilingualvec.find({"lang_origin":lang_origin}):
        origin_word = 1.0*np.array([i['vec']])
        origin_word = origin_word/np.sum(origin_word)
        origin_word = origin_word/norm_vector
        origin_word = origin_word/np.linalg.norm([origin_word])

        dot_product = np.dot(origin_word,target_words)
        max_index = dot_product.argsort()[-5:][::-1]
        for j in max_index[0][-5:]:
           print "STRING:"+i['word']+":"+target_words_strings[j]+":"+str(dot_product[0][j])
        count += 1
        if count > 10:
           break

if __name__ == '__main__':
    find_closest("eng","hin")