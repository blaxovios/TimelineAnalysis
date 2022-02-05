import numpy as np
import pandas as pd
import statsmodels.api as sm
from matplotlib import pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.arima_model import ARIMA
import itertools
import warnings
warnings.filterwarnings('ignore')

# Read data from 1960 - 2015
output_file = r'C:\Users\tsepe\PycharmProjects\TimelineAnalysis\files\results.csv'
data = pd.read_csv(output_file, sep=';', index_col=0, parse_dates=True)[1:59]
data.plot()
plot_acf(data) #Autocorrelation is decaying, so our time series is not stationary. Also it has trend.
plt.show()

#Converting time series to stationary, meaning that the mean, variance and covariance are constant over time.
#We take the differences from the data
data_diff = data.diff(periods=1) # intergrated of order 1, denoted by d (for difference), one of the parameter of ARIMA model
data_diff = data_diff[1:] #Remove first NaN value
data_diff.plot()
plot_acf(data_diff)
plt.show()

# Split data
x = data.values
train = x[:53] # Data as train data
test = x[53:] # Data to test data
predictions = []

# 1. SARIMA Model
model_sarima = SARIMAX(train, order=(9,0,1))
model_sarima_fit = model_sarima.fit()
predictions_sarima = model_sarima_fit.predict(start=len(train), end=(len(data)-1))
plt.plot(test, label = 'Actual Data')
plt.plot(predictions_sarima, color='red', label = 'Prediction Data for same years')
plt.legend(loc = 'best')
plt.show()

# 10 year future prediction
predictions_sarima_future = model_sarima_fit.predict(start=len(data), end=(len(data)+10))
plt.plot(predictions_sarima_future, color='blue', label = '10 year Prediction')
plt.xlabel('Years forward')
plt.ylabel('Publications')
plt.title('Forecasted publications')
plt.legend(loc = 'best')
plt.show()

# SARIMA Model Evaluation
# The lower the error the better the model
error = np.sqrt(mean_squared_error(test, predictions_sarima))
print('Test RMSE: %.3f' % error)


# 2. ARIMA Model
# Find optimal p, d, q. Pick by lowest value of "(p,d,q) value"
p=d=q=range(0,5)
pdq = list(itertools.product(p,d,q))
warnings.filterwarnings('ignore')
for param in pdq:
    try:
        model_arima = ARIMA(train, order=param)
        model_arima_fit = model_arima.fit()
        print(param, model_arima_fit.aic)
    except:
        continue

# Parameters: p, d, q where p = periods taken for autoregressive model,
# d = integrated order, difference
# q = periods in moving average model
model_arima = ARIMA(train, order = (3,2,1)).fit()
print(model_arima.aic)
predictions_arima = model_arima.predict(start=len(train), end=(len(data)-1))
plt.plot(test, label = 'Actual Data')
plt.plot(predictions_arima, color='red', label = 'Prediction Data for same years')
plt.legend(loc = 'best')
plt.show()

# Predict Future Data
final_model = ARIMA(data, order = (3,2,1)).fit() # Build on full dataset
fc, se, conf = final_model.forecast(10) # Forecast 10 years forward
fc_series = pd.Series(fc)
plt.plot(fc_series, label='Forecast')
plt.xlabel('Years forward')
plt.ylabel('Publications')
plt.title('Forecasted publications')
plt.legend(loc = 'best')
plt.show()

# ARIMA Model Evaluation
# The lower the error the better the model
error = np.sqrt(mean_squared_error(test, predictions_arima))
print('Test RMSE: %.3f' % error)
