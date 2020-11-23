import statsmodels.api as sm
# Ignore harmless warnings 
import warnings 
warnings.filterwarnings("ignore") 
import pandas as pd
import numpy as np




def process_df(df):
  n=len(df)
  num_array = np.arange(n)
  df.reindex(num_array)
  df=df['Stock_Price']

  df = df.astype(float) 
  print(np.dtype(df))
  

  return df
  
def arima(df):

  df=process_df(df)
  print("Y()")

  mod = sm.tsa.statespace.SARIMAX(df,
                                order=(1, 1, 1),
                                seasonal_order=(1, 1, 1, 12),
                                enforce_stationarity=False,
                                enforce_invertibility=False)    

    
  result = mod.fit() 
  
  preds= result.predict(start=0,end=101,dynamic=False)
  print("PREDS")
  print(preds)

  print(result.summary())
  print("FINISHED MODEL")

  return preds

