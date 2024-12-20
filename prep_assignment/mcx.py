from classiq import *

@qfunc
def mcx(k: CInt, cbits: QNum, target: QBit):
    control(ctrl=(cbits==2**k-1), stmt_block=(lambda: X(target)))