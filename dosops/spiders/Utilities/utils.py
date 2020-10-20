from pandas import read_csv


def load_ids(self, path, column_id):
    return list(read_csv(path)[column_id])


def xpath_stylisation(self, text):
    return '\n        ' + text + '\n      '


def isValidXpath(self, xpathresult):
    if xpathresult == []:
        raise AttributeError
