from matplotlib import pyplot as plt
from matplotlib import dates as mdates
import yfinance as yf
import datetime


def plot_prediction(df,close_tomorrow,last_n_days=400):
    
    lof_dates = list(map(get_date_string,df['Date']))
    plt.plot(lof_dates[-last_n_days:],df['Close'].values[-last_n_days:])
    date_tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    plt.plot(date_tomorrow,close_tomorrow,marker='+',markeredgecolor='green',markerfacecolor='none',markersize=12,linestyle='',label='Prediction')
    
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1,7)))
    plt.gca().xaxis.set_minor_locator(mdates.MonthLocator())
    plt.gcf().autofmt_xdate()

    plt.gca().grid(True)
    plt.gca().set_ylabel(r'Close price [\$]')
    plt.gca().set_xlabel(r'Date')
    plt.legend()
    plt.title(f"Predicted close price for {date_tomorrow.strftime('%Y-%m-%d')}: ${float(close_tomorrow):.2f}")
    plt.savefig(f"fig-prediction_for_{date_tomorrow.strftime('%Y%m%d')}.pdf")


def get_date_string(date):
    #return date.strftime('%Y-%m-%d')
    return date.to_datetime64()


if __name__ == "__main__":
    from mlstockpredictor.data.stock import get_stock_data
    df = get_stock_data('TSLA')
    invented_value = 232.232 #for testing purposes only (avoid running prediction while testing plot)
    plot_prediction(df,invented_value)
