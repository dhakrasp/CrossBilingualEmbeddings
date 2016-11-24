from common import *
from sklearn.metrics import pairwise_distances
from ranking import *

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
    if elem_vec is None:
        print("Word " + word + " not found!")
        return
    max_index = elem_vec.argsort()[-5:][::-1]
    words = sorted(db.hinglish.find({"lang":lang_target}).distinct("words"))
    for i in max_index:
        print(words[i] + " " + str(i) + " " + str(elem_vec[i]))

if __name__ == '__main__':
    translate_word("fountain","hin")
