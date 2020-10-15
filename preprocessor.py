import jieba

__stopwords = (i.strip() for i in open("./Data/stopwords_zh.txt", "r"))


def cleanstop(words):
    res = []
    for i in words:
        if i not in __stopwords:
            res.append(i)
    return res


def chprocess(sent):
    w = jieba.lcut(sent)
    words = []
    for i in w:
        s = 1
        for j in i:
            if '\u4e00' > j or j > '\u9fff':
                s = 0
                break
        if s == 1:
            words.append(i)
    words = cleanstop(words)
    return words
