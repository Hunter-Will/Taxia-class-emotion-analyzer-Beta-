from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
import Doc2vec
import os
import Bot_main


def train(bot, datapath="./Data/corpus"):
    trainer = ChatterBotCorpusTrainer(bot)
    trainer.train(datapath)

    fnames = []
    if os.path.isdir(datapath):
        for rt, dirs, files in os.walk(datapath):
            for f in files:
                fnames.append(os.path.join(rt, f))

    Doc2vec.train(fnames)


if __name__ == "__main__":
    bot = Bot_main.new_bot_instance()
    train(bot)
