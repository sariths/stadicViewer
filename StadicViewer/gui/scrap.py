class Main(object):
    def __init__(self,a,b):
        self.a = a
        self.b = b


class JsonData(object):
    def __init__(self,p,q):
        self.p = p
        self.q = q

class Main2(Main,JsonData):
    def __init__(self):
        print("ia m ")
        self.x = 42
    def something(self):
        print(self.p)
class Main3(Main,JsonData):
    def __init__(self):
        self.x = 43
        print("I am going to run")

class Final(Main2,Main3,JsonData):
    def __init__(self,a,b):
        pass

