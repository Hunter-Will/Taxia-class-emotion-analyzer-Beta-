import jieba

def cleanstop(words):
    stopwords=[i.strip() for i in open("./stopwords_zh.txt","r")]
    res=[]
    for i in words:
        if i not in stopwords:
            res.append(i)
    return res

def chprocess(sent):
    w=jieba.lcut(sent)
    words=[]
    for i in w:
        s=1
        for j in i:
            if '\u4e00'>j or j>'\u9fff':
                s=0
                break
        if s==1:
            words.append(i)
    words=cleanstop(words)
    return words
