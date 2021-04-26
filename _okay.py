from flask import Flask,request,render_template,url_for
import yfinance as yf
from dateutil.relativedelta import relativedelta
import json
import plotly
import plotly.graph_objs as go


app = Flask(__name__)

@app.route("/")
def home():
	return render_template('base.html')

@app.route("/plot",methods=['POST'])
def plot():
	symbol = request.form["symbol"]
	duration = int(request.form["months"])

	data = yf.download(symbol)

	latest_date = data.iloc[-1].name
	start_date = latest_date - relativedelta(months = duration)
	df = data[start_date:latest_date]
	
	
	df.reset_index(inplace=True)

	fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])])
	fig.update_layout(
    title="Chart for Stock : "+symbol,
     width=1000,
    height=700,
    yaxis_title="Prices",
    legend_title=symbol,
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="RebeccaPurple"
    	)
		)	
	graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)	
	return render_template('home.html',graphJSON = graphJSON)

if __name__ == "__main__":
	app.run()