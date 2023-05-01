def loadconfig(file:str):
    from json import load
    f=open(file)
    return load(f)
    