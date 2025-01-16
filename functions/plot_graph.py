from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import pandas_ta as ta
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score
from functions.technical_indicators import calculate_technical_indicators

class PlotGraph:
    def __init__(self, data, ticker, window, std):
        self.data = data
        self.ticker = ticker
        self.window = window
        self.std = std
            
        self.data = self.data.dropna()
        
    def technical_indicators(self):
        self.data = calculate_technical_indicators(self.data, self.window, self.std)
        return self.data
    
    def get_values(self):
        return self.data
    
    def plot_main_candle_graph(self):
        
        if len(self.data.columns) <= 5:
            self.data = self.technical_indicators()

        # Create a figure with subplots: 2 rows, 1 column
        fig = make_subplots(rows=3, cols=1,
                            vertical_spacing=0.15, 
                            subplot_titles=("Candlestick Chart", "Volume", "RSI"))

        # Candlestick Chart
        fig.add_trace(go.Candlestick(
            x=self.data.index,
            open=self.data["Open"],
            high=self.data["High"],
            low=self.data["Low"],
            close=self.data["Close"],
            name=f"{self.ticker} Stock Price",
            legendgroup="group",
            legendgrouptitle_text="Candlestick Chart",
        ), row=1, col=1)

        fig.add_trace(go.Scatter(
            x=self.data.index,
            y=self.data["SMA"],
            mode="lines",
            name=f"SMA-{self.window}",
            line=dict(color="blue", width=1),
            legendgroup="group",
        ), row=1, col=1)

        fig.add_trace(go.Scatter(
            x=self.data.index,
            y=self.data["EMA"],
            mode="lines",
            name=f"EMA-{self.window}",
            line=dict(color="orange", width=1),
            legendgroup="group"
        ), row=1, col=1)

        fig.add_trace(go.Scatter(
            x=self.data.index,
            y=self.data[f"BBL_{self.window}_{self.std}"],
            mode="lines",
            name=f"BBL-{self.window}-{self.std}",
            line=dict(color="green", width=1),
            legendgroup="group"
        ), row=1, col=1)

        fig.add_trace(go.Scatter(
            x=self.data.index,
            y=self.data[f"BBM_{self.window}_{self.std}"],
            mode="lines",
            name=f"BBM-{self.window}-{self.std}",
            line=dict(color="orange", width=1),
            legendgroup="group"
        ), row=1, col=1)

        fig.add_trace(go.Scatter(
            x=self.data.index,
            y=self.data[f"BBU_{self.window}_{self.std}"],
            mode="lines",
            name=f"BBU-{self.window}-{self.std}",
            line=dict(color="red", width=1),
            legendgroup="group"
        ), row=1, col=1)
        
        # Volume Chart
        fig.add_trace(go.Bar(
            x=self.data.index,
            y=self.data["Volume"],
            name=f"{self.ticker} Volume",
            legendgroup="group2",
            legendgrouptitle_text="Trading Volume"
        ), row=2, col=1)

        # RSI Chart
        fig.add_trace(go.Scatter(
            x=self.data.index,
            y=self.data["RSI"],
            mode="lines",
            name=f"RSI",
            line=dict(color="blue", width=1),
            legendgroup="group3",
            legendgrouptitle_text="RSI Chart"
        ), row=3, col=1)

        fig.add_trace(go.Scatter(
            x=self.data.index,
            y=np.ones(len(self.data["RSI"])) * 100, 
            mode="lines",
            name=f"100 Line",
            line=dict(color="rgb(169, 169, 169)", width=1),
            legendgroup="group3"
        ), row=3, col=1)
        
        fig.add_trace(go.Scatter(
            x=self.data.index,
            y=np.ones(len(self.data["RSI"])) * 70,
            mode="lines",
            name=f"70 Line",
            line=dict(color="red", dash="dash", width=1),
            legendgroup="group3"
        ), row=3, col=1)

        fig.add_trace(go.Scatter(
            x=self.data.index,
            y=np.ones(len(self.data["RSI"])) * 30,
            mode="lines",
            name=f"30 Line",
            line=dict(color="red", dash="dash", width=1),
            legendgroup="group3"
        ), row=3, col=1)

        fig.add_trace(go.Scatter(
            x=self.data.index,
            y=np.zeros(len(self.data["RSI"])),
            mode="lines",
            name=f"0 Line",
            line=dict(color="rgb(169, 169, 169)", width=1),
            legendgroup="group3"
        ), row=3, col=1)

        # Customize the x-axis to show ticks per year
        fig.update_layout(
            title=f"{self.ticker} Stock Price",
            width=1200,
            height=800,
            template="plotly_dark",
            xaxis=dict(
                tick0=self.data.index[0],
                rangeselector=dict(
                    buttons=list([
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(step="all", label="All")
                    ]),
                    bgcolor="rgb(50, 50, 50)",  # Dark grey background for the buttons
                    activecolor="rgb(100, 100, 100)",  # Light grey for the active button
                    font=dict(color="white"),  # White text for buttons
                )
            ),
            legend=dict(
                bgcolor="rgb(50, 50, 50)",  # Light grey background for the legend
                bordercolor="rgb(169, 169, 169)",  # Grey border around the legend
                borderwidth=1,  # Border width of the legend
                font=dict(color="white"),  # White text in the legend
                itemsizing="constant",  # Ensure legend items are evenly spaced
                groupclick="toggleitem"
            )
        )

        # Add y-axis labels
        fig.update_yaxes(title_text="Price", row=1, col=1)
        fig.update_yaxes(title_text="Volume", row=2, col=1)
        fig.update_yaxes(title_text="RSI", row=3, col=1)
        # Add x-axis labels
        fig.update_xaxes(matches="x", row=2, col=1)
        fig.update_xaxes(title_text="Date", matches="x", row=3, col=1)


        fig.update_layout(xaxis_rangeslider_visible=False)
        fig.show()
    
    def plot_evaluate_model(self, predicted_values):
        
        date = self.data.index
        
        if len(self.data.columns) <= 5:
            self.data = self.technical_indicators()

        predicted_values = calculate_technical_indicators(predicted_values, self.window, self.std)
        
        # Create a figure with subplots: 5 rows, 2 column
        fig = make_subplots(rows=5, cols=2, 
                            start_cell="top-left",
                            specs= [
                                [{}, {}],
                                [{}, {}],
                                [{"colspan": 2}, None],
                                [{"colspan": 2}, None],
                                [{"colspan": 2}, None]
                            ],
                            vertical_spacing=0.1, 
                            subplot_titles=("Open Price", 
                                            "Close Price", 
                                            "High Price", 
                                            "Low Price", 
                                            "Candlestick",
                                            "Volume",
                                            "RSI")
                            )
        
        # Open Price
        fig.add_trace(go.Scatter( # Actual Open Price
            x=date,
            y=self.data["Open"],
            mode="lines",
            name="Actual Price",
            line=dict(color="green", width=1),
            legendgroup="open",
            legendgrouptitle_text="Open Chart"
        ), row=1, col=1)
        fig.add_trace(go.Scatter( # Predicted Open Price
            x=date,
            y=predicted_values["Open"],
            mode="lines",
            name="Predicted Price",
            line=dict(color="blue", width=1),
            legendgroup="open"
        ), row=1, col=1)
        
        # High Price
        fig.add_trace(go.Scatter( # Actual High Price
            x=date,
            y=self.data["High"],
            mode="lines",
            name="Actual Price",
            line=dict(color="green", width=1),
            legendgroup="high",
            legendgrouptitle_text="High Chart"
        ), row=1, col=2)
        fig.add_trace(go.Scatter( # Predicted High Price
            x=date,
            y=predicted_values["High"],
            mode="lines",
            name="Predicted Price",
            line=dict(color="blue", width=1),
            legendgroup="high"
        ), row=1, col=2)
        
        # Low Price
        fig.add_trace(go.Scatter( # Actual Low Price
            x=date,
            y=self.data["Low"],
            mode="lines",
            name="Actual Price",
            line=dict(color="green", width=1),
            legendgroup="low",
            legendgrouptitle_text="Low Chart"
        ), row=2, col=1)
        fig.add_trace(go.Scatter( # Predicted Low Price
            x=date,
            y=predicted_values["Low"],
            mode="lines",
            name="Predicted Price",
            line=dict(color="blue", width=1),
            legendgroup="low"
        ), row=2, col=1)
        
        # Close Price
        fig.add_trace(go.Scatter( # Actual Close Price
            x=date,
            y=self.data["Close"],
            mode="lines",
            name="Actual Price",
            line=dict(color="green", width=1),
            legendgroup="close",
            legendgrouptitle_text="Close Chart"
        ), row=2, col=2)
        fig.add_trace(go.Scatter( # Predicted Close Price
            x=date,
            y=predicted_values["Close"],
            mode="lines",
            name="Predicted Price",
            line=dict(color="blue", width=1),
            legendgroup="close"
        ), row=2, col=2)
        
        # Candlestick Chart
        fig.add_trace(go.Candlestick( # Actual Candlestick
            x=date,
            open=self.data["Open"],
            high=self.data["High"],
            low=self.data["Low"],
            close=self.data["Close"],
            name=f"Actual {self.ticker} Stock Price",
            increasing_line_color="rgb(0, 245, 155)",
            decreasing_line_color="rgb(112, 20, 242)",
            legendgroup="candlestick",
            legendgrouptitle_text="Candlestick Chart"
        ), row=3, col=1)
        fig.add_trace(go.Candlestick( # Predicted Candlestick
            x=date,
            open=predicted_values["Open"],
            high=predicted_values["High"],
            low=predicted_values["Low"],
            close=predicted_values["Close"],
            name=f"Predicted {self.ticker} Stock Price",
            increasing_line_color="rgb(96, 239, 255)",
            decreasing_line_color="rgb(0, 97, 255)",
            legendgroup="candlestick"
        ), row=3, col=1)
        
        # Volume Line
        fig.add_trace(go.Bar(
            x=date,
            y=self.data["Volume"],
            name="Actual Volume",
            marker_color="green",
            legendgroup="volume",
            legendgrouptitle_text="Volume Chart"
        ), row=4, col=1)
        fig.add_trace(go.Bar(
            x=date,
            y=predicted_values["Volume"],
            name="Predicted Volume",
            marker_color="blue",
            legendgroup="volume"
        ), row=4, col=1)
        
        # RSI Line
        fig.add_trace(go.Scatter(
            x=date,
            y=self.data["RSI"],
            mode="lines",
            name=f"RSI from Actual Close Price",
            line=dict(color="green", width=1),
            legendgroup="RSI",
            legendgrouptitle_text="RSI Chart"
        ), row=5, col=1)
        fig.add_trace(go.Scatter(
            x=date,
            y=predicted_values["RSI"],
            mode="lines",
            name=f"RSI from Predicted Close Price",
            line=dict(color="blue", width=1),
            legendgroup="RSI"
        ), row=5, col=1)

        # RSI Threshold
        fig.add_trace(go.Scatter(
            x=date,
            y=np.ones(len(self.data["RSI"])) * 100, 
            mode="lines",
            name=f"100 Line",
            line=dict(color="rgb(169, 169, 169)", width=1),
            legendgroup="RSI"
        ), row=5, col=1)

        fig.add_trace(go.Scatter(
            x=date,
            y=np.ones(len(self.data["RSI"])) * 70,
            mode="lines",
            name=f"70 Line",
            line=dict(color="red", dash="dash", width=1),
            legendgroup="RSI"
        ), row=5, col=1)
        
        fig.add_trace(go.Scatter(
            x=date,
            y=np.ones(len(self.data["RSI"])) * 30,
            mode="lines",
            name=f"30 Line",
            line=dict(color="red", dash="dash", width=1),
            legendgroup="RSI"
        ), row=5, col=1)


        fig.add_trace(go.Scatter(
            x=date,
            y=np.zeros(len(self.data["RSI"])),
            mode="lines",
            name=f"0 Line",
            line=dict(color="rgb(169, 169, 169)", width=1),
            legendgroup="RSI"
        ), row=5, col=1)
        
        fig.update_layout(
            title=f"Evaluate Model for Prediction of {self.ticker} Stock Price",
            width=1200,
            height=1000,
            template="plotly_dark",
            xaxis5=dict(rangeslider=dict(visible=False)),
            legend=dict(
                bgcolor="rgb(50, 50, 50)",  # Light grey background for the legend
                bordercolor="rgb(169, 169, 169)",  # Grey border around the legend
                borderwidth=1,  # Border width of the legend
                font=dict(color="white"),  # White text in the legend
                itemsizing="constant",  # Ensure legend items are evenly spaced
                groupclick="toggleitem"
            )
        )
        
        # Add y-axis labels
        fig.update_yaxes(title_text="Price", row=1, col=1)
        fig.update_yaxes(title_text="Price", row=1, col=2)
        fig.update_yaxes(title_text="Price", row=2, col=1)
        fig.update_yaxes(title_text="Price", row=2, col=2)
        fig.update_yaxes(title_text="Price", row=3, col=1)
        fig.update_yaxes(title_text="RSI", row=5, col=1)
        # Add x-axis labels
        fig.update_xaxes(title_text="Date", row=1, col=1)
        fig.update_xaxes(title_text="Date", row=1, col=2)
        fig.update_xaxes(title_text="Date", row=2, col=1)
        fig.update_xaxes(title_text="Date", row=2, col=2)
        fig.update_xaxes(matches="x5", row=4, col=1)
        fig.update_xaxes(title_text="Date", matches="x5", row=5, col=1)
        
        fig.show()
    
    def plot_evaluate_table(self, predicted_values):
        # Metrics for each column
        columns = predicted_values.columns
        metrics = ["<b>Features</b>", "<b>MAE</b>", "<b>RMSE</b>", "<b>R2 Score</b>", "<b>MAPE</b>"]
        mae_list, rmse_list, r2_score_list, mape_list = [], [], [], []

        for column in columns:
            actual = self.data[column].values
            predicted = predicted_values[column].values
            
            component_mae   = mean_absolute_error(actual, predicted)
            component_rmse  = root_mean_squared_error(actual, predicted)
            component_r2    = r2_score(actual, predicted)
            component_mape  = np.mean(np.abs((actual - predicted) / actual)) * 100
            
            mae_list.append(f"{component_mae:.3f}")
            rmse_list.append(f"{component_rmse:.3f}")
            r2_score_list.append(f"{component_r2:.3f}")
            mape_list.append(f"{component_mape:.3f}%")     
        
        # Create a table with Plotly
        fig = go.Figure(
            data=[
                go.Table(
                    header=dict(
                        values=metrics,
                        fill_color="lightgrey",
                        align="center",
                        font=dict(size=12, color="black"),
                    ),
                    cells=dict(
                        values=[columns, mae_list, rmse_list, r2_score_list, mape_list],
                        fill_color="white",
                        align="center",
                        font=dict(size=12, color="black"),
                    ),
                )
            ]
        )

        # Update layout
        fig.update_layout(
            title="Metrics for Each Column",
            width=800,
            height=320,
            template="plotly_dark",
        )
        
        fig.show()
        
        
        
        
        
        
        