from math import sqrt

import jieba

__NUM = 10
VEC0 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

__notdic = []
__sentdic = {}
__degdic = {}

with open("./Data/sentidic.csv", "r") as f:
    for i in f:
        if i[0] == ',':
            continue
        l = i.split(',')
        __sentdic[l[0]] = [float(j) for j in l[1:]]
with open("./Data/notdic.dat", "r") as f:
    __notdic = [i.strip() for i in f]
with open("./Data/degdic.dat", "r") as f:
    for i in f:
        l = i.split(',')
        __degdic[l[0]] = float(l[1])


def VecAdd(vec1, vec2):
    global __NUM
    vec0 = []
    for i in range(__NUM):
        vec0.append(vec1[i] + vec2[i])
    return vec0


def VecMul(vec, num):
    vec0 = []
    for i in vec:
        vec0.append(i * num)
    return vec0


def SentimentVec(wordlist):
    global VEC0
    vec = VEC0
    vec1 = VEC0
    stack = []
    cnt = 0
    for i in wordlist:
        if i in __notdic:
            stack.append(i)
        if i in __degdic:
            stack.append(i)
        if i in __sentdic:
            vec1 = __sentdic[i]
            cnt += 1
            while len(stack) > 0:
                if stack[-1] in __notdic:
                    vec1 = VecMul(vec1, -1)
                if stack[-1] in __degdic:
                    vec1 = VecMul(vec1, __degdic[stack[-1]])
                stack.pop()
            vec = VecAdd(vec, vec1)
    if cnt == 0:
        cnt = 1
    return VecMul(vec, 1 / cnt)


def VecCos(vec1, vec2):
    global __NUM
    ans = 0
    m1 = 0
    m2 = 0
    for i in range(__NUM):
        ans += vec1[i] * vec2[i]
        m1 += vec1[i] * vec1[i]
        m2 += vec2[i] * vec2[i]
    if (m1 * m2 == 0):
        ans = 0
    else:
        ans = ans / (sqrt(m1) * sqrt(m2))
    return ans, m1, m2


# a.b/a^2


def SentiCmp(str1, str2, correct=1):
    v1 = SentimentVec(jieba.lcut(str1.text))
    v2 = SentimentVec(jieba.lcut(str2.text))
    score, a, b = VecCos(v1, v2)
    if a == 0:
        tmp = 0
    else:
        tmp = score * b / a
        if tmp > 1:
            tmp = 1 / tmp
    return score, tmp * correct
