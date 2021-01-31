# Calibration_Animation
An example of calibrating a basic equity model, complete with animation.

The aim of this short project is to illustrate how a very basic stochastic model can be calibrated to a target mean and standard deviation over a 1 year time horizon via Monte Carlo projections and an optimiser function.

## DataViewer.py
It is an example of downloading financial data into a pandas data frame using a class.  The financial data is obtained via the package yfinance, there are three being used at the moment: FTSE100, FTSE250 and S&P500.  The class has several methods for: downloading data, calculating log returns and then plotting them as a time series or a density.  There is no error handling currenetly.  There are numerous other methods which could be added to make it more useful, but the framework is there.

To use it the three yfinance variables need setting.  Then in the main function the various class methods can be used.  Naturally, the plotting arguments can be adjusted in the class to suit what is needed.

## CalibrationAnimation.py
The set-up is to calibrate a basic equity model to produced some desired output after 1 year.  It is a simple toy example as in the model being used one could use some historical estimate to set the parameters.

The example uses the FTSE 100 index and starts with a value of 6000.  This is then projected forward each trading day over the next year.  This is done via Monte Carlo and currently displays in the middle chart the paths over the next year for 100 trials.  The right hand chart then shows the distribution of the FTSE 100 after 1 year.  

Given this is supposed to be a calibration of the model there are two parameters to control the daily change in the index each day of the projection.  They broadly represent the mean (mu) and standard deviation (sigma) of the underlying daily return distribution.  The Monte Carlo part then samples from this distribution for a given mu and sigma.  The top left chart shows the value of mu and sigma in the grid.  A basic optimiser function is defined (in this example it is trivial becuase it is known exactly what the required mu and sigma are) but it is more for illustration.  For a given mu and sigma the value of the optimiser is plotted in the bottom left 3D chart for a given mu and sigma.  At the end the aim of the calibration would be to select the values of mu/sigma corresponding to the lowest value of the optimiser.  The animation then runs through different mu and sigmas.

The code is mainly variables and the set-up of the charts.  The two main functions are the Monte Carloa and the animation.
