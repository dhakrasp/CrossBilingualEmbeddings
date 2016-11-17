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
	if elem_vec is None:
		print("Word " + word + " not found!")
		return
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
	target_words = np.transpose(np.array(target_words))
	target_words =  target_words/ np.linalg.norm(target_words, axis=0)
	

	count = 0
	for i in db.bilingualvec.find({"lang_origin":lang_origin}):
		origin_word = 1.0*np.array([i['vec']])
		origin_word = origin_word/np.sum(origin_word)
		origin_word = origin_word/norm_vector
		origin_word = origin_word/np.linalg.norm([origin_word])

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
		max_index = dot_product.argsort()[-5:][::-1]
		for j in max_index[0][-5:]:
		   print "STRING:"+i['word']+":"+target_words_strings[j]+":"+str(dot_product[0][j])
		# max_similarity = np.argmax(dot_product[0])
		# print "STRING:"+i['word']+":"+target_words_strings[max_similarity]+":"+str(dot_product[0][max_similarity])
		count += 1
		if count > 100:
		   break

def get_vector(word, lang_origin, lang_target):
	client = MongoClient("localhost", 27017)
	db = client["nlprokz"]
	word_entry = db.bilingualvec.find_one({"lang_origin":lang_origin, "word":word, "lang_target":lang_target})
	if word_entry is None:
		return None
	vec = 1.0*np.array(word_entry['vec'])
	vec = vec/np.linalg.norm(vec)
	return vec

def get_sentence_vector(sentence, lang_origin, lang_target):
	# lang_origin = "eng"
	# lang_target = "hin"
	sent_vector = None
	for word in sentence:
		word_vector = get_vector(word.lower(), lang_origin, lang_target)
		if word_vector is not None:
			if sent_vector is None:
				sent_vector = word_vector
			else:
				sent_vector += word_vector
	if sent_vector is not None:
		# print("Normalising...")
		sent_vector = sent_vector/np.linalg.norm(sent_vector)
	return sent_vector


def get_sentences(filename):
	sentences = []
	f = open(filename)
	lines = f.readlines()
	f.close()
	i = 0
	for line in lines[1:]:
		grams = re.split(r'\s',line.strip().replace("\\"," "))
		id = grams[0]
		temp = grams[1:]
		sentence = temp[::2]
		sentences.append(sentence)
		i += 1
	return sentences

def get_sentence_matrix(sentences, lang_origin, lang_target):
	matrix = []
	c = 0
	for s in sentences:
		sent_vector = get_sentence_vector(s, lang_origin, lang_target)
		if sent_vector is None:
			print("Sentence vetor not found.")
			print "%s"%" ".join(s)
		else:
			matrix.append(sent_vector)
		c += 1
		if c > 100:
			break
	return matrix


def align_sentences(filename1, filename2):
	eng_sentences = get_sentences(filename1)
	hin_sentences = get_sentences(filename2)
	alignment = []
	similarity = []
	count = 0

	hin_sentences = get_sentences(filename2)
	eng_sentences = get_sentences(filename1)
	hm = get_sentence_matrix(hin_sentences, "hin", "hin")
	hm = np.transpose(hm)
	em = get_sentence_matrix(eng_sentences, "eng", "hin")
	corr = np.dot(em, hm)
	l = corr.shape
	acc = 0.0
	for i in range(0, l[1]):
		j = np.argmax(corr[i])
		print(eng_sentences[i])
		hs = hin_sentences[j]
		if i == j:
			acc += 1.0
		print("%s"%" ".join(hs))
		print('_'*30)
	print(100*acc/l[1])

	# for e in eng_sentences[1:]:
	# 	best_sim =  0
	# 	best_in = 0
	# 	eng_sent_vec = get_sentence_vector(e, "eng", "hin")
	# 	if eng_sent_vec is None:
	# 		# print("English sentence vector not generated!")
	# 		continue
	# 	index = 0
	# 	hin_mat = []
	# 	for h in hin_sentences:
	# 		hin_sent_vec = get_sentence_vector(h, "hin", "hin")
	# 		if hin_sent_vec is not None:
	# 			hin_mat.append(hin_sent_vec)

	# 		dot_product = np.dot(eng_sent_vec,np.transpose(hin_sent_vec))
	# 		if dot_product > best_sim:
	# 			best_sim = dot_product
	# 			best_in = index
	# 		index += 1
	# 	alignment.append(best_in)
	# 	similarity.append(best_sim)
	# 	print(e)
	# 	print(hin_sentences[best_in])
	# 	print("\n" + '-'*30 + "\n")
	# 	count += 1
	# 	if count > 2:
	# 		break

	# for i in xrange(len(eng_sentences)):
	# 	print(eng_sentences[i])
	# 	j = alignment[i]
	# 	print(hin_sentences[j])



if __name__ == '__main__':
	# dump_sentences()
	# dump_matrix("eng","hin")
	# dump_matrix("hin","hin")
	# find_closest("eng","hin")
	# translate_word("hill","hin")

	# lang_origin = "eng"
	# lang_target = "hin"
	# sentence = ['Train', 'runs', 'fast', '.']
	# sent_vector = get_sentence_vector(sentence, lang_origin, lang_target)
	# print(sent_vector)
	filename1 = 'Corpus/test/eng_tourism_set03.txt'
	filename2 = 'Corpus/test/hin_tourism_set03.txt'
	align_sentences(filename1, filename2)
	# hin_sentences = get_sentences(filename2)
	# eng_sentences = get_sentences(filename1)
	# hm = get_sentence_matrix(hin_sentences, "hin", "hin")
	# em = get_sentence_matrix(eng_sentences, "eng", "hin")
	# print(m)
