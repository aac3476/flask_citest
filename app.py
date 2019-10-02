# -*- coding: utf-8 -*-  
"""
Create on 10-02 13:01 2019
@Author ywx 
@File app.py
"""

from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(host='0.0.0.0')