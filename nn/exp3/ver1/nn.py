import gensim, logging
#from sklearn.neural_network import MLPRegressor
import sys
import numpy as np
from scipy import spatial
from operator import itemgetter
import datetime
now = datetime.datetime.now()
time=str(now.hour)+"_"+str(now.minute)+"_"+str(now.second)+"-"+str(now.day)+"_"+str(now.month)+"_"+str(now.year)
#print time
#exit()
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
model_s=gensim.models.Word2Vec.load(sys.argv[3]+".model")
model_t=gensim.models.Word2Vec.load(sys.argv[4]+".model")

list_of_word_x=[]
list_of_word_y=[]
cheat_list={}
flag=1
for k,v in dict_words.items():
	tot=0
	list_w=[]
	for m,n in v.items():
		tot+=n
	for m,n in v.items():
		n=n/tot
		list_w.append([m,n])
		#print k,m,n
	list_w=sorted(list_w,key=itemgetter(1),reverse=True)
	rangea=1
	cheat_list[k]={list_w[0][0]}
	for i in range(rangea):
		x_val=[]
		y_val=[]
		for valx,valy in zip(model_s[k],model_t[list_w[i][0]]):
			x_val.append(valx)
			y_val.append(valy)
		list_of_word_x.append(x_val)
		list_of_word_y.append(y_val)
		#if flag==1:
		#	break
	#if flag==1:
	#	break
print list_of_word_x,list_of_word_y
exit()
clf = MLPRegressor(verbose=True,solver='lbfgs',max_iter=4000, activation='tanh',alpha=1e-5,hidden_layer_sizes=(500), random_state=1,learning_rate='adaptive')
'''
list_of_word_x=[]
list_of_word_y=[]

for line in ftext:
	line=line.strip().split('|||')
	l=line[1].strip().split()
	break
x_word=[]	
x_val=model_s['Foreign']
x_word.append('Foreign')
y_val=model_t[l[0]]
list_of_word_x.append(x_val)
list_of_word_y.append(y_val)
x_val=model_s['media']
x_word.append('media')
y_val=model_t[l[1]]
list_of_word_x.append(x_val)
list_of_word_y.append(y_val)
x_val=model_s['here']
x_word.append('here')
y_val=model_t[l[7]]
list_of_word_x.append(x_val)
list_of_word_y.append(y_val)
x_val=model_s['is']
x_word.append('is')
y_val=model_t[l[3]]
list_of_word_x.append(x_val)
list_of_word_y.append(y_val)
x_val=model_s['and']
x_word.append('and')
y_val=model_t[l[8]]
list_of_word_x.append(x_val)
list_of_word_y.append(y_val)
'''
clf.fit(list_of_word_x,list_of_word_y)
'''
for word,vec_x,vec_y in zip(x_word,list_of_word_x,list_of_word_y):
	output=clf.predict(vec_x)
	#print output,y_val
	kyun=[]
	for i in output:
		kyun.append(i)
	model_word_vector = np.array( kyun, dtype='f')
	op_word= model_t.most_similar(output, topn=1)
	for j in op_word:
		print j[0],word
	#t_w=j[0]

'''
f_x_test=open(sys.argv[3])
f_y_test=open(sys.argv[4])
#f_y_test_output=open(sys.argv[7]+time,"w")
line_output_y=[]
count=0
done_words=[]
count=0
tot=0
predicted=[]
actual=[]
s_word=[]
print "sssssssssssssssssssssssssss"
for line in f_x_test:
	line=line.strip().split()
	flag=1
	for word in line:
		count+=1
		po=[]
		if word not in model_s.vocab and word not in cheat_list:
			flag=0
			continue
		if word in done_words:
			continue			
		done_words.append(word)
		for x in model_s[word]:
			po.append(x)
		output=clf.predict([po])
		line_output_y.append(output)
		if word in model_s.vocab and word in cheat_list:
			ref=[]
			cheat_list[word]=list(cheat_list[word])
			
			for x in cheat_list[word]:
				ref.append(x)
			x="".join(x)	
			hin_ref=model_t[x]
			op=output[0]
			kyun=[]
			for i in op:
				kyun.append(i)
			model_word_vector = np.array( kyun, dtype='f')
			op_word= model_t.most_similar([model_word_vector], topn=1)
			for j in op_word:
				if j[0]==x:
					print word,j[0],x
				t_w=j[0]
			predicted.append(t_w)
			s_word.append(word)
			actual.append(x)
		#break
	#break
			
count=0
tot=0
for ref,out in zip(actual,predicted):
	if ref==out:
		count+=1
	#f_y_test_output.write(ref
	#print ref,out
	tot+=1
print count,tot

