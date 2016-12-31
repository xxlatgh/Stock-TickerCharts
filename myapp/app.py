from flask import Flask, render_template, request, redirect

import requests
import simplejson as json
import pandas as pd
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import HoverTool

app = Flask(__name__)

app.vars={}

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

@app.route('/') #route decorator bind a function to a url
def main():
  return redirect('/index')

@app.route('/index', methods=['GET', 'POST'])
def index():
  return render_template('index.html')

@app.route('/output', methods=['GET','POST'])
def output():
  if request.form['ticker_symbol'] == 'MSFT':
      app.vars['ticker_symbol'] = request.form['ticker_symbol']
#      apistr = 'https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?date.gte=20161123&date.lt=20161223&ticker=FB,MSFT,C,AA,AMZN&api_key=8sHzNYmYsdGN9T1wPytJ'

      f=open('ticker1.txt','w')
      f.write('Ticker: %s\n'%(app.vars['ticker_symbol']))
#      f.write('api: %s\n'%(apistr))
      f.close()
      return render_template('output.html')
  else:
      return render_template('index.html')

@app.route('/mainpage, methods=['GET','POST'])
def mainpage():
    #return redirect('/index')
    return render_template('index.html')

if __name__ == '__main__':
  app.run(host='0.0.0.0')
