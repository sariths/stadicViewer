# # coding=utf-8
# from __future__ import  print_function
# import linecache
#
# fileName = open(r"D:\rtrace_rsensor\cl.RAD")
#
# def dosomething(listName):
#     for lines in listName:
#         yield lines
#
#
#
# x = range(30,60,2)
# y = dosomething(x)
# print(next(y))
# print(next(y))
# # for lines in fileName:
#     # print(lines,end='')
#
# # fileName.close()


class Sarith(object):

    pass


class Subr(Sarith):
    def __repr__(self):
        return "I belong to Sarith"

sarith = Sarith()
sub = Subr()

print(sarith)
print(sub)

print(isinstance(sub,Sarith))