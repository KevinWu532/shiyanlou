#!/usr/bin/env python3

import sys

def finally_wage(num, wage):
    insurance = wage * 0.165
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
    print("{}:{:.2f}".format(num,wage-insurance-pay_taxes))

try:
    if len(sys.argv) < 2:
        raise ValueError
    else:
        for arg in sys.argv[1:]:
            kw = arg.split(":")
            if kw[0] is str or kw[1] is str:
                raise ValueError
            else:
                finally_wage(int(kw[0]),int(kw[1]))
except ValueError:
    print("Parameter Error")
