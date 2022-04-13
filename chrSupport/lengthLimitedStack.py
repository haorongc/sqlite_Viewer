from collections import deque


class LengthLimitedStack(deque):
    defaultMaxLen = 5

    def __init__(self, maxLen=None):
        if maxLen != None:
            self.setMaxLen(maxLen)
        else:
            self.setMaxLen(self.defaultMaxLen)

    def last(self, defaultValue=None):
        try:
            return self[-1]
        except:
            return defaultValue

    def setMaxLen(self, maxLen):
        self.maxLen = maxLen

    def append(self, newElem):
        super().append(newElem)
        if len(self) > self.maxLen:
            self.popleft()

    def safePop(self, defaultValue=None):
        try:
            a = self.pop()
        except:
            # how to print system message?
            print('\t! failed to pop')
            return defaultValue
        else:
            # pop as normal
            return a


if __name__ == '__main__':

    stack = LengthLimitedStack(3)
    for i in range(5):
        stack.append(i)

    # a = stack[-1]
    # print(a)
    for i in range(5):
        a = stack.last()
        print(a)
        stack.safePop()
