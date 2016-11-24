import os
import re
import numpy as np
from pymongo import MongoClient
from pymongo import UpdateOne
from pymongo.collection import Collection
from ranking import *

def dump_sentences(collection_name, path):
	client = MongoClient('localhost', 27017)
	db = client['nlprokz']
	collection = Collection(db, collection_name)
	count = 0
	# for root, dirs, files in os.walk('Corpus/small/'):
	for root, dirs, files in os.walk(path):
		for basename in files:
			filename = os.path.join(root, basename)
			print(filename)
			lang = basename.split('_')[0]
			print(lang)
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
				# if "eng" in filename:
				# 	lang = "eng"
				# else:
				# 	lang = "hin"
				bulk_grams.append({"identifier":id,"lang":lang,"words":words,"pos_tags":pos_tags})
			count += len(bulk_grams)
			print 'Inserted '+str(count)
			collection.insert_many(bulk_grams)
	collection.remove({"identifier":"ID"})

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

def dump_matrix(lang_origin,lang_target, sent_coll_name, vec_coll_name):
	client = MongoClient('localhost', 27017)
	db = client['nlprokz']
	sent_coll = Collection(db, sent_coll_name)
	vec_coll = Collection(db, vec_coll_name)
	words = sorted(sent_coll.find({"lang":lang_target}).distinct("words"))
	count = 0
	count_update = 0
	for i in sent_coll.find({"lang":lang_origin}):
		hindi_sentence = sent_coll.find_one({"identifier":i['identifier'],"lang":lang_target})
		bulk_vec = []
		for j in i["words"]:
			vec_count = vec_coll.count({"word":j.lower()})
			if vec_count > 0:
				doc = vec_coll.find_one({"word":j.lower()})
				vec = doc["vec"]
				for k in xrange(len(words)):
					if words[k] in hindi_sentence["words"]:
						vec[k] += 1
				count_update += 1
				#print "INSERTS:"+str(count_update)
				vec_coll.update_one({"word":j.lower()},{"$set":{"vec":vec,"lang_origin":lang_origin,"lang_target":lang_target}})
			else:
				vec = []
				for k in words:
					if k in hindi_sentence["words"]:
						vec.append(1)
					else:
						vec.append(0)
				count += 1
				vec_coll.insert({"word":j.lower(),"vec":vec,"lang_origin":lang_origin,"lang_target":lang_target})
				print(lang_origin+ " : " + lang_target + " : NEW INSERTS:"+str(count))

if __name__ == '__main__':
	sent_coll_name = "hinglish"
	path = 'Corpus/small/'
	vec_coll_name = "bilingualvec"
	dump_sentences(sent_coll_name, path)
	dump_matrix("eng","hin", sent_coll_name, vec_coll_name)
	dump_matrix("hin","hin", sent_coll_name, vec_coll_name)