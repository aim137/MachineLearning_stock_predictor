from matplotlib import pyplot as plt
from matplotlib import dates as mdates
import yfinance as yf
import datetime


def plot_prediction(df,prediction,n_days=400,ticker='TSLA',mode_validate=False):
    
    n_days = max(n_days,prediction.shape[0])
    # Actual data
    lof_dates = list(map(get_date_string,df['Date']))
    plt.plot(lof_dates[-n_days:],df['Close'].values[-n_days:],label=f"{ticker}")

    if mode_validate:
        # Validated data
        plt.plot(lof_dates[-prediction.shape[0]:],prediction,label=f"Validation")
    else:
        # Predicted data
        date_tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        plt.plot(date_tomorrow,prediction,marker='+',markeredgecolor='green',markerfacecolor='none',markersize=12,linestyle='',label='Prediction')
    
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1,7)))
    plt.gca().xaxis.set_minor_locator(mdates.MonthLocator())
    plt.gcf().autofmt_xdate()

    plt.gca().grid(True)
    plt.gca().set_ylabel(r'Close price [\$]')
    plt.gca().set_xlabel(r'Date')
    plt.legend()
    plt.title(f"{ticker}",loc='left')
    if not mode_validate:
        plt.annotate(f"Prediction for {date_tomorrow.strftime('%Y-%m-%d')}:
                    ${float(prediction):.2f}",
                    (0.5,1.025),xycoords='axes fraction')

    if mode_validate:
        tag = f"validation_up_to_{datetime.date.today().strftime('%Y%m%d-%H.%M.%S')}"
    else:
        tag = f"prediction_for_{date_tomorrow.strftime('%Y%m%d')}"

    plt.savefig(f"fig-{tag}.pdf")
    plt.close()


def get_date_string(date):
    #return date.strftime('%Y-%m-%d')
    return date.to_datetime64()


def plot_optimisation():
    pass

if __name__ == "__main__":
    from mlstockpredictor.data.stock import get_stock_data
    df = get_stock_data('TSLA')
    invented_value = 232.232 #for testing purposes only (avoid running prediction while testing plot)
    plot_prediction(df,invented_value)
