import gensim.models
import smart_open
from preprocessor import chprocess

def read_corpus(fname,tokens_only=False):
    with smart_open.open(fname,encoding="utf-8") as f:
        for i,line in enumerate(f):
            tokens=chprocess(line)
            if tokens_only:
                yield tokens
            else:
                yield gensim.models.doc2vec.TaggedDocument(tokens,[i])

def newmodel(fname,vsize=500,mcnt=2,epch=20):
    train_data=list(read_corpus(fname))
    model=gensim.models.doc2vec.Doc2Vec(vector_size=vsize,min_count=mcnt,epochs=epch)
    model.build_vocab(train_data)
    print("Training...")
    model.train(train_data,total_examples=model.corpus_count,epochs=model.epochs)
    print("Training finished")
    model.save("./Doc2Vec")
    return model
def retrain(fname,vsize=500,mcnt=2,epch=20):
    train_data=list(read_corpus(fname))
    model=gensim.models.doc2vec.Doc2Vec
