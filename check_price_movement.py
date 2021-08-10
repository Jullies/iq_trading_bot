import plotly.graph_objs as go
import os
import pandas as pd
import xlsxwriter

class showInBrowser:
    def __init__(self):
        pass
    
    def saveCurrentFigure(self, data, title):
        fig = go.Figure()
        assign_name = title.replace('/','_').replace("=X", "")
        if(os.path.exists('website/bot/assets/'+assign_name) == False):
            os.mkdir('website/bot/assets/'+assign_name) 
        temp_paths = ['excel', 'html', 'model','log']
        for tmp_path in temp_paths:
            if(os.path.exists('website/bot/assets/%s/%s'%(assign_name, tmp_path)) == False):
                os.mkdir('website/bot/assets/%s/%s'%(assign_name, tmp_path))
       
        
        fig.add_trace(go.Candlestick(x=data.index,
                        open=data['Open'],
                        high=data['High'],
                        low=data['Low'],
                        close=data['Close'], name = 'market data'))
        
        fig.update_layout(
            title='%s live share price evolution'%(title),
            yaxis_title='Stock Price')
        
        fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list([
                    dict(count=15, label="15m", step="minute", stepmode="backward"),
                    dict(count=45, label="45m", step="minute", stepmode="backward"),
                    dict(count=1, label="HTD", step="hour", stepmode="todate"),
                    dict(count=3, label="3h", step="hour", stepmode="backward"),
                    dict(step="all")
                ])
            )
        )
        fig.write_html('website/bot/assets/%s/html/current.html'%(assign_name)) 
        workbook = xlsxwriter.Workbook('website/bot/assets/%s/excel/current.xlsx'%(assign_name))
        worksheet = workbook.add_worksheet()   
        
        worksheet.write(0, 0, 'Datetime')
        worksheet.write(0, 1, 'Open')
        worksheet.write(0, 2, 'High')
        worksheet.write(0, 3, 'Low')
        worksheet.write(0, 4, 'Close')
        worksheet.write(0, 5, 'Adj Close')
        worksheet.write(0, 6, 'Volume')
        
        r = 1
        for date, row in data.T.iteritems():
            thistime = str(date).replace('+03:00', "")
            thispdtime = pd.to_datetime(thistime)
            worksheet.write(r, 0, thispdtime)
            worksheet.write(r, 1, row['Open'])
            worksheet.write(r, 2, row['High'])
            worksheet.write(r, 3, row['Low'])
            worksheet.write(r, 4, row['Close'])
            worksheet.write(r, 5, row['Adj Close'])
            worksheet.write(r, 6, row['Volume'])
            r+=1
        workbook.close()