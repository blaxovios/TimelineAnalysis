import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.arima_model import ARIMA
import itertools
import logging

from src.functions import GeneralFunctions


general_functions = GeneralFunctions()
general_functions.local_logger()
configs_dict = general_functions.load_toml('configs/config.toml')


class TimeSeriesAnalysis(object):
    def __init__(self) -> None:
        pass
    
    def read_data(self) -> pd.DataFrame:
        # Read data from 1960 - 2015
        data = pd.read_csv(filepath_or_buffer=configs_dict["GENERAL"]["DATA_FILE_PATH"], sep=';', index_col=0, parse_dates=True)[1:59]
        data.plot()
        plot_acf(data) # Autocorrelation is decaying, so our time series is not stationary. Also it has trend.
        plt.show()
        return data

    def make_stationary(self, data: pd.DataFrame) -> None:
        # Converting time series to stationary, meaning that the mean, variance and covariance are constant over time.
        # We take the differences from the data
        data_diff = data.diff(periods=1)    # intergrated of order 1, denoted by d (for difference), one of the parameter of ARIMA model
        data_diff = data_diff[1:]   # Remove first NaN value
        data_diff.plot()
        plot_acf(data_diff)
        plt.show()
        return

    def time_series_analysis(self) -> None:
        # Split data
        x = data.values
        train = x[:53] # Data as train data
        test = x[53:] # Data to test data

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
        logging.info('Test RMSE: %.3f' % error)

        # 2. ARIMA Model
        # Find optimal p, d, q. Pick by lowest value of "(p,d,q) value"
        p=d=q=range(0,5)
        pdq = list(itertools.product(p,d,q))
        for param in pdq:
            try:
                model_arima = ARIMA(train, order=param)
                model_arima_fit = model_arima.fit()
                logging.info(param, model_arima_fit.aic)
            except Exception as e:
                logging.error(e)
                continue

        # Parameters: p, d, q where p = periods taken for autoregressive model,
        # d = integrated order, difference
        # q = periods in moving average model
        model_arima = ARIMA(train, order = (3,2,1)).fit()
        logging.info(model_arima.aic)
        predictions_arima = model_arima.predict(start=len(train), end=(len(data)-1))
        plt.plot(test, label = 'Actual Data')
        plt.plot(predictions_arima, color='red', label = 'Prediction Data for same years')
        plt.legend(loc = 'best')
        plt.show()

        # Predict Future Data
        final_model = ARIMA(data, order = (3,2,1)).fit() # Build on full dataset
        fc, _se, _conf = final_model.forecast(10) # Forecast 10 years forward
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
        logging.info('Test RMSE: %.3f' % error)
        return
    
    def plot_publications(self) -> None:
        data = pd.read_csv(filepath_or_buffer=configs_dict["GENERAL"]["PUBLICATIONS_FILE_PATH"], sep='\s+', header=None)[1:]
        data = pd.DataFrame(data)

        x = data[0]
        y = data[1]
        plt.plot(x, y,'b', label='Publications')
        plt.grid()
        plt.title('"Computer Graphics field publications per year"')
        plt.xlabel('Year', fontsize = 15)
        plt.ylabel('Publications', fontsize = 15)
        plt.xticks(rotation=45)
        plt.legend()
        plt.show()
        return


if __name__ == "__main__":
    time_series_analysis = TimeSeriesAnalysis()
    data = time_series_analysis.read_data()
    time_series_analysis.make_stationary(data)
    time_series_analysis.time_series_analysis()
    time_series_analysis.plot_publications()