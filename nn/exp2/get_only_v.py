import sys
fopen_s=open(sys.argv[1])
fopen_t=open(sys.argv[2])
fopen_s_v=open(sys.argv[1]+"_verb_only","w")
fopen_t_v=open(sys.argv[2]+"_verb_only","w")
def return_v(temp):
	oneline=[]
	for word_pos in temp:
		word_pos=word_pos.split('\\')
		if word_pos[1]=="":
			continue
		if word_pos[1][0]=='V':
			oneline.append(word_pos[0])
	return " ".join(oneline)

for line_s,line_t in zip(fopen_s,fopen_t):
	temp_s=line_s.strip().split()
	temp_t=line_t.strip().split()
	oneline_s=return_v(temp_s)
	oneline_t=return_v(temp_t)
	print oneline_s,oneline_t
	fopen_s_v.write(oneline_s)
	fopen_s_v.write("\n")
	fopen_t_v.write(oneline_t)
	fopen_t_v.write("\n")
fopen_s.close()
fopen_t.close()
fopen_s_v.close()
fopen_t_v.close()