from chatterbot.trainers import ChatterBotCorpusTrainer as cbt
import os

datapath="./Data/chinese/"

def train(bot):
    trainer=cbt(bot)
    trainer.train(datapath)
