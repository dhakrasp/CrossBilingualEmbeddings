# CrossBilingualEmbeddings
A NLP team project for finding the cross bilingual embeddings (dictionary) for English and Hindi.

Hinton[4] gave a hint towards learning distributed representations for symbolic input which was explored in Bengio[5] paper to create neural network based probabilistic language model, this distributed representation led to word2vec[6]. These developments led to usage of vectors as representations for textual data. Word2vec, phrase2vec, doc2vec were all the resultant tools. In simple form word2vec model gives vector representations of words depending on their context in data (on which model is trained). Now this model creates a sort of complex multidimensional space for all vectors (words) of particular language.

These are said to be feature embeddings of words in specific language. Now if we have some sort of vector space in which there are vector representations of two different languages. Than that is said to cross bilingual embeddings. One thing to note is that these embedding are not found directly by say training word2vec model on data containing data from both languages. Bilingual embeddings mean that feature vectors of words for both languages will exist in a certain meaningful way. 

Examples for bilingual embeddings :
Words like run and दौड़ना in bilingual embedding setting will have vector representations which will be very closed or these two vectors can be mapped to each other through some transformation function.
Word like book can have vector in some place in between vector points of किताब and दर्ज in this bilingual settings.


# References 

[1] GloVe: Global Vectors for Word Representation -- Jeffrey Pennington,   Richard Socher,   Christopher D. Manning http://nlp.stanford.edu/projects/glove/


[2] Bilingual Word Embeddings from Parallel and Non-parallel Corpora for Cross-Language Text Classification -- Aditya Mogadala, Achim Rettinger https://www.aclweb.org/anthology/N/N16/N16-1083.pdf


[3] Bilingual Word Embeddings for Phrase-Based Machine Translation -- Will Y. Zou† , Richard Socher, Daniel Cer, Christopher D. Manning http://ai.stanford.edu/~wzou/emnlp2013_ZouSocherCerManning.pdf 


[4] Hinton, Geoffrey E. "Learning distributed representations of concepts." Proceedings of the eighth annual conference of the cognitive science society. Vol. 1. 1986.
http://www.cogsci.ucsd.edu/~ajyu/Teaching/Cogs202_sp13/Readings/hinton86.pdf


[5] Bengio, Yoshua, et al. "A neural probabilistic language model." journal of machine learning research 3.Feb (2003): 1137-1155.
http://www.jmlr.org/papers/volume3/bengio03a/bengio03a.pdf


[6] Mikolov, Tomas, et al. "Efficient estimation of word representations in vector space." arXiv preprint arXiv:1301.3781 (2013).
https://arxiv.org/abs/1301.3781
[7] Dyer, Chris, et al. "cdec: A decoder, alignment, and learning framework for finite-state and context-free translation models." Proceedings of the ACL 2010 System Demonstrations. Association for Computational Linguistics, 2010.
http://cs.jhu.edu/~jonny/pub/P10-4002.pdf

