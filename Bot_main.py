### Require chatterbot
from Sentiment import SentimentVec
from preprocessor import cleanstop,chprocess
from chatterbot import ChatBot
from ResponseSelection import sentiment_response
import ChatTrain
import os
import sys

def inie():
    with open("./Data/SelfEom","w") as f:
        for i in range(10):
            f.write('0 ')
            
def Launch(rl=False):
    inie()
    if not os.path.isfile("database.db"):
        bot=ChatBot("bot1",
                    storage_adapter='chatterbot.storage.SQLStorageAdapter',
                    logic_adapters=['LogicAdapters.BasicAdapter'],
                    response_selection=sentiment_response,
                    database_uri='sqlite:///database.db',
        ) 
        ChatTrain.train(bot)
    else:
        bot=ChatBot("bot1",
                    read_only=rl,
                    storage_adapter='chatterbot.storage.SQLStorageAdapter',
                    logic_adapters=['LogicAdapters.BasicAdapter'],
                    response_selection=sentiment_response,
                    database_uri='sqlite:///database.db',
        )
    return bot

def Chat(bot):
    while True:
        try:
            s=input(">")
            r=bot.get_response(s)
            vec=SentimentVec(cleanstop(chprocess(s)))
            with open("./Data/SelfEom","r") as f:
                tmp=list(f.read().split())
                vec0=[]
                for i in tmp:
                    vec0.append(float(i))
            with open("./Data/SelfEom","w") as f:
                for i in range(len(vec0)):
                    vec0[i]+=vec[i]
                    vec0[i]-=vec0[i]*0.2
                    f.write(str(vec0[i])+' ')
            if(r.confidence>=0.9):
                with open("./Data/tmp/Conv.dat","a") as f:
                    f.write(s+'\n')
                    f.write(r.text+'\n')
            else:
                with open("./Data/default_resp.dat","a") as f:
                    f.write(s+'\n')
            print("bot:"+r.text)
        except:
            ChatTrain.train(bot,"./Data/tmp")
            break
        
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
        
        
