import requests
import simplejson as json

def parsestr(arr):
    '''
    this function takes an array of strings and return the value of a string
    input:["String", "ticker"]
    output: ticker
    '''
    text = arr.split('",')[1] # this is an hack, '",' ensures getting values instead of 28)" as in the following case (["BigDecimal(50,28)", "adj_high"])
    newstr = text[2:-2]
    return newstr

def parsedata(arr):
    '''
    this function takes an array of strings and return a list of values
    '''
    mystring=arr[1:-1]
    mylist=mystring.split(", ")
    return mylist

def getColArray(arrDict):
    '''
    this function takes an array of dictionaries in json format
    and returns the array of column names
    '''
    newArray=[]
    for i in range(len(arrDict)):
        arraystr = json.dumps(arrDict[i].values())
        colName = parsestr(arraystr)
        newArray.append(colName)
    return newArray

def getDataArray(allData, lst):
    '''
    this function takes a json array
    and returns an data array
    '''
    dataArr=[]
    for dataCol in allData:
        currDict=dict()
        for d in dataCol:
            idx=dataCol.index(d)
            currDict[lst[idx]]= d
        dataArr.append(currDict)
    return dataArr
