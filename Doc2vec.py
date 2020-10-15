from chatterbot.trainers import ChatterBotCorpusTrainer
import os
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from preprocessor import chprocess
import smart_open
import yaml

__model_path = "./Data/Doc2Vec"


def read_corpus(fname, tokens_only=False):
    ext = os.path.splitext(fname)[1]
    with smart_open.open(fname, encoding="utf-8") as f:
        if ext == "yml" or ext == "yaml":
            i = 0
            doc = yaml.load(f, Loader=yaml.FullLoader)
            for dialog in doc["conversations"]:
                for line in dialog:
                    tokens = chprocess(line)
                    if tokens_only:
                        yield tokens
                    else:
                        yield TaggedDocument(tokens, [i])
                        i = i + 1
        else:
            for i, line in enumerate(f):
                tokens = chprocess(line)
                if tokens_only:
                    yield tokens
                else:
                    yield TaggedDocument(tokens, [i])


def read_glob_corpus(fnames, tokens_only=False):
    for f in fnames:
        for doc in read_corpus(f, tokens_only):
            yield doc


def newmodel(fname, vsize=500, mcnt=2, epch=20):
    train_data = list(read_corpus(fname))
    model = Doc2Vec(
        vector_size=vsize, min_count=mcnt, epochs=epch)
    model.build_vocab(train_data)
    print("Training...")
    model.train(train_data, total_examples=model.corpus_count,
                epochs=model.epochs)
    print("Training finished")
    model.save(__model_path)
    return model


if not os.path.isfile(__model_path):
    model = newmodel("./Data/model_data/default.dat")
else:
    model = Doc2Vec.load(__model_path)


def vecl(words):
    v = model.infer_vector(words)
    return v


def train(fnames):
    if not isinstance(fnames, list):
        fnames = [fnames]

    train_data = list(read_glob_corpus(fnames))
    model.build_vocab(train_data, update=True)
    print("Training...")
    model.train(train_data, total_examples=model.corpus_count,
                epochs=model.epochs)
    print("Training finished")
    model.save(__model_path)
