import glob
import os
import re
import numpy as np
from pymongo import MongoClient
from pymongo import UpdateOne
from pymongo.collection import Collection
from sklearn.metrics import pairwise_distances
from ranking import *

def get_word_vector(word, lang_origin, lang_target, collection):
	word_entry = collection.find_one({"lang_origin":lang_origin, "word":word, "lang_target":lang_target})
	if word_entry is None:
		return None
	vec = 1.0*np.array(word_entry['vec'])
	vec = vec/(np.linalg.norm(vec)+0.001)
	return vec

def get_sentence_vector(sentence, lang_origin, lang_target, collection):
	sent_vector = None
	for word in sentence:
		word_vector = get_word_vector(word.lower(), lang_origin, lang_target, collection)
		if word_vector is not None:
			if sent_vector is None:
				sent_vector = word_vector
			else:
				sent_vector += word_vector
	if sent_vector is not None:
		# print("Normalising...")
		sent_vector = sent_vector/(np.linalg.norm(sent_vector)+0.001)
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

def get_sentence_matrix(sentences, lang_origin, lang_target, collection):
	matrix = []
	c = 0
	for s in sentences:
		sent_vector = get_sentence_vector(s, lang_origin, lang_target, collection)
		if sent_vector is None:
			print("Sentence vetor not found.")
			print "%s"%" ".join(s)
		else:
			matrix.append(sent_vector)
		c += 1
	return matrix


def align_sentences(filename1, filename2, collection_name):
	client = MongoClient("localhost", 27017)
	db = client["nlprokz"]
	coll = Collection(db, collection_name)

	target_sents = get_sentences(filename2)
	origin_sents = get_sentences(filename1)

	basename = filename1.split('/')[-1]
	lang_origin = basename.split('_')[0]
	basename = filename2.split('/')[-1]
	lang_target = basename.split('_')[0]

	print(lang_origin+"----->"+lang_target)

	target_mat = get_sentence_matrix(target_sents, lang_target, "hin", coll)
	target_mat = np.transpose(target_mat)
	orgin_mat = get_sentence_matrix(origin_sents, lang_origin, "hin", coll)
	corr = np.dot(orgin_mat, target_mat)
	l = corr.shape
	acc = 0.0
	for i in range(0, l[1]):
		j = np.argmax(corr[i])
		print("%s"%" ".join(origin_sents[i]))
		if i == j:
			acc += 1.0
		print("%s"%" ".join(target_sents[j]))
		print(corr[i][j])
		print('_'*50)
	print(100*acc/l[1])

if __name__ == '__main__':
	filename1 = 'Corpus/Test/eng_tourism_set04.txt'
	filename2 = 'Corpus/Test/hin_tourism_set04.txt'
	align_sentences(filename1, filename2, 'bilingualvec')