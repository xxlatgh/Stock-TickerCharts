import requests
import simplejson as json
from .parse import parsestr, parsedata, getColArray, getDataArray

def getstockdata():
    #getting all stock data, can't specify date intervals in this case 
    #apistr = 'https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?date.gte=20161130&date.lt=20161230&qopts.export=true&api_key=8sHzNYmYsdGN9T1wPytJ'

    apistr = 'https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?date.gte=20161130&date.lt=20161230&ticker=FB,MSFT,GOOG,AMZN&api_key=8sHzNYmYsdGN9T1wPytJ'

    r = requests.get(apistr)
    #r.text
    parsedJson = json.loads(r.text)
    jsonData = parsedJson['datatable']
    colNameList = getColArray(jsonData['columns'])
    data =getDataArray(jsonData['data'], colNameList)  #datList is a list of list
    return data
