#!/usr/bin/env python3

import sys
import csv
from multiprocessing import Process, Queue

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
    def __init__(self, dic):
        self.dic = dic
        #self.userdata = self._read_users_data()

    def _read_users_data(self, queue1):
        try:
            with open(self.dic['-d']) as f:
                data = list(csv.reader(f))
                #print(data)
                for x in data:
                    userdata=[x[0],x[1]]
                    '''
                    c=(x[0],x[1])
                    userdata.append(c)
                    '''
                    queue1.put(userdata)
        except:
            print("文件读取出错，请检查工资文件是否正确")
    
class IncomeCalculator(object):
    def __init__(self, dic, config, userdata):
        self.dic  = dic
        self.config = config
        self.userdata = userdata
    
    def calc_for_all_userdata(self):
        shebao = 0
        result = []
        
        for k,v in self.config.items():            
            if k == 'JiShuL':
                JiShuL = float(v)
            elif k == 'JiShuH':
                JiShuH = float(v)
            else:
                shebao += float(v)
        for x in self.userdata:
            data = []
            user = x[0]
            wage = int(x[1])
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
        return result

    def export(self , default= 'csv'):
        result = self.calc_for_all_userdata()
        try:
            with open(self.dic['-o'],'w') as f:
                csv.writer(f).writerows(result)
        except:
            print("写入文件失败")

if __name__ == '__main__':
    '''
    a = Args()
    b = Config(a.part())
    d = UserData(a.part())
    calc = IncomeCalculator(a.part(), b.config, d.userdata)
    calc.export()
    '''

    paths = Args().part()
    print(paths)
    config = Config(paths).config
    print(config)
    queue1 = Queue()
    queue2 = Queue()
    process = []
    userdata = UserData(paths)
    process.append(Process(target=userdata._read_user_data,args=(queue1)))
    
