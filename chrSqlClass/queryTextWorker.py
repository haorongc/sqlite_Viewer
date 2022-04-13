from chrSupport.dictWorker import DictWorker

dictWorker = DictWorker()


class QueryTextWorker:
    def importSearchDict(self, searchDict, searchFields=None):
        if searchDict == None:
            self.hasWhereConstraint = False
            return

        # searchDict is a dict, not None,
        # unpack key-value and exclude unwanted fields
        self.searchFields, self.searchValues = dictWorker.conciseKeysValues6dict(searchDict, fields2keep=searchFields)
        if len(self.searchFields) > 0:
            self.hasWhereConstraint = True
        else:
            self.hasWhereConstraint = False

    def genWhereClause(self):
        if self.hasWhereConstraint == False:
            return ''

        equalPhrases = []
        for field in self.searchFields:
            equalPhrases.append(f'{field}=?')
        equalSentence = ' and '.join(equalPhrases)
        return f'where {equalSentence}'

    def genParams(self):
        if self.hasWhereConstraint == False:
            return []
        return self.searchValues
