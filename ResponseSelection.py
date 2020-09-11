from Sentiment import VecCos,SentimentVec,VEC0
from random import choice

CONLIMIT=0.9

def sentiment_response(input_statement,respslist):
    f=open("./Data/emotion.dat","r")
    vec=list(f.read().split())
    f.close()
    resv=VEC0
    res=input_statement
    vcos=0
    vcos1=0
    l=[]
    for resp in respslist:
        v2=SentimentVec(resp)
        vcos1,a,b=VecCos(vec,v2)
        if vcos<=vcos1:
            resv=v2
            res=resp
            vcos=vcos1
        if vcos1>=CONLIMIT:
            l.append(resp)
    if l.empty():
        res.confidence=vcos1
        return res
    res=choice(l)
    res.confidence=VecCos(vec,SentimentVec(res))
    return res
        

