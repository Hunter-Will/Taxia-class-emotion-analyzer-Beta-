from chatterbot.conversations import Statement
from Doc2vec import vecl
from preprocessor import chprocess
from math import sqrt

def VectorCmp(sta1,sta2):
    v1=vecl(chprocess(sta1.text))
    v2=vecl(chprocess(sta2.text))
    m1=m2=ans=0
    for i in range(len(v1)):
        ans+=v1[i]*v2[i]
        m1+=v1[i]*v1[i]
        m2+=v2[i]*v2[i]
    return ans/(sqrt(m1)*sqrt(m2))
    
