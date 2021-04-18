import pickle

import requests
import gzip

import json

import csv

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

urlAPI = "https://api.syosetu.com/novelapi/api/"

limit = 50
searchStartPlace = 1

paramOptions = {
    "gzip": "5",
    "out": "json",
    "of": "t-n-u-w-l-s",
    "lim": str(limit),
    # "st":"1",
    "order": "ncodedesc",
    "minlen": "500000",
    "kaiwaritu": "30-60",
    # "buntai":"6-4-2",
}


def getDataByAPI(start):
    # paramOptions["lim"]=limit
    paramOptions["st"] = str(start)
    param = "?"
    for key in paramOptions:
        value = paramOptions[key]

        text = key + "=" + value
        param += text + "&"

    param = param[:-1]

    url = urlAPI + param

    print(url)

    res = requests.get(url=url)
    # pickle.dump(res,open("../SaveData/resForTest","wb"))
    #
    # res=pickle.load(open("../SaveData/resForTest","rb"))

    pathGzip = "../SaveData/latest.gz"
    with open(pathGzip, "wb")as f:
        f.write(res.content)

    with gzip.open(pathGzip, "rb")as f:
        content = f.read()

    data = json.loads(content)
    return data


notWords = [
    "!",
    "?",
    "！",
    "？",
    "件",
    "ます",
    "ました",
    "…",
]

titleSplitChar = [
    " ",
    "　",
    "〜",
    "-",
    "ー",
    "－",
    "「",
    "【",
]
titleLengthLimit = len("これくらいの長さを超えたらさすがにアウトでしょ")


def checkTitleNotSave(title):
    for word in notWords:
        if word in title:
            # print("out")
            # print(title)
            return True

    titleFirst = title
    for i in titleSplitChar:
        titleFirst = titleFirst.split(i)[0]
    if len(titleFirst) > titleLengthLimit:
        # print("out")
        # print(title)
        return True
    return False


with open("../Settings/ignoreList.csv", "r", encoding="utf-8")as f:
    reader = csv.reader(f)
    ignoreCSV = [row for row in reader]
    ignoreNCodes = [row[1] for row in ignoreCSV[1:]]


def checkNCodeInIgnoreList(NCode):
    if NCode in ignoreNCodes:
        # print("out")
        # print(NCode)
        return True
    return False


foundDataList = []


def initCSV(data):
    with open("../SaveData/latest.csv", "w", encoding="utf-8")as f:
        text = ""
        for key in data[1]:
            text += key + ","
        text += "\n"
        f.write(text)


def addDataToList(data):
    for row in data[1:]:
        text = ""
        notSave = False
        for key in row:
            value = row[key]
            if key == "ncode":
                notSave = checkNCodeInIgnoreList(value)
            elif key == "title":
                notSave = checkTitleNotSave(value)

            if notSave:
                break
            # value=
            value = str(value)
            value = value.replace("\n", "myTextEscapeEnter")
            text += value + ","
        text += "\n"

        if not notSave:
            foundDataList.append(text)
            with open("../SaveData/latest.csv", "a", encoding="utf-8")as f:
                try:
                    f.write(text)
                except Exception as e:
                    print(e)

def getLatestData(searchStartPlace):
    while len(foundDataList) < 50:
        data = getDataByAPI(searchStartPlace)
        print("start api : {0}".format(searchStartPlace))
        if searchStartPlace == 1:
            initCSV(data)
        addDataToList(data)

        searchStartPlace += limit

def searchAndCreateCSV():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    getLatestData(searchStartPlace)

if __name__ == '__main__':
    searchAndCreateCSV()