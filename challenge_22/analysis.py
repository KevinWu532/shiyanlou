import pandas as pd

def analysis(file,user_id):
    times = 0
    minutes = 0
    x = pd.read_json(file)
    times = x[x['user_id'] == user_id]['minutes'].size
    minutes = x[x['user_id']== user_id]['minutes'].sum()
    return times, minutes
