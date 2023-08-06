#Final Trend And Season Module
import pandas as pd
import numpy as np
from  itertools import product
import matplotlib.pyplot as plt

#linear regression coefficient function
def estimate_coef_jm(x, y):
'''
This function takes in two variables and generates b_1 and b_0 coefficients from a linear regression y = (b_1*x) + b_0

Input
    x - the independent variable
    y - the dependent variable

Returns
    b_0 - Y intercept 
    b_1 - slope
'''
    #convert input to np arrays
    x = np.array(x)
    y = np.array(y)

    # number of observations/points
    n = np.size(x)
 
    # mean of x and y vector
    m_x = np.mean(x)
    m_y = np.mean(y)
 
    # calculating cross-deviation and deviation about x
    SS_xy = np.sum(y*x) - n*m_y*m_x
    SS_xx = np.sum(x*x) - n*m_x*m_x
 
    # calculating regression coefficients
    b_1 = SS_xy / SS_xx
    b_0 = m_y - b_1*m_x
 
    return (b_0, b_1)


#Trend and Season function
def trend_season_jm(y):
'''
This function takes in the dependent variable of a time series and computes a seasonal forecast the same number of 

Input
    y - the dependent variable

Returns
    b_0 - Y intercept 
    b_1 - slope
'''
    #generate the date interval for x
    x = [i for i in range(1,len(y)+1)]
    
    #return the linear regression coefficients
    coeffs = estimate_coef_jm(x,y)
    
    #extend the interval by a complete period 
    new_interval = [x+interval[-1] for x in interval]
    
    #generate the linear regression values for each interval
    LR_values = [(x*coeffs[1])+coeffs[0] for x in interval]
    LR_new_values = [(x*coeffs[1])+coeffs[0] for x in new_interval]
    
    #find the seasonal adj
    seasonal_adj = [(num1 / num2) for num1, num2 in zip(LR_values, LR_new_values)]
    
    #Produce the trend and season forecast
    Trend_season = [(num1 / num2) for num1, num2 in zip(value, seasonal_adj)]
    Trend_season_rounded = [round(num, 0) for num in Trend_season]
    
    #append the results for a plot
    complete_period = interval + new_interval
    complete_LR = LR_values + LR_new_values
    
    # plotting the data
    plt.plot(interval, value, color = "g")
    plt.plot(new_interval, Trend_season, color = "b")
    plt.plot(complete_period, complete_LR, color = "m")
    plt.show()
 
    return Trend_season_rounded