import os
import sys
#os.system("python train_vec_model.py "+sys.argv[1]+" "+sys.argv[2])
#os.system("~/Decoder/cdec/corpus/paste-files.pl "+sys.argv[1]+" "+sys.argv[2]+" > combine_"+sys.argv[1]+"_"+sys.argv[2])
temp="combine_"+sys.argv[1]+"_"+sys.argv[2]
#os.system("~/Decoder/cdec/word-aligner/fast_align -i "+temp+" -v -o > "+temp+".fwd_align")#option of -d can be done on a different version to see the effect
#os.system("~/Decoder/cdec/word-aligner/fast_align -i "+temp+" -r -v -o > "+temp+".rev_align")
#os.system("~/Decoder/cdec/utils/atools -i "+temp+".fwd_align -j "+temp+".rev_align -c grow-diag-final-and > "+temp+".gdfa")
os.system("python nn.py "+temp+".gdfa combine_"+sys.argv[1]+"_"+sys.argv[2]+" "+sys.argv[1]+" "+sys.argv[2]+" "+sys.argv[3]+" "+sys.argv[4]+" "+sys.argv[5]+"")


