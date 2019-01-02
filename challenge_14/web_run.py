# -*- coding: UTF-8 -*-

from flask import request
from flask import Flask
from flask import render_template
from ele import ele_red_packet


app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def phone_number_form():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        phone_number = request.form['phone']
        get_red_packet = ele_red_packet(phone_number)
        return render_template('index.html', phone_number=get_red_packet)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
