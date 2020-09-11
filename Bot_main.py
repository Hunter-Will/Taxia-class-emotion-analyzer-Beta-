### Require chatterbot

from chatterbot import ChatBot
import ChatTrain
import os
import sys

def inie():
    with open("./Data/SelfEom","r") as f:
        for i in range(10):
            f.write('0 ')
            
def Launch(rl=False):
#    inie()
    if not os.path.isfile("database.db"):
        bot=ChatBot("bot1",
                    storage_adapter='chatterbot.storage.SQLStorageAdapter',
                    logic_adapters=['LogicAdapters.BasicAdapter'],
                    database_uri='sqlite:///database.db',
        ) 
        ChatTrain.train(bot)
    else:
        bot=ChatBot("bot1",
                    read_only=rl,
                    storage_adapter='chatterbot.storage.SQLStorageAdapter',
                    logic_adapters=['LogicAdapters.BasicAdapter'],
                    database_uri='sqlite:///database.db',
        )
    return bot

def Chat(bot):
    while True:
        s=input(">")
        r=bot.get_response(s)
        ##if r.confidence>0.8:
        with open("./Data/tmp/Conv.dat","a") as f:
            f.write(s+'\n')
            f.write(r.text+'\n')
        print("bot:"+r.text)

        
        
###========main=========
if __name__=="__main__" :
    try:
        f=sys.argv[1]
        if f=="run":
            rl=False
            try:
                s=sys.argv[2]
                if(s=="-s"):
                    rl=True
            except:
                pass
            finally:
                bot=Launch(rl)
                Chat(bot)
        elif f=="learn":
            try:
                s=sys.argv[2]
            except:
                s="./Data/tmp"
            finally:
                bot=Launch(rl)
                ChatTrain.train(bot,s)
        elif f=="help":
            print("run")
            print("    Launch the bot and start to chat with you")
            print(" -s Stop learning from the chat")
            print("learn filename")
            print("    Learn from the specific file -- 'filename'. If no filename input, bot will learn from the last conversation(if have)")
        else:
            print("We didn't have this command :(")
    except:
        rl=False
        try:
            s=sys.argv[1]
            if(s=="-s"):
                rl=True
        except:
            pass
        finally:
            bot=Launch(rl)
            Chat(bot)
        
        
