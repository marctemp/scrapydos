from pandas import read_csv


def load_ids(path, column_id='ID'):
    return list(read_csv(path)[column_id])


def xpath_stylisation(text):
    return '\n        ' + text + '\n      '


def is_valid_xpath(xpathresult):
    if xpathresult == []:
        raise AttributeError
