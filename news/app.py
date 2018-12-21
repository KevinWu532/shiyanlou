#!/usr/bin/env python3
import os, json
from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)
path = '/home/shiyanlou/files'

@app.route('/')
def index():
    #title
    titles = {}
    files = os.listdir(path)
    for i in files:
        i_path = os.path.join(path, i)
        with open(i_path) as f:
            titles[os.path.splitext(i)[0]] = json.load(f)['title']
    return render_template('index.html',titles=titles)

@app.route('/files/<filename>')
def file_index(filename):
    #print filename.json
    #if file is None redirect 404 
    file_path = os.path.join(path,filename+'.json')
    if os.path.exists(file_path):
        with open(file_path) as f:
            content = json.load(f)
        return render_template('file.html',content=content)
    else:
        return redirect('not_found')

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html',text='shiyanlou 404')

if __name__ == '__main__':
    app.run()
