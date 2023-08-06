#Trend and Season Package

This package contains two methods

estimate_coef_jm(x, y): This function takes in two variables and generates b_1 and b_0 coefficients from a linear regression y = (b_1*x) + b_0
Input
    x - the independent variable
    y - the dependent variable
Returns
    b_0 - Y intercept 
    b_1 - slope
 
 
def trend_season_jm(y): This function takes in the dependent variable of a time series and computes a seasonal forecast the same number of events. Note this method assumes one complete period is represented in the data as it computes out the seasonal forecast of another complete period.
Input
    y - the dependent variable
Returns
    b_0 - Y intercept 
    b_1 - slope
    