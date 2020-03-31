import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
import seaborn as sns
import timeit
import io

# Get directory of HooHacks folder
import os
rootPath = os.path.abspath(os.path.join(os.path.dirname(__file__),"../.."))

# Reading in the data
daily_adjusted = pd.read_csv('VantageData/daily_adjusted_IBM.csv')
weekly_adjusted = pd.read_csv('VantageData/weekly_adjusted_IBM.csv')
monthly_adjusted = pd.read_csv('VantageData/monthly_adjusted_IBM.csv')

# Graph dimensions and formatting
graph_dim = (8, 6)  # use 11.2, 8.27 for A4 dimensions
AXIS_FONTSIZE = 8
fig, ax = plt.subplots(figsize=graph_dim)

# allParameters = list(daily_adjusted.columns)
# parameters = allParameters[1:7]
# parameters.remove('adjusted_close')
frequencies = ['daily', 'weekly', 'monthly']

def makeLinePlot(x='timestamp', y='open', freq='daily'):
    makeLinePlotMultiple(x=x, y=[y], freq=freq)

def makeLinePlotMultiple(x='timestamp', y=['open'], freq='daily', ytitle='index', xinterval=10):
    # Generate lineplot
    data = globals()[freq + '_adjusted']
    for param in y:
        lineplot = sns.lineplot(x=x, y=param, data=data)
    lineplot.xaxis.set_major_locator(ticker.MultipleLocator(xinterval))
    plt.xticks(rotation=30, fontsize=AXIS_FONTSIZE)
    plt.legend(labels=y)
    plt.xlabel('timestamp')
    plt.ylabel(ytitle)
    return lineplot.figure

def saveBytes(figure, params, freq='daily'):
    bytes_image = io.BytesIO()
    figure.savefig(bytes_image, bbox_inches='tight', format='png')
    bytes_image.seek(0)
    plt.clf()
    return bytes_image

def savePlot(figure, params, freq='daily'):
    # Save the file
    filename = freq + ''.join(params) + ".png"
    filePath = rootPath + "/static/img/stocks/" + filename
    figure.savefig(filePath, bbox_inches='tight')
    plt.clf()

def clearPlots():
    plt.clf()

def generateStockPlots(freq, xinterval=10, option='save'):
    paramsOpenClose=['open', 'close']
    paramsHighLow=['high', 'low']
    paramsVolume=['volume']
    if option == 'bytes':
        bytesOpenClose = saveBytes(makeLinePlotMultiple(y=paramsOpenClose, freq=freq, xinterval=xinterval), paramsOpenClose, freq=freq)
        bytesHighLow = saveBytes(makeLinePlotMultiple(y=paramsHighLow, freq=freq, xinterval=xinterval), paramsHighLow, freq=freq)
        bytesVolume = saveBytes(makeLinePlotMultiple(y=paramsVolume, freq=freq, ytitle='Shares (in tens of millions)', xinterval=xinterval), paramsVolume, freq=freq)
        return {"openclose": bytesOpenClose, "highlow": bytesHighLow, "volume": bytesVolume}
    else:
        savePlot(makeLinePlotMultiple(y=paramsOpenClose, freq=freq, xinterval=xinterval), paramsOpenClose, freq=freq)
        savePlot(makeLinePlotMultiple(y=paramsHighLow, freq=freq, xinterval=xinterval), paramsHighLow, freq=freq)
        savePlot(makeLinePlotMultiple(y=paramsVolume, freq=freq, ytitle='Shares (in tens of millions)', xinterval=xinterval), paramsVolume, freq=freq)


def allPlots():
    dailyPlots = generateStockPlots(freq='daily', option='bytes')
    weeklyPlots = generateStockPlots(freq='weekly', xinterval=50, option='bytes')
    monthlyPlots = generateStockPlots(freq='monthly', option='bytes')
    return {"daily": dailyPlots, "weekly": weeklyPlots, "monthly": monthlyPlots}

# print(allPlots())

# generateStockPlots('monthly', xinterval=50)

# mygraph = makeLinePlotMultiple(y=['open', 'close'], freq='daily', xinterval=10)
# savePlot(figure=mygraph, params=['open', 'close'], freq='daily')
