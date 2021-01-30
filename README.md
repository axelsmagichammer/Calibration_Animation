# Calibration_Animation
An example of calibrating a basic equity model, complete with animation.

The aim of this short project is to illustrate how a basic stochastic model can be calibrated to a 

## DataViewer.py
It is an example of downloading financial data into a pandas data frame using a class.  The financial data is obtained via the package yfinance, there are three being used at the moment: FTSE100, FTSE250 and S&P500.  The class has several methods for: downloading data, calculating log returns and then plotting them as a time series or a density.  There is no error handling currenetly.  There are numerous other methods which could be added to make it more useful, but the framework is there.

To use it the three yfinance variables need setting.  Then in the main function the various class methods can be used.  Naturally, the plotting arguments can be adjusted in the class to suit what is needed.

## CalibrationAnimation.py

