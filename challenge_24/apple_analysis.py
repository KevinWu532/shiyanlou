import pandas as pd

def quarter_volume():
    data = pd.read_csv("apple.csv",header=0)
    '''
    data = data.set_index(pd.to_datetime(data['Date']))
    data = data.resample('Q').sum()
    second_volume = data.sort_values(by='Volume',ascending=False)['Volume'][1]
    '''
    second_volume = data.set_index(pd.to_datetime(data['Date'])).resample('Q').sum().sort_values(by='Volume',ascending=False)['Volume'][1]
    return second_volume

if __name__ == '__main__':
    print(quarter_volume())
