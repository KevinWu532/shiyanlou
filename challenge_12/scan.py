#!/usr/bin/env python3

import getopt, sys, socket

def get_status(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.1)
    try:
        s.connect((host, port))
        print("{} open".format(port))
    except Exception as err:
        print("{} closed".format(port))
    finally:
        s.close()

def args():
    opt, args = getopt.getopt(sys.argv[1:],'h:p:',['host=','port='])
    for k, v in opt:
        if k in ("-h","--host"):
            try:
                s = v.split(".")
                if len(s) != 4:
                    raise ValueError
                else:
                    host = v
            except ValueError:
                print("Parameter Error")
        if k in ("-p","--port"):
            try:
                s = v.split("-")
                if len(s) > 2:
                    raise ValueError
                else:
                    port = s
            except ValueError:
                print("Parameter Error")
    return host, port

if __name__ == "__main__":
    arg = args()
    if len(arg[1]) == 1:
        get_status(arg[0], int(arg[1][0]))
    else:
        for port in range(int(arg[1][0]), int(arg[1][1])+1):
            get_status(arg[0], port)
