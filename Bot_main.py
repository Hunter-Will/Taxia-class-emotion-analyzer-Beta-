### Require chatterbot

from chatterbot import ChatBot
import ChatTrain
import os

###========main=========
if __name__=="__main__" :
    if not os.path.isfile("database.db"):
        bot=ChatBot("bot1",
                    storage_adapter='chatterbot.storage.SQLStorageAdapter',
                    logic_adapters=['LogicAdapters.BasicAdapter'],
                    database_uri='sqlite:///database.db',
        ) 
        ChatTrain.train(bot)
    else:
        bot=ChatBot("bot1",
                    storage_adapter='chatterbot.storage.SQLStorageAdapter',
                    logic_adapters=['LogicAdapters.BasicAdapter'],
                    database_uri='sqlite:///database.db',
        ) 
    while True:
        s=input(">")
        r=bot.get_response(s)
        print("bot:"+r.text)
        
        
