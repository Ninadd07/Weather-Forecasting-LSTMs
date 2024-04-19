APIGen - Web Scraping using the World Weather API, to populate historical weather data and make dataset

Exploratory Analysis - Visualize the data to identify patterns, randomness and seasonality in time series.

Train - Run the datasets into an after normalization LSTM Model to generate and output weights in form of an exported model.

Main - Import the weights and predict the next weather in series using a Sliding Window 

Weather Function - Renormalize the data and generate results to display on the app.

App - Use streamlit to deploy the LSTM Model and generate weather on a 3 - hourly basis.

feature engineering can be challenging for such time series data, hence a deep learning approach is the best


HOW TO RUN ?

DatasetGenerator.py can be called by specifying path to your train and test data folders
train.py can be run to train the model and exports weights in provided directory.
app.py can be run to trigger and run the rest of the files, by proving the command

'python -m streamlit run app.py'