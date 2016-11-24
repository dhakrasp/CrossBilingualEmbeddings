import gensim, logging
from sklearn.neural_network import MLPRegressor
import sys
import numpy as np
from operator import itemgetter
falign=open(sys.argv[1])
ftext=open(sys.argv[2])
dict_words={}
for align,line in zip(falign,ftext):
	line=line.strip().split("|||")
	x=line[0].strip().split()
	y=line[1].strip().split()
	align=align.strip().split()
	#line[0],line[1] two parallel lines
	for a in align:
		a = a.split("-")
		if x[int(a[0])] not in dict_words.keys():
			dict_words[x[int(a[0])]] = {}
			dict_words[x[int(a[0])]][y[int(a[1])]] = 1.0
		else:
			if y[int(a[1])] not in dict_words[x[int(a[0])]].keys() :
				dict_words[x[int(a[0])]][y[int(a[1])]] = 1.0
			else:
				dict_words[x[int(a[0])]][y[int(a[1])]]+=1.0
falign.close()
ftext.close()
#f_x=open(sys.argv[3]+".input","w")
#f_y=open(sys.argv[4]+".output","w")
model_s=gensim.models.Word2Vec.load(sys.argv[3]+".model")
model_t=gensim.models.Word2Vec.load(sys.argv[4]+".model")
list_of_word_x=[]
list_of_word_y=[]
for k,v in dict_words.items():
	tot=0
	list_w=[]
	for m,n in v.items():
		tot+=n
	for m,n in v.items():
		n=n/tot
		list_w.append([m,n])
		#print k,m,n
	#take top 5 words in t if they exist other wise take how many are there
	list_w=sorted(list_w,key=itemgetter(1),reverse=True)
	if len(list_w)>5:
		rangea=5
	else:
		rangea=len(list_w)
	for i in range(rangea):
		x_val=[]
		y_val=[]
		for valx,valy in zip(model_s[k],model_t[list_w[i][0]]):
			x_val.append(valx)
			y_val.append(valy)
		x_val.append(i)
		y_val.append(list_w[i][1])
		list_of_word_x.append(x_val)
		list_of_word_y.append(y_val)
		#f_x.write("%s\n" % x_val)
		#f_y.write("%s\n" % y_val)
#f_x.close()
#f_y.close()
#exit()
clf = MLPRegressor(solver='lbfgs', activation='tanh',alpha=1e-5,hidden_layer_sizes=(17), random_state=1,learning_rate='adaptive')
clf.fit(list_of_word_x,list_of_word_y)
f_x_test=open(sys.argv[5])
f_y_test_output=open(sys.argv[7],"w")
line_output_y=[]
for line in f_x_test:
	line=line.strip().split()
	for word in line:
		po=[]
		if word not in model_s.vocab:
			continue
		for x in model_s[word]:
			po.append(x)
		po.append(0)#can introduce another loop to get values 1-5
		output=clf.predict([po])
		line_output_y.append(output)
for y in line_output_y:
	f_y_test_output.write("%s\n"%y)
f_y_test_output.close()
#model_s=gensim.models.Word2Vec.load(sys.argv[3]+".model")
#model_t=gensim.models.Word2Vec.load(sys.argv[4]+".model")
'''
po=[]
for x in model_s['can']:
	po.append(x)
po.append(0)
output=clf.predict([po])
op=output[0][:-
yt=[]
for x in op:
	yt.append(x)
op=model_t.most_similar(positive=yt, topn=1)
print op
'''
exit()
