import dash
from dash import html, callback, Output,  Input, dcc,ctx, ALL, State
from src.components.stock.backtesting.rsi import backtestRsi
from src.components.stock.backtesting.macd_rsi import backtestMacdRsi
from src.components.stock.backtesting.plot_candlestick import plot_candlestick
from src.components.stock.backtesting.plot_volume import plot_volume
from src.components.stock.backtesting.plot_profit_loss import plot_profit_loss
from src.components.stock.stock_layout_functions import get_stock_id_from_url
from src.components.stock.backtesting.sma_crossover import backtestSmaCrossover
from src.components.stock.single_stock_base_layout import stock_base_layout
from src.components.stock.backtesting.plot_equity import plot_equity
from src.components.stock.backtesting.backtesting_settings import generate_backtesting_settings
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd
import dash_bootstrap_components as dbc
import dash_table



dash.register_page(__name__, path_template="/stocks/<stock_id>/backtesting")

@callback([Output("average-short-container", "style"), Output("average-long-container", "style")], Input("user-input-store", "data"))
def show_sma_inputs(data):
    
    if (data["strategy"] == "sma"):
       
        return {"visibility" : "visible"}, {"visibility" : "visible"}
    else:
        return {"visibility" : "hidden"}, {"visibility" : "hidden"}
    


@callback([Output("subplot-figure","figure") ,Output("input-invalid","style"), Output("results-table", "data")], [Input("run-backtest", "n_clicks"), Input("url","pathname")], State('user-input-store', 'data'))
def runSMA(n_clicks, url, user_inputs):
    

  
    
    if (n_clicks > 0):
        strategy = user_inputs.get('strategy', 'macd')  # Default to 'macd' if strategy is None
        take_profit = user_inputs.get('take_profit')
        stop_loss = user_inputs.get('stop_loss')
        buy_amount = user_inputs.get('buy_amount')
        stock_id = get_stock_id_from_url(url)
        average_short = -1 ##temp place holder
        average_long = -2 ##temp place holder
        if (take_profit is not None):
            take_profit = take_profit/100
        if (stop_loss is not None):
            stop_loss = stop_loss/100
        if strategy == 'sma':
            average_short = user_inputs['average_short']
            average_long = user_inputs['average_long']
            stats = backtestSmaCrossover(stock_id, averageShort=average_short, averageLong=average_long,
                                            takeProfit=take_profit, stopLoss=stop_loss, buyAmount=buy_amount)
        elif strategy == 'macd':
            stats = backtestMacdRsi(stock_id, takeProfit=take_profit, stopLoss=stop_loss, buyAmount=buy_amount)
        elif strategy == 'rsi':
            stats = backtestRsi(stock_id, takeProfit=take_profit, stopLoss=stop_loss, buyAmount=buy_amount)
        fig = make_subplots(
            rows=4, cols=1,
            shared_xaxes=True,
            subplot_titles=("Equity Curve", "Profit/Loss", "Candlestick Chart", "Volume Chart"),
            vertical_spacing=0.03,
            )
        
        # Define layout
        layout = dict(
            title="Backtesting",
            hovermode="x unified",
            
        
        )
        

        if (stats is None or average_long == average_short):
            fig = go.Figure()
            fig.update_layout(
                title='Equity Curve',
                xaxis_title='Time',
                yaxis_title='Equity Value',
                legend=dict(x=0.02, y=0.98),
                plot_bgcolor='#F1F1F1',
                paper_bgcolor='#F1F1F1',
            )
            return fig, {"visibility" : "visible"}, []
      
        
        equity_curve = stats['Equity Curve']
        trades = stats["Trades"]
        candlestick = stats["Candlestick"]
        trade_duration = f"{stats['Avg Trade Duration'].days} days"
        results_table_data = [{
            'Total Return': stats['Total Return'],
            'Max Drawdown': stats['Max Drawdown'],
            'Avg Trade Duration': trade_duration,
            'Win Rate': stats['Win Rate']
        }]
      

        equity_curve = equity_curve.reset_index()
        # Merge the trades with the full dataset to expand the rows
        merged_data = pd.merge(equity_curve, trades, left_on='Date', right_on='EntryTime', how='left')
        # Keep only the relevant trade columns after merging (and the Date column)
        trade_columns = ['Date', 'EntryPrice', 'ExitPrice', 'PnL', 'ReturnPct', "ExitTime", "EntryTime"]
        filtered_trade = merged_data[trade_columns]
        
        # Plot equity curve using Plotly
        # plot_equity(equity_curve=equity_curve , main_fig=fig)
        plot_equity(equity_curve=equity_curve, main_fig= fig)
        plot_profit_loss(trades=filtered_trade,  main_fig= fig)
        plot_candlestick(candlestick, filtered_trade, fig)
        plot_volume(candlestick_data=candlestick, main_fig=fig)
        
        fig.update_layout(layout)
        return fig, {"visibility" : "hidden"},  results_table_data

    else:
        fig = go.Figure()
        fig.update_layout(
            title='Equity Curve',
            xaxis_title='Time',
            yaxis_title='Equity Value',
            legend=dict(x=0.02, y=0.98),
            plot_bgcolor='#F1F1F1',
            paper_bgcolor='#F1F1F1',
        )
        return fig, {"visibility" : "hidden"}, []


def layout(stock_id=None, **kwargs):
    
     
    
    return(
    stock_base_layout(stock_id),
    dcc.Store(id='user-input-store'),  # Store for user inputs
    generate_backtesting_settings(),
      
    
    
    html.Button('Run Backtest', id='run-backtest', n_clicks=0, className="mt-4 bg-blue-400 rounded-lg p-2 mb-4"),
    html.P("Invalid Input!", className="font-bold text-red-600 ", id="input-invalid"),
    html.H3("Result Stats" , className="mb-2"),
    dash_table.DataTable(
        id='results-table',
        columns=[
            {'name': 'Total Return [%]', 'id': 'Total Return',"type": "numeric", "format": { "specifier": ".4s"}},
            {'name': 'Max Drawdown [%]', 'id': 'Max Drawdown',"type": "numeric", "format": { "specifier": ".4s"}},
            {'name': 'Avg Trade Duration', 'id': 'Avg Trade Duration'},
            {'name': 'Win Rate [%]', 'id': 'Win Rate',"type": "numeric", "format": { "specifier": ".4s"}}
        ],
        data=[],  # Pass the data to the table
        style_table={'width': '50%'},  # Customize width as needed
        style_cell={
            'textAlign': 'center',  # Align text
            'font_family': 'Arial',
            'font_size': '16px',
        },
        
    ),
    
    
    dcc.Graph(id = "subplot-figure",  style={'height': '1500px' }, className="mt-4"),

 
    
    )