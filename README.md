# List of modules doing various executions

### Installation

1. Python version 3.12 required.
2. Secondly, create a virtual environment for Python 3 with `python3.12 -m venv venv` and then activate with `source venv/bin/activate`.
3. Then, we need to install dependencies based on [pyproject.toml](pyproject.toml) file. Use `pip install --upgrade --upgrade-strategy eager -e .`.
⚠️ Be aware that if you use the existing requirements file to install dependencies, you may have compatibility issues due to different machines.
4. To avoid pushing files larger than 100 MB, use `find . -size +100M | cat >> .gitignore` and `find . -size +100M | cat >> .git/info/exclude`.

### Project Description

This project is designed to perform advanced time series analysis on historical data, focusing on making the data stationary for accurate forecasting with ARIMA and SARIMAX models. It includes functionalities for data loading, visualization, and preparation, setting the stage for sophisticated statistical modeling and evaluation. The project is structured to be scalable and potentially applicable to various time series datasets, making it a versatile tool for data analysts and scientists interested in forecasting and trend analysis.