import Doc2vec_train
import gensim.models
from os import path

if not path.isfile("Doc2Vec"):
    model=Doc2vec_train.newmodel("./testdata")
else:
    model=gensim.models.load("./Doc2Vec")    

def vecl(words):
    v=model.infer_vector(words)
    return v
