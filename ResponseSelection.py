from Sentiment import VecCos, SentimentVec, VEC0
from random import choice
from threading import RLock

CONLIMIT = 0.9

vec = [0.0] * 10
__lock = RLock()


def update(vec0):
    try:
        __lock.acquire()
        for i in range(len(vec)):
            vec[i] += vec0[i]
            vec[i] *= 0.8
    finally:
        __lock.release()


def sentiment_response(input_statement, respslist):
    try:
        __lock.acquire()
        resv = VEC0
        res = input_statement
        vcos = 0
        vcos1 = 0
        l = []
        for resp in respslist:
            v2 = SentimentVec(resp)
            vcos1, a, b = VecCos(vec, v2)
            if vcos <= vcos1:
                resv = v2
                res = resp
                vcos = vcos1
            if vcos1 >= CONLIMIT:
                l.append(resp)
        if l.empty():
            res.confidence = vcos1
            return res
        res = choice(l)
        res.confidence = VecCos(vec, SentimentVec(res))
        return res
    finally:
        __lock.release()
