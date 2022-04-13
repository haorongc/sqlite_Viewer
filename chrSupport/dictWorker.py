from chrSupport.basicFun import dprt


class DictWorker:
    def indexMap6list(self, names):
        name_index = dict()
        for i, name in enumerate(names):
            name_index[name] = i
        return name_index

    def conciseKeysValues6dict(self, infoDict, fields2keep=None):
        if fields2keep == None:
            keys = list(infoDict.keys())
            values = list(infoDict.values())
            return keys, values
        else:
            conciseDict = self.copy8intersectFields(infoDict, fields2keep)
            keys = list(conciseDict.keys())
            values = list(conciseDict.values())
            return keys, values

    def copy8intersectFields(self, infoDict, fields):
        if infoDict == None:
            return None

        if fields == None:
            return infoDict

        newDict = dict()
        for key, value in infoDict.items():
            if key in fields:
                newDict[key] = value
        return newDict

    def copy8excludeFields(self, infoDict, fields):
        newDict = dict()
        for key, value in infoDict.items():
            if key not in fields:
                newDict[key] = value
        return newDict


if __name__ == '__main__':
    dictWorker = DictWorker()
    dict1 = {'a': 1, 'b': 2, 'c': 3}
    dict2 = dictWorker.copy8excludeFields(dict1, ['a', 'e'])
    dict3 = dictWorker.copy8intersectFields(dict1, ['a', 'e'])
    print(dict2)
    print(dict3)
