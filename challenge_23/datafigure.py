import pandas as pd
from matplotlib import pyplot as plt

data = pd.read_json('user_study.json')
a= data[['user_id','minutes']].groupby('user_id').sum()
x = a.index
y = a['minutes']

def data_plot():
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    ax.set_title('StudyData')
    
    ax.set_xlabel('User ID')
    ax.ser_ylabel('Study Time')
    
    ax.plot(x,y)
    plt.show()
    return ax
    
