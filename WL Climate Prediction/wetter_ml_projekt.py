# -*- coding: utf-8 -*-
"""Wetter ML Projekt.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1pVD_ljrf36eC33rlev3EsCnL1KA_-9dN

**Data collection**

I downloaded the data files from NOAA's Local Climatological Data (LCD) [site](https://www.ncei.noaa.gov/cdo-web/datatools/lcd) specifically focused on [West Lafayette](https://www.ncei.noaa.gov/cdo-web/datasets/LCD/stations/WBAN:14835/detail), Indiana. I downloaded the climate change indicator data from [Copernicus](https://cds.climate.copernicus.eu/cdsapp#!/search?type=dataset) [(CO2 Levels)](https://cds.climate.copernicus.eu/cdsapp#!/dataset/satellite-carbon-dioxide?tab=overview) [(Climate Indices)](https://cds.climate.copernicus.eu/cdsapp#!/dataset/sis-extreme-indices-cmip6?tab=overview) (GFDL-ESM4 (USA) Model and SSP3-7.0 for aerosol emissions) [(global temperature anomalies)](https://cds.climate.copernicus.eu/cdsapp#!/dataset/seasonal-postprocessed-single-levels?tab=overview). Need data on (NOx levels, other important aerosols, heat wave data, etc)

Naturally, it's important to read the [Dataset Documentation](https://www.ncei.noaa.gov/pub/data/cdo/documentation/LCD_documentation.pdf) before working with the data and during the preprocessing stage to understand how to deal with different values. For further understanding, please read NOAA's [GSOM Summary](https://www.ncei.noaa.gov/pub/data/cdo/documentation/GSOM_documentation.pdf)

# Objective & Plan

Project Plan: West Lafayette, Indiana Weather Prediction Using Machine Learning with Consideration of Climate Change

A coding project which uses machine learning and data from decades of weather patterns of each day to determine yearly climate patterns while incorporating climate change indicators.

#### Goals
1. **Primary Goal**: Develop a machine learning model to predict yearly climate patterns using historical weather data while accounting for climate change effects.
2. **Secondary Goal**: Enhance the model's accuracy and robustness with advanced techniques and external climate data.

#### Tasks and Completion Plan
3. **Feature Engineering**
   - **Task**: Extract and create relevant features from the dataset.
   - **How to Complete**: Create new features like moving averages, seasonal indicators.
   - **Potential Issues**: Determining the most relevant features and overfitting with too many features
5. **Model Training**
   - **Task**: Train the selected models on the preprocessed data.
   - **How to Complete**: Tune hyperparameters using grid search or randomized search.
   - **Potential Issues**: Overfitting or underfitting during training.

6. **Model Evaluation**
   - **Task**: Evaluate the performance of the trained models.
   - **How to Complete**:
     - Use metrics such as mean squared error (MSE), mean absolute error (MAE), and R-squared.
     - Compare model predictions with actual data.
   - **Potential Issues**:
     - Ensuring that evaluation metrics reflect the model's real-world performance.
     - Balancing between bias and variance.

7. **Incorporate Climate Change Factors**
   - **Task**: Integrate climate change data into the model to account for long-term trends.
   - **How to Complete**:
     - Obtain climate change data (e.g., CO2 levels, temperature anomalies).
     - Include these factors as features in the model.
   - **Potential Issues**:
     - Finding reliable and comprehensive climate change datasets.
     - Integrating these datasets with weather data effectively.

8. **Final Model Selection and Fine-Tuning**
   - **Task**: Select the best-performing model and fine-tune it.
   - **How to Complete**:
     - Analyze evaluation results to choose the best model.
     - Perform additional fine-tuning to optimize performance.
   - **Potential Issues**:
     - Overfitting during the fine-tuning process.
     - Ensuring model generalization to unseen data.

9. **Deployment**
   - **Task**: Deploy the final model for making real-time predictions.
   - **How to Complete**:
     - Create a web application or API to serve the model.
     - Use Flask/Django for web deployment, or FastAPI for creating APIs.
   - **Potential Issues**:
     - Ensuring scalability and performance of the deployed model.
     - Handling real-time data efficiently.

#### Potential Issues and Mitigations

- **Data Quality**: Ensure thorough data cleaning and preprocessing.
- **Model Overfitting/Underfitting**: Use cross-validation and regularization techniques.
- **Computational Resources**: Utilize cloud services (e.g., AWS, Google Cloud) for training and deployment.
- **Integration of Climate Data**: Careful feature engineering and validation.

#### Extra Features to Add

1. **Interactive Visualizations**
   - Create interactive dashboards to visualize weather predictions and climate trends using Plotly or Dash.

2. **Model Explanation**
   - Implement techniques like SHAP (SHapley Additive exPlanations) to explain model predictions and understand feature importance.

3. **Automated Data Pipeline**
   - Develop an automated data pipeline to continuously update the model with new data.

5. **Weather Alerts**
   - Integrate a notification system to alert users about significant weather changes or extreme weather events.

6. **User Interface**
   - Develop a user-friendly interface for non-technical users to interact with the model and view predictions.

# Combining & loading the data
"""

import os
import pandas as pd
import numpy as np

#pd.set_option('display.max_columns', None)

# Load the dataset
climate_data_original = pd.read_csv("/content/combined_weather_data.csv")
climate_data = climate_data_original.copy()

"""After I checked the data, I saw that most of the columns had a small amount of non-null values compared to the number of columns and found that the 'threshhold' was 'HourlySeaLevelPressure'. After that, every column had a small number of values compared to the number of rows"""

# Get non-null counts for each column
non_null_counts = climate_data.notnull().sum()

# Create a summary DataFrame
summary_df = pd.DataFrame({
    'Column': non_null_counts.index,
    'Non-Null Count': non_null_counts.values
})

# Sort the summary DataFrame by 'Non-Null Count' in descending order
sorted_summary_df = summary_df.sort_values(by='Non-Null Count', ascending=False)

''' # Remove these apostrophes to see the full list
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
'''

# Display the sorted summary
print(sorted_summary_df)

# Calculate the number of non-null values in each column
non_null_counts = climate_data.notnull().sum()

# Find the threshold based on 'HourlySeaLevelPressure'
threshold = non_null_counts['HourlySeaLevelPressure']

# Filter columns to keep based on the threshold
columns_to_keep = non_null_counts[non_null_counts >= threshold].index

# Ensure columns_to_remove are only those present in the DataFrame
columns_to_remove = ['STATION', 'REPORT_TYPE', 'REPORT_TYPE.1', 'SOURCE', 'SOURCE.1', 'REM', 'WindEquipmentChangeDate']
columns_to_remove = [col for col in columns_to_remove if col in columns_to_keep]

climate_data = climate_data[columns_to_keep] # Create a new DataFrame with only the columns to keep
climate_data = climate_data.drop(columns=columns_to_remove) # Drop the columns specified for removal

pd.set_option('display.max_columns', None)
climate_data.head()

"""# Preprocessing

There are some parts of the data where a character is given with or instead of the number value provided. These characters are:

1. "T" = trace precipitation amount or snow depth (an amount too small to measure, usually < 0.005 inches water equivalent) (appears instead of numeric value)
2. "s" = suspect value (appears with value)
3. "M" = missing value (appears instead of value)
4. Blank = value is unreported (nothing appears or "NaN")
5. "*" = Amounts included in following measurement; time distribution unknown
- for temps, these are used to indicate the extreme for the day and month, these can be deleted

Below shows how we dealt with them
"""

exclude_columns = ['DATE'] # Columns to exclude from filling missing values

# Define the function to clean the data
def clean_data(value):
    if value == 'T':
        return 0.0025  # A small value representing trace amount
    elif value == 's':
        return np.nan  # Suspect value can be treated as missing value
    elif value == 'M':
        return np.nan  # Missing value
    elif value == '*' or value == '':
        return np.nan  # Unreported value
    else:
        try:
            # Convert to float if possible
            return float(value)
        except ValueError:
            return np.nan  # If the value cannot be converted to float, treat it as missing

# Apply the cleaning function to the entire DataFrame except for the excluded columns
for col in climate_data.columns:
    if col not in exclude_columns:
        climate_data[col] = climate_data[col].apply(clean_data)

# Define a function to compute window mean
def compute_window_mean(df, col, idx, window_size):
    # Define the window
    start_idx = max(0, idx - window_size)
    end_idx = min(len(df), idx + window_size + 1)

    # Extract the window of values
    window_values = df[col].iloc[start_idx:end_idx]

    # Drop NaN values from the window and calculate mean
    non_nan_values = window_values.dropna()
    if len(non_nan_values) > 0:
        return non_nan_values.mean()
    return np.nan

# Define a function to fill missing values
def fill_missing_values(df, exclude_cols, window_size=10):
    # First pass: Fill missing values with mean of full windows
    df_filled = df.copy()
    for col in df.columns:
        if col not in exclude_cols and pd.api.types.is_numeric_dtype(df[col]):
            for idx in df[df[col].isna()].index:
                mean_value = compute_window_mean(df, col, idx, window_size)
                if not pd.isna(mean_value):
                    df_filled.at[idx, col] = mean_value

    # Second pass: Handle any remaining missing values
    for col in df.columns:
        if col not in exclude_cols and pd.api.types.is_numeric_dtype(df[col]):
            for idx in df_filled[df_filled[col].isna()].index:
                mean_value = compute_window_mean(df, col, idx, window_size)
                if pd.isna(mean_value):
                    # If we cannot calculate a mean, use the column's global mean
                    mean_value = df[col].mean()
                df_filled.at[idx, col] = mean_value

    return df_filled

# Apply the function
climate_data = fill_missing_values(climate_data, exclude_columns)

"""Imputing outliers"""

def impute_outliers(data, strategy='median', threshold=1.5):
    Q1 = np.percentile(data, 25)
    Q3 = np.percentile(data, 75)
    IQR = Q3 - Q1
    lower_bound = Q1 - (threshold * IQR)
    upper_bound = Q3 + (threshold * IQR)

    if strategy == 'median':
        fill_value = np.median(data)
    elif strategy == 'mean':
        fill_value = np.mean(data)
    else:
        raise ValueError("Strategy must be 'median' or 'mean'")

    data = np.where((data < lower_bound) | (data > upper_bound), fill_value, data)
    return data

imputed_data = impute_outliers(climate_data['HourlyWetBulbTemperature'])

# Convert 'DATE' column to datetime
climate_data['DATE'] = pd.to_datetime(climate_data['DATE'], format='ISO8601')

# Set 'DATE' column as index
climate_data.set_index('DATE', inplace=True)

# Sort the DataFrame by the datetime index
climate_data.sort_index(inplace=True)

climate_data.to_csv('updated_climate_data.csv', index=True)

climate_data.head()

"""Direct influence on temperature

1. **HourlyDryBulbTemperature** - Directly measures the current air temperature, essential for predicting future temperatures.
2. **HourlyDewPointTemperature** - Indicates moisture in the air, which affects temperature and weather conditions.
3. **HourlyRelativeHumidity** - Affects the perception of temperature and can influence how temperature changes.
4. **HourlyWetBulbTemperature** - Provides a measure of humidity’s effect on temperature, which is useful in predicting temperature changes.

Indirectly influences temperature
5. **HourlySeaLevelPressure** - Affects weather patterns and can indirectly influence temperature.
6. **HourlyStationPressure** - Related to sea level pressure and affects weather conditions that can influence temperature.
7. **HourlyVisibility** - Primarily related to atmospheric conditions rather than temperature directly.
8. **HourlyAltimeterSetting** - Measures atmospheric pressure but is less directly related to temperature prediction.
9. **HourlyPrecipitation** - Affects weather conditions but is less directly related to temperature prediction compared to other factors.

Not sure

10. **HourlyWindSpeed** - Influences temperature by affecting heat transfer and can impact how temperature changes.
11. **HourlyWindDirection** - Impacts temperature indirectly by changing wind patterns and influencing weather.
"""

climate_data.describe()

"""# Visualizations"""

import os
import pandas as pd
import numpy as np

climate_data = pd.read_csv("/content/updated_climate_data.csv")

# Convert 'DATE' column to datetime
climate_data['DATE'] = pd.to_datetime(climate_data['DATE'], format='ISO8601')

# Set 'DATE' column as index
climate_data.set_index('DATE', inplace=True)

# Sort the DataFrame by the datetime index
climate_data.sort_index(inplace=True)

climate_data.tail()

altimeter = climate_data['HourlyAltimeterSetting']
altimeter.plot()

hourlydew = climate_data['HourlyDewPointTemperature']
hourlydew.plot()

hourlydry = climate_data['HourlyDryBulbTemperature']
hourlydry.plot()

hourlyRH = climate_data['HourlyRelativeHumidity']
hourlyRH.plot()

hourlypressure = climate_data['HourlySeaLevelPressure']
hourlypressure.plot()

"""something is odd here. need to look further into it"""

hourlywet = climate_data['HourlyWetBulbTemperature']
hourlywet.plot()

hourlywindspeed = climate_data['HourlyWindSpeed']
hourlywindspeed.plot()

"""# Pipeline (Ensemble Model)

Here, I'm using an ensemble (hybrid model) of Random Forest and LSTM to capture short-term weather patterns and long-term (10 years to 30 years) climate trends.The RF model handles non-linear relationships and is robust to overfitting for large datasets. I'm using an LSTM for temporal dependencies.

https://youtu.be/LDRbO9a6XPU?si=tBt9vtEuVp92Lj4S

https://youtu.be/d12ra3b_M-0?si=H564MFe7Oxv0IMre

pytorch tutorial: https://youtu.be/V_xro1bcAuA?si=7ts-lWXfXzIaw6il
"""

from keras.models import load_model
from keras.models import Sequential
from keras.layers import LSTM, Dense
from keras.preprocessing.sequence import TimeseriesGenerator
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib

# Assuming climate_data is your DataFrame
X = climate_data.drop(columns=['HourlyWetBulbTemperature'])
y = climate_data['HourlyWetBulbTemperature']

# Step 3: Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 4: Define preprocessing steps for Random Forest
preprocessor_rf = Pipeline([
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())
])

# Step 5: Define the Random Forest model
model_rf = RandomForestRegressor(n_estimators=100, random_state=42)

# Step 6: Create a pipeline for Random Forest
pipeline_rf = Pipeline([
    ('preprocessor', preprocessor_rf),
    ('model', model_rf)
])

# Step 7: Train the Random Forest model
pipeline_rf.fit(X_train, y_train)

# Step 8: Prepare data for LSTM
# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Create sequences for LSTM
time_steps = 10
train_generator = TimeseriesGenerator(X_train_scaled, y_train, length=time_steps, batch_size=32)
test_generator = TimeseriesGenerator(X_test_scaled, y_test, length=time_steps, batch_size=32)

# Step 9: Define the LSTM model
model_lstm = Sequential()
model_lstm.add(LSTM(50, activation='relu', input_shape=(time_steps, X_train.shape[1])))
model_lstm.add(Dense(1))
model_lstm.compile(optimizer='adam', loss='mse')

# Step 10: Train the LSTM model
model_lstm.fit(train_generator, epochs=50, validation_data=test_generator)

# Step 11: Make predictions with both models
y_pred_rf = pipeline_rf.predict(X_test)
y_pred_lstm = model_lstm.predict(test_generator)
y_pred_lstm = y_pred_lstm.flatten()

# Step 12: Combine predictions (simple average)
combined_predictions = (y_pred_rf[time_steps:] + y_pred_lstm) / 2

# Step 13: Evaluate the combined model
mse_combined = mean_squared_error(y_test[time_steps:], combined_predictions)
print('Mean Squared Error (Combined):', mse_combined)

# Optional: Deploy the model for new predictions
# Save models or create a function to combine predictions from both models for new data

# Step 14: Save the trained models
joblib.dump(pipeline_rf, 'random_forest_climate_model.pkl')
model_lstm.save('lstm_climate_model.h5')

"""**Making predictions**"""

import joblib
from keras.models import load_model

# Step 15: Function to load models and make combined predictions
def load_models():
    # Load the saved models
    pipeline_rf = joblib.load('random_forest_climate_model.pkl')
    model_lstm = load_model('lstm_climate_model.h5')
    return pipeline_rf, model_lstm

def make_predictions(X_new, time_steps=10):
    # Load models
    pipeline_rf, model_lstm = load_models()

    # Preprocess new data
    X_new_scaled = pipeline_rf.named_steps['preprocessor'].transform(X_new)

    # Make predictions with Random Forest
    y_pred_rf = pipeline_rf.predict(X_new)

    # Prepare data for LSTM predictions
    new_generator = TimeseriesGenerator(X_new_scaled, np.zeros(len(X_new_scaled)), length=time_steps, batch_size=1)
    y_pred_lstm = model_lstm.predict(new_generator)
    y_pred_lstm = y_pred_lstm.flatten()

    # Combine predictions (simple average)
    combined_predictions = (y_pred_rf[time_steps:] + y_pred_lstm) / 2

    return combined_predictions

# Example usage for new data
# X_new = ...  # Replace with new data
# combined_predictions = make_predictions(X_new)
# print(combined_predictions)