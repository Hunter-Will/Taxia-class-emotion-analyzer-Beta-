# Require chatterbot
from chatterbot import ChatBot
from ResponseSelection import sentiment_response
import ChatTrain
import os
import sys
import traceback


def new_bot_instance(rl=False):
    if not os.path.isfile("./Data/database.db"):
        bot = ChatBot(
            "bot1",
            storage_adapter='chatterbot.storage.SQLStorageAdapter',
            logic_adapters=['LogicAdapters.BasicAdapter'],
            response_selection=sentiment_response,
            database_uri='sqlite:///./Data/database.db',
        )
        ChatTrain.train(bot)
    else:
        bot = ChatBot(
            "bot1",
            read_only=rl,
            storage_adapter='chatterbot.storage.SQLStorageAdapter',
            logic_adapters=['LogicAdapters.BasicAdapter'],
            response_selection=sentiment_response,
            database_uri='sqlite:///./Data/database.db',
        )
    return bot


def launch(bot):
    while True:
        try:
            statement = input("> ")
            response = bot.get_response(statement)
            print("bot: " + response.text)
        except KeyboardInterrupt:
            break
        except:
            traceback.print_exc()


# ========main=========
if __name__ == "__main__":
    try:
        f = sys.argv[1]
        if f == "run":
            rl = False
            try:
                s = sys.argv[2]
                if(s == "-s"):
                    rl = True
            except:
                pass
            finally:
                bot = new_bot_instance(rl)
                launch(bot)
        elif f == "learn":
            try:
                s = sys.argv[2]
            except:
                s = "./Data/tmp"
            finally:
                bot = new_bot_instance(rl)
                ChatTrain.train(bot, s)
        elif f == "help":
            print("run")
            print("    Launch the bot and start to chat with you")
            print(" -s Stop learning from the chat")
            print("learn filename")
            print("    Learn from the specific file -- 'filename'. If no filename input, bot will learn from the last conversation(if have)")
        else:
            print("We didn't have this command :(")
    except:
        rl = False
        try:
            s = sys.argv[1]
            if(s == "-s"):
                rl = True
        except:
            pass
        finally:
            bot = new_bot_instance(rl)
            launch(bot)
