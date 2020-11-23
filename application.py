import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go
import time
import numpy as np
import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import prediction
import os
import sys
import matplotlib.pyplot as plt
from dash.dependencies import Input, Output

application=app = dash.Dash(__name__)

# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)

import boto3
import pandas as pd
#from sagemaker import get_execution_role

#role = get_execution_role()
bucket='stocks-dump'
data_key = 'stocks-dump.json'
data_location = 's3://{}/{}'.format(bucket, data_key)
background_color="#003366"
#pd.read_csv(data_location)

import json

def get_data():
    bucket='stocks-dump'
    data_key = 'stocks-dump.json'
    data_location = 's3://{}/{}'.format(bucket, data_key)
    s3 = boto3.resource('s3')
    obj = s3.Object(bucket, data_key)
    data = json.load(obj.get()['Body']) 
    
    json_data = [] # your list with json objects (dicts)
    df=pd.DataFrame(columns=['Company','Date_Time','Stock Price','Nasdaq','S&P 50','DowJones'])
    for item in data:
        df.loc[len(df)]=[item['Company'],item['Date_Time'],item['Stock Price'],item['Nasdaq'], item['S&P 50'], item['DowJones']]
    
    
    
    df['Date_Time']= pd.to_datetime(df['Date_Time'])
    df = df.rename(columns={'Stock Price': 'Stock_Price'})
    df = df.sort_values(by="Date_Time")
    
    
    
    
    df_display=df.sort_values(by="Date_Time",ascending=False)
    df_display=df_display.head(15)
    return df.tail(100),df_display

df,df_display=get_data()



def draw_graphs(df):
    fig = px.line(df, x="Date_Time", y="Stock_Price", labels = {'x':'Date-Time', 'y':'Amazon Stock Price'},
                    title="Amazon Stock Price", color_discrete_sequence =['red'])
                    
  
    fig1= px.line(df, x="Date_Time", y="Nasdaq", labels = {'x':'Date-Time', 'y':'Nasdaq'},
                    title="NASDAQ",)
    fig2= px.line(df, x="Date_Time", y="S&P 50",labels = {'x':'Date-Time', 'y':'S&P 50'},
                    title="S&P 50",)
    
    fig3= px.line(df, x="Date_Time", y="DowJones")
    
    
    fig.update_layout(title_x=0.5,
                    paper_bgcolor=background_color,
                    font_color="white",
                    title_font_color="white")
                    
                    
    
                    
    fig1.update_layout(title_x=0.5,
                
                    paper_bgcolor=background_color,
                    font_color="white",
                    title_font_color="white")
                    
    
                    
    fig2.update_layout(title_x=0.5,
                    paper_bgcolor=background_color,
                    font_color="white",
                    title_font_color="white")
    
    fig3.update_layout(title_x=0.5,
                    paper_bgcolor=background_color,
                    font_color="white",
                    title_font_color="white")
    
    return fig,fig1,fig2,fig3

fig,fig1,fig2,fig3=draw_graphs(df)
ab_test=df_display.iloc[0,2]
ab='$'+str(ab_test)
pred=0
# ------------------------------------------------------------------------------
# App layot


button_style={ 'border': 'none','color':'black','padding':'15px 32px',
            'text-align': 'center','text-decoration':'none',
            'font-size': '24px','align':'center'}

def app_layout(df,df_display):
    app.layout = html.Div([

    html.H1("Stock Price Predictions", style={'text-align': 'center','color':'white'}),

     html.Div([
    dcc.Graph(id='my_bee_map', figure=fig),], style={'height':'50%'}),
    
        html.Div([
    html.P('{}'.format(ab),
						
							)],style={'align':'center',
							'color':'white',
									'fontSize': 40,
									  'margin': 'auto',
                                        'width':'9%',
                                        'height':'10%',
                                        'border': '3px solid #FFFF00',
                                        'padding': '6px'

								}),
    
    
    
    html.Div([
    
    html.Button('Refresh', id='btn-nclicks-1', n_clicks=0, 
    style=button_style),
    
    html.Button('Predict', id='btn-nclicks-2', n_clicks=0,
    style=button_style)
    ],
    style=button_style),
    
    

    html.Div(id='container-button-timestamp',style={'text-align':'center',
							'color':'white',
									'fontSize': 40,
									  'margin': 'auto',
 

								}
        
        ),
        
    
    html.Div([
        dcc.Graph(id='my_bee_map1', figure=fig1),
        
        ], style={'width': '50%','display': 'inline-block'}),
    
    html.Div([
        dcc.Graph(id='my_bee_map2', figure=fig2),
        
        ], style={'width': '50%', 
        'align': 'right',
        'display': 'inline-block'}),

    #html.Div([
        #dcc.Graph(id='my_bee_map3', figure=fig3),
        
        #], style={'width': '50%','align':'center','display': 'inline-block'}),
    

    html.Div([
    dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in df_display.columns],
    data=df_display.to_dict('records'),
    style_cell={
        'backgroundColor': 'black',
        'color': 'white'
    },
    )]),
    

    ], style={
  'backgroundColor':background_color,
  'position':'absolute',
  'width':'100%',
  'height':'100%',
  'top':'0px',
  'left':'0px'
  
})

app_layout(df,df_display)

# ------------------------------------------------------------------------------

@app.callback(Output('container-button-timestamp', 'children'),
              [Input('btn-nclicks-1', 'n_clicks'),
               Input('btn-nclicks-2', 'n_clicks')])




         
def displayClick(btn1,btn2):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    print(changed_id)
    msg=str()

    if 'btn-nclicks-2.n_clicks' == changed_id:
        print("YES")
        preds=prediction.arima(df)
        pred=round(float(preds.tail(1).values),2)
        text=str()
     
        num=round(abs(float(ab_test)-float(pred)),2)
        print(round(float(preds.tail(1).values),2))
        
        if float(pred)>float(ab_test):
            text='Increase by '
        elif float(pred)<float(ab_test):
            text='Decrease by '
        else:
            text='No Change'

        pred='$'+str(pred)

        msg = "The Predicted Price is: " +pred +'. '+text + '$'+str(num)

        
        
        '''
        df['predicted']=np.array(preds)
        fig_pred = px.line(df, x="Date_Time", y=["Stock_Price","predicted"], labels = {'x':'Date-Time', 'y':'Amazon Stock Price'})
 
        pred_graph2 = dcc.Graph(
        figure=fig_pred)
        '''
        
        
    elif 'btn-nclicks-1.n_clicks' == changed_id:
        print("YES")
        os.execl(sys.executable, sys.executable, *sys.argv)
    else:
        print("")
    
    return html.Div(msg)

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(host='0.0.0.0',port=8080,debug=True)
