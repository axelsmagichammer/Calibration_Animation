import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
import seaborn as sns

# Graphs set-up
sns.set(color_codes=True)
plt.interactive(False)

# yfinance set-up variables
startdate = '1900-01-01'  # enter as a string
enddate = '2020-12-31'  # enter as a string
finsymbol = {'^FTSE': 'FTSE_100', '^FTMC': 'FTSE_250', '^GSPC': 'S&P_500'}  # dictionary for the data required,
# see https://finance.yahoo.com for tickers/symbols

# A class to store the data and with some methods for loading the data,
# calculating daily log retunrs and stats, plotting log returns.


class DataFrame:

    def __init__(self, start_date, end_date, finsymbol_dict):
        self.start_date = start_date
        self.end_date = end_date
        self.finsymbol_dict = finsymbol_dict
        self.df = pd.DataFrame(yf.download(list(self.finsymbol_dict.keys()),
                                           start=self.start_date, end=self.end_date, progress=False))
        self.logmeans = 0
        self.logsds = 0

    def preparereturnsdata(self):
        self.df = self.df[['Adj Close']]
        if len(self.finsymbol_dict) > 1:
            self.df.columns = self.df.columns.droplevel(0)
        self.df.columns = self.finsymbol_dict.values()

    def calculatelogreturns(self):
        logmeans = dict()
        logsds = dict()
        for name in list(self.finsymbol_dict.values()):
            namekey = name + '_log_return'
            self.df[namekey] = np.log(self.df[name] / self.df[name].shift(1))
        self.df.dropna(how='any', axis=0, inplace=True)
        for name in list(self.finsymbol_dict.values()):
            namekey = name + '_log_return'
            logmeans.update({namekey: self.df[namekey].mean()})
            logsds.update({namekey: self.df[namekey].std()})
        self.logmeans = logmeans
        self.logsds = logsds

    def graphlogreturns(self):
        fig, ax = plt.subplots(len(self.finsymbol_dict), 1, sharex=True, sharey=True,
                               squeeze=False, figsize=(13, 8), linewidth=0.01)
        for count, name in enumerate(list(self.finsymbol_dict.values()), start=0):
            namekey = name + '_log_return'
            ax[count, 0].set(title=namekey, ylabel='Daily log returns', facecolor='linen')
            ax[count, 0].grid(color='black')
            ax[count, 0].spines['top'].set_color('black')
            ax[count, 0].spines['right'].set_color('black')
            ax[count, 0].spines['bottom'].set_color('black')
            ax[count, 0].plot(self.df[namekey], c=np.random.random(3,))
        fig.tight_layout()
        plt.show()

    def graphlogdensity(self):
        fig, ax = plt.subplots(len(self.finsymbol_dict), 1, sharex=True, sharey=True,
                               squeeze=False, figsize=(13, 8), linewidth=0.01)
        for count, name in enumerate(list(self.finsymbol_dict.values()), start=0):
            namekey = name + '_log_return'
            titlename = name + ' log return density'
            ax[count, 0].set(title=titlename, facecolor='linen')
            ax[count, 0].grid(color='black')
            ax[count, 0].spines['top'].set_color('black')
            ax[count, 0].spines['right'].set_color('black')
            ax[count, 0].spines['bottom'].set_color('black')
            sns.kdeplot(self.df[namekey], shade=True, color=np.random.random(3,), ax=ax[count, 0])
        fig.tight_layout()
        plt.show()

# The main function using the input variables to create the DataFrame class.  It can be changed depending on uses.


def main():
    data = DataFrame(startdate, enddate, finsymbol)
    data.preparereturnsdata()
    data.calculatelogreturns()
    print(data.df)
    print(data.logmeans)
    data.graphlogreturns()


if __name__ == "__main__":
    main()
