#!/usr/bin/env python3

import sys
import csv
from multiprocessing import Process, Pool, Queue, Lock

class Args(object):
    def __init__(self):
        self.args = sys.argv[1:]

    def part(self):
        reslut = {}
        parameter = ('-c', '-d', '-o')		
        try:
            for x in parameter:
                index = self.args.index(x)
                filepath = self.args[index + 1]
                reslut[x] = filepath
            return reslut
        except:
            print("参数格式错误")

class Config(object):
    def __init__(self, dic):
        self.dic = dic
        self.config = self._read_config()
        
    def _read_config(self):
        config = {}
        try:
            with open(self.dic['-c']) as f:
                for i in f:
                    a = i.split("=")
                    config[a[0].strip()] = a[1].strip()
            return config
        except:
            print("文件读取出错，请检查配置文件是否正确")

    def get_config(self, value):
        return self.config[value]

class UserData(object):
    def __init__(self, dic, lock, queue):
        self.dic = dic
        self.lock = lock
        self.queue = queue
        self.userdata = self._read_users_data()

    def _read_users_data(self):
        
        try:
            with open(self.dic['-d']) as f:
                data = list(csv.reader(f))
                #print(data)
                for x in data:
                    with self.lock:
                        userdata = []
                        c=(x[0],x[1])
                        userdata.append(c)
                        self.queue.put(userdata)
            return userdata
        except:
            print("文件读取出错，请检查工资文件是否正确")
    
class IncomeCalculator(object):
    def __init__(self, dic, config ):
        self.dic  = dic
        self.config = config
        
    
    def calc_for_all_userdata(self, lock, queue1, queue2):
        shebao = 0
        result = []
        userdata = queue1.get()
        for k,v in self.config.items():            
            if k == 'JiShuL':
                JiShuL = float(v)
            elif k == 'JiShuH':
                JiShuH = float(v)
            else:
                shebao += float(v)
        
        data = []
        user = userdata[0]
        wage = int(userdata[1])
        data.append(user)
        data.append(wage)
        if wage < JiShuL:
            insurance = JiShuL * shebao
        elif wage < JiShuH:
            insurance = wage * shebao
        else:
            insurance = JiShuH * shebao
        data.append('{:.2f}'.format(insurance))
        if wage <= 3500:
            pay_taxes = 0
        else:
            need_pay_taxes = wage - insurance - 3500
            if need_pay_taxes <= 1500:
                pay_taxes = need_pay_taxes * 0.03
            elif need_pay_taxes <= 4500:
                pay_taxes = need_pay_taxes * 0.1 - 105
            elif need_pay_taxes <= 9000:
                pay_taxes = need_pay_taxes * 0.2 - 555
            elif need_pay_taxes <= 35000:
                pay_taxes = need_pay_taxes * 0.25 - 1005
            elif need_pay_taxes <= 55000:
                pay_taxes = need_pay_taxes * 0.3 - 2755
            elif need_pay_taxes <= 80000:
                pay_taxes = need_pay_taxes * 0.35 - 5505
            else:
                pay_taxes = need_pay_taxes * 0.45 - 13505
            data.append('{:.2f}'.format(pay_taxes))
        finally_wage = wage - insurance - pay_taxes
        data.append('{:.2f}'.format(finally_wage))
        result.append(data)
        queue2.put(data)
        return result

    def export(self , queue2, default= 'csv'):
        result = queue2.get()
        try:
            with open(self.dic['-o'],'a') as f:
                csv.writer(f).writerows(result)
        except:
            print("写入文件失败")

if __name__ == '__main__':
    a = Args().part()
    b = Config(a)

    lock = Lock()
    queue1 = Queue()
    queue2 = Queue()
    
    Process(target=UserData, args=(a, lock, queue1)).start()
    calc = IncomeCalculator(a, b.config)
    Process(target=calc.calc_all_userdata, args=(lock, queue1, queue2)).start()
    Process(target=calc.export, args=(queue2,)).start()

    '''
    d = UserData(a)
    calc = IncomeCalculator(a.part(), b.config, d.userdata)
    calc.export()
    '''
