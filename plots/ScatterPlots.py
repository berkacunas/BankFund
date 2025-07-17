from datetime import datetime, date, timedelta
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import matplotlib.cm as cm

import numpy as np
import random
    
def foo1():

    fig = plt.figure()
    fig.subplots_adjust(bottom=0.2)
    ax = fig.add_subplot(111)

    N=3*10**6
    delta=np.random.normal(size=N)
    vf=np.random.normal(size=N)
    dS=np.random.normal(size=N)

    idx=random.sample(range(N),1000)

    plt.scatter(delta[idx],vf[idx],c=dS[idx],alpha=0.7,cmap=cm.Paired)
    plt.show()

def foo2():
    
    # Import libraries using import keyword
    import numpy as np
    import matplotlib.pyplot as plt

    # Setting Plot and Axis variables as subplots()
    # function returns tuple(fig, ax)
    Plot, Axis = plt.subplots()

    # Adjust the bottom size according to the
    # requirement of the user
    plt.subplots_adjust(bottom=0.25)

    # Set the x and y axis to some dummy data
    t = np.arange(0.0, 100.0, 0.1)
    s = np.sin(2*np.pi*t)

    # plot the x and y using plot function
    l = plt.plot(t, s)

    # Choose the Slider color
    slider_color = 'White'

    # Set the axis and slider position in the plot
    axis_position = plt.axes([0.2, 0.1, 0.65, 0.03],
                            facecolor = slider_color)
    slider_position = Slider(axis_position,
                            'Pos', 0.1, 90.0)

    # update() function to change the graph when the
    # slider is in use
    def update(val):
        pos = slider_position.val
        Axis.axis([pos, pos+10, -1, 1])
        Plot.canvas.draw_idle()

    # update function called using on_changed() function
    slider_position.on_changed(update)

    # Display the plot
    plt.show()

def plot2(df: pd.DataFrame, begin_date: date = date.min, end_date: date = date.today()):
    
    df['Dt'] = pd.to_datetime(df['Dt'], format='%Y-%m-%d %H:%M:%S.%f')
    
    v_data = df.query("Dt >= @begin_date and Dt < @end_date")
    
    plt.figure()
    plt.scatter(data=v_data, x="Dt", y="UnitSharePrice", linewidths=1, marker=".", alpha=0.5, color="blue")
    plt.xticks(rotation=90)
    plt.grid()
    plt.legend()
    plt.title("TIV Fonu")
    # ax = plt.gca()
    # ax.set_xlim([xmin, xmax])
    # ax.set_ylim([30, 40])
    plt.show()


    # data = pd.DataFrame( { 'Dt': pd.to_datetime(dates), 'UnitPrice': df.UnitSharePrice } )
    # data.plot(x='Dt', y='UnitPrice', marker='o', linestyle='none')
    
    
def plot3():
    
    plt.style.use('_mpl-gallery')

    # make data
    x = np.linspace(0, 10, 100)
    y = 4 + 1 * np.sin(2 * x)
    x2 = np.linspace(0, 10, 25)
    y2 = 4 + 1 * np.sin(2 * x2)
    
    print(f"x: {x}")
    print(f"x2: {x2}")

    # plot
    fig, ax = plt.subplots()

    ax.plot(x2, y2 + 2.5, 'x', markeredgewidth=2)
    ax.plot(x, y, linewidth=2.0)
    ax.plot(x2, y2 - 2.5, 'o-', linewidth=2)

    ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
        ylim=(0, 8), yticks=np.arange(1, 8))

    plt.show()

def plot(df: pd.DataFrame, begin_date: date = date.min, end_date: date = date.today()):
    
    plt.style.use('_mpl-gallery')
    
    # df_daterange = pd.date_range(start=begin_date, end=end_date)
    # print(f"type: {type(df_daterange)}\n{df_daterange}")
    
    df['Dt'] = pd.to_datetime(df['Dt'], format='%Y-%m-%d %H:%M:%S.%f')
    
    data = df.query("Dt >= @begin_date and Dt < @end_date and Code == 'TIV'")
    data.sort_values(by='Dt', ascending=True, inplace=True)
    # data.to_csv("test.csv")

    x = data['Dt']
    y = data['UnitSharePrice']
    
    # fig = plt.figure(figsize=(10, 10))
    
    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True
    
    fig, ax = plt.subplots()
    
    ax.plot(x, y, linewidth=2, c='blue')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(True)
    ax.spines['bottom'].set_visible(True)
    
    plt.title('Kumpula temperatures in June 2016')
    plt.xlabel('Date')
    plt.ylabel('Temperature [°F]')
    
    # plt.plot(x, y)
    plt.show()
    
    print()

def scatter(df: pd.DataFrame):
    
    print(df.columns)
    plt.figure()
    plt.scatter(data=df, x="Dt", y="UnitSharePrice", linewidths=1, marker=".", alpha=0.5, color="green")
    plt.grid()
    plt.title("Yaş Kilo Dağılım Grafiği")
    plt.show()

# def grafik1():
#     veri = pandas.read_csv("./madalya_duzenli.csv")

#     seaborn.scatterplot(data=veri, x="boy", y="kilo" )
#     plt.xlabel("Boy Değeri")
#     plt.ylabel("Kilo Değeri")
#     plt.show()

# def maaslar_grafigi():
#     veri = pandas.read_csv("./madalya_duzenli.csv")
#     plt.Figure()  # plt oluşturduğumuzu belirttik
#     plt.scatter(data=veri, x="yas", y="kilo", linewidths=3,
#                 marker="o", alpha=0.5, color="green")
#     plt.grid()
#     plt.title("Yaş Kilo Dağılım Grafiği")
#     plt.show()

# def bargrafik():
#     veri = pandas.read_csv("./maaslar_verisi.csv")
#     maaslar = veri["salary"].head(40)
#     tecrube = veri["job_title"].head(40)

#     figure, eksen = plt.subplots()
#     renk = plt.gca()
#     renk.set_facecolor("pink")

#     eksen.barh(tecrube, maaslar, color="gray", facecolor="red",
#                linestyle="-")
#     plt.grid()
#     plt.title("Maaşlar - İş Tanımı Grafiği")
#     plt.show()

# bargrafik()
