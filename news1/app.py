#!/usr/bin/env python3
from datetime import datetime
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/news'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class File(db.Model):
    __tablename__ = 'file'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    created_time = db.Column(db.DateTime)
    category_id = db.Column(db.Integer,db.ForeignKey('category.id'))
    category = db.relationship('Category', backref='categorys') 
    content = db.Column(db.Text)
   
    def __init__(self, title, created_time, category, content):
        self.title = title
        self.created_time = created_time
        self.category = category
        self.content = content


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __init__(self,name):
        self.name = name
    

@app.route('/')
def index():
    #title
    files = File.query.all()
    return render_template('index.html',files=files)

@app.route('/files/<file_id>')
def file_index(file_id):
    #print filename.json
    #if file is None redirect 404 

    content = File.query.get(file_id)
    if content is None:
        return redirect('not_found')
    else:
        return render_template('file.html',content=content)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html',text='shiyanlou 404')

if __name__ == '__main__':
    app.run()
