import requests
import simplejson as json
import pandas as pd
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import HoverTool


def scatter_with_hover(df, x, y,
                       fig=None, cols=None, name=None, marker='x',
                       fig_width=500, fig_height=500, **kwargs):
    """
    Plots an interactive scatter plot of `x` vs `y` using bokeh, with automatic
    tooltips showing columns from `df`.
    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing the data to be plotted
    x : str
        Name of the column to use for the x-axis values
    y : str
        Name of the column to use for the y-axis values
    fig : bokeh.plotting.Figure, optional
        Figure on which to plot (if not given then a new figure will be created)
    cols : list of str
        Columns to show in the hover tooltip (default is to show all)
    name : str
        Bokeh series name to give to the scattered data
    marker : str
        Name of marker to use for scatter plot
    **kwargs
        Any further arguments to be passed to fig.scatter
    Returns
    -------
    bokeh.plotting.Figure
        Figure (the same as given, or the newly created figure)
    Example
    -------
    fig = scatter_with_hover(df, 'A', 'B')
    show(fig)
    fig = scatter_with_hover(df, 'A', 'B', cols=['C', 'D', 'E'], marker='x', color='red')
    show(fig)
    Author
    ------
    Robin Wilson <robin@rtwilson.com>
    with thanks to Max Albert for original code example
    """

    # If we haven't been given a Figure obj then create it with default
    # size etc.
    if fig is None:
        fig = figure(width=fig_width, height=fig_height, tools=['box_zoom', 'reset'])

    # We're getting data from the given dataframe
    source = ColumnDataSource(data=df)

    # We need a name so that we can restrict hover tools to just this
    # particular 'series' on the plot. You can specify it (in case it
    # needs to be something specific for other reasons), otherwise
    # we just use 'main'
    if name is None:
        name = 'main'

    # Actually do the scatter plot - the easy bit
    # (other keyword arguments will be passed to this function)
    fig.scatter(df[x], df[y], source=source, name=name, marker=marker, **kwargs)

    # Now we create the hover tool, and make sure it is only active with
    # the series we plotted in the previous line
    hover = HoverTool(names=[name])

    if cols is None:
        # Display *all* columns in the tooltips
        hover.tooltips = [(c, '@' + c) for c in df.columns]
    else:
        # Display just the given columns in the tooltips
        hover.tooltips = [(c, '@' + c) for c in cols]

    hover.tooltips.append(('index', '$index'))

    # Finally add/enable the tool
    fig.add_tools(hover)

    return fig

def codeinput():
    pass
    return codestr

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

#Prices for all tickers for the last month
#apistr = 'https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?date.gte=20161123&date.lt=20161223&ticker=FB,MSFT,C,AA,AMZN&qopts.export=true&api_key=8sHzNYmYsdGN9T1wPytJ'

#'cue uses to choose among the only provided tickers'
apistr = 'https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?date.gte=20161130&date.lt=20161230&ticker=FB,MSFT,GOOG,AMZN&api_key=8sHzNYmYsdGN9T1wPytJ'

r = requests.get(apistr)
#r.text

parsedJson = json.loads(r.text)
jsonData = parsedJson['datatable']
print jsonData['data'][0]## bug is here
print jsonData['data'][0][0]
colNameList = getColArray(jsonData['columns'])
data =getDataArray(jsonData['data'], colNameList)  #datList is a list of list

#creating the DataFrame
df = pd.DataFrame(data)
#myticker = codeinput()
myticker = 'FB'
mypx = 'close'
tickerDF = df[df['ticker']==myticker]
Yaxis = tickerDF[mypx].values #the closing price in the last month, Y axis
Xaxis = tickerDF['date'].values # the dates in the last month, X axis

# plot the data
fig  = figure(width = 500, height=500, tools = ['box_zoom', 'reset'])
source = ColumnDataSource(data=df)
name = 'main'
fig.scatter(Xaxis, Yaxis, source=source, name=name, marker='x')
#<bokeh.models.renderers.GlyphRenderer object at 0x7fbf3de14bd0>
hover = HoverTool(names = [name])
hover.tooltips = [(c, '@' + c) for c in df.columns]
hover.tooltips.append(('index','$index'))
fig.add_tools(hover)
