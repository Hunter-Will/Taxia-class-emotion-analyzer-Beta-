from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

TNUM=3

def Pretrain(bot):
    cnt=0
    Pretrainer=ListTrainer(bot)
    print("Pretraining")
    with open("./Data/PreTrainData.dat","r") as ptf:
        tl=ptf.readlines()
        Pretrainer.train(tl)
    sf=open("./Data/Selftrain.dat","r")
    sl=sf.readlines()
    sk=open("./Data/SelfKnowledge","r")
    for i in sk:
        if i[-1:]=='\n':
            i=i[:-1]
            a,b=i.split('=')
        for j,k in enumerate(sl):
            sl[j]=k.replace(a,b)
    for i in range(TNUM):        
        Pretrainer.train(sl)
    print("Finish pretraining")
    sl.close()
    sk.close()
    return
