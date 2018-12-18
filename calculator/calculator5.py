#!/usr/bin/env python3

import sys
import csv
from multiprocessing import Process, Queue

class Args(object):
    def __init__(self):
        args = sys.argv[1:]
        self.c = args[args.index('-c') + 1]
        self.d = args[args.index('-d') + 1]
        self.o = args[args.index('-o') + 1]

args = Args()

class Config(object):
    def __init__(self):
        self.config = self._read_config()
        
    def _read_config(self):
        config = {"s":0}
        with open(args.c) as f:
            for i in f.readlines():
                a = i.split("=")
                m, n = a[0].strip(),a[1].strip()
                if m == 'JiShuL' or m == 'JiShuH':
                    config[m] = float(n)
                else:
                    config['s'] += float(n)
        return config
config = Config().config

class UserData(object):
    def __init__(self):
        with open(args.d) as f:
            data = list(csv.reader(f))
        self.data = data
data = UserData().data

def calc(i):
    z = int(i)
    s = config.get('s')
    sb = z * s
    if z < config.get('JiShuL'):
        sb = config['JiShuL'] * s
    elif z > config.get('JiShuH'):
        sb = config['JiShuH'] * s
    x = (z - sb -3500)
    if x <0:
        m = 0
    elif x <= 1500:
        m = x * 0.03 
    elif x <= 4500:
        m = x * 0.1 - 105
    elif x <= 9000:
        m = x * 0.2 - 555
    elif x <= 35000:
        m = x * 0.25 - 1005
    elif x <= 55000:
        m = x * 0.3 - 2755
    elif x <= 80000:
        m = x * 0.35 -5505
    else:
        m = x * 0.45 - 13505
    sh = z - sb - m
    return [z, format(sb, '.2f'), format(m, '.2f'), format(sh, '.2f')]

q1, q2 = Queue(), Queue()
def p3():
    with open(args.o, 'a') as f:
        while True:
            try:
                csv.writer(f).writerow(q2.get(timeout=0.1))
            except queue.Empty:
                return


def p1():
    for i in data:
        q1.put(i)

def p2():
    def run():
        while True:
            try: 
                a, b = q1.get(timeout=0.1)
                x = calc(b)
                x.insert(0, a)
                yield x
            except queue.Empty:
                return
    for i in run():
        q2.put(i)

Process(target=p1).start()
Process(target=p2).start()
Process(target=p3).start()
