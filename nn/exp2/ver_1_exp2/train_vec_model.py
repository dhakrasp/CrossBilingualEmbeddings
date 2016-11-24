import gensim, logging
import sys
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
f_s=open(sys.argv[1])
f_t=open(sys.argv[2])
def make_w2v(f_s,f_t):
	line_s=[]
	for line in f_s:
		line=line.strip().split()
		line_s.append(line)
	line_t=[]
	for line in f_t:
		line=line.strip().split()
		line_t.append(line)
	f_s.close()
	f_t.close()
	model_s = gensim.models.Word2Vec(line_s,size=100, window=5, min_count=1, workers=4)
	model_t = gensim.models.Word2Vec(line_t,size=100, window=5, min_count=1, workers=4)
	model_s.save(sys.argv[1]+".model")
	model_t.save(sys.argv[2]+".model")
make_w2v(f_s, f_t)