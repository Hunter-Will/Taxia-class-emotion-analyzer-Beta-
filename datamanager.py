def DataSearcher(filepath,text):
    try:
        f=open(filepath,"r")
    except:
        print("Can not find the file")
        raise Exception
    else:
        for i in f:
            if i[-1:]=='\n':
                i=i[:-1]
            j,k=i.split('=')
            if j==text:
                return k
    return ""
