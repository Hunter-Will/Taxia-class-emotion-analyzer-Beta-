from chatterbot.trainers import ChatterBotCorpusTrainer as cbt
from Doc2vec_train import retrain
import os

def train(bot,datapath="./Data/chinese"):
    trainer=cbt(bot)
    trainer.train(datapath)
    if os.isdir(datapath):
        for rt,dirs,files in os.walk(datapath):
            for f in files:
                retrain(os.path.join(rt,f))
