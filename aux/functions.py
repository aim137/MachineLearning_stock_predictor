from matplotlib import pyplot as plt
from matplotlib import dates as mdates
import yfinance as yf
import datetime
#from icecream import ic


def plot_prediction(df,prediction,n_days=120,ticker='TSLA',is_validate=False):
    
    n_days = max(n_days,prediction.shape[0])
    # Actual data
    lof_dates = list(map(get_date_string,df['Date']))
    plt.plot(lof_dates[-n_days:],df['Close'].values[-n_days:],label=f"{ticker}")

    if is_validate:
        # Validated data
        plt.plot(lof_dates[-prediction.shape[0]:],prediction,label=f"Validation")
    else:
        # Predicted data
        date_tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        plt.plot(date_tomorrow,prediction,marker='+',markeredgecolor='green',markerfacecolor='none',markersize=12,linestyle='',label='Prediction')
    
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(bymonth=get_month_tics(n_days)))
    plt.gca().xaxis.set_minor_locator(mdates.MonthLocator())
    plt.gcf().autofmt_xdate()

    plt.gca().grid(True)
    plt.gca().set_ylabel(r'Close price [\$]')
    plt.gca().set_xlabel(r'Date')
    plt.legend()
    plt.title(f"{ticker}",loc='left')
    if not is_validate:
        plt.annotate(f"Prediction for {date_tomorrow.strftime('%Y-%m-%d')}: ${float(prediction):.2f}",
                    (0.5,1.025),xycoords='axes fraction')

    if is_validate:
        tag = f"validation_up_to_{datetime.date.today().strftime('%Y%m%d-%H.%M.%S')}"
    else:
        tag = f"prediction_for_{date_tomorrow.strftime('%Y%m%d')}"

    plt.savefig(f"fig-{ticker}-{tag}.pdf")
    plt.close()


def get_date_string(date):
    #return date.strftime('%Y-%m-%d')
    return date.to_datetime64()

def get_month_tics(n):
    if n < 150: return [1, 3, 5, 7, 9, 11]
    if n < 370: return [1, 4, 7, 10]
    if n < 1100: return [1, 7]
    return [1]

def plot_optimisation():
    pass

if __name__ == "__main__":
    from mlstockpredictor.data.stock import get_stock_data
    import numpy as np
    df = get_stock_data('TSLA')
    invented_value = np.array([[232.232]]) #for testing purposes only (avoid running prediction while testing plot)
    plot_prediction(df,invented_value,n_days=1000)
