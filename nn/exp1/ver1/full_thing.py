import os
#os.system("python train_vec_model.py train.en train.hi")
#os.system("~/Decoder/cdec/corpus/paste-files.pl train.en train.hi > en_hi")
#os.system("~/Decoder/cdec/word-aligner/fast_align -i en_hi -v -o > cor.fwd_align")#option of -d can be done on a different version to see the effect
#os.system("~/Decoder/cdec/word-aligner/fast_align -i en_hi -r -v -o > cor.rev_align")
#os.system("~/Decoder/cdec/utils/atools -i cor.fwd_align -j cor.rev_align -c grow-diag-final-and > cor.gdfa")
os.system("python nn.py cor.gdfa en_hi train.en train.hi test.en test.hi output_values")


