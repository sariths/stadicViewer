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
        self.x = 42
    def something(self):
        print(self.p)
class Main3(Main,JsonData):
    def __init__(self):
        self.x = 43

class Final(Main2,Main3,JsonData):
    def __init__(self,a,b):
        Main.__init__(self,31,21)
        JsonData.__init__(self,100,200)
        Main2.__init__(self)
        Main3.__init__(self)

